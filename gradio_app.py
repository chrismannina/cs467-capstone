# app.py
import gradio as gr

from src.config import Config
from src.log import setup_logging
from src.document import Document
from src.vector_store import VectorStore
from src.chat import Chat
cfg_file = "C:\\Users\\machris\\projects\\cs467-capstone\\src\\config.yaml"
# Load configuration
config = Config(cfg_file)

# Set up logging
logger = setup_logging(config)

# Set up vector store
document_paths = config.document_paths
try:
    db = VectorStore()
    logger.info("Loading vector store.")
    db.load()
    logger.info("Successfully loaded vector store.")
    # for index, doc_path in enumerate(document_paths):
    #     logger.info(f"Processing document: {doc_path}")
    #     doc = Document(
    #         document_path=doc_path,
    #         split_method=config.split_method,
    #         chunk_size=int(config.chunk_size),
    #         chunk_overlap=int(config.chunk_overlap),
    #     )
    #     if index == 0:
    #         # Use create_from_docs for the first document
    #         db.create_from_docs(doc.get_split_document())
    #     else:
    #         db.add_docs(doc.get_split_document())
    # db.save()
except Exception as e:
    logger.error(f"Failed to process documents: {e}")

# Set up chat
logger.info("Initializing chat.")
chat = Chat(config=config, retriever=db.retriever())

# Create Gradio app
logger.info("Building UI.")
app = gr.Blocks(title="GuidelineGPT", css="footer {visibility: hidden}")
with app:
    gr.Markdown("# 🐍 GuidelineGPT")
    gr.Markdown("### Clinical Practice Guidelines Q&A")
    gr.Markdown(" ⚡ <em>This is a demo. This project is still a work in progress.<em>")
    with gr.Tab("Q&A Chat"):
        gr.ChatInterface(chat.qa_response)
    gr.Markdown(
        """
    <p style="font-size: 0.8em; color: gray;">
        Created by <a href="mailto:machris@med.umich.edu" style="color: gray;">Chris Mannina</a> 📧 | 
        <a href="https://github.com/chrismannina" style="color: gray;">GitHub</a> 👤
    </p>
    """
    )

if __name__ == "__main__":
    app.launch()
