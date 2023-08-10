import re
import requests


def validate_openai_key(api_key):
    """
    Validate the OpenAI API key by sending a test request.

    Parameters:
    - api_key (str): The OpenAI API key to validate.

    Returns:
    - bool: True if the API key is valid, False otherwise.
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "text-davinci-003",
        "prompt": "Translate the following English text to French: 'Hello'",
        "max_tokens": 10,
    }

    response = requests.post(
        "https://api.openai.com/v1/engines/davinci/completions",
        headers=headers,
        json=data,
    )

    # Check if the response status code is 200 (OK)
    if response.status_code == 200:
        return True
    else:
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
