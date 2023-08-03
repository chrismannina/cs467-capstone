# chat_manager.py
from collections import defaultdict
from chat import Chat
from vector_store_manager import VectorStoreManager

class ChatManager:
    def __init__(self, vector_store_manager: VectorStoreManager):
        self.vector_store_manager = vector_store_manager
        self.chats = {}

    def create_chat(self, id, vector_store_ids):
        chat = Chat(self.vector_store_manager)
        for vector_store_id in vector_store_ids:
            chat.add_vector_store(vector_store_id)
        self.chats[id] = chat

    def get_chat(self, id):
        return self.chats[id]

    def delete_chat(self, id):
        del self.chats[id]
