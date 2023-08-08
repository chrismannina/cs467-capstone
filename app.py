import os
import tempfile
import streamlit as st
from streamlit_chat import message

from src.config import Config
from src.log import setup_logging
from src.document import Document
from src.vector_store import VectorStore
from src.chat import Chat

# from langchain.docstore.document import Document
# from PyPDF2 import PdfReader

cfg_file = "C:\\Users\\machris\\projects\\cs467-capstone\\src\\config.yaml"
# cfg_file = "/Users/chrismannina/cs-projects/school/cs467-capstone/src/cfg_mac.yaml"

def handle_userinput(user_question, conversation):
    response = conversation.ask(user_question)
    answer = response["answer"]
    answer = answer.replace("$", "\$")
    st.write(answer)

def main():
    st.set_page_config(page_title="GuidelineGPT", page_icon=":books:")

    # Header
    st.header(":red[Chat with PDFs] :books:")

    # Sidebar for document upload
    with st.sidebar:
        st.subheader(":red[Your PDFs]")
        uploaded_files = st.file_uploader(":blue[Upload your PDFs]", accept_multiple_files=True)
        if st.button("Process PDF") and uploaded_files:
            with st.spinner("Processing"):
                # Load configuration
                cfg = Config(cfg_file)
                
                # Set up logging
                logger = setup_logging(cfg)

                logger.info("Creating vector store.")
                db = VectorStore()

                logger.info("Processing document.")
                for index, doc_path in enumerate(uploaded_files):
                    temp_file = tempfile.NamedTemporaryFile(delete=False)
                    temp_file.write(doc_path.read())
                    temp_file_path = temp_file.name

                    doc = Document(
                        document_path=temp_file_path,
                        split_method=cfg.split_method,
                        chunk_size=int(cfg.chunk_size),
                        chunk_overlap=int(cfg.chunk_overlap),
                    )
                    if index == 0:
                        # Use create_from_docs for the first document
                        db.create_from_docs(doc.get_split_document())
                    else:
                        db.add_docs(doc.get_split_document())
                    temp_file.close()
                    if temp_file_path:
                        os.remove(temp_file_path)
                db.save()

                retriever = db.retriever()
                logger.info("Initializing chat.")
                st.session_state.conversation = Chat(config=cfg, retriever=retriever)

    # Q&A interface
    if "conversation" in st.session_state:
        user_question = st.text_input(":blue[Ask a Question about your PDF : ]")
        if user_question:
            handle_userinput(user_question, st.session_state.conversation)

if __name__ == "__main__":
    main()