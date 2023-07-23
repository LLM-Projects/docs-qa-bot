from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Weaviate
from langchain.chains import RetrievalQAWithSourcesChain
from langchain import OpenAI

from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

import streamlit as st

@st.cache_data
def chat_with_pdf(_text, _embeddings, chat_prompt):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_text(_text)

    system_template="""Use the following pieces of context to answer the users question. 


    Begin!
    ----------------
    {summaries}
    """

    messages = [
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template("{question}")
    ]
    prompt = ChatPromptTemplate.from_messages(messages)


    docsearch = Weaviate.from_texts(
        texts,
        _embeddings,
        weaviate_url=st.secrets["WEAVIATE_CLUSTER_URL"],
        by_text=False,
        metadatas=[{"source": f"{i}-pl"} for i in range(len(texts))],
    )

    def get_chain(store):
        chain_type_kwargs = {"prompt": prompt}
        chain = RetrievalQAWithSourcesChain.from_chain_type(
            OpenAI(temperature=0), 
            chain_type="stuff", 
            retriever=store.as_retriever(),
            chain_type_kwargs=chain_type_kwargs,
            reduce_k_below_max_tokens=True
        )
        return chain
    
    chain = get_chain(docsearch)


    # chain = RetrievalQAWithSourcesChain.from_chain_type(
    #     OpenAI(temperature=0), chain_type="stuff", retriever=docsearch.as_retriever()
    # )

    response = chain(
        {"question": chat_prompt},
        return_only_outputs=True,
    )

    print(response["answer"])
    return response["answer"]
