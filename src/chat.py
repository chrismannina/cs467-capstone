"""Class and methods for LLM chat."""
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain, ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate


class Chat:
    def __init__(self, db, temperature=0, llm_model="gpt-3.5-turbo"):
        self.db = db
        self.llm_model = llm_model
        self.temperature = temperature


from langchain.chains import RetrievalQA
from langchain.llms import OpenAIChat

qa = RetrievalQA.from_chain_type(
    llm=OpenAIChat(model="gpt-3.5-turbo"),
    chain_type="stuff",
    retriever=db.as_retriever(),
)


llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

_template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""
CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)
condense_question_chain = LLMChain(
    llm=llm,
    prompt=CONDENSE_QUESTION_PROMPT,
)


from langchain.chains.combine_documents.stuff import StuffDocumentsChain

from langchain.chains import create_qa_with_sources_chain

qa_chain = create_qa_with_sources_chain(llm)


doc_prompt = PromptTemplate(
    template="Content: {page_content}\nSource: {source}",
    input_variables=["page_content", "source"],
)

final_qa_chain = StuffDocumentsChain(
    llm_chain=qa_chain,
    document_variable_name="context",
    document_prompt=doc_prompt,
)

qa = ConversationalRetrievalChain(
    question_generator=condense_question_chain,
    retriever=faiss_db.as_retriever(),
    memory=memory,
    combine_docs_chain=final_qa_chain,
)

query = "What is the 90-day cost for metoprolol?"
result = qa({"question": query})
result
