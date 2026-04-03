# /commit

Analyse all unstaged and staged changes, group related files together, and commit them in logical batches.

## Instructions

1. Run `git status` to see all changed files (staged and unstaged)
2. Run `git diff` to understand what changed in each file
3. Group the changed files into logical batches where each batch contains only related files
4. For each batch:
   a. Show the user which files are in this batch and the reason for grouping
   b. Show the proposed commit message
   c. Ask for confirmation before staging and committing
   d. If confirmed, run `git add <files>` then `git commit -m "<message>"`
   e. If the user wants to edit the message, use their version instead
5. Repeat for each batch until all changes are committed

## Conventional Commits Format

```
<type>(<scope>): <short description>

[optional body]
```

### Types
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes only (README, CLAUDE.md, PRD.md, etc.)
- `style`: Formatting, missing semicolons, etc. (no logic change)
- `refactor`: Code change that is neither a fix nor a feature
- `test`: Adding or updating tests
- `chore`: Build process, dependencies, config files (requirements.txt, .gitignore, etc.)
- `perf`: Performance improvement

### Scope (optional)
Use the area of the codebase affected:
- `backend`, `frontend`, `rag`, `prompts`, `routes`, `config`, `docker`, `deps`

### Rules
- Subject line: 72 characters max
- Use imperative mood: "add feature" not "added feature"
- No full stop at the end of the subject line
- All commit messages must be in British English (e.g., "organise" not "organize", "initialise" not "initialize", "colour" not "color")

## Examples

```
feat(rag): add document ingestion pipeline for INZ URLs

fix(backend): handle failed URL fetch gracefully in ingest.py

docs: update CLAUDE.md with agent usage policy

chore(deps): add langchain-google-genai to requirements.txt

feat(frontend): implement role selection screen in Streamlit UI

refactor(rag): extract URL config into separate urls.py module
```

## Notes
- If there are no changes at all, inform the user and stop
- Never mix unrelated files in the same commit (e.g., do not commit RAG changes and UI changes together)
- If a file change is unclear, run `git diff <file>` to inspect it before deciding which batch it belongs to
