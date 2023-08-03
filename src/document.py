"""Class and methods for documents"""
import uuid
import logging

from langchain.document_loaders import OnlinePDFLoader, PyPDFLoader
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
)


class Document:
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
        # Create IDs for each chunk
        return [str(uuid.uuid4()) for _ in self.split_document]

    def get_document(self):
        # Return document
        return self.document

    def get_split_document(self):
        # Return document chunks
        return self.split_document

    def get_ids(self):
        # Return list of IDs for document
        return self.split_document_ids

    def print_chunks(self):
        # Print the chunked representation of the document
        chunks = self.split()
        for i, chunk in enumerate(chunks):
            print(f"Document chunk {i}: {chunk}")


# TODO: split out metadatas from docs - then update funcs for vectorDB.
# TODO: will need to use add_texts vectorstore funcs, then we can use IDs, and save metadata to the Doc class
# TODO: this will give ability tyo add more and delete documents and search more easily from metadata.
# TODO: add function/method to clean the split texts - could try using ChatGPT to clean each sentence? Or

# elif self.split_method == "tiktoken":
#     splitter = CharacterTextSplitter.from_tiktoken_encoder(
#         chunk_size=self.chunk_size,
#         chunk_overlap=self.chunk_overlap
#     )

# def split_documents(self, documents: Iterable[Document]) -> List[Document]:
#     """Split documents."""
#     texts, metadatas = [], []
#     for doc in documents:
#         texts.append(doc.page_content)
#         metadatas.append(doc.metadata)
#     return self.create_documents(texts, metadatas=metadatas)

# def create_documents(self, texts: List[str], metadatas: Optional[List[dict]] = None) -> List[Document]:
#         """Create documents from a list of texts."""
#         _metadatas = metadatas or [{}] * len(texts)
#         documents = []
#         for i, text in enumerate(texts):
#             index = -1
#             for chunk in self.split_text(text):
#                 metadata = copy.deepcopy(_metadatas[i])
#                 if self._add_start_index:
#                     index = text.find(chunk, index + 1)
#                     metadata["start_index"] = index
#                 new_doc = Document(page_content=chunk, metadata=metadata)
#                 documents.append(new_doc)
#         return documents
