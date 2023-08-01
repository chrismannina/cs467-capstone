"""Class and methods for vector database."""
import uuid

from langchain.vectorstores import FAISS, Chroma
from langchain.embeddings import OpenAIEmbeddings

class Vectorstore:
    def __init__(self, db_name="FAISS", embeddings_model="OpenAIEmbeddings", folder_path="../db", index_name="index"):
        self.db_name = db_name
        self.embeddings_model = embeddings_model
        self.embeddings = self.__embeddings()
        self.folder_path = folder_path
        self.index_name = index_name
        self.vectorstore = None
     
    def __embeddings(self):
        if self.embeddings_model == "OpenAIEmbeddings":
            return OpenAIEmbeddings()
        else: 
            raise ValueError(f"Invalid embeddings model: {self.embeddings_model}")
    
    def create_from_docs(self, documents, ids=None):
        # Initialize from documents and embeddings
        if self.db_name == "FAISS":
            self.vectorstore = FAISS.from_documents(documents, self.embeddings, ids=ids)
            return self.vectorstore
        elif self.db_name == "Chroma":
            # TODO: implement Chroma 
            pass
        else: 
            raise ValueError(f"Invalid vectorstore: {self.db_name}")
    
    def save(self):
        # Save current vector database
        if self.db_name == "FAISS":
            self.vectorstore.save_local(folder_path=self.folder_path, index_name=self.index_name)
        elif self.db_name == "Chroma":
            # TODO: implement Chroma 
            pass
        else: 
            raise ValueError(f"Invalid vectorstore: {self.db}")
        
    def load(self):
        # Load vector database
        # TODO: Implement try/except block 
        if self.db_name == "FAISS":
            self.vectorstore = FAISS.load_local(folder_path=self.folder_path, embeddings=self.embeddings, index_name=self.index_name)
            return self.vectorstore
        elif self.db_name == "Chroma":
            # TODO: implement Chroma 
            pass
        else: 
            raise ValueError(f"Invalid vectorstore: {self.db}")
        
    def add_docs(self, documents, ids=None):
        # Add documents to vectorstore
        if self.db_name == "FAISS":
            return self.vectorstore.add_documents(documents)
        elif self.db_name == "Chroma":
            # TODO: implement Chroma 
            pass
        else: 
            raise ValueError(f"Error adding document to {self.db_name}")
        
    def similarity_search(self, query, k=4):
        # Perform similarity search in database
        return self.vectorstore.similarity_search(query=query, k=k)
    
    def similarity_search_with_score(self, query, k=4):
        # Perform similarity search in database
        return self.vectorstore.similarity_search_with_score(query=query, k=k)
    
    def retriever(self):
        return self.vectorstore.as_retriever()

# TODO: Once Document class has IDs and metadatas, we can update Vectorstore class with delete function and add_texts function. 
# TODO: this will give better control over the database and what docs we add/delete, and give future ability to search based on metadata (and alter it)
    # =
    # chroma_db = Chroma.from_documents(
    #     documents=documents, 
    #     embedding=embeddings, 
    #     persist_directory="../db"
    # )
    #     def embed_docs(self, documents):
    #     print(self.embeddings)
    #     return self.embeddings.embed_documents(documents) 
    
    # def embed_query(self, query):
    #     return self.embeddings.embed_query(query) 

    # from langchain.vectorstores import FAISS
    # faiss_db = FAISS.from_documents(documents, embeddings)
    # # faiss_db = FAISS.from_documents(documents, embeddings, persist_directory="db")

    # query = "What is the 90-day cost for metoprolol?"
    # docsearch = faiss_db.similarity_search(query, k=5) # can use k arg to specify how many similar sentences/objects. e.g. for 10 you call faiss_db.similarity_search(query, k=10)
    # docsearch