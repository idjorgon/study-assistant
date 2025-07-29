import streamlit as st
import os
from tavily import TavilyClient
from openai import AzureOpenAI
from dotenv import load_dotenv
from flashcards import generate_flashcards, search_internet, search_books
from quiz import generate_quiz
from summary import summarize_text
from langchain.chat_models import AzureChatOpenAI

# Set up your OpenAI API key and credentials
load_dotenv(".env")
api_key = os.getenv('AZURE_OPENAI_API_KEY')
api_endpoint = os.getenv('AZURE_ENDPOINT')
deployment_name = os.getenv('DEPLOYMENT_NAME')
apiversion = os.getenv('AZURE_OPENAI_API_VERSION')
tavilyclient = os.getenv('TAVILY_KEY')

# Initialize OpenAI client
client = AzureOpenAI(
  azure_endpoint=api_endpoint,
  api_key=api_key,
  api_version=apiversion
)

tavily_client = TavilyClient(api_key=tavilyclient)

llmClient = AzureChatOpenAI(
    openai_api_key=api_key,
    azure_endpoint=api_endpoint,
    openai_api_version=apiversion,
    deployment_name=deployment_name,
    temperature=0.7
)

# Main Study Assistant Function


def study_assistant():
    with st.sidebar:
        (
            "[View the source code]"
            "(https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
        )
        (
            "[![Open in GitHub Codespaces]"
            "(https://github.com/codespaces/badge.svg)]"
            "(https://codespaces.new/streamlit/llm-examples?quickstart=1)"
        )

    st.title(" My Study Assistant ")

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    if "stage" not in st.session_state:
        st.session_state["stage"] = "main_menu"

    # Initialize chat history and state
    if st.session_state["stage"] == "main_menu":
        if (
            not st.session_state["messages"]
            or "Welcome to the GenAI Study"
            not in st.session_state["messages"][-1]["content"]
        ):
            st.session_state["messages"].append(
                {
                    "role": "assistant",
                    "content": (
                        "Welcome to the GenAI Study Assistant!:\n"
                        "1. Generate Flashcards 📚\n"
                        "2. Summarize Text 📜\n"
                        "3. Generate Quiz 🌎 \n"
                        "4. Ask me anything!"
                    ),
                }
            )

    # Display chat messages
    for msg in st.session_state["messages"]:
        st.chat_message(msg["role"]).write(msg["content"])

    # Main menu logic
    if st.session_state["stage"] == "main_menu":
        choice = st.text_input("Enter your choice .. ")

        if choice:
            st.session_state["messages"].append(
                {
                    "role": "user",
                    "content": choice
                }
            )
            if choice == "1":
                st.session_state["stage"] = "flashcard"
            elif choice == "2":
                st.session_state["stage"] = "summarize"
            elif choice == "3":
                st.session_state["stage"] = "quiz"
            elif choice == "4":
                st.session_state["stage"] = "query"
            else:
                bot_reply = "Invalid choice. Please try again."
                st.session_state["messages"].append(
                    {
                        "role": "assistant",
                        "content": bot_reply
                    }
                )
                st.chat_message("assistant").write(bot_reply)

    # Summarize text logic
    if st.session_state["stage"] == "summarize":
        text = st.text_input(
            "Enter the text you'd like to summarize: ",
            key="summary_input"
        )

        if text:
            summary = summarize_text(text, client, deployment_name)
            st.session_state["messages"].append(
                {
                    "role": "assistant",
                    "content": text
                }
            )
            st.session_state["messages"].append(
                {
                    "role": "assistant",
                    "content": summary
                }
            )
            st.chat_message("assistant").write(summary)

            st.session_state.pop("summary_input", None)
            st.session_state["stage"] == "main_menu"
            st.rerun()

    # Flashcard generation logic
    elif st.session_state["stage"] == "flashcard":
        flashcard_word = st.text_input(
            "Enter the text you'd like to convert into flashcards"
        )

        if flashcard_word:
            bot_reply = "Generating Flashcards for ..." + flashcard_word
            st.session_state["messages"].append(
                {
                    "role": "assistant",
                    "content": bot_reply
                }
            )
            st.chat_message("assistant").write(bot_reply)
            flashcards = generate_flashcards(flashcard_word, llmClient)
            st.session_state["messages"].append(
                {
                    "role": "assistant",
                    "content": flashcards
                }
            )
            st.chat_message("assistant").write(flashcards)
            bot_reply = "Here are some recent books to improve on your learning...."  # noqa: E501
            st.session_state["messages"].append(
                {
                    "role": "assistant",
                    "content": bot_reply
                }
            )
            st.chat_message("assistant").write(bot_reply)
            search = search_books(flashcard_word, tavily_client)

            sources = search.get("results", [])
            if sources:
                for i, source in enumerate(sources[:2], 1):
                    st.chat_message("assistant").write(
                        f"**Source {i}:** [{source.get('title', 'No Title')}]"
                        f"({source.get('url', '')})\n"
                    )
            else:
                st.chat_message("assistant").write("No recent study material found.")  # noqa: E501

    # Quiz generation logic
    elif st.session_state["stage"] == "quiz":
        text = st.text_input("Enter the text you'd like to use for generating a quiz:")  # noqa: E501

        if text:
            bot_reply = "Generating Quiz ..." + text
            st.session_state["messages"].append({"role": "assistant", "content": bot_reply})  # noqa: E501
            st.chat_message("assistant").write(bot_reply)
            quiz = generate_quiz(text, client, deployment_name)
            st.session_state["messages"].append({"role": "assistant", "content": text})  # noqa: E501
            st.session_state["messages"].append({"role": "assistant", "content": quiz})  # noqa: E501
            st.chat_message("assistant").write(quiz)

    # Flashcard ask me anything logic
    elif st.session_state["stage"] == "query":
        query = st.text_input("Ask me anything:")

        if query:
            bot_reply = "Searching most recent research /books/ articles..." + query  # noqa: E501
            st.session_state["messages"].append({"role": "assistant", "content": bot_reply})  # noqa: E501
            st.chat_message("assistant").write(bot_reply)
            search = search_internet(query, tavily_client, top_k=3)

            sources = search.get("results", [])
            if sources:
                for i, source in enumerate(sources, 1):
                    st.chat_message("assistant").write(
                        f"**Source {i}:** [{source.get('title', 'No Title')}]({source.get('url', '')})\n\n"  # noqa: E501
                        f"📌 {source.get('content', 'No content')}"
                    )
            else:
                st.chat_message("assistant").write("No sources found.")

# Run the assistant
if __name__ == "__main__":
    study_assistant()
