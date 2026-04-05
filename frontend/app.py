"""Streamlit chat UI for Pathfinder NZ."""

import requests
import streamlit as st

BACKEND_URL = "http://localhost:8000"

SUGGESTED_QUESTIONS = {
    "employer": [
        "What type of accreditation do I need to hire overseas workers?",
        "Do I need to advertise the job before applying for a Job Check?",
        "What documents do I need to include in a Job Offer?",
    ],
    "applicant": [
        "What visa do I need to work as a software engineer in NZ?",
        "How do I apply for the Skilled Migrant Category resident visa?",
        "What are the requirements for a partner visa?",
    ],
}


def send_message(message: str) -> dict:
    """Send a message to the backend API."""
    history = [
        {"role": msg["role"], "content": msg["content"]}
        for msg in st.session_state.messages
    ]
    response = requests.post(
        f"{BACKEND_URL}/chat",
        json={
            "message": message,
            "role": st.session_state.role,
            "history": history,
        },
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def show_role_selection():
    """Display the role selection screen."""
    st.title("Pathfinder NZ")
    st.markdown("*Your guide to New Zealand visas — powered by official INZ documents.*")
    st.markdown("---")
    st.subheader("Select your role to get started:")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏢 I'm an Employer / HR Manager", use_container_width=True):
            st.session_state.role = "employer"
            st.session_state.messages = []
            st.rerun()
    with col2:
        if st.button("🧳 I'm a Visa Applicant or Immigrant", use_container_width=True):
            st.session_state.role = "applicant"
            st.session_state.messages = []
            st.rerun()

    st.markdown("---")
    st.caption(
        "Pathfinder NZ provides general information based on official Immigration "
        "New Zealand documents. It is not legal advice. For complex situations, "
        "please consult a licensed immigration adviser."
    )


def show_chat():
    """Display the chat interface."""
    role_emoji = "🏢" if st.session_state.role == "employer" else "🧳"
    role_label = (
        "Employer / HR" if st.session_state.role == "employer"
        else "Visa Applicant"
    )

    st.title("Pathfinder NZ")

    header_html = f"""
    <div style="display: flex; align-items: center; gap: 10px; margin-top: -10px; margin-bottom: 20px;">
        <span style="
            background: #f0f2f6;
            border-radius: 20px;
            padding: 4px 14px;
            font-size: 0.85rem;
            font-weight: 500;
            color: #31333f;
        ">{role_emoji} {role_label}</span>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

    if st.button("↩ Change Role", type="tertiary"):
        st.session_state.role = None
        st.session_state.messages = []
        st.rerun()

    # Welcome message with suggested questions
    if not st.session_state.messages:
        st.markdown("**Welcome! Here are some questions you might ask:**")
        for question in SUGGESTED_QUESTIONS[st.session_state.role]:
            if st.button(question, key=question):
                st.session_state.pending_question = question
                st.rerun()

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Process pending suggested question
    pending = st.session_state.pop("pending_question", None)

    # Chat input
    prompt = st.chat_input("Ask a question about New Zealand visas...")
    active_prompt = pending or prompt

    if active_prompt:
        st.session_state.messages.append({"role": "user", "content": active_prompt})
        with st.chat_message("user"):
            st.markdown(active_prompt)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            placeholder.markdown("Searching INZ documents... ⏳")
            try:
                result = send_message(active_prompt)
                answer = result["answer"]
            except Exception as e:
                answer = f"Sorry, an error occurred: {e}"
            placeholder.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

    # Clear conversation button
    if st.session_state.messages:
        if st.button("Clear Conversation"):
            st.session_state.messages = []
            st.rerun()


def main():
    st.set_page_config(page_title="Pathfinder NZ", page_icon="🗺️", layout="centered")

    st.markdown(
        """
        <style>
        /* Hide default Streamlit running indicator and stop button */
        header [data-testid="stStatusWidget"] { display: none; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    if "role" not in st.session_state:
        st.session_state.role = None
    if "messages" not in st.session_state:
        st.session_state.messages = []

    with st.sidebar:
        st.markdown("### ⚠️ Disclaimer")
        st.caption(
            "This information is based on official Immigration New Zealand "
            "documents and is provided for general guidance only. It is not "
            "legal advice. For decisions that may significantly affect your "
            "visa status, please consult a licensed immigration adviser."
        )

    if st.session_state.role is None:
        show_role_selection()
    else:
        show_chat()


if __name__ == "__main__":
    main()
