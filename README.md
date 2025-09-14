## Requirements

- Must be able to make requests to an LLM
- Support for Chat Completions
- Support for structured outputs
- Support for Ollama or OpenAI
- Allow multi-turn interactions
- Should take into account user preferences, dietary restrictions, medical issues, allergies, age range
- Should pull in datasets to ground responses
- Some evals 

### Nice to Haves

- Specific handling of diabetes
- Specific handling of hypertension
- Specific handling for people on GLP-1
- Cites sources in responses
- Setup simple frontend wrapper
- Deploy it somewhere and make it public
- Support for Responses API


## Rough Plan

1. Init repo + Poetry
2. Basic POC interacting with local LLM
3. Flesh out that interaction and abstract bits to allow interacting with either Ollama/OpenAI apis
4. Flesh out interaction to support structured outputs
5. Create basic prompts
6. Further develop prompts to dynamically intake user data and customize responses
7. Add tools or prompt construction logic to fetch data to use to customize responses
8. Add citations to responses
9. Add evals
10. Add a simple frontend wrapper
11. Deploy