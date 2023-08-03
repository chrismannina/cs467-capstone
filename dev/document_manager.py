# document_manager.py
from collections import defaultdict
from document import Document

class DocumentManager:
    def __init__(self):
        self.documents = {}
        # self.documents = defaultdict(Document):

    def create_document(self, id, document_path, split_method, chunk_size, chunk_overlap):
        self.documents[id] = Document(
            document_path=document_path,
            split_method=split_method,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def get_document(self, id):
        return self.documents[id]

    def delete_document(self, id):
        del self.documents[id]
