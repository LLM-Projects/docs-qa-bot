# Docs QA Bot🤖
![Docs QA Bot Thumbnail](https://user-images.githubusercontent.com/81156510/251808915-1f5b357c-03e7-4c8b-894d-603fdc3d9ecc.png)
A streamlit app that enables users to interact with the uploaded PDF. You can ask questions or doubts regarding the PDF and our Chatbot would answer them with a friendly response.

## Tech stack
- 🐍Python
- 🛑🔥Streamlit
- 🦜️🔗Langchain
- 🔰Weaviate
- ❇️OpenAI
- 🆚Git & Github
- 🤗Hugging Face (used for testing purpose)
- 🥭MongoDB (used for testing purpose)

## Demo App
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://pdf-docs-bot.streamlit.app/)

## Working
Let's breakdown the working of the app into chunks to make it easier to understand:
- Upload the PDF
- Extract the text from the PDF file
- Generate embeddings of the text
- Store the embeddings in the vectorstore
- Retrieve the closest match
- Display the results in a Chatbot (Interface)

### Upload the PDF
<img width="728" alt="image" src="https://user-images.githubusercontent.com/81156510/251799550-555e8cb2-e0cd-48c5-8510-9b0df63cd71f.png">

- It has to be a file with `.pdf` extension and it must be within 15 MB for time being.
- Then this file will be used for further processing.


### Extract the text from the PDF file
<img width="868" alt="image" src="https://user-images.githubusercontent.com/81156510/251801666-2064ba4d-327f-49b7-9faf-a1823184089c.png">
- We need to extract the text from the PDF for which we use [PyPDF2](https://pypdf2.readthedocs.io/en/3.0.0/) library and does its part really well and quick.

### Generate embeddings of the text
<img width="216" alt="image" src="https://user-images.githubusercontent.com/81156510/251802153-f8468ff6-cd4d-4d30-a324-7db8d0daf0c7.png">
- We are then using generated text and to split the text into small chunks and create documents and are fed as input into the OpenAI Embedding library.

### Store the embeddings in the vectorstore
<img width="548" alt="image" src="https://user-images.githubusercontent.com/81156510/251802715-171ee306-77dd-48d3-91f6-2342ff575d0c.png">
- We are storing the embeddings into the Weaviate vectorstore where we have a certain schema to maintain modularity and all the embeddings are stored there.

### Retrieve the closest match
<img width="1653" alt="image" src="https://user-images.githubusercontent.com/81156510/251803274-691b681c-70ab-4f3e-896b-c447d5681091.png">
- We then run the Weaviate hybrid search on the schema, using Langchain and OpenAI that will return the closest match

### Display the results in a Chatbot (Interface)
<img width="548" alt="image" src="https://github.com/LLM-Projects/docs-qa-bot/blob/main/assets/UI.png">
- Finally we display the results as a chat like interface provided by Streamlit
