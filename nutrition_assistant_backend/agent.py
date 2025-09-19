from clients.openai_service import OpenAIService
from openai import OpenAI

from dotenv import load_dotenv

from tools.tavily_tools import tavily_search
from tools.beautiful_soup_tools import fetch_clean_text
from enum import Enum
from pydantic import BaseModel
from prompts import QUESTION_TYPE_PROMPT


class QuestionType(str, Enum):
    specific_restaurant = "specific_restaurant"
    restaurant_recommendation = "restaurant_recommendation"
    general_nutrition_info = "general_nutrition_info"
    recipe_suggestion = "recipe_suggestion"
    website_content = "website_content"
    other = "other"


class QuestionTypeResponse(BaseModel):
    type: QuestionType
    search: str | None = None


def handle_specific_restaurant(user_input, result, chat_history, service, client):
    if not result.parsed.search:
        raise Exception("No search found in result", result)
    menu_results = tavily_search(result.parsed.search)
    print("Menu Results:", menu_results)
    results = menu_results.get("results", [])
    if results:
        for result in results:
            # We have a simplistic bs4 scraper that can easily fail on some sites
            # So we will try/catch until we successfully fetch to avoid breaking the whole flow
            try:
                if "url" in result:
                    menu_content = fetch_clean_text(result["url"])
                    print("Menu Content:", menu_content)
                    # Once we found a result with some menu content, we can stop
                    break
                else:
                    print("No menu URLs found in Tavily results.")
            except Exception as e:
                print(f"Error fetching menu from {result.get('url')}: {e}")
    else:
        print("No results found from Tavily search.")

    specific_restaurant_prompt = f"""You are an expert nutrition assistant. 

    Here is the menu content we found for the restaurant they mentioned: {menu_content}.

    Here are the results we found when searching for the restaurant's menu: {menu_results}. 

    Use that information and your expertise to answer the user's question as best as you can."""

    final_response = service.generate_response(
        user_input=user_input,
        system_prompt=specific_restaurant_prompt,
        client=client,
        chat_history=chat_history,
    )
    print("Final Response:", final_response.content)
    return final_response


def handle_restaurant_recommendation(user_input, result, chat_history, service, client):
    if not result.parsed.search:
        raise Exception("No search found in result", result)
    rec_results = tavily_search(result.parsed.search)
    print("Recommendation Results:", rec_results)
    results = rec_results.get("results", [])

    recommendation_prompt = f"""You are an expert nutrition assistant.

    The user is asking for restaurant recommendations in a city or for a specific cuisine. Here are the search results you can use to inform your answer:
    {results}

    Use the above information and your nutrition expertise to recommend restaurants that fit the user's request, and provide nutrition advice or healthy options based on the info provided. If the user mentioned dietary restrictions or preferences, take those into account. Include URLs as citations if relevant.

    If applicable, suggest healthier alternatives or modifications to menu items to better align with the user's nutrition goals. Suggest up to 3 options, but only if good options are in the results.
    """

    final_response = service.generate_response(
        user_input=user_input,
        system_prompt=recommendation_prompt,
        client=client,
        chat_history=chat_history,
    )
    print("Final Response:", final_response.content)
    return final_response

def handle_other(user_input, result, chat_history, service, client):
    context = ""
    # If a search query is provided, run it and use the results as context
    if result.parsed.search and result.parsed.search != "none":
        other_results = tavily_search(result.parsed.search)
        print("Other Results:", other_results)
        results = other_results.get("results", [])
        context = f"""\nHere is some context from a web search that may be relevant:
            {results}"""

    other_prompt = f"""You are an expert nutrition assistant.{context}
    
    Use your expertise and any contextual information to answer the user's question or continue the conversation.
    """

    final_response = service.generate_response(
        user_input=user_input,
        system_prompt=other_prompt,
        client=client,
        chat_history=chat_history,
    )
    print("Final Response:", final_response.content)
    return final_response

def handle_recipe_suggestion(user_input, result, chat_history, service, client):
    if not result.parsed.search:
        raise Exception("No search found in result", result)
    recipe_results = tavily_search(result.parsed.search)
    print("Recipe Results:", recipe_results)
    results = recipe_results.get("results", [])
    context = f"\nHere are some recipe search results that may be relevant:\n{results}"

    recipe_prompt = f"""You are an expert nutrition assistant.{context}

Use your expertise and any contextual information to suggest healthy recipes or meal ideas that fit the user's request. If the user mentioned dietary restrictions or preferences, take those into account. 

Provide URLs if available for the recipes you cite.
"""

    final_response = service.generate_response(
        user_input=user_input,
        system_prompt=recipe_prompt,
        client=client,
        chat_history=chat_history,
    )
    print("Final Response:", final_response.content)
    return final_response


def handle_general_nutrition_info(user_input, result, chat_history, service, client):
    if not result.parsed.search:
        raise Exception("No search found in result", result)
    nutrition_results = tavily_search(result.parsed.search)
    print("Nutrition Results:", nutrition_results)
    results = nutrition_results.get("results", [])
    context = f"\nHere is some nutrition info from a web search that may be relevant:\n{results}"

    nutrition_prompt = f"""You are an expert nutrition assistant.{context}

Use your expertise and any contextual information to answer the user's nutrition question. Be clear, concise, and cite sources if relevant.
"""

    final_response = service.generate_response(
        user_input=user_input,
        system_prompt=nutrition_prompt,
        client=client,
        chat_history=chat_history,
    )
    print("Final Response:", final_response.content)
    return final_response

def handle_website_content(user_input, result, chat_history, service, client):
    if not result.parsed.search or result.parsed.search == "none":
        raise Exception("No URL found in result for website_content", result)
    url = result.parsed.search
    print(f"Fetching website content from: {url}")
    try:
        website_text = fetch_clean_text(url)
    except Exception as e:
        print(f"Error fetching website content from {url}: {e}")
        website_text = ""

    website_prompt = f"""You are an expert nutrition assistant.

Here is the content extracted from the website the user referenced:
{website_text}

Use this information and your expertise to answer the user's question as best as you can.
"""

    final_response = service.generate_response(
        user_input=user_input,
        system_prompt=website_prompt,
        client=client,
        chat_history=chat_history,
    )
    print("Final Response:", final_response.content)
    return final_response


if __name__ == "__main__":
    load_dotenv()

    chat_history = []

    client = OpenAI()
    service = OpenAIService()

    while True:
        user_input = input(
            "Hello, I am your nutrition assistant. How can I help you today?\n\n"
        )
        if not user_input:
            print("No input provided")
            continue

        ## We are indentifying the user's intent first to route to the right prompt/tool logic
        result = service.generate_response(
            user_input=user_input,
            system_prompt=QUESTION_TYPE_PROMPT,
            client=client,
            chat_history=chat_history,
            response_format=QuestionTypeResponse,
        )
        print(result)

        if result.parsed.type == QuestionType.specific_restaurant:
            final_response = handle_specific_restaurant(
                user_input, result, chat_history, service, client
            )
        elif result.parsed.type == QuestionType.restaurant_recommendation:
            final_response = handle_restaurant_recommendation(
                user_input, result, chat_history, service, client
            )
        elif result.parsed.type == QuestionType.recipe_suggestion:
            final_response = handle_recipe_suggestion(
                user_input, result, chat_history, service, client
            )
        elif result.parsed.type == QuestionType.general_nutrition_info:
            final_response = handle_general_nutrition_info(
                user_input, result, chat_history, service, client
            )
        elif result.parsed.type == QuestionType.website_content:
            final_response = handle_website_content(
                user_input, result, chat_history, service, client
            )
        else:
            final_response = handle_other(
                user_input, result, chat_history, service, client
            )

        if final_response:
            user_message = {"role": "user", "content": user_input}
            assistant_message = {"role": "assistant", "content": final_response.content}
            chat_history.extend([user_message, assistant_message])
