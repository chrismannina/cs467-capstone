"""Module for managing chat interactions, including retrieval and response generation.

This module provides the Chat class which oversees chat interactions, leveraging
the capabilities of large language models, document retrieval, and other utilities.
"""
from src import prompts
import logging
import re
from langchain.chat_models import ChatOpenAI
from langchain.chains import (
    RetrievalQA,
    ConversationalRetrievalChain,
    StuffDocumentsChain,
    LLMChain,
)
from langchain.schema import HumanMessage, AIMessage
from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder,
)

# Imports for deprecated Gradio chat function
from langchain.callbacks.manager import trace_as_chain_group
from src.utils import remove_non_ascii


class Chat:
    """
    Class to manage chat interactions, including retrieval and response generation.

    This class provides functionalities to:
    - Create various chains for processing user queries and generating responses.
    - Maintain a chat history.
    - Generate model-based responses to user queries.

    Attributes:
    - config (object): Configuration settings for the chat.
    - retriever (object): The retriever used to fetch relevant document chunks.
    - conversational (bool): Determines if the chat mode is conversational (ConversationalRetrievalChain or RetrievalQA).
    - combine_docs_chain (object): Chain for combining document chunks into prompts.
    - qa_chain (object): Main Q&A chain.
    - chat_history (list): History of chat interactions.

    """

    def __init__(
        self,
        config,
        retriever=None,
        conversational=True,
        qa_prompt=prompts.CHAT_QA_PROMPT,
    ):
        self.config = config
        self.retriever = retriever
        self.conversational = conversational
        self.qa_prompt = qa_prompt
        self.combine_docs_chain = self.__create_combine_docs_chain()
        self.qa_chain = self.__create_qa_chain()
        self.chat_history = []

    def __create_llm(self):
        """
        Wrapper around OpenAI Chat large language models. Needs an environment variable ``OPENAI_API_KEY`` set with an API key.
        Note the `model_kwargs` parameter holds any model parameters that are valid with openai.ChatCompletion.create(...). This
        includes but not limited to model, messages, temperature. Need to still look at langchain source code and see how it is
        implemented.
        """
        return ChatOpenAI(
            model_name=self.config.llm_model, temperature=self.config.temperature
        )

    def __create_question_generator(self):
        """
        Create and return the question generator, which is an LLM chain with a specific prompt.
        """
        llm = self.__create_llm()
        question_generator_prompt = PromptTemplate.from_template(
            prompts.CONDENSE_QUESTION_PROMPT
        )
        return LLMChain(llm=llm, prompt=question_generator_prompt)

    def __create_combine_docs_chain(self):
        """
        Create and return a LLM chain that prepares a user query and combines document chunks into a prompt.
        """
        doc_prompt = PromptTemplate.from_template(prompts.DOCUMENT_PROMPT)
        doc_var_name = prompts.DOCUMENT_VARIABLE_NAME

        system_prompt = SystemMessagePromptTemplate.from_template(prompts.SYSTEM_PROMPT)
        prompt = ChatPromptTemplate(
            messages=[
                system_prompt,
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessagePromptTemplate.from_template("{question}"),
            ]
        )

        llm = self.__create_llm()
        llm_chain = LLMChain(llm=llm, prompt=prompt)

        return StuffDocumentsChain(
            llm_chain=llm_chain,
            document_prompt=doc_prompt,
            document_variable_name=doc_var_name,
            # document_separator="---------", # default "\n\n"
        )

    def __create_qa_chain(self):
        """
        Creates either a ConversationalRetrievalChain or RetrievalQA.
        """
        if self.conversational:
            llm = self.__create_llm()
            condense_question_prompt = PromptTemplate(
                input_variables=["chat_history", "question"],
                template=prompts.CONDENSE_QUESTION_PROMPT,
            )
            prompt = PromptTemplate(
                input_variables=["question", "context"], template=self.qa_prompt
            )
            combine_docs_chain_kwargs = {"prompt": prompt}
            # Note if using memory = ConversationBufferMemory(...) for chat memory with return_messages=True you may
            # need to include input_key="question" and output_key="answer" as args to avoid errors.
            return ConversationalRetrievalChain.from_llm(
                llm=llm,
                retriever=self.retriever,
                condense_question_prompt=condense_question_prompt,
                chain_type="stuff",
                combine_docs_chain_kwargs=combine_docs_chain_kwargs,
                return_source_documents=True,
                verbose=True,
            )
        else:
            llm = self.__create_llm()
            prompt = PromptTemplate(
                input_variables=["question", "context"],
                template=self.qa_prompt,
            )
            chain_type_kwargs = {"prompt": prompt}
            qa = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=self.retriever,
                chain_type_kwargs=chain_type_kwargs,
                return_source_documents=True,
                verbose=True,
            )
            return qa

    def format_terms(self, text):
        """Format the given text for better visibility.

        Converts quoted text to bold and replaces newline characters with HTML line breaks.

        Args:
            text (str): The input text.

        Returns:
            str: The formatted text.
        """
        formatted_text = re.sub(r'[“"”]([^”“]+)[“"”]', r"<b>\1</b>", text)
        formatted_text = formatted_text.replace("\n", "<br>")
        return formatted_text

    def ask(self, question):
        """Accepts a user's question and returns the model's response.

        Depending on the mode (conversational or not), this method processes the user's
        query differently and leverages different chains to generate the response.

        Args:
            question (str): The user's query.

        Returns:
            dict/str: The model's response.
        """
        if self.conversational:
            answer = self.qa_chain(
                {"question": question, "chat_history": self.chat_history}
            )
            self.chat_history.append((question, answer["answer"]))
        else:
            answer = self.qa_chain(question)

            self.chat_history.append((question, answer["result"]))

        return answer

    # DEPRECATED - switched to Streamlit
    def gradio_chat(self, message, history):
        """Method for Gradio's ChatInterface chatbot UI. DEPRECATED as the application now uses Streamlit for the UI."""
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
