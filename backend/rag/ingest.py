"""Scrape INZ documents and ingest them into ChromaDB."""

import argparse
import json
import logging
import os
import time

from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from backend.config import OPENAI_API_KEY, CHROMA_DB_PATH
from backend.rag.urls import ALL_URLS
from backend.rag.manifest import (
    content_hash,
    load_manifest,
    save_manifest,
    utc_now_iso,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

BATCH_SIZE = 100
MAX_RETRIES = 3

# Ceiling on how many chunks a single `refresh_changed` run will embed.
# OpenAI's paid tier has no daily quota comparable to Gemini's free tier,
# so this exists only as a sane upper bound for unattended runs, not a
# quota workaround. URLs that don't fit within the cap are left untouched
# (both in Chroma and in the manifest) so the next scheduled run picks
# them up.
MAX_CHUNKS_PER_RUN = int(os.getenv("MAX_CHUNKS_PER_RUN", "5000"))


def _get_ingested_urls() -> set[str]:
    """Return source URLs already stored in ChromaDB."""
    try:
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=OPENAI_API_KEY,
        )
        vs = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings)
        results = vs._collection.get(include=["metadatas"])
        return {m.get("source", "") for m in results["metadatas"]}
    except Exception:
        return set()


def _scrape(url: str):
    """Scrape a single URL and stamp source/title metadata.

    Returns the list of loaded `Document`s, or `None` on failure (the
    error is logged here).
    """
    try:
        loader = WebBaseLoader(url)
        docs = loader.load()
        for doc in docs:
            title = (doc.metadata.get("title") or "").strip()
            doc.metadata["source"] = url
            doc.metadata["title"] = title
        logger.info("Loaded: %s", url)
        return docs
    except Exception as e:
        logger.error("Failed to load %s: %s", url, e)
        return None


def _embed_in_batches(vectorstore, chunks: list) -> int:
    """Embed and store chunks in batches, retrying on 429s.

    Returns the number of chunks embedded (always `len(chunks)` — the
    caller is responsible for any `MAX_CHUNKS_PER_RUN` capping before
    calling this, since `ingest_documents` intentionally embeds its
    full chunk list in one call with no cap).
    """
    total_batches = (len(chunks) + BATCH_SIZE - 1) // BATCH_SIZE
    for i in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[i : i + BATCH_SIZE]
        batch_num = i // BATCH_SIZE + 1

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                logger.info("Embedding batch %d/%d (%d chunks)...", batch_num, total_batches, len(batch))
                vectorstore.add_documents(batch)
                break
            except Exception as e:
                if "429" in str(e) and attempt < MAX_RETRIES:
                    wait = 20 * attempt
                    logger.warning("Rate limited on batch %d, retrying in %ds (attempt %d/%d)...", batch_num, wait, attempt, MAX_RETRIES)
                    time.sleep(wait)
                else:
                    raise

    return len(chunks)


def _delete_by_source(vectorstore, url: str) -> int:
    """Delete all chunks in the vectorstore whose `source` metadata is `url`.

    Returns the number of chunks deleted. This must be called before
    re-adding chunks for a URL whose content changed, to avoid
    duplicating chunks already stored from a previous ingestion run.
    """
    ids = vectorstore.get(where={"source": url}).get("ids", [])
    if ids:
        vectorstore.delete(ids=ids)
    return len(ids)


def _make_vectorstore() -> Chroma:
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=OPENAI_API_KEY,
    )
    return Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings)


def refresh_changed(dry_run: bool = False) -> dict:
    """Scrape all configured URLs, diff against the manifest, and only
    re-embed URLs whose content has actually changed.

    Args:
        dry_run: If True (the `--check` path), only scrape and diff —
            never touch ChromaDB or the manifest file.

    Returns:
        A JSON-serialisable summary dict describing what changed,
        what's new, what failed, and how many chunks were embedded.
    """
    manifest = load_manifest()
    manifest_urls = manifest.setdefault("urls", {})

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    failed: list[str] = []
    new_urls: list[dict] = []
    changed_urls: list[dict] = []
    unchanged_urls: list[str] = []

    # Per-URL scrape results kept around so changed/new URLs aren't re-scraped.
    scraped: dict[str, list] = {}
    # (entry, is_changed) in the same order URLs were encountered in ALL_URLS,
    # for new/changed URLs only.
    to_process: list[tuple[dict, bool]] = []

    for url in ALL_URLS:
        docs = _scrape(url)
        if docs is None:
            failed.append(url)
            continue

        text = "".join(doc.page_content for doc in docs)
        new_hash = content_hash(text)
        prior_entry = manifest_urls.get(url)
        title = (docs[0].metadata.get("title") if docs else "") or ""

        if prior_entry is None:
            entry = {"url": url, "title": title}
            new_urls.append(entry)
            scraped[url] = docs
            to_process.append((entry, False))
        elif prior_entry.get("content_sha256") != new_hash:
            entry = {"url": url, "title": title}
            changed_urls.append(entry)
            scraped[url] = docs
            to_process.append((entry, True))
        else:
            unchanged_urls.append(url)

    unchanged_count = len(unchanged_urls)

    if dry_run:
        return {
            "changed": changed_urls,
            "new": new_urls,
            "failed": failed,
            "unchanged_count": unchanged_count,
            "chunks_embedded": 0,
            "truncated": False,
        }

    vectorstore = _make_vectorstore()
    now = utc_now_iso()

    chunks_embedded = 0
    running_total = 0
    truncated = False
    truncated_urls: list[str] = []

    embedded_new: list[dict] = []
    embedded_changed: list[dict] = []

    for entry, is_changed in to_process:
        url = entry["url"]
        docs = scraped[url]
        url_chunks = splitter.split_documents(docs)

        if running_total + len(url_chunks) > MAX_CHUNKS_PER_RUN:
            truncated = True
            truncated_urls.append(url)
            continue

        if is_changed:
            _delete_by_source(vectorstore, url)

        actually_embedded = _embed_in_batches(vectorstore, url_chunks)
        running_total += actually_embedded
        chunks_embedded += actually_embedded

        content_text = "".join(doc.page_content for doc in docs)
        manifest_urls[url] = {
            "content_sha256": content_hash(content_text),
            "chunk_count": len(url_chunks),
            "last_changed": now,
            "last_checked": now,
        }

        if is_changed:
            embedded_changed.append(entry)
        else:
            embedded_new.append(entry)

    # Unchanged URLs: just bump last_checked (never touch failed URLs'
    # manifest entries — a scrape failure must never look like a check).
    for url in unchanged_urls:
        manifest_urls[url]["last_checked"] = now

    save_manifest(manifest)

    logger.info(
        "Refresh complete. %d new, %d changed, %d unchanged, %d failed, %d chunks embedded%s.",
        len(embedded_new),
        len(embedded_changed),
        unchanged_count,
        len(failed),
        chunks_embedded,
        " (truncated, will resume next run)" if truncated else "",
    )

    return {
        "changed": embedded_changed,
        "new": embedded_new,
        "failed": failed,
        "unchanged_count": unchanged_count,
        "chunks_embedded": chunks_embedded,
        "truncated": truncated,
        "truncated_urls": truncated_urls,
    }


def ingest_documents(resume: bool = False) -> None:
    """Scrape INZ URLs and store chunks in ChromaDB.

    This is the manual/local full-ingestion entry point. It upserts:
    for every URL being (re-)ingested, any existing chunks for that URL
    are deleted before new chunks are added, so re-running it never
    duplicates data. It also seeds/updates `data/refresh_manifest.json`
    for every URL it touches, so `refresh_changed` has a correct
    baseline to diff against on the next scheduled run.

    Args:
        resume: If True, skip URLs already in ChromaDB.
    """
    urls_to_ingest = ALL_URLS
    if resume:
        already_ingested = _get_ingested_urls()
        urls_to_ingest = [u for u in ALL_URLS if u not in already_ingested]
        logger.info("Resume mode: %d URLs already ingested, %d remaining.", len(already_ingested), len(urls_to_ingest))
        if not urls_to_ingest:
            logger.info("All URLs already ingested. Nothing to do.")
            return

    docs_by_url: dict[str, list] = {}
    for url in urls_to_ingest:
        docs = _scrape(url)
        if docs is None:
            continue
        docs_by_url[url] = docs

    if not docs_by_url:
        logger.error("No documents were loaded. Aborting ingestion.")
        return

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    vectorstore = _make_vectorstore()
    manifest = load_manifest()
    manifest_urls = manifest.setdefault("urls", {})

    # Process one URL at a time: delete its old chunks, embed its new
    # ones, and record it in the manifest immediately. If a later URL
    # hits an unrecoverable error (e.g. daily quota exhaustion), every
    # URL already processed in this run stays correctly upserted —
    # nothing is bulk-deleted upfront and left unreplaced.
    total_chunks = 0
    urls_list = list(docs_by_url.items())
    for url, docs in urls_list:
        url_chunks = splitter.split_documents(docs)
        _delete_by_source(vectorstore, url)
        _embed_in_batches(vectorstore, url_chunks)
        total_chunks += len(url_chunks)

        text = "".join(doc.page_content for doc in docs)
        now = utc_now_iso()
        manifest_urls[url] = {
            "content_sha256": content_hash(text),
            "chunk_count": len(url_chunks),
            "last_changed": now,
            "last_checked": now,
        }
        save_manifest(manifest)

    logger.info(
        "Ingestion complete. %d chunks stored across %d URLs in %s.",
        total_chunks,
        len(docs_by_url),
        CHROMA_DB_PATH,
    )


def _print_summary(summary: dict, action: str) -> None:
    print(f"\n=== INZ document refresh summary ({action}) ===")
    print(f"New URLs:       {len(summary['new'])}")
    for entry in summary["new"]:
        print(f"  + {entry['url']}")
    print(f"Changed URLs:   {len(summary['changed'])}")
    for entry in summary["changed"]:
        print(f"  ~ {entry['url']}")
    print(f"Unchanged URLs: {summary['unchanged_count']}")
    print(f"Failed URLs:    {len(summary['failed'])}")
    for url in summary["failed"]:
        print(f"  ! {url}")
    print(f"Chunks embedded: {summary['chunks_embedded']}")
    print(f"Truncated:       {summary['truncated']}")
    print("===============================================\n")


def _write_summary_json(summary: dict, path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
        f.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scrape INZ documents and (re-)ingest them into ChromaDB.",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--resume",
        action="store_true",
        help="Full ingestion, skipping URLs already present in ChromaDB.",
    )
    group.add_argument(
        "--check",
        action="store_true",
        help="Dry run: scrape and diff against the manifest, but do not write to ChromaDB or the manifest.",
    )
    group.add_argument(
        "--refresh-changed",
        action="store_true",
        help="Scrape all URLs and only re-embed those whose content has changed since the last run.",
    )
    parser.add_argument(
        "--summary-json",
        metavar="PATH",
        help="When combined with --check or --refresh-changed, also write the run summary as JSON to PATH.",
    )
    args = parser.parse_args()

    if args.check:
        summary = refresh_changed(dry_run=True)
        _print_summary(summary, "check")
        if args.summary_json:
            _write_summary_json(summary, args.summary_json)
    elif args.refresh_changed:
        summary = refresh_changed(dry_run=False)
        _print_summary(summary, "refresh-changed")
        if args.summary_json:
            _write_summary_json(summary, args.summary_json)
    else:
        ingest_documents(resume=args.resume)


if __name__ == "__main__":
    main()
