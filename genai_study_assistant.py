import streamlit as st
import os
from openai import AzureOpenAI
import faiss
import numpy as np
from dotenv import load_dotenv

# Set up your OpenAI API key and credentials
load_dotenv(".env")
api_key = os.getenv('AZURE_OPENAI_API_KEY')
api_endpoint = os.getenv('AZURE_ENDPOINT')
deployment_name = os.getenv('DEPLOYMENT_NAME')

client = AzureOpenAI(
  azure_endpoint=api_endpoint,
  api_key=api_key,  
  api_version="2025-01-01-preview"
)
    
# Initialize FAISS index
embedding_dim = 1536  # Dimensionality of OpenAI's model embedding
faiss_index = faiss.IndexFlatL2(embedding_dim)  # L2 distance for similarity search
flashcard_metadata = []  # List to store flashcard metadata (question, answer)

# Function to generate embeddings using OpenAI
def generate_embedding(text):
    """Generate an embedding vector for a given text using OpenAI's model."""
    response = client.embeddings.create(input=text, model=deployment_name)
    return np.array(response['data'][0]['embedding'], dtype=np.float32)

# Store flashcards in FAISS
def store_flashcard(question, answer):
    """Store a flashcard's embedding and metadata in FAISS."""
    text = f"Q: {question}\nA: {answer}"
    embedding = generate_embedding(text)
    faiss_index.add(np.array([embedding]))  # Add embedding to FAISS index
    flashcard_metadata.append({"question": question, "answer": answer})  # Store metadata

# Retrieve similar flashcards
def search_flashcards(query, top_k=3):
    """Search for similar flashcards in FAISS based on a query."""
    query_embedding = generate_embedding(query)
    distances, indices = faiss_index.search(np.array([query_embedding]), top_k)  # FAISS search
    results = [flashcard_metadata[i] for i in indices[0] if i < len(flashcard_metadata)]
    return results

# Generate flashcards using OpenAI
def generate_flashcards(text):
    """Generate flashcards (Q&A pairs) from input text."""

    messages = [
        {"role": "system", "content": "You are an assistant that creates educational flashcards."},
        {"role": "user", "content": f"Create flashcards in Q&A format from the following text:\n\n{text}"}
    ]

    response = client.chat.completions.create(
        model=deployment_name,
        messages=messages,
        max_tokens=300,
        temperature=0.5
    )
    # Extract and return the flashcards
    flashcards = response.choices[0].message.content
    #print(flashcards)
    return flashcards

# Summarize text using OpenAI
def summarize_text(text):
    """Summarize the input text."""
    
    messages = [
        {"role": "system", "content": "You are an assistant that summarizes input text."},
        {"role": "user", "content": f"Summarize the following text into concise bullet points:\n\n{text}"}
    ]
    
    response = client.chat.completions.create(
        model=deployment_name,
        messages=messages,
        max_tokens=150,
        temperature=0.5
    )
    return response.choices[0].message.content

# Generate quizzes using OpenAI
def generate_quiz(text):
    """Generate multiple-choice questions from input text."""
    
    messages = [
        {"role": "system", "content": "You are an assistant that generates multiple-choice questions from input text."},
        {"role": "user", "content": f"Generate multiple-choice questions from the input text:\n\n{text}"}
    ]
        
    response = client.chat.completions.create(
        model=deployment_name,
        messages=messages,
        max_tokens=300,
        temperature=0.7
    )

    return response.choices[0].message.content

# Main Study Assistant Function
def study_assistant():

    with st.sidebar:
        "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
        "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title(" My Study Assistant ")

# Initialize chat history and state
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Welcome to the GenAI Study Assistant!:\n1. Generate Flashcards 📚\n2. Summarize Text 📜\n3. Generate Quiz 🌎 \n4. Search Flashcards!"}]
    st.session_state["stage"] = "main_menu"

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# if choice:
#     st.chat_message("user").write(choice)
#     st.session_state.messages.append({"role": "user", "content": choice})

if st.session_state.stage == "main_menu":
    choice = st.text_input("Enter your choice .. ") 
    
    if choice:
        st.session_state.messages.append({"role": "user", "content": choice})
    
        if choice == "1":
            st.session_state["stage"]="flashcard"
        
        elif choice == "2":
            st.session_state["stage"]="summarize"      
        # text = input("\nEnter the text you'd like to summarize:\n")
        # print("\nSummarizing Text...")      
        # print(f"\nSummary:\n{summary}")
    
        elif choice == "3":
            st.session_state["stage"]="quiz"
        
        elif choice == "4":
            st.session_state["stage"]="query"
    
        else:
            bot_reply ="Invalid choice. Please try again."
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            st.chat_message("assistant").write(bot_reply)
       

if st.session_state["stage"] == "summarize":
    text=st.text_input("Enter the text you'd like to summarize:")
        
    if text:
        summary = summarize_text(text)
        st.session_state.messages.append({"role": "assistant", "content": summary})
        st.chat_message("assistant").write(summary)

elif st.session_state["stage"] == "flashcard":
    flashcard_word=st.text_input("Enter the text you'd like to convert into flashcards")
            
    if flashcard_word:
        bot_reply= "Generating Flashcards for ..." + flashcard_word
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        st.chat_message("assistant").write(bot_reply)
        #text = input("\nEnter the text you'd like to convert into flashcards:\n")
        #print("\nGenerating Flashcards...")
        flashcards = generate_flashcards(flashcard_word)
        st.session_state.messages.append({"role": "assistant", "content": flashcards})
        st.chat_message("assistant").write(flashcards)
        # print(f"\nFlashcards:\n{flashcards}")
        
        # Store flashcards in FAISS
        for line in flashcards.split("\n"):
            if line.startswith("Q:"):
                question = line[3:].strip()
                answer_index = flashcards.find(f"A:", flashcards.find(line))
                answer = flashcards[answer_index + 3:].split("\n")[0].strip()
                store_flashcard(question, answer)
        
        print("\nFlashcards have been stored locally in FAISS.")

elif st.session_state["stage"] == "quiz" :
    text=st.text_input("Enter the text you'd like to use for generating a quiz:")
        
    if text:    
        bot_reply= "Generating Quiz ..." + text
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        st.chat_message("assistant").write(bot_reply)
        # print("\nGenerating Quiz...")
        quiz = generate_quiz(text)
        st.session_state.messages.append({"role": "assistant", "content": quiz})
        st.chat_message("assistant").write(quiz)
        # print(f"\nQuiz:\n{quiz}")

elif st.session_state["stage"] == "query" :
    query=st.text_input("Enter your flashcard search query:")
        # query = input("\nEnter your flashcard search query:\n")

    if query:
        bot_reply= "Searching Flashcards..." + query
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        st.chat_message("assistant").write(bot_reply)
        
        # print("\nSearching Flashcards...")
        results = search_flashcards(query)
        st.session_state.messages.append({"role": "assistant", "content": results})
        st.chat_message("assistant").write(results)
        # print("\nRelevant Flashcards:")
        for match in results:
            print(f"Q: {match['question']}\nA: {match['answer']}\n")

# Run the assistant
if __name__ == "__main__":
    study_assistant()
