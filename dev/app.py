# app.py
import gradio as gr
from pprint import pprint
from colorama import Fore, Style

from config import Config
from chat_manager import ChatManager
from document_manager import DocumentManager
from vector_store_manager import VectorStoreManager

from utils import format_context, format_metadata, format_retrieved_docs

from langchain.schema import HumanMessage, AIMessage
from langchain.callbacks.manager import trace_as_chain_group

# Config 
config = Config("config.yaml")

# Setup managers
document_manager = DocumentManager()
vector_store_manager = VectorStoreManager(document_manager)
chat_manager = ChatManager(vector_store_manager)

document_path = r"C:\Users\machris\projects\cs467-capstone\files\mm_htn_guidelines.pdf"
# Create default chat, document, and vector store
document_manager.create_document('default', document_path=document_path,
            split_method=config.split_method,
            chunk_size=int(config.chunk_size),
            chunk_overlap=int(config.chunk_overlap),)
vector_store_manager.create_vector_store('default', ['default'])  # This creates a vector store with the 'default' document
chat_manager.create_chat('default', ['default'])  # This creates a chat with the 'default' vector store
# Get the default chat, document, and vectorstore
current_chat = chat_manager.get_chat('default')
current_document = document_manager.get_document('default')
current_vectorstore = vector_store_manager.get_vector_store('default')

# Functions to handle adding a new document to the vector database
def add_document(document):
    try:
        document_manager.create_document(
            'new_document', 
            document.name, 
            config.split_method, 
            int(config.chunk_size), 
            int(config.chunk_overlap)
        )
        current_document = document_manager.get_document('new_document')
        current_vectorstore.add_docs(current_document.get_split_document())
        current_vectorstore.save()
        return "Document added successfully!"
    except Exception as e:
        return f"Error occurred while adding document: {str(e)}"

def relevant_docs(search_query):
    docs = current_vectorstore.retriever().get_relevant_documents(search_query)
    metadata = format_metadata(docs)
    return metadata

chat_dropdown = gr.Dropdown(choices=list(chat_manager.chats.keys()))
def switch_chat(chat_id):
    global current_chat
    current_chat = chat_manager.get_chat(chat_id)
    return f"Switched to chat {chat_id}"

def qa_response(message, history):
    # Convert message history into format for the `question_generator_chain`
    convo_string = "\n\n".join([f"Human: {h}\nAssistant: {a}" for h, a in history])
    # Convert message history into LangChain format for the final response chain
    messages = []
    for human, ai in history:
        messages.append(HumanMessage(content=human))
        messages.append(AIMessage(content=ai))
    # Wrap all actual calls to chains in a trace group
    with trace_as_chain_group("qa_response") as group_manager:
        # Generate search query.
        search_query = current_chat.question_generator_chain.run(
            question=message, 
            chat_history=convo_string, 
            callbacks=group_manager
        )
        # Retrieve relevant docs
        docs = current_vectorstore.retriever().get_relevant_documents(search_query, callbacks=group_manager)
        
        # TODO: move these to the utils - printing docs in color
        # TODO: need to have better method of logging/debug printing
        print(Fore.GREEN) # set color to green
        pprint(docs) # pretty print docs
        print(Style.RESET_ALL) # reset color to default
        
        # Answer question
        answer = current_chat.combine_docs_chain.run(
            input_documents=docs,
            chat_history=messages,
            question=message,
            callbacks=group_manager,
        )

        return answer

# Create Gradio app
app = gr.Blocks(title="GuidelineGPT", css="footer {visibility: hidden}")
with app:
    gr.Markdown("# 💊 GuidelineGPT")
    gr.Markdown("### Clinical Practice Guidelines Q&A")
    gr.Markdown(" ⚠️ <em>This is a demo. This project is still a work in progress.<em>")
    # Ask questions about the documents
    with gr.Tab("Q&A Chat"):
        chat = gr.ChatInterface(qa_response)
        chat_select = gr.Interface(fn=switch_chat, inputs=chat_dropdown, outputs="text")
        # Add a document to the vector database
    with gr.Tab("Upload Document"):
        document = gr.File()
        add_button = gr.Button("📄 Upload")
        status = gr.Textbox(label="Status")
        add_button.click(fn=add_document, inputs=document, outputs=status)
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
