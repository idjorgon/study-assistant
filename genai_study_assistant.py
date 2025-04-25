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
    """Generate an embedding vector for a given text using OpenAI's embedding model."""
    response = client.Embedding.create(input=text, model="gpt-4-32k")
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

    response = client.completions.create(
        model=deployment_name,
        prompt=messages,
        max_tokens=300,
        temperature=0.5
    )
    # Extract and return the flashcards
    flashcards = response.choices[0].message["content"].strip()
    print(flashcards)
    return flashcards

# Summarize text using OpenAI
def summarize_text(text):
    """Summarize the input text."""
    prompt = f"""
    Summarize the following text into concise bullet points:
    ---
    {text}
    ---
    Summary:
    - 
    """
    response = client.chat.completions.create(
        model=deployment_name,
        prompt=prompt,
        max_tokens=150,
        temperature=0.5
    )
    return response.choices[0].text.strip()

# Generate quizzes using OpenAI
def generate_quiz(text):
    """Generate multiple-choice questions from input text."""
    prompt = f"""
    Create 3 multiple-choice questions from the following text. Each question should have 4 options and the correct answer should be marked with an asterisk (*):
    ---
    {text}
    ---
    Questions:
    1. 
    """
    response = client.chat.completions.create(
        model=deployment_name,
        prompt=prompt,
        max_tokens=300,
        temperature=0.7
    )
    return response.choices[0].text.strip()

# Main Study Assistant Function
def study_assistant():
    print("Welcome to the GenAI Study Assistant!")
    print("Choose an option:")
    print("1. Generate Flashcards")
    print("2. Summarize Text")
    print("3. Generate Quiz")
    print("4. Search Flashcards")
    choice = input("Enter your choice (1/2/3/4): ")

    if choice == "1":
        text = input("\nEnter the text you'd like to convert into flashcards:\n")
        print("\nGenerating Flashcards...")
        flashcards = generate_flashcards(text)
        print(f"\nFlashcards:\n{flashcards}")
        
        # Store flashcards in FAISS
        for line in flashcards.split("\n"):
            if line.startswith("Q:"):
                question = line[3:].strip()
                answer_index = flashcards.find(f"A:", flashcards.find(line))
                answer = flashcards[answer_index + 3:].split("\n")[0].strip()
                store_flashcard(question, answer)
        
        print("\nFlashcards have been stored locally in FAISS.")

    elif choice == "2":
        text = input("\nEnter the text you'd like to summarize:\n")
        print("\nSummarizing Text...")
        summary = summarize_text(text)
        print(f"\nSummary:\n{summary}")
    
    elif choice == "3":
        text = input("\nEnter the text you'd like to use for generating a quiz:\n")
        print("\nGenerating Quiz...")
        quiz = generate_quiz(text)
        print(f"\nQuiz:\n{quiz}")
    
    elif choice == "4":
        query = input("\nEnter your flashcard search query:\n")
        print("\nSearching Flashcards...")
        results = search_flashcards(query)
        print("\nRelevant Flashcards:")
        for match in results:
            print(f"Q: {match['question']}\nA: {match['answer']}\n")
    
    else:
        print("Invalid choice. Please try again.")

# Run the assistant
if __name__ == "__main__":
    study_assistant()