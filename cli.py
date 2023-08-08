from src.config import Config
from src.log import setup_logging
from src.document import Document
from src.vector_store import VectorStore
from src.chat import Chat

cfg_file = "/Users/chrismannina/cs-projects/school/cs467-capstone/src/cfg_mac.yaml"
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


def main():
    query = ""
    while query != "quit":
        query = input("question: \n")
        chat.ask(query)
        # result = chat.ask(query)


if __name__ == "__main__":
    main()
