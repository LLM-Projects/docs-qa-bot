from PyPDF2 import PdfReader
import streamlit as st

@st.cache_data()
def extract_text(_file):
    """
        :param file: the PDF file to extract
    """
    content = ""
    reader = PdfReader(_file)
    number_of_pages = len(reader.pages)

    # Scrape text from multiple pages
    for i in range(number_of_pages):
        page = reader.pages[i]
        text = page.extract_text()
        content = content + text

    return content

