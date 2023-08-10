import re
import logging
import requests
import openai

# Set up a logger for the function
logger = logging.getLogger(__name__)


def validate_openai_key(api_key):
    """
    Validate the OpenAI API key by sending a test request.

    Parameters:
    - api_key (str): The OpenAI API key to validate.

    Returns:
    - bool: True if the API key is valid, False otherwise.
    """

    openai.api_key = api_key
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'CHEESE'."},
            ],
            max_tokens=10,
        )
        # Check if the response has an 'id' attribute, indicating success
        if hasattr(response, "id"):
            return True
        else:
            logger.warning(
                f"OpenAI API did not return the expected response. Response: {response}"
            )
            return False
    except Exception as e:
        logger.error(f"Error occurred while validating OpenAI API key: {e}")
        return False


def remove_non_ascii(text):
    return re.sub(r"[^\x00-\x7F]+", " ", text)


def print_formatted_output(data):
    # TODO: conversational chat vs single qa have different variables (conversational: question, answer. single qa: query, result. both: source_documents)
    # Printing the question
    print(f"Question: {data['question']}\n")

    # Printing the chat history if present
    source_documents = None
    if data.get("chat_history"):
        print("Chat History:")
        for idx, message in enumerate(data["chat_history"]):
            if isinstance(message, HumanMessage):
                print(f"\tUser {idx+1}: {message.content}")
            elif isinstance(message, AIMessage):
                print(f"\tAI {idx+1}: {message.content}")
                if (
                    message.additional_kwargs
                    and "source_documents" in message.additional_kwargs
                ):
                    source_documents = message.additional_kwargs["source_documents"]
        print("\n")

    # Printing the answer
    print(f"Answer: {data['answer']}\n")

    # Printing the source documents
    if source_documents:
        print("Source Documents:")
        for idx, document in enumerate(source_documents):
            source = document["metadata"].get("source")
            page = document["metadata"].get("page")
            content = document["page_content"].replace("\n", " ").strip()
            print(
                f"\tDocument {idx+1} (Source: {source}, Page: {page}): {content[:100]}..."
            )  # Printing the first 100 characters for brevity
        print("\n")
