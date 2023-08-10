"""Module for managing vector databases and related operations.

This module provides the VectorStore class which offers functionalities for handling vector databases, 
embedding documents, and performing similarity searches.
"""
import logging
from langchain.vectorstores import FAISS, Chroma
from langchain.embeddings import OpenAIEmbeddings


class VectorStore:
    """Class to handle vector databases and operations.

    This class provides functionalities to:
    - Create, save, and load vector databases.
    - Add documents to vector databases.
    - Perform similarity searches on vector databases.

    Attributes:
    - db_name (str): Name of the vector database (e.g., "FAISS").
    - embeddings_model (str): Name of the embeddings model (e.g., "OpenAIEmbeddings").
    - embeddings (object): Embeddings object based on embeddings_model.
    - folder_path (str): Path to the folder where the database is or will be saved.
    - index_name (str): Name of the database index.
    - vector_store (object): Vector database object.
    """
    def __init__(
        self,
        db_name="FAISS",
        embeddings_model="OpenAIEmbeddings",
        folder_path="../db",
        index_name="index",
    ):
        self.db_name = db_name
        self.embeddings_model = embeddings_model
        self.embeddings = self.__embeddings()
        self.folder_path = folder_path
        self.index_name = index_name
        self.vector_store = None

    def __embeddings(self):
        if self.embeddings_model == "OpenAIEmbeddings":
            return OpenAIEmbeddings()
        else:
            raise ValueError(f"Invalid embeddings model: {self.embeddings_model}")

    def create_from_docs(self, documents, ids=None):
        """Create a vector database from a list of documents.
        
        Args:
            documents (list): List of documents to be added to the database.
            ids (list, optional): List of IDs corresponding to the documents.
        
        Returns:
            object: Vector database object.
        """
        try:
            if self.db_name == "FAISS":
                 # Will need to implement document IDs for the document chunks for more control over what is stored. This will always be None currently.
                self.vector_store = FAISS.from_documents(
                    documents, self.embeddings, ids=ids
                )
                return self.vector_store
            elif self.db_name == "Chroma":
                # TODO: implement Chroma
                self.vector_store = Chroma.from_documents(
                    documents=documents,
                    embedding=self.embeddings,
                    persist_directory="../db"
                )
                pass
            else:
                raise ValueError(f"Invalid vector store: {self.db_name}")
        except Exception as e:
            logging.error(f"Failed to create vector store: {e}")
            return None

    def save(self):
        """Save the current vector database to a local directory."""
        try:
            if self.db_name == "FAISS":
                self.vector_store.save_local(
                    folder_path=self.folder_path, index_name=self.index_name
                )
            elif self.db_name == "Chroma":
                # TODO: implement Chroma
                pass
            else:
                raise ValueError(f"Invalid vector store: {self.db}")
        except Exception as e:
            logging.error(f"Failed to save vector store: {e}")

    def load(self):
        """Load a vector database from a local directory."""
        try:
            if self.db_name == "FAISS":
                self.vector_store = FAISS.load_local(
                    folder_path=self.folder_path,
                    embeddings=self.embeddings,
                    index_name=self.index_name,
                )
                return self.vector_store
            elif self.db_name == "Chroma":
                # TODO: implement Chroma
                pass
            else:
                raise ValueError(f"Invalid vector store: {self.db}")
        except Exception as e:
            logging.error(f"Failed to load vector store: {e}")
            return None

    def add_docs(self, documents):
        """Add documents to the vector database.
        
        Args:
            documents (list): List of documents to be added.
        
        Returns:
            list: List of document IDs added to the database.
       """
        try:
            if self.db_name == "FAISS":
                return self.vector_store.add_documents(documents)
            elif self.db_name == "Chroma":
                # TODO: implement Chroma
                pass
            else:
                raise ValueError(f"Error adding document to {self.db_name}")
        except Exception as e:
            logging.error(f"Failed to add documents to vector store: {e}")
            return []

    def similarity_search(self, query, k=4):
        """Perform a similarity search in the vector database.
        
        Args:
            query (str): Query to search for.
            k (int): Number of top results to retrieve.
        
        Returns:
            list: List of most similar documents/entries.
       """
        return self.vector_store.similarity_search(query=query, k=k)

    def similarity_search_with_score(self, query, k=4):
        """Perform a similarity search in the vector database and get scores.
        
        Args:
            query (str): Query to search for.
            k (int): Number of top results to retrieve.
        
        Returns:
            list: List of most similar documents/entries along with scores.
       """
        return self.vector_store.similarity_search_with_score(query=query, k=k)

    def retriever(self):
        """Get the vector database retriever object.
        
        Returns:
            object: Retriever object.
       """
        return self.vector_store.as_retriever()
