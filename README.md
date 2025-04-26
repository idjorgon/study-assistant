# Study Assistant

Welcome to the **Study Assistant** repository

## Features
- **Flashcards**
- **Summarize Test**
- **Generate Quiz**

## Getting Started

Create .env file - please reach out for credentials

## Example Workflow

### 1. Generating Flashcards

User Input:
Enter the text you'd like to convert into flashcards:

Photosynthesis is the process by which green plants and some other organisms use sunlight to synthesize foods with the help of chlorophyll. The process involves carbon dioxide and water, resulting in the production of glucose and oxygen.

Assistant Output:
Generating Flashcards...

Flashcards:
1. Q: What is photosynthesis?
   A: The process by which green plants and some organisms use sunlight to synthesize food.
2. Q: What are the main reactants in photosynthesis?
   A: Carbon dioxide and water.
3. Q: What are the main products of photosynthesis?
   A: Glucose and oxygen.


### 2. Summarizing Text

User Input:
Enter the text you'd like to summarize:

Photosynthesis is the process by which green plants and some other organisms use sunlight to synthesize foods with the help of chlorophyll. The process involves carbon dioxide and water, resulting in the production of glucose and oxygen.

Assistant Output:
Summarizing Text...

Summary:
- Photosynthesis is a process used by green plants to synthesize food using sunlight.
- Reactants: carbon dioxide and water.
- Products: glucose and oxygen.


### 3. Generating a Quiz

User Input:
Enter the text you'd like to use for generating a quiz:

Photosynthesis is the process by which green plants and some other organisms use sunlight to synthesize foods with the help of chlorophyll. The process involves carbon dioxide and water, resulting in the production of glucose and oxygen.

Assistant Output:
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


### 4. Searching Flashcards

User Input:
Enter your flashcard search query: 
What is photosynthesis?

Assistant Output:
Searching Flashcards...

Relevant Flashcards:
Q: What is photosynthesis?
A: The process by which green plants and some organisms use sunlight to synthesize food.

Q: What are the main reactants in photosynthesis?
A: Carbon dioxide and water.

Q: What are the main products of photosynthesis?
A: Glucose and oxygen.

## Planning Board

Add connection to the model
Prompt Engineering
Chat Completion
Chaining of the prompts, agents
Chatbox UI

#### Questions & Answers

Q. Vector Database concepts + embeddings suggestions; 
A. Not the end of the world if no vector database

Q. Can we use any Huggingface model? Clarification on model? 
A. Can use any model - no client data

Q. If there is any use case that Joe feels like where we can use Embeddings and vector store? 
A. Can create a knowledge store for our use case

Q. Could we use two models together like picture generation models or any hugging face model? 
A. Yes, Dall-e; would have to have two different calls for two models

Q. Can we deploy other models in Azure? 
A. Can deploy da-vinci; double check with Joe first
