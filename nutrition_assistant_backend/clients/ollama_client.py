from ollama import chat, ChatResponse, Message

from constants import DEFAULT_OLLAMA_MODEL
from prompts import DEFAULT_SYSTEM_PROMPT


def generate_response(
    user_input: str,
    model: str = DEFAULT_OLLAMA_MODEL,
    system_prompt: str = DEFAULT_SYSTEM_PROMPT,
    stream: bool = False,
    chat_history: list[Message] = None,
) -> str | None:
    if not user_input or not user_input.strip():
        return "Invalid input. Please provide a valid query."

    try:
        messages = (
            [{"role": "system", "content": system_prompt}]
            + chat_history
            + [{"role": "user", "content": user_input}]
        )

        if stream:
            message = ""
            for chunk in chat(model=model, messages=messages, stream=True):
                message += chunk["message"]["content"]
                print(chunk["message"]["content"], end="", flush=True)
            print()
            return message
        else:
            response: ChatResponse = chat(model=model, messages=messages)
            return response.message.content
    except Exception as e:
        return f"An error occurred: {str(e)}"


if __name__ == "__main__":
    chat_history = []
    while True:
        user_input = input("Hi, how can I help you today?\n\n")
        if not user_input:
            print("No input provided")
            continue
        result = generate_response(user_input, stream=True, chat_history=chat_history)
        new_messages = [
            {
                "role": "user",
                "content": user_input,
            },
            {
                "role": "assistant",
                "content": result,
            },
        ]
        chat_history.extend(new_messages)
