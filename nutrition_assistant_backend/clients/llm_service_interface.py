from typing import Any


class LLMServiceInterface:
    def generate_response(
        self, user_input: str, chat_history: list[Any] = None, **kwargs
    ) -> str:
        raise NotImplementedError
