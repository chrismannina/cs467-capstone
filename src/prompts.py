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

# Dictionary structure to hold multiple Q&A prompts
QA_PROMPTS = {
    "Normal": {
        "Simple": {
            "description": "Standard Q&A prompt for general interactions.",
            "prompt": """Context: {context}
                =========
                Question: {question}"""
        },
        "Default": {
            "description": "Standard Q&A prompt for general interactions.",
            "prompt": """Use the following pieces of context to answer the question at the end. 
                If you don't know the answer, just say that you don't know, don't try to make up an answer. 
                Context: {context}
                =========
                Question: {question}"""
        },
        "Strict Contextual": {
            "description": "Answer strictly from the context. If unsure, state it.",
            "prompt": "Based on the provided context: {context}, answer the following without making assumptions: {question}. If the answer isn't clear from the context, state that you don't know."
        },
        "Inferential": {
            "description": "Infer based on context if a direct answer isn't available.",
            "prompt": "Using the context: {context} as a guiding reference, address the inquiry: {question}. If the context doesn't have a direct answer, use it to infer the best possible response."
        },
        "Acknowledge, Then Answer": {
            "description": "Acknowledge the absence of a direct answer, then provide the best response.",
            "prompt": "Examine the context: {context}. Address the question: {question}. If the context doesn't provide a clear answer, acknowledge that and then provide the best possible response."
        },
        "Analytical": {
            "description": "A direct and analytical approach to the question.",
            "prompt": "Given the context: {context}. Address the query: {question}."
        },
        "Contextual Deep Dive": {
            "description": "Prompt that emphasizes a deeper understanding of the context.",
            "prompt": "Deeply analyze the following context: {context}. Based on this, answer: {question}."
        },
        "Inquisitive": {
            "description": "A curious approach to the question.",
            "prompt": "Considering the information: {context}, what can be inferred about {question}?"
        }
    },
    "Medical": {
        "Medical Analysis": {
            "description": "Provide a detailed analysis of the medical context.",
            "prompt": "Medical Context: {context}. For a professional medical audience, analyze and respond to the inquiry: {question}. Note: Do not suggest seeking medical consultation, as this is for professional reference."
        },
        "Medical Inference": {
            "description": "Infer based on the medical context if a direct answer isn't evident.",
            "prompt": "Medical Information: {context}. Using this information, address the medical query: {question}. If the direct answer isn't available, infer based on the given data. Reminder: This is a professional inquiry, do not suggest seeking medical consultation."
        },
        "Medical Clarity": {
            "description": "Provide a clear and concise medical response.",
            "prompt": "Medical Data: {context}. For clarity, elucidate on the following medical query: {question}. Note: This information is for professional use; avoid suggesting medical consultations."
        },
        "Medical Deep Dive": {
            "description": "Delve deep into the medical topic based on the context.",
            "prompt": "Medical Contextual Data: {context}. Dive deep into the subject and provide insights on: {question}. This is a professional medical inquiry; refrain from suggesting medical consultations."
        }
    },
    "Humor": {
        "Zapp Brannigan": {
            "description": "Q&A in the style of Zapp Brannigan from Futurama.",
            "prompt": """Based on the context provided, provide an answer to the best of your knowledge. Use your skills to determine what kind of context is provided and tailor your response accordingly. 
                When providing an answer, choose the tone of voice and humor of Zapp Brannigan from Futurama. Also, use html bullet list format when needed.
                Question: {question}
                =========
                {context}
                =========
                """
        },
        "Ron Burgundy": {
            "description": "Deliver the answer with the confidence and flair of Ron Burgundy from Anchorman.",
            "prompt": "Straight from the Channel 4 News Team and based on the classy information: {context}, Ron Burgundy proudly presents the answer to: {question}. Stay classy!"
        },
        "Mr. T": {
            "description": "Answer with the tough love and no-nonsense style of Mr. T.",
            "prompt": "Listen up, fool! After looking at {context}, Mr. T says {question} is:"
        },
        "Eminem": {
            "description": "Drop the answer like a rap verse, inspired by Eminem.",
            "prompt": "With a beat and the story of {context}, Slim Shady raps out the truth about {question} like:"
        },
        "Captain Kirk": {
            "description": "Command the answer like Captain Kirk from Star Trek.",
            "prompt": "From the final frontier and with the knowledge of {context}, Starfleet's answer to {question} is:"
        },
        "Yoda": {
            "description": "Answer in the style of Master Yoda from Star Wars.",
            "prompt": "In the wisdom of the Force, given {context} it is, answer {question} I must."
        },
        "Sherlock Holmes": {
            "description": "Deduce the answer like Sherlock Holmes.",
            "prompt": "After careful deduction from the facts: {context}, my conclusion to {question} is elementary."
        },
        "Shakespeare": {
            "description": "Answer in a Shakespearean style.",
            "prompt": "In the grand prose of old, given the tale of {context}, prithee enlighten us on: {question}"
        }
    }
}


# Retrieve available Q&A prompt names for the Streamlit dropdown
# AVAILABLE_QA_PROMPTS = [prompt["name"] for category in QA_PROMPTS.values() for _, prompt in category.items()]

