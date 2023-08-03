# References:
# https://huggingface.co/spaces/Gradio-Blocks/document-qa/blob/main/app.py
# https://github.com/hwchase17/conversation-qa-gradio/blob/master/app.py
# https://huggingface.co/spaces/ysharma/ChatGPT4
# https://huggingface.co/spaces/ysharma/ChatGPT4/blob/main/app.py
# https://huggingface.co/spaces/fffiloni/langchain-chat-with-pdf-openai/blob/main/app.py

import gradio as gr

from pprint import pprint
from colorama import Fore, Style

from config import Config
from document import Document
from vector_store import VectorStore
from utils import format_context, format_metadata, format_retrieved_docs


from langchain.chat_models import ChatOpenAI
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain.schema import HumanMessage, AIMessage
from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from langchain.callbacks.manager import trace_as_chain_group



# from tempfile import NamedTemporaryFile

# def handle_upload(file):
#     with NamedTemporaryFile(delete=False) as tmp:
#         tmp.write(file.read())
#     return tmp.name  # This is the path to the temporary file


# Now you can use tmp_file_path in the rest of your program

# Setup
config = Config("config.yaml")

document_paths = [
    r"C:\Users\machris\projects\cs467-capstone\files\mm_htn_guidelines.pdf"
    # r"C:\Users\machris\projects\cs467-capstone\files\NCCN_aml_2023_Guidelines.pdf",
    # r"C:\Users\machris\projects\cs467-capstone\files\How I treat acute myeloid leukemia in the era of new drugs.pdf",
    # r"C:\Users\machris\projects\cs467-capstone\files\How I treat acute myeloid leukemia presenting with preexisting comorbidities.pdf",
    # r"C:\Users\machris\projects\cs467-capstone\files\How I treat AML incorporating the updated classifications and guidelines.pdf",
]
db = VectorStore()
for index, doc_path in enumerate(document_paths):
    doc = Document(
        document_path=doc_path,
        split_method=config.split_method,
        chunk_size=int(config.chunk_size),
        chunk_overlap=int(config.chunk_overlap),
    )
    if index == 0:
        # Use create_from_docs for the first document
        db.create_from_docs(doc.get_split_document())
    else:
        db.add_docs(doc.get_split_document())
db.save()


retriever = db.retriever()



# Functions to handle adding a new document to the vector database
def add_document(document):
    try:
        new_doc = Document(
            document_path=document.name,
            split_method=config.split_method,
            chunk_size=int(config.chunk_size),
            chunk_overlap=int(config.chunk_overlap),
        )
        db.add_docs(new_doc.get_split_document())
        db.save()
        return "Document added successfully!"
    except Exception as e:
        return f"Error occurred while adding document: {str(e)}"



# Set up our chain that can answer questions based on documents.
document_prompt = PromptTemplate(
    input_variables=["page_content"], template="{page_content}"
)
document_variable_name = "context"
llm = ChatOpenAI(temperature=0)

prompt_template = """Use the following pieces of context to answer user questions. If you don't know the answer, just say that you don't know.

--------------

{context}"""

system_prompt = SystemMessagePromptTemplate.from_template(prompt_template)
prompt = ChatPromptTemplate(
    messages=[
        system_prompt,
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{question}"),
    ]
)
llm_chain = LLMChain(llm=llm, prompt=prompt)
combine_docs_chain = StuffDocumentsChain(
    llm_chain=llm_chain,
    document_prompt=document_prompt,
    document_variable_name=document_variable_name,
    document_separator="---------",
)

# Set up a chain that controls how the search query for the vector_store is generated
template = """Combine the chat history and follow up question into a search query.

Chat History:

{chat_history}

Follow up question: {question}
"""

prompt = PromptTemplate.from_template(template)
llm = ChatOpenAI(temperature=0)
question_generator_chain = LLMChain(llm=llm, prompt=prompt)



def relevant_docs(search_query):
    docs = retriever.get_relevant_documents(search_query)
    metadata = format_metadata(docs)
    return metadata



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
        search_query = question_generator_chain.run(
            question=message, chat_history=convo_string, callbacks=group_manager
        )
        # Retrieve relevant docs
        docs = retriever.get_relevant_documents(search_query, callbacks=group_manager)
        
        # TODO: move these to the utils - printing docs in color
        # TODO: need to have better method of logging/debug printing
        print(Fore.GREEN) # set color to green
        pprint(docs) # pretty print docs
        print(Style.RESET_ALL) # reset color to default
        
        # Answer question
        answer = combine_docs_chain.run(
            input_documents=docs,
            chat_history=messages,
            question=message,
            callbacks=group_manager,
        )
        # adding metadata/citation at bottom
        # metadata = format_metadata(docs)
        # response = answer + f"\n\n{metadata}"

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
