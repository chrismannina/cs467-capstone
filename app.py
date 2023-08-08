import os
import tempfile
import json
import streamlit as st

# from streamlit_chat import message
import re

from src.config import Config
from src.log import setup_logging
from src.document import Document
from src.vector_store import VectorStore
from src.chat import Chat

cfg_file = "C:\\Users\\machris\\projects\\cs467-capstone\\src\\config.yaml"
# cfg_file = "/Users/chrismannina/cs-projects/school/cs467-capstone/src/cfg_mac.yaml"

personal_info = """
\n
st.markdown("---")
st.markdown("### Made by Chris Mannina")
st.markdown("[Email me](mailto:chrismannina@example.com) | [GitHub](https://github.com/chrismannina)")
"""


def clean_document_chunks(chunks):
    cleaned_chunks = {}
    for idx, chunk in enumerate(chunks):
        page_content = chunk.page_content
        # Remove '\n', '\t', '\n\n', extra spaces, and leading 'COPY'
        cleaned_content = re.sub(r"\n|\t|\s{2,}", " ", page_content).replace("COPY", "")
        cleaned_chunks[idx + 1] = cleaned_content
    return cleaned_chunks


def handle_userinput(user_question, conversation):
    response = conversation.ask(user_question)
    answer = response["answer"]
    answer = answer.replace("$", "\\$")
    st.write(answer)
    # Convert the response to JSON format
    json_response = json.dumps(response, default=lambda o: o.__dict__, indent=4)

    # Display retrieved document chunks
    with st.expander("View Retrieved Documents"):
        cleaned_chunks = clean_document_chunks(response["source_documents"])
        st.write(cleaned_chunks)


def main():
    st.set_page_config(page_title="DocDigest MD", page_icon=":stethoscope:")

    hide_default_format = """<style>
                            #MainMenu {visibility: hidden; }
                            footer {visibility: hidden;}
                            </style>
                            """
    st.markdown(hide_default_format, unsafe_allow_html=True)

    # Header with branding
    st.header(":page_facing_up::mag: DocDigest MD")
    st.subheader("Simplifying Medical Documents")
    st.write(
        "Leverage the power of language models to get insights from your medical documents."
    )

    # Sidebar for settings adjustments and document upload
    with st.sidebar:
        with st.expander(":information_source: Getting Started", expanded=False):
            # st.markdown("### Getting Started")
            st.markdown("- Adjust settings if required.")
            st.markdown("- Upload your medical documents.")
            st.markdown("- Ask any relevant questions about the document.")
            st.markdown("- View retrieved document chunks for more context.")
            # if st.button("Got it!"):
            #     st.session_state.onboarded = True

        with st.expander(":gear: Settings", expanded=False):
            # st.subheader(":gear: Settings")
            if not st.session_state.get("data_processed"):
                # Model selection
                model_option = st.selectbox(
                    "Select the LLM Model",
                    ["gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-4", "gpt-4-32k"],
                    index=0,
                )

                # Temperature adjustment
                temperature = st.slider(
                    "Adjust LLM Temperature",
                    min_value=0.0,
                    max_value=2.0,
                    value=0.0,
                    step=0.1,
                )

                # Chunk size and overlap adjustment
                chunk_size = st.slider(
                    "Adjust Chunk Size",
                    min_value=100,
                    max_value=3000,
                    value=2000,
                    step=50,
                )
                chunk_overlap = st.slider(
                    "Adjust Chunk Overlap",
                    min_value=0,
                    max_value=500,
                    value=100,
                    step=50,
                )
            if st.session_state.get("data_processed"):
                if st.button("Reset App"):
                    # Delete the database files
                    db_dir = "C:\\Users\\machris\\projects\\cs467-capstone\\db"
                    for file in os.listdir(db_dir):
                        os.remove(os.path.join(db_dir, file))

                    # Reset session state variables
                    if "data_processed" in st.session_state:
                        del st.session_state.data_processed
                    if "conversation" in st.session_state:
                        del st.session_state.conversation

                    # Rerun the Streamlit app
                    st.experimental_rerun()

        if not st.session_state.get("data_processed"):
            with st.expander(":file_folder: Upload Documents", expanded=False):
                uploaded_files = st.file_uploader(
                    ":blue[Upload Medical PDFs]", accept_multiple_files=True
                )
                if st.button("Process Document") and uploaded_files:
                    with st.spinner("Processing"):
                        # Load configuration and adjust settings
                        cfg = Config(cfg_file)
                        cfg.llm_model = model_option
                        cfg.temperature = temperature
                        cfg.chunk_size = chunk_size
                        cfg.chunk_overlap = chunk_overlap
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
                        st.session_state.conversation = Chat(
                            config=cfg, retriever=retriever
                        )
                        st.session_state.data_processed = True

        with st.expander(":computer: About", expanded=False):
            st.markdown("### Medical Document Q&A")
            st.markdown("#### How it works?")
            st.markdown(
                """When a document is uploaded, text is extracted from the document. This text is then split into shorter text chunks, 
                        and an embedding is created for each text chunk. When the user asks a question, an embedding is created for the question, 
                        and a similarity search is performed to find the file chunk embeddings that are most similar to the question (i.e. have highest 
                        cosine similarities with the question embedding). An API call is then made to the completions endpoint, with the question and 
                        the most relevant file chunks are included in the prompt. The generative model then gives the answer to the question found in 
                        the file chunks, if the answer can be found in the extracts.
                        """
            )
            st.markdown("---")
            st.markdown(
                "Made by Chris Mannina [📧](mailto:machris@umich.edu) | [👤](https://github.com/chrismannina)"
            )

    # # User Onboarding
    # if not st.session_state.get("onboarded"):
    #     with st.expander("Harness the power of advanced language models to get insights from your medical documents."):
    #         st.markdown("### Getting Started")
    #         st.markdown("- Adjust settings if required.")
    #         st.markdown("- Upload your medical documents.")
    #         st.markdown("- Ask any relevant questions about the document.")
    #         st.markdown("- View retrieved document chunks for more context.")
    #         if st.button("Got it!"):
    #             st.session_state.onboarded = True

    # Q&A Section
    if "conversation" in st.session_state:
        user_question = st.text_input(
            "Enter your question about the uploaded documents:"
        )
        if user_question:
            handle_userinput(user_question, st.session_state.conversation)

    # st.footer(
    #     """
    # <p style="font-size: 0.8em; color: gray;">
    #     Created by <a href="mailto:machris@med.umich.edu" style="color: gray;">Chris Mannina</a> 📧 |
    #     <a href="https://github.com/chrismannina" style="color: gray;">GitHub</a> 👤
    # </p>
    # """
    # )


if __name__ == "__main__":
    main()
