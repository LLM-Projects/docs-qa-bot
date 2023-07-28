# External libraries
import streamlit as st
from streamlit_chat import message
import time
from PyPDF2 import PdfReader

# Internal file imports
from extract import extract_text
from embeddings import create_embeddings
from store import store_embeddings
# from qa import search_qa
from chat import chat_with_pdf

# Start of streamlit application
st.title("PDF QA Bot using Langchain")

# Intitialization
st.header("File upload")
file = st.file_uploader("Choose a file (PDF)", type="pdf", help="file to be parsed")

if file is not None:
    # @st.cache_data
    data = extract_text(file)
    # st.text(data, help="Extracted text from uploaded pdf")

    # Create, display, search and query the embeddings
    st.header("Create Embeddings")
    texts, embeddings, embeds_df = create_embeddings(
        data, st.secrets["OPENAI_API_KEY"]
    )
    st.text("Created successfully...")

    if store_embeddings(embeds_df):
        st.success("Data saved successfully...", icon="✅")
    else:
        st.error("Operation not successful. Please reach out to support...", icon="❌")

else:
    st.error("Upload the file to proceed further", icon="🚨")

# Create, display, search and query the embeddings
# st.header("Create Embeddings")
# texts, embeddings, embeds_df = create_embeddings(
#     data, st.secrets["OPENAI_API_KEY"]
# )
# st.text("Created successfully...")

# if store_embeddings(embeds_df):
#     st.success("Data saved successfully...", icon="✅")
# else:
#     st.error("Operation not successful. Please reach out to support...", icon="❌")

# st.header("Ask QA to your PDF...")
# prompt = st.text_input("Enter your query to retrieve answer from my knowledge...")
# if(prompt):
#     st.text(search_qa(texts, embeddings, prompt))
#     st.text('Works...')
# st.header("Ask QA to your PDF...")
# prompt = st.text_input("Enter some text", "")
# response = search_qa(texts, embeddings, prompt)
# st.write("Answer:", response)

# Chat component to chat with your uploaded PDF
st.header("Chat with your PDF...")
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def get_text():
    input_text = st.chat_input("Enter your query to retrieve answer from my knowledge...")
    return input_text

user_input = get_text()

if user_input:
    output = chat_with_pdf(data, embeddings, user_input)

    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')

