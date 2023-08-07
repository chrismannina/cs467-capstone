import logging
import prompts
from utils import remove_non_ascii

from langchain.chat_models import ChatOpenAI
from langchain import RetrievalQA
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


class Chat:
    def __init__(self, config, retriever=None, conversational=True):
        self.config = config
        self.retriever = retriever
        self.conversational = conversational    # Boolean - we can specify if we want simple Q&A or coversational Q&A (chat memory/history)
        self.llm_chain = None
        self.combine_docs_chain = None
        self.question_generator_chain = None
        self.setup_chains()
    def ask(self, question):
        ask = RetrievalQA.from_chain_type(llm=llm,
                                 chain_type="stuff",
                                 retriever=vector_db.as_retriever(),
                                 chain_type_kwargs=chain_type_kwargs,
                                 verbose=True,
                                 #return_source_documents=True
                                )
        return ask
    def setup_chains(self):
        document_prompt = PromptTemplate(
            input_variables=["page_content"], template=prompts.DOCUMENT_PROMPT_TEMPLATE
        )
        document_variable_name = prompts.DOCUMENT_VARIABLE_NAME

        llm = ChatOpenAI(temperature=self.config.temperature)

        system_prompt = SystemMessagePromptTemplate.from_template(
            prompts.PROMPT_TEMPLATE
        )

        prompt = ChatPromptTemplate(
            messages=[
                system_prompt,
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessagePromptTemplate.from_template("{question}"),
            ]
        )

        self.llm_chain = LLMChain(llm=llm, prompt=prompt)

        self.combine_docs_chain = StuffDocumentsChain(
            llm_chain=self.llm_chain,
            document_prompt=document_prompt,
            document_variable_name=document_variable_name,
            document_separator="---------",
        )

        question_generator_prompt = PromptTemplate.from_template(
            prompts.QUESTION_GENERATOR_PROMPT
        )

        self.question_generator_chain = LLMChain(
            llm=llm, prompt=question_generator_prompt
        )

    def qa_response(self, message, history):
        convo_string = "\\n\\n".join(
            [f"Human: {h}\\nAssistant: {a}" for h, a in history]
        )
        messages = []
        for human, ai in history:
            messages.append(HumanMessage(content=human))
            messages.append(AIMessage(content=ai))

        with trace_as_chain_group("qa_response") as group_manager:
            try:
                search_query = self.question_generator_chain.run(
                    question=message, chat_history=convo_string, callbacks=group_manager
                )
                docs = self.retriever.get_relevant_documents(
                    search_query, callbacks=group_manager
                )
                doc_retrieval_logger = logging.getLogger("doc_retrieval")
                doc_retrieval_logger.info(
                    f"Documents retrieved: {remove_non_ascii(str(docs))}"
                )
                answer = self.combine_docs_chain.run(
                    input_documents=docs,
                    chat_history=messages,
                    question=message,
                    callbacks=group_manager,
                )
            except Exception as e:
                logging.error(f"Failed to generate response: {e}")
                answer = "Sorry, I was unable to generate a response."
            return answer
