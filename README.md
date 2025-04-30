# Study Assistant

Welcome to the **Study Assistant** repository!


## Features

- **Generate Flashcards**
- **Summarize Test**
- **Generate Quiz**
- **Ask Questions**

## Getting Started

1. Create a .venv environment in VSCode (you'll need Python as a prerequisite)
2. Create .env file for API keys and other env variables (reach out for credentials):

+ AZURE_OPENAI_API_KEY
+ AZURE_ENDPOINT
+ AZURE_OPENAI_API_VERSION
+ DEPLOYMENT_NAME
+ TAVILY_KEY

3. Install dependencies located in requirements.txt

## Usage

- Type `streamlit run genai_study_assistant.py` in your terminal


## Example Workflow

### 1. Generating Flashcards

Input:
Enter the text you'd like to convert into flashcards:

Photosynthesis is the process by which green plants and some other organisms use sunlight to synthesize foods with the help of chlorophyll. The process involves carbon dioxide and water, resulting in the production of glucose and oxygen.

Generating Flashcards...

Flashcards:
1. Q: What is photosynthesis?
   A: The process by which green plants and some organisms use sunlight to synthesize food.
2. Q: What are the main reactants in photosynthesis?
   A: Carbon dioxide and water.
3. Q: What are the main products of photosynthesis?
   A: Glucose and oxygen.


### 2. Summarizing Text

Input:
Enter the text you'd like to summarize:

Photosynthesis is the process by which green plants and some other organisms use sunlight to synthesize foods with the help of chlorophyll. The process involves carbon dioxide and water, resulting in the production of glucose and oxygen.

Summarizing Text...

Summary:
- Photosynthesis is a process used by green plants to synthesize food using sunlight.
- Reactants: carbon dioxide and water.
- Products: glucose and oxygen.


### 3. Generating a Quiz

Input:
Enter the text you'd like to use for generating a quiz:

Photosynthesis is the process by which green plants and some other organisms use sunlight to synthesize foods with the help of chlorophyll. The process involves carbon dioxide and water, resulting in the production of glucose and oxygen.

Generating Quiz...

Quiz:
1. What is the primary pigment involved in photosynthesis?
   a) Hemoglobin
   b) Chlorophyll *
   c) Melanin
   d) Keratin

2. What are the main products of photosynthesis?
   a) Carbon dioxide and glucose
   b) Glucose and oxygen *
   c) Oxygen and chlorophyll
   d) Water and sunlight

3. What are the two main reactants in photosynthesis?
   a) Glucose and oxygen
   b) Carbon dioxide and water *
   c) Chlorophyll and sunlight
   d) Oxygen and water


### 4. Asking Questions

Ask any question and wait for the response (we are using Tavily to answer this based on most recent studies/books/reasearches).


## Concepts we used

1. LLM
2. Prompt Engineering
3. Chat Completion
4. Langchain, chaining of the prompts
5. Chatbox UI
6. Tavily


## Future/proposed enhancements

1. Adding images/pictures
2. Level of difficulty
