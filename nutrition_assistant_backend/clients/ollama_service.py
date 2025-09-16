from ollama import chat, ChatResponse, Message

from constants import DEFAULT_OLLAMA_MODEL
from prompts import DEFAULT_SYSTEM_PROMPT
from clients.llm_service_interface import LLMServiceInterface


class OllamaService(LLMServiceInterface):
    def generate_response(
        self,
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
                return response.message
        except Exception as e:
            return f"An error occurred: {str(e)}"
