from src import prompts
import logging
from src.utils import remove_non_ascii
import json

from langchain.chat_models import ChatOpenAI
from langchain.chains import (
    RetrievalQA,
    RetrievalQAWithSourcesChain,
    ConversationalRetrievalChain,
    StuffDocumentsChain,
    LLMChain,
)
from langchain.memory import ConversationBufferMemory

# from langchain.chains.combine_documents.stuff import StuffDocumentsChain
# from langchain.chains.llm import LLMChain
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
        self.conversational = conversational  # Boolean - we can specify if we want simple Q&A or coversational Q&A (chat memory/history)
        self.combine_docs_chain = self.__create_combine_docs_chain()
        self.qa_chain = self.__create_qa_chain()
        # self.setup_chains()

    def __create_llm(self):
        return ChatOpenAI(
            model_name=self.config.llm_model, temperature=self.config.temperature
        )

    def __create_question_generator(self):
        llm = self.__create_llm()
        question_generator_prompt = PromptTemplate.from_template(
            prompts.QUESTION_GENERATOR_PROMPT
        )
        return LLMChain(llm=llm, prompt=question_generator_prompt)

    def __create_combine_docs_chain(self):
        # Format a document into a string based on a prompt template.
        doc_prompt = PromptTemplate.from_template(prompts.DOCUMENT_PROMPT)
        doc_var_name = prompts.DOCUMENT_VARIABLE_NAME
        llm = self.__create_llm()
        system_prompt = SystemMessagePromptTemplate.from_template(prompts.PROMPT_TEMPLATE)
        prompt = ChatPromptTemplate(
            messages=[
                system_prompt, 
                MessagesPlaceholder(variable_name="chat_history"), 
                HumanMessagePromptTemplate.from_template("{question}")
            ]
        )
        llm_chain = LLMChain(llm=llm, prompt=prompt)
        return StuffDocumentsChain(
            llm_chain=llm_chain,
            document_prompt=doc_prompt,
            document_variable_name=doc_var_name,
            document_separator="---------", # default "\n\n"
        )

    def __create_qa_chain(self):
        if self.conversational:
            
            memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True,
                input_key="question",
                output_key="answer",
            )
            return ConversationalRetrievalChain(
                question_generator=self.__create_question_generator(),
                retriever=self.retriever,
                memory=memory,
                combine_docs_chain=self.combine_docs_chain,
                return_source_documents=True,
                verbose=True,
            )
        else:
            # llm = self.__create_llm()
            return RetrievalQA(
                combine_documents_chain=self.combine_docs_chain,
                retriever=self.retriever,
                return_source_documents=True,
                verbose=True,
            )
            
            
    # https://python.langchain.com/docs/use_cases/question_answering/how_to/question_answering

    def ask(self, question):
        if self.conversational:
            messages = []
            for human, ai in history:
                messages.append(HumanMessage(content=human))
                messages.append(AIMessage(content=ai))
       
            response = self.qa_chain({"question": question, "chat_history": messages})
            # # self.print_formatted_output(response)
            json_response = json.dumps(
                response, default=lambda o: o.__dict__, indent=4
            )  # Convert the response to JSON format
            print(json_response)
            return response
        else:
            response = self.qa_chain(question) 
            # # self.print_formatted_output(response)
            json_response = json.dumps(
                response, default=lambda o: o.__dict__, indent=4
            )  # Convert the response to JSON format
            print(json_response)
            return response

    def gradio_chat(self, message, history):
        convo_string = "\\n\\n".join(
            [f"Human: {h}\\nAssistant: {a}" for h, a in history]
        )
        messages = []
        for human, ai in history:
            messages.append(HumanMessage(content=human))
            messages.append(AIMessage(content=ai))

        with trace_as_chain_group("qa_response") as group_manager:
            try:
                ques_gen_chain = self.__create_question_generator()
                search_query = ques_gen_chain.run(
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
        # response = self.qa_chain(message)
        # json_response = json.dumps(response, default=lambda o: o.__dict__, indent=4)  # Convert the response to JSON format
        # print(json_response)
        # return response["answer"]

    # def setup_chains(self):

    #     document_prompt = PromptTemplate(
    #         input_variables=["page_content"], template=prompts.DOCUMENT_PROMPT_TEMPLATE
    #     )
    #     document_variable_name = prompts.DOCUMENT_VARIABLE_NAME

    #     llm = ChatOpenAI(temperature=self.config.temperature)

    #     system_prompt = SystemMessagePromptTemplate.from_template(
    #         prompts.PROMPT_TEMPLATE
    #     )

    #     prompt = ChatPromptTemplate(
    #         messages=[
    #             system_prompt,
    #             MessagesPlaceholder(variable_name="chat_history"),
    #             HumanMessagePromptTemplate.from_template("{question}"),
    #         ]
    #     )

    #     self.llm_chain = LLMChain(llm=llm, prompt=prompt)

    #     self.combine_docs_chain = StuffDocumentsChain(
    #         llm_chain=self.llm_chain,
    #         document_prompt=document_prompt,
    #         document_variable_name=document_variable_name,
    #         document_separator="---------",
    #     )

    #     question_generator_prompt = PromptTemplate.from_template(
    #         prompts.QUESTION_GENERATOR_PROMPT
    #     )

    #     self.question_generator_chain = LLMChain(
    #         llm=llm, prompt=question_generator_prompt
    #     )

    # def _setup_chains(self):
    #     # reference: https://api.python.langchain.com/en/latest/llms/langchain.llms.openai.OpenAIChat.html#langchain.llms.openai.OpenAIChat
    #     llm = ChatOpenAI(model_name=self.config.llm_model, temperature=self.config.temperature)

    #     # Setup chat based QA
    #     if self.conversational:
    #         # https://api.python.langchain.com/en/latest/schema/langchain.schema.memory.BaseMemory.html#langchain.schema.memory.BaseMemory
    #         # memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    #         chat = ConversationalRetrievalChain.from_llm(llm=llm, retriever=self.retriever, return_generated_question=True, ) #, memory=memory)

    #     else:

    # def ask(self, question):
    #     ask = RetrievalQA.from_chain_type(llm=llm,
    #                              chain_type="stuff",
    #                              retriever=self.retriever,
    #                              chain_type_kwargs=chain_type_kwargs,
    #                              verbose=True,
    #                              #return_source_documents=True
    #                             )
    #     return ask
