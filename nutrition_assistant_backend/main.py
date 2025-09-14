from clients.openai_client import completions_request
from openai import OpenAI

if __name__ == "__main__":
    client = OpenAI()
    chat_history = []
    while True:
        user_input = input(
            "Hello, I am your nutrition assistant. How can I help you today?\n\n"
        )
        if not user_input:
            print("No input provided")
            continue
        result = completions_request(
            user_input, client=client, chat_history=chat_history
        )
        print(result.content)

        user_message = {"role": "user", "content": user_input}
        assistant_message = {"role": "assistant", "content": result.content}
        chat_history.extend([user_message, assistant_message])
