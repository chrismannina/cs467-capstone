# prompts.py
DOCUMENT_PROMPT_TEMPLATE = "{page_content}"
DOCUMENT_VARIABLE_NAME = "context"

PROMPT_TEMPLATE = """Use the following pieces of context to answer user questions. If you don't know the answer, just say that you don't know.

--------------

{context}"""

QUESTION_GENERATOR_PROMPT = """Combine the chat history and follow up question into a search query.

Chat History:

{chat_history}

Follow up question: {question}
"""
