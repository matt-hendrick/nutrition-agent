from clients.openai_service import OpenAIService
from clients.ollama_service import OllamaService
from openai import OpenAI

if __name__ == "__main__":
    client = OpenAI()
    service = OpenAIService()
    ollama_service = OllamaService()
    chat_history = []
    while True:
        user_input = input(
            "Hello, I am your nutrition assistant. How can I help you today?\n\n"
        )
        if not user_input:
            print("No input provided")
            continue
        result = service.generate_response(
            user_input, client=client, chat_history=chat_history
        )
        # result = ollama_service.generate_response(
        #     user_input, stream=False, chat_history=chat_history
        # )
        print(result.content)

        user_message = {"role": "user", "content": user_input}
        assistant_message = {"role": "assistant", "content": result.content}
        chat_history.extend([user_message, assistant_message])
