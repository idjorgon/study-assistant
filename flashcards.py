import faiss
import numpy as np


# Generate flashcards using OpenAI
def generate_flashcards(text,client, deployment_name):
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

# Initialize FAISS index
embedding_dim = 1536  # Dimensionality of OpenAI's model embedding
faiss_index = faiss.IndexFlatL2(embedding_dim)  # L2 distance for similarity search
flashcard_metadata = []  # List to store flashcard metadata (question, answer)

# Function to generate embeddings using OpenAI
def generate_embedding(text,client, deployment_name):
    """Generate an embedding vector for a given text using OpenAI's model."""
    response = client.embeddings.create(input=text, model=deployment_name)
    return np.array(response['data'][0]['embedding'], dtype=np.float32)

# Store flashcards in FAISS
def store_flashcard(question, answer,client, deployment_name):
    """Store a flashcard's embedding and metadata in FAISS."""
    text = f"Q: {question}\nA: {answer}"
    embedding = generate_embedding(text,client, deployment_name)  # Generate embedding
    faiss_index.add(np.array([embedding]))  # Add embedding to FAISS index
    flashcard_metadata.append({"question": question, "answer": answer})  # Store metadata

# Retrieve similar flashcards
def search_flashcards(query, client, deployment_name,top_k=3):
    """Search for similar flashcards in FAISS based on a query."""
    query_embedding = generate_embedding(query,client, deployment_name)  # Generate embedding for the query
    distances, indices = faiss_index.search(np.array([query_embedding]), top_k)  # FAISS search
    results = [flashcard_metadata[i] for i in indices[0] if i < len(flashcard_metadata)]
    return results


