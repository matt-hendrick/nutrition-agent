from clients.openai_service import OpenAIService
from openai import OpenAI
from tools.tavily_tools import tavily_search
from tools.beautiful_soup_tools import fetch_clean_text
from enum import Enum
from pydantic import BaseModel
from prompts import QUESTION_TYPE_PROMPT
from typing import Dict, List, Optional, Any

PROMPT_PREFIX = "You are an expert nutrition assistant.\n"
PROMPT_SUFFIX = """
Format your answer in raw markdown. Use markdown lists, headings, and bold where appropriate.
Cite your sources using markdown links, for example: [Little Goat Diner Menu](https://www.littlegoatchicago.com/menu).
The result will be directly passed to a React Markdown JSX component to render to the user.

Example:
- **Breakfast:** Pancakes, eggs, hashbrowns
- **Sandwiches:** Tonkatsu, Shrimp Sammie

Sources:
- [Little Goat Diner Menu](https://www.littlegoatchicago.com/menu)
"""

def construct_prompt(main_prompt_content: str) -> str:
    return f"{PROMPT_PREFIX}{main_prompt_content}{PROMPT_SUFFIX}"

class QuestionType(str, Enum):
    specific_restaurant = "specific_restaurant"
    restaurant_recommendation = "restaurant_recommendation"
    general_nutrition_info = "general_nutrition_info"
    recipe_suggestion = "recipe_suggestion"
    website_content = "website_content"
    other = "other"

class QuestionTypeResponse(BaseModel):
    type: QuestionType
    search: Optional[str] = None

class Agent:
    def __init__(self, service=None, client=None):
        self.service = service or OpenAIService()
        self.client = client or OpenAI()
        self.threads: Dict[str, List[Dict[str, str]]] = {}

    def get_history(self, thread_id: str) -> List[Dict[str, str]]:
        return self.threads.setdefault(thread_id, [])

    def add_to_history(self, thread_id: str, user_input: str, assistant_output: str):
        history = self.get_history(thread_id)
        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": assistant_output})

    def classify_question(
        self, user_input: str, chat_history: List[Dict[str, str]]
    ) -> Any:
        return self.service.generate_response(
            user_input=user_input,
            system_prompt=QUESTION_TYPE_PROMPT,
            client=self.client,
            chat_history=chat_history,
            response_format=QuestionTypeResponse,
        )

    def handle(self, user_input: str, thread_id: str) -> str:
        chat_history = self.get_history(thread_id)
        result = self.classify_question(user_input, chat_history)
        handler_map = {
            QuestionType.specific_restaurant: self.handle_specific_restaurant,
            QuestionType.restaurant_recommendation: self.handle_restaurant_recommendation,
            QuestionType.recipe_suggestion: self.handle_recipe_suggestion,
            QuestionType.general_nutrition_info: self.handle_general_nutrition_info,
            QuestionType.website_content: self.handle_website_content,
            QuestionType.other: self.handle_other,
        }
        handler = handler_map.get(result.parsed.type, self.handle_other)
        response = handler(user_input, result, chat_history)
        self.add_to_history(thread_id, user_input, response.content)
        return response.content

    def handle_specific_restaurant(self, user_input, result, chat_history):
        if not result.parsed.search:
            raise Exception("No search found in result", result)
        menu_results = tavily_search(result.parsed.search)
        results = menu_results.get("results", [])
        menu_content = ""
        if results:
            for result_item in results:
                try:
                    if "url" in result_item:
                        menu_content = fetch_clean_text(result_item["url"])
                        break
                except Exception:
                    continue
        main_prompt_content = (
            f"Here is the menu content we found: {menu_content}. "
            f"Here are the search results: {menu_results}. "
            "Use that information and your expertise to answer the user's question."
        )
        prompt = construct_prompt(main_prompt_content)
        return self.service.generate_response(
            user_input=user_input,
            system_prompt=prompt,
            client=self.client,
            chat_history=chat_history,
        )

    def handle_restaurant_recommendation(self, user_input, result, chat_history):
        if not result.parsed.search:
            raise Exception("No search found in result", result)
        rec_results = tavily_search(result.parsed.search)
        results = rec_results.get("results", [])
        main_prompt_content = (
            "The user is asking for restaurant recommendations. Here are the search results:\n"
            f"{results}\n"
            "Use the above information and your nutrition expertise to recommend restaurants and provide nutrition advice."
        )
        prompt = construct_prompt(main_prompt_content)
        return self.service.generate_response(
            user_input=user_input,
            system_prompt=prompt,
            client=self.client,
            chat_history=chat_history,
        )

    def handle_recipe_suggestion(self, user_input, result, chat_history):
        if not result.parsed.search:
            raise Exception("No search found in result", result)
        recipe_results = tavily_search(result.parsed.search)
        results = recipe_results.get("results", [])
        main_prompt_content = (
            f"Here are some recipe search results:\n{results}\n"
            "Use your expertise to suggest healthy recipes or meal ideas."
        )
        prompt = construct_prompt(main_prompt_content)
        return self.service.generate_response(
            user_input=user_input,
            system_prompt=prompt,
            client=self.client,
            chat_history=chat_history,
        )

    def handle_general_nutrition_info(self, user_input, result, chat_history):
        if not result.parsed.search:
            raise Exception("No search found in result", result)
        nutrition_results = tavily_search(result.parsed.search)
        results = nutrition_results.get("results", [])
        main_prompt_content = (
            f"Here is some nutrition info from a web search:\n{results}\n"
            "Use your expertise to answer the user's nutrition question."
        )
        prompt = construct_prompt(main_prompt_content)
        return self.service.generate_response(
            user_input=user_input,
            system_prompt=prompt,
            client=self.client,
            chat_history=chat_history,
        )

    def handle_website_content(self, user_input, result, chat_history):
        if not result.parsed.search or result.parsed.search == "none":
            raise Exception("No URL found in result for website_content", result)
        url = result.parsed.search
        try:
            website_text = fetch_clean_text(url)
        except Exception:
            website_text = ""
        main_prompt_content = (
            f"Here is the content extracted from the website:\n{website_text}\n"
            "Use this information and your expertise to answer the user's question."
        )
        prompt = construct_prompt(main_prompt_content)
        return self.service.generate_response(
            user_input=user_input,
            system_prompt=prompt,
            client=self.client,
            chat_history=chat_history,
        )

    def handle_other(self, user_input, result, chat_history):
        context = ""
        if result.parsed.search and result.parsed.search != "none":
            other_results = tavily_search(result.parsed.search)
            results = other_results.get("results", [])
            context = f"\nHere is some context from a web search:\n{results}"
        main_prompt_content = (
            f"{context}\nUse your expertise to answer the user's question."
        )
        prompt = construct_prompt(main_prompt_content)
        return self.service.generate_response(
            user_input=user_input,
            system_prompt=prompt,
            client=self.client,
            chat_history=chat_history,
        )