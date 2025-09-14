from openai import OpenAI
from openai.types.chat.chat_completion_message import ChatCompletionMessage

from constants import DEFAULT_OPENAI_MODEL
from prompts import DEFAULT_SYSTEM_PROMPT
from pydantic import BaseModel
from clients.llm_service_interface import LLMServiceInterface

OPENAI_MODELS_THAT_SUPPORT_TEMPERATURE = ["gpt-4.1"]
OPENAI_MODELS_THAT_SUPPORT_REASONING_EFFORT = ["gpt-5", "gpt-5-mini"]


class OpenAIService(LLMServiceInterface):
    def generate_response(
        self,
        user_input: str,
        system_prompt: str = DEFAULT_SYSTEM_PROMPT,
        model: str = DEFAULT_OPENAI_MODEL,
        chat_history: list[ChatCompletionMessage] | None = None,
        response_format: BaseModel | None = None,
        temperature: float = 0.0,
        reasoning_effort: str | None = "minimal",
        client: OpenAI | None = None,
    ):
        if not user_input:
            raise Exception("User input not provided")

        if not client:
            client = OpenAI()

        messages = (
            [{"role": "system", "content": system_prompt}]
            + (chat_history or [])
            + [
                {
                    "role": "user",
                    "content": user_input,
                }
            ]
        )

        try:
            kwargs = {
                "model": model,
                "messages": messages,
            }

            # Some reasoning models do not support temperature
            if model in OPENAI_MODELS_THAT_SUPPORT_TEMPERATURE:
                kwargs["temperature"] = temperature

            if (
                reasoning_effort
                and model in OPENAI_MODELS_THAT_SUPPORT_REASONING_EFFORT
            ):
                kwargs["reasoning_effort"] = reasoning_effort

            if response_format:
                completion = client.beta.chat.completions.parse(
                    **kwargs,
                    response_format=response_format,
                )
            else:
                completion = client.chat.completions.create(**kwargs)
            return completion.choices[0].message
        except Exception as e:
            print(e)
            return ChatCompletionMessage(
                role="assistant", content="I encountered an issue."
            )
