import argparse
from clients.openai_service import OpenAIService
from clients.ollama_service import OllamaService
from openai import OpenAI

from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Nutrition Assistant")
    parser.add_argument(
        "--service",
        choices=["openai", "ollama"],
        default="openai",
        help="Choose which LLM service to use (default: openai)",
    )
    args = parser.parse_args()

    chat_history = []

    if args.service == "openai":
        client = OpenAI()
        service = OpenAIService()
        use_openai = True
    else:
        service = OllamaService()
        use_openai = False

    while True:
        user_input = input(
            "Hello, I am your nutrition assistant. How can I help you today?\n\n"
        )
        if not user_input:
            print("No input provided")
            continue

        if use_openai:
            result = service.generate_response(
                user_input, client=client, chat_history=chat_history
            )
        else:
            result = service.generate_response(
                user_input, stream=False, chat_history=chat_history
            )

        print(result.content)

        user_message = {"role": "user", "content": user_input}
        assistant_message = {"role": "assistant", "content": result.content}
        chat_history.extend([user_message, assistant_message])
