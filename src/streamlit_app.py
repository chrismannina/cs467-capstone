# app.py
import streamlit as st
import logging

from config import Config
from log import setup_logging
from document import Document
from vector_store import VectorStore
from chat import Chat

# Load configuration
config = Config("config.yaml")

# Set up logging
logger = setup_logging(config)

# Set up vector store
document_paths = config.document_paths
try:
    db = VectorStore()
    # logger.info("Loading vector store.")
    # # db.load()
    # logger.info("Successfully loaded vector store.")
    for index, doc_path in enumerate(document_paths):
        logger.info(f"Processing document: {doc_path}")
        doc = Document(
            document_path=doc_path,
            split_method=config.split_method,
            chunk_size=int(config.chunk_size),
            chunk_overlap=int(config.chunk_overlap),
        )
        if index == 0:
            # Use create_from_docs for the first document
            db.create_from_docs(doc.get_split_document())
        else:
            db.add_docs(doc.get_split_document())
    db.save()
except Exception as e:
    logger.error(f"Failed to process documents: {e}")

# Set up chat
logger.info("Initializing chat.")
chat = Chat(config=config, retriever=db.retriever())

# Create Gradio app
logger.info("Building UI.")

# Create Streamlit app
st.title("🐍 GuidelineGPT")
st.subheader("Clinical Practice Guidelines Q&A")
st.markdown(" ⚡ <em>This is a demo. This project is still a work in progress.<em>")

user_input = st.text_input("Type your question here...")

if user_input:
    response = chat.qa_response(user_input)
    st.text_area("Response:", value=response, height=200)

st.markdown(
    """
    <p style="font-size: 0.8em; color: gray;">
        Created by <a href="mailto:machris@med.umich.edu" style="color: gray;">Chris Mannina</a> 📧 | 
        <a href="https://github.com/chrismannina" style="color: gray;">GitHub</a> 👤
    </p>
    """,
    unsafe_allow_html=True,
)
