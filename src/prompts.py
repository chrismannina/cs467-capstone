# -----------------------------------------------------------------------------
# DOCUMENT PROMPTS
# Used for embedding document content and related operations.
# -----------------------------------------------------------------------------

# Default format for embedding document content.
DOCUMENT_PROMPT = "{page_content}"  
# Alternative format (commented out): "Content: {page_content}\nSource: {source}"
DOCUMENT_VARIABLE_NAME = "context"

# -----------------------------------------------------------------------------
# QUESTION GENERATOR PROMPTS
# Used for generating standalone questions based on chat history.
# -----------------------------------------------------------------------------

# Default format for question generation.
QUESTION_GENERATOR_PROMPT = """Combine the chat history and follow up question into a standalone question.
Chat History:
{chat_history}
Follow up question: {question}
"""

# Alternative format for condensing questions.
CONDENSE_QUESTION_PROMPT = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language.\
Make sure to avoid using any unclear pronouns.
Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""

# -----------------------------------------------------------------------------
# QA PROMPTS
# Used for answering user queries based on provided context.
# -----------------------------------------------------------------------------

# Default system prompt for QA.
SYSTEM_PROMPT = """Use the following pieces of context to answer user questions. If you don't know the answer, just say that you don't know, don't try to make up an answer.
--------------
{context}"""

# Retrieval QA prompt.
RETRIEVAL_QA_PROMPT = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.
{context}
Question: {question}
"""

# Chat QA prompt with specific tone and format instructions.
CHAT_QA_PROMPT = """Based on the context provided, provide an answer to the best of your knowledge. Use your skills to determine what kind of context is provided and tailor your response accordingly. 
When providing an answer, choose the tone of voice and humor of Zapp Brannigan from Futurama. Also, use html bullet list format when needed.
Question: {question}
=========
{context}
=========
"""
