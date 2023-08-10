"""Module for handling and processing documents in the application.

This module provides the Document class which represents a document and offers functionalities to load, split, 
and access its content.
"""
import uuid
import logging

from langchain.document_loaders import OnlinePDFLoader, PyPDFLoader
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
)


class Document:
    """Class to represent and manage a document.

    This class provides functionalities to load a document from a path, split its content based on a specified method,
    and access its chunks and corresponding unique IDs.

    Attributes:
        document_path (str): Path to the document.
        split_method (str): Method to use for splitting the document content.
        chunk_size (int): Size of each chunk after splitting.
        chunk_overlap (int): Number of overlapping characters between chunks.
        document (str): Loaded content of the document.
        split_document (list): List of document chunks after splitting.
        split_document_ids (list): List of unique IDs for each chunk.
    """

    def __init__(
        self, document_path, split_method="recursive", chunk_size=1000, chunk_overlap=10
    ):
        self.document_path = document_path
        self.split_method = split_method
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.document = self.__load()
        self.split_document = self.__split()
        self.split_document_ids = self.__create_ids()

    def __load(self):
        """Load the document content from the provided path.

        Returns:
            str: Loaded content of the document.
        """
        try:
            if self.document_path.startswith("http"):
                loader = OnlinePDFLoader(self.document_path)
            elif self.document_path.endswith(".pdf"):
                loader = PyPDFLoader(self.document_path)
            else:
                raise ValueError(f"Invalid document path: {self.document_path}")
            return loader.load()
        except Exception as e:
            logging.error(f"Failed to load document: {e}")
            return None

    def __split(self):
        """Split the loaded document content based on the specified method.

        Uses either RecursiveCharacterTextSplitter or CharacterTextSplitter
        based on the split_method attribute.

        Returns:
            list: List of document chunks after splitting.
        """
        try:
            if self.split_method == "recursive":
                # TODO: implement a way to add the characters e.g. \n \t etc
                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
                )
            elif self.split_method == "character":
                splitter = CharacterTextSplitter(
                    chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
                )
            else:
                raise ValueError(f"Invalid split_method: {self.split_method}")
            return splitter.split_documents(self.document)
        except Exception as e:
            logging.error(f"Failed to split document: {e}")
            return []

    def __create_ids(self):
        """Creates IDs for document chunks.

        Returns:
            list: IDs for document chunks (UUID4)
        """
        return [str(uuid.uuid4()) for _ in self.split_document]

    def get_document(self):
        """Get full document.

        Returns:
            Full document that was loaded by loader.
        """
        return self.document

    def get_split_document(self):
        """Getter for document chunks.

        Returns:
            list: Document chunks
        """
        return self.split_document

    def get_ids(self):
        """Returns list of document chunk ids.

        Returns:
            list: IDs for document chunks (UUID4)
        """
        return self.split_document_ids

    def print_chunks(self):
        """Method to print document chunks with corresponding index number."""
        chunks = self.split()
        for i, chunk in enumerate(chunks):
            print(f"Document chunk {i}: {chunk}")
