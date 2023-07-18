import os
import argparse

from langchain.document_loaders import OnlinePDFLoader, PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain.vectorstores.faiss import FAISS


def load_doc(doc_path):
    # load the file (if the file is a URL, load the PDF file from the URL)
    # will need to add functionality for txt, etc.
    if doc_path.startswith("http"):
        loader = OnlinePDFLoader(doc_path)
    elif doc_path.endswith(".pdf"):
        loader = PyPDFLoader(doc_path)
    return loader.load()
    
    
def split_doc(document, method, chunk_size, chunk_overlap):
    # split by separator and merge by character count
    if method == "char":
        text_splitter = CharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
    # recursively split until below the chunk size limit
    elif method == "recursive":
        # Create a RecursiveCharacterTextSplitter object
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
    elif method == "tiktoken":
        # create a CharacterTextSplitter object
        text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
    else:
        print("error: missing split arg")
        # TODO: other split methods? spaCy, nltk, etc?
        # TODO: should be a try and then raise error here isntead

    return text_splitter.split_documents(document)


def embed_and_save_docs_to_faiss(documents, faiss_path, embeddings=OpenAIEmbeddings()):
    faiss_db = FAISS.from_documents(documents, embeddings)
    faiss_db.save_local(faiss_path)


def main(*args):
    document = load_doc(args.doc_path)
    split_documents = split_doc(document, args.split_mode, args.chunk_size, args.chunk_overlap)
    embed_and_save_docs_to_faiss(split_documents, args.faiss_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--chunk_size", type=int, default=1000, help="Please specify the chunk_size for CharacterTextSplitter within a number less than or equal to 4096.")
    parser.add_argument("--chunk_overlap", type=int, default=200, help="Please specify the chunk_overlap for CharacterTextSplitter within a number less than or equal to 4096.")
    parser.add_argument("--doc_path", type=str, default="", help="Please specify the path of the pdf to be read.")
    parser.add_argument("--split_mode", type=str, default="recursive", help="Please specify the split mode. (char, recursive, tiktoken)")
    parser.add_argument("--faiss_path", type=str, default="../db/faiss_index", help="Please specify the name of the created Faiss object.")
    args = parser.parse_args()

    main(args)
