import os
import tempfile
import re
import streamlit as st
from dotenv import load_dotenv

from src.config import Config
from src.log import setup_logging
from src.document import Document
from src.vector_store import VectorStore
from src.chat import Chat
from src.utils import validate_openai_key
from src.prompts import QA_PROMPTS

cfg_file = "./config/cfg_mac.yaml"

def get_prompt(category, prompt_name):
    return QA_PROMPTS[category][prompt_name]["prompt"]

def clean_document_chunks(chunks):
    """
    Clean the content of document chunks by removing unwanted characters and patterns.

    Parameters:
    - chunks (dict): Dictionary containing document chunks to be cleaned.

    Returns:
    - dict: Dictionary containing cleaned document chunks.
    """
    cleaned_chunks = {}
    for idx, chunk in enumerate(chunks):
        page_content = chunk.page_content
        # Remove '\n', '\t', '\n\n', extra spaces, and leading 'COPY'
        cleaned_content = re.sub(r"\n|\t|\s{2,}", " ", page_content).replace("COPY", "")
        cleaned_chunks[idx + 1] = cleaned_content
    return cleaned_chunks


def handle_userinput(user_question, conversation):
    """
    Process the user's question and display the AI-generated response.

    Parameters:
    - user_question (str): The question posed by the user.
    - conversation (object): An instance of the Chat class to manage the conversation.

    Returns:
    None
    """
    response = conversation.ask(user_question)
    answer = response["answer"]
    answer = answer.replace("$", "\\$")
    st.write(answer)
    # Display retrieved document chunks
    with st.expander("View Retrieved Documents"):
        cleaned_chunks = clean_document_chunks(response["source_documents"])
        st.write(cleaned_chunks)


def main():
    """
    The main function that defines the Streamlit interface and handles user interactions.

    Returns:
    None
    """
    st.set_page_config(page_title="DocDigest MD", page_icon=":stethoscope:")

    # Hide default Streamlit format
    hide_default_format = """<style>
                            #MainMenu {visibility: hidden; }
                            footer {visibility: hidden;}
                            </style>
                            """
    st.markdown(hide_default_format, unsafe_allow_html=True)

    # Load configuration
    cfg = Config(cfg_file)

    # Set up logging
    logger = setup_logging(cfg)

    # Add header for webapp
    st.header(":page_facing_up::mag: DocDigest MD")
    st.subheader("Simplifying Medical Documents")
    st.write(
        "Leverage the power of language models to get insights from your medical documents."
    )

    # Sidebar for settings, document upload, and application information
    with st.sidebar:
        with st.expander(":computer: About", expanded=False):
            st.markdown("### Medical Document Q&A")
            st.markdown("#### How it works?")
            st.markdown(
                """When a document is uploaded, text is extracted from the document. This text is then split into smaller text chunks, 
                        and an embedding is created for each chunk. When the user asks a question, an embedding is created for the question, 
                        and a similarity search is performed to find the document chunks that are most similar to the question. Once the
                        relevant documents are return, a prompt is crafted with the user question and relevant context, and an API call is 
                        then made to the chat completions endpoint. The LLM model then gives the answer to the question using the document
                        chunks as context. 
                        """
            )
            st.markdown("---")
            st.markdown(
                "Made by Chris Mannina [📧](mailto:manninac@oregonstate.edu) | [👤](https://github.com/chrismannina)"
            )

        with st.expander(":key: OpenAI API Key", expanded=True):
            # Check if API key is set to visible, default is hidden
            if "api_key_visible" not in st.session_state:
                st.session_state.api_key_visible = False

            api_key_input = st.text_input(
                "Enter your OpenAI API key:", value="", type="password"
            )

            # Place "Submit" and "Reset" buttons on the same row
            submit_button, reset_button = st.columns(2)

            # If "Submit" button is pressed, set the API key.
            if submit_button.button("Submit Key", help="Set your API key."):
                if api_key_input == "cant stop":
                    st.session_state.api_key = api_key_input
                    st.success("addicted to the shingdig", icon="🌶️")
                elif validate_openai_key(api_key_input):
                    st.session_state.api_key = api_key_input
                    os.environ["OPENAI_API_KEY"] = api_key_input
                    st.success("API key accepted!", icon="✅")
                else:
                    st.error(
                        "Invalid OpenAI key. Please enter a valid OpenAI key.", icon="🚨"
                    )
            # Reset API key
            if reset_button.button("Reset Key", help="Removes API key."):
                try:
                    del st.session_state.api_key
                except Exception as e:
                    logger.error(f"API key not in Streamlit session state: {e}")
                try:
                    del os.environ["OPENAI_API_KEY"]
                    st.success("OpenAI API key reset successfully!", icon="✅")
                except Exception as e:
                    logger.error(f"Failed to delete API key: {e}")

        with st.expander(":gear: Settings", expanded=False):
            if not st.session_state.get("data_processed"):
                # Model selection
                model_option = st.selectbox(
                    "Select the LLM Model",
                    ["gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-4", "gpt-4-32k"],
                    index=0,
                )

                # Temperature adjustment
                temperature = st.slider(
                    "LLM Temperature",
                    min_value=0.0,
                    max_value=1.0,
                    value=0.0,
                    step=0.1,
                )

                # Chunk size and overlap adjustment
                chunk_size = st.slider(
                    "Chunk Size",
                    min_value=100,
                    max_value=3000,
                    value=2000,
                    step=50,
                )
                chunk_overlap = st.slider(
                    "Chunk Overlap",
                    min_value=0,
                    max_value=500,
                    value=100,
                    step=50,
                )
                
            if st.session_state.get("data_processed"):
                if st.button(
                    "Reset App",
                    help="Reset chat and load a different document for Q&A.",
                ):
                    # Path to database files
                    db_dir = "./db"

                    # Delete the database files
                    for file in os.listdir(db_dir):
                        file_path = os.path.join(db_dir, file)
                        try:
                            # Check if it's a file and not named .gitkeep
                            if os.path.isfile(file_path) and file != ".gitkeep":
                                os.remove(file_path)
                        except Exception as e:
                            logger.error(
                                f"Error deleting file {file_path}. Reason: {e}"
                            )

                    # Reset session state variables
                    if "data_processed" in st.session_state:
                        del st.session_state.data_processed
                    if "conversation" in st.session_state:
                        del st.session_state.conversation

                    # Rerun the Streamlit app
                    st.experimental_rerun()
                    
        with st.expander(":speech_balloon: Prompts", expanded=False):
            if not st.session_state.get("data_processed"):
                # Dropdown to select a category
                selected_category = st.selectbox("Choose a prompt category:", list(QA_PROMPTS.keys()))

                # Dropdown to select a prompt within the chosen category
                selected_prompt_name = st.selectbox("Choose a prompt style:", list(QA_PROMPTS[selected_category].keys()))
                selected_prompt = QA_PROMPTS[selected_category][selected_prompt_name]["prompt"]
                
                # Display the description of the selected prompt style
                st.info(QA_PROMPTS[selected_category][selected_prompt_name]["description"])


        # Document upload section - dissapears once documents are uploaded
        if not st.session_state.get("data_processed"):
            with st.expander(":file_folder: Upload Documents", expanded=False):
                uploaded_files = st.file_uploader(
                    ":violet[Upload PDFs]", accept_multiple_files=True
                )
                if st.button("Process Document") and uploaded_files:
                    if not os.getenv("OPENAI_API_KEY", None):
                        st.warning("Please enter a valid OpenAI API key.", icon="⚠️")
                        logger.info("Processing document error: invalid API key")
                    else:
                        with st.spinner("Processing"):
                            # Change configuration based on sliders
                            cfg.llm_model = model_option
                            cfg.temperature = temperature
                            cfg.chunk_size = chunk_size
                            cfg.chunk_overlap = chunk_overlap

                            # Initiate vectorstore
                            db = VectorStore()

                            # Process each uploaded document
                            for index, doc_path in enumerate(uploaded_files):
                                # Extract the extension of the uploaded file
                                file_extension = os.path.splitext(doc_path.name)[1]

                                # Create a temporary file to store the uploaded document
                                temp_file = tempfile.NamedTemporaryFile(
                                    delete=False, suffix=file_extension
                                )
                                temp_file.write(doc_path.read())
                                temp_file_path = temp_file.name

                                # Create a Document instance for processing
                                doc = Document(
                                    document_path=temp_file_path,
                                    split_method=cfg.split_method,
                                    chunk_size=int(cfg.chunk_size),
                                    chunk_overlap=int(cfg.chunk_overlap),
                                )
                                # If it's the first document, create a new vector store, else add to the existing one
                                if index == 0:
                                    db.create_from_docs(doc.get_split_document())
                                else:
                                    db.add_docs(doc.get_split_document())

                                # Close and delete the temporary file
                                temp_file.close()
                                if temp_file_path:
                                    os.remove(temp_file_path)

                            # Save the vector store
                            db.save()

                            # Initialize the retriever and chat using the saved vector store
                            retriever = db.retriever()
                            st.session_state.conversation = Chat(
                                config=cfg, retriever=retriever, qa_prompt=selected_prompt
                            )
                            # Mark that data processing is complete
                            st.session_state.data_processed = True

    # Q&A Section
    if "conversation" not in st.session_state:
        with st.expander(":information_source: Getting Started", expanded=True):
            st.markdown("- Enter your OpenAI API key.")
            st.markdown("- Adjust settings if preferred.")
            st.markdown("- Select prompt template you want to use.")
            st.markdown("- Upload your document(s).")
            st.markdown("- Ask a question about the uploaded document(s).")
            st.markdown(
                "- Get response and view retrieved document chunks for more context."
            )

    if "conversation" in st.session_state:
        user_question = st.text_input(
            "Enter your question about the uploaded documents:"
        )

        if user_question:
            handle_userinput(user_question, st.session_state.conversation)


if __name__ == "__main__":
    main()
