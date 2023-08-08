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

# cfg_file = "C:\\Users\\machris\\projects\\cs467-capstone\\src\\config.yaml"
cfg_file = "/Users/chrismannina/cs-projects/school/cs467-capstone/src/cfg_mac.yaml"


def handle_userinput(user_question):
    response = st.session_state.conversation({"question": user_question})
    st.session_state.chat_history = response["chat_history"]

    for i, message in enumerate(st.session_state.chat_history):
        st.write(message.content)
        # if i % 2 == 0:
        #     st.write(user_template.replace(
        #         "{{MSG}}", message.content), unsafe_allow_html=True)
        # else:
        #     st.write(bot_template.replace(
        #         "{{MSG}}", message.content), unsafe_allow_html=True)


def main():
    st.set_page_config(page_title="GuidelineGPT", page_icon=":books:")
    # st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header(":red[Chat with PDFs] :books:")
    user_question = st.text_input(":blue[Ask a Questions about your PDF : ]")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        # st.subheader(":red[Enter your OpenAI API key]")
        # user_api_key = st.text_input(":blue[Your API KEY]", type="password", key="api_key_input")
        # if st.button("Enter"):
        #     os.environ["OPENAI_API_KEY"] = user_api_key
        st.subheader(":red[Your PDFs]")
        uploaded_files = st.file_uploader(
            ":blue[Upload your PDFs]", accept_multiple_files=True
        )
        if st.button("Process PDF"):
            with st.spinner("Processing"):
                # Load configuration
                cfg = Config(cfg_file)
                print(cfg.log_to_file)
                # Set up logging
                logger = setup_logging(cfg)

                logger.info("Creating vector store.")
                db = VectorStore()

                logger.info("Processing document.")

                if uploaded_files is not None:
                    for index, doc_path in enumerate(uploaded_files):
                        print(index, doc_path)

                        logger.info(f"Processing document: {doc_path}")
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

                print(db.vector_store)
                retriever = db.retriever()

                logger.info("Initializing chat.")
                # chat = Chat(config=cfg, retriever=retriever)

                # create conversation chain
                st.session_state.conversation = Chat(config=cfg, retriever=retriever)


if __name__ == "__main__":
    main()
