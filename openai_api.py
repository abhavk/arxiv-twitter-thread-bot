from openai import OpenAI
import os
import tiktoken
from dotenv import load_dotenv

# Specify the path to your .env file here (optional if it's in your project root)
dotenv_path = '.env'

# Load the environment variables
load_dotenv(dotenv_path)

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def create_chat_completion(
    system_message,
    user_message,
    turbo: bool = True,
    temperature: float = 0.69,
    *_,
    **kwargs,
):
    """Create a chat completion using the OpenAI API with GPT 4

    Args:
        messages: A list of messages to feed to the chatbot.
        kwargs: Other arguments to pass to the OpenAI API chat completion call.
    Returns:
        OpenAIObject: The ChatCompletion response from OpenAI

    """
    model = "gpt-4-0613"
    encoding = tiktoken.encoding_for_model(model)
    token_count = 0
    token_count += len(encoding.encode(system_message))
    token_count += len(encoding.encode(user_message))

    if turbo:
        model = "gpt-4-0125-preview"
        print(f"Turbo mode enabled. Token count: {token_count}")
    else:
        if token_count > 8000:
            print(f"Turbo is not set, but the token count is {token_count}. Using GPT-4-0125-preview")
            model = "gpt-4-0125-preview"
    print(model)
    chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_message,
                },
                {
                    "role": "user",
                    "content": user_message,
                }
            ],
            model=model,
            temperature=temperature
        )
    if not hasattr(chat_completion, "error"):
        print(f"Response: {chat_completion}")

    return chat_completion