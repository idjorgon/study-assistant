import numpy as np
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain

subtopics_prompt = PromptTemplate(
    input_variables=["topic"],
    template="""
You are an expert educator. Break down the following topic into 5 important
subtopics. Output only the subtopics as a simple numbered list.

Topic: {topic}
"""
)

# Prompt 2 - Generate Flashcards
flashcards_prompt = PromptTemplate(
    input_variables=["subtopics"],
    template="""
                You are an expert flashcard generator.
                For each subtopic below, generate one flashcard in the following format,
                all on one line:

                Q: <question>? A: <answer>.

                Instructions:
                - Question and answer must be on the same line
                - Separate question and answer clearly using "Q: " and "A: "
                - Add bullet points before each flashcard
                - dd line break after each flashcard
                - Keep questions clear and answers concise and informative

                Subtopics:
                {subtopics}

                Flashcards:
                """
)

# Generate flashcards using OpenAI


def generate_flashcards(text, llmClient):
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

    return result['flashcards']

# Function to generate embeddings using OpenAI


def generate_embedding(text, client, deployment_name):
    """Generate an embedding vector for a given text using OpenAI's model."""
    response = client.embeddings.create(input=text, model=deployment_name)
    return np.array(response['data'][0]['embedding'], dtype=np.float32)

# Retrieve results from tavily AI calls for any question asked


def search_internet(query, client, top_k=3):
    """Search the internet."""
    queries = "Give the lastest studies/reasearch paper regarding " + query
    responses = client.search(queries, max_result=3)
    return responses

# Retrieve Books urls and names from tavily AI calls for a given topic


def search_books(topic, client):
    """Search the internet via Tavily AI."""
    query = (
        "Provide me the recent and most relevant books url that can be helpful for basic learning on topic "
        + topic
    )
    responses = client.search(query, max_result=2)
    return responses
