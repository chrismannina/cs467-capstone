# References:
# https://huggingface.co/spaces/Gradio-Blocks/document-qa/blob/main/app.py
# https://github.com/hwchase17/conversation-qa-gradio/blob/master/app.py
# https://huggingface.co/spaces/ysharma/ChatGPT4
# https://huggingface.co/spaces/ysharma/ChatGPT4/blob/main/app.py
# https://huggingface.co/spaces/fffiloni/langchain-chat-with-pdf-openai/blob/main/app.py

import gradio as gr

# Used for formatting util functions
import os
from collections import defaultdict
from urllib.parse import urlparse

from config import Config
from document import Document
from vectorstore import Vectorstore

from langchain.chat_models import ChatOpenAI
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain.schema import HumanMessage, AIMessage
from langchain.prompts import PromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain.callbacks.manager import trace_as_chain_group


# from tempfile import NamedTemporaryFile

# def handle_upload(file):
#     with NamedTemporaryFile(delete=False) as tmp:
#         tmp.write(file.read())
#     return tmp.name  # This is the path to the temporary file



# Now you can use tmp_file_path in the rest of your program

# Setup
config = Config("config.yaml")
doc = Document(
    document_path=r"C:\Users\machris\projects\cs467-capstone\files\How I treat acute myeloid leukemia in the era of new drugs.pdf",  
    split_method=config.split_method,
    chunk_size=int(config.chunk_size),
    chunk_overlap=int(config.chunk_overlap)
    )
db = Vectorstore()
db.load()
db.add_docs(doc.get_split_document())
# db.create_from_docs(doc.get_split_document())
db.save()
# db.load()
retriever = db.retriever()

# Functions to handle adding a new document to the vector database
def add_document(document):
    # doc_path = handle_upload(file)
    # print(doc_path)
    new_doc = Document(
        document_path=document,
        split_method=config.split_method,
        chunk_size=int(config.chunk_size),
        chunk_overlap=int(config.chunk_overlap)
    )
    db.add_docs(new_doc.get_split_document())
    db.save()
    return "Document added successfully!"

# Set up our chain that can answer questions based on documents.
document_prompt = PromptTemplate(input_variables=["page_content"], template="{page_content}")
document_variable_name = "context"
llm = ChatOpenAI(temperature=0)

prompt_template = """Use the following pieces of context to answer user questions. If you don't know the answer, just say that you don't know.

--------------

{context}"""

system_prompt = SystemMessagePromptTemplate.from_template(prompt_template)
prompt = ChatPromptTemplate(
    messages=[system_prompt, 
              MessagesPlaceholder(variable_name="chat_history"), 
              HumanMessagePromptTemplate.from_template("{question}")]
    )
llm_chain = LLMChain(llm=llm, prompt=prompt)
combine_docs_chain = StuffDocumentsChain(
    llm_chain=llm_chain,
    document_prompt=document_prompt,
    document_variable_name=document_variable_name,
    document_separator="---------"
    )

# Set up a chain that controls how the search query for the vectorstore is generated
template = """Combine the chat history and follow up question into a search query.

Chat History:

{chat_history}

Follow up question: {question}
"""
prompt = PromptTemplate.from_template(template)
llm = ChatOpenAI(temperature=0)
question_generator_chain = LLMChain(llm=llm, prompt=prompt)

def format_context(documents):
    formatted_context = ""
    for doc in documents:
        source = doc.metadata.get('source', 'Unknown source')
        page = doc.metadata.get('page', 'Unknown page')
        content = doc.page_content
        formatted_context += f"Source: {source}\nPage: {page}\nContent: {content}\n\n"
    return formatted_context


def format_metadata(documents):
    # Using defaultdict to automatically handle new sources
    source_pages = defaultdict(list)
    
    for doc in documents:
        # Get the filename only, not the full path
        full_path = doc.metadata.get('source', 'Unknown source')
        if full_path.startswith(('http://', 'https://')):
            filename = urlparse(full_path).path.rsplit('/', 1)[-1]
        else:
            filename = os.path.basename(full_path)
        page = doc.metadata.get('page', 'Unknown page')
        
        # Incrementing page number by 1, as it's 0-indexed
        page = int(page) + 1
        
        # Appending page to respective source
        source_pages[filename].append(page)
    
    formatted_metadata = ""
    for source, pages in source_pages.items():
        # Sorting pages for display
        pages = sorted(pages)
        
        # Grouping continuous pages 
        page_groups = []
        group_start = group_end = pages[0]

        for page in pages[1:]:
            if page - group_end > 1:
                page_groups.append((group_start, group_end))
                group_start = page
            group_end = page
        page_groups.append((group_start, group_end))

        page_strs = []
        for start, end in page_groups:
            if start == end:
                page_strs.append(str(start))
            else:
                page_strs.append(f"{start}-{end}")
        
        formatted_metadata += f"- {source} (pages: {', '.join(page_strs)})\n"

    return formatted_metadata

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
			question=message, 
			chat_history=convo_string, 
			callbacks=group_manager
		)
		# Retrieve relevant docs
		docs = retriever.get_relevant_documents(search_query, callbacks=group_manager)

		# Answer question
		answer = combine_docs_chain.run(
			input_documents=docs, 
			chat_history=messages, 
			question=message, 
			callbacks=group_manager
		)
		# metadata = format_metadata(docs)
		# response = answer + f"\n\nSource(s): \n{metadata}"
		return answer
  		# # Answer question
		# return combine_docs_chain.run(
		# 	input_documents=docs, 
		# 	chat_history=messages, 
		# 	question=message, 
		# 	callbacks=group_manager
		# )
                                     
# Create Gradio app
app = gr.Blocks(css="footer {visibility: hidden}")
with app:
	gr.Markdown("# 💊 GuidelineGPT")
	gr.Markdown("### Clinical Practice Guidelines Q&A")
	gr.Markdown("<em>NOTE: This is a demo. This project is still a work in progress.<em>")
	# Ask questions about the documents
	with gr.Tab('Chat'):
		chat = gr.ChatInterface(qa_response)
  	# Add a document to the vector database
	with gr.Tab('Add Document'):
		document = gr.File()
		add_button = gr.Button("📄 Add")
		status = gr.Textbox(label="Status")
		add_button.click(fn=add_document, inputs=document.name, outputs=status)
	gr.Markdown("<sub>Created by Chris Mannina</sub>")

if __name__ == "__main__":
	app.launch()