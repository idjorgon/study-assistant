import asyncio
import faiss
import numpy as np
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain

subtopics_prompt = PromptTemplate(
    input_variables=["topic"],
    template="""
You are an expert educator. Break down the following topic into 5 important subtopics. Output only the subtopics as a simple numbered list.

Topic: {topic}
"""
)

# Prompt 2 - Generate Flashcards
flashcards_prompt = PromptTemplate(
    input_variables=["subtopics"],
    template="""
You are a flashcard creator. For each of the following subtopics, create a simple flashcard. Each flashcard should have a Question and Answer format. Keep the explanation concise but clear.

Subtopics:
{subtopics}
"""
)

# Generate flashcards using OpenAI
def generate_flashcards(text,llmClient):
    
    """Generate flashcards (Q&A pairs) from input text."""
    # Chain 1 - Subtopics Generation
    subtopics_chain = LLMChain(
        llm=llmClient,
        prompt=subtopics_prompt,
        output_key="subtopics",
    )

    # Chain 2 - Flashcards Generation
    flashcards_chain = LLMChain(
        llm=llmClient,
        prompt=flashcards_prompt,
        output_key="flashcards",
    )

    # 4. Chain them together
    overall_chain = SequentialChain(
        chains=[subtopics_chain, flashcards_chain],
        input_variables=["topic"],
        output_variables=["subtopics", "flashcards"],
        verbose=True,  # (optional) show intermediate steps
    )
    input_topic = text

    # Run the final chain
    result = overall_chain.invoke({"topic": input_topic})

    #print(flashcards)
    return result['flashcards']

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
def search_internet(query, client,top_k=3):
    """Search the internet."""
    queries ="Give the lastest studies/reasearch paper regarding " + query
    responses = client.search(queries , max_result=3)  # Generate embedding for the query
    return responses


