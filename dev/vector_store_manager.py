# vector_store_manager.py
from collections import defaultdict
from vector_store import VectorStore
from document_manager import DocumentManager

class VectorStoreManager:
    def __init__(self, document_manager: DocumentManager):
        self.document_manager = document_manager
        self.vector_stores = {}

    def create_vector_store(self, id, document_ids):
        vector_store = VectorStore()
        for document_id in document_ids:
            document = self.document_manager.get_document(document_id)
            vector_store.add_docs(document.get_split_document())
        vector_store.save()
        self.vector_stores[id] = vector_store

    def get_vector_store(self, id):
        return self.vector_stores[id]

    def delete_vector_store(self, id):
        del self.vector_stores[id]
