import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError(
        "Hey! You haven't set an API key! Try changing .env and putting your API key there!"
    )

client = genai.Client(api_key=api_key)


def main():
    print("Welcome to the chatbot! Type 'exit' or 'quit' to end the chat.")

    conversation_history = []

    # One-shot CLI mode
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
        conversation_history.append(
            types.Content(role="user", parts=[types.Part(text=user_input)])
        )

        response = client.models.generate_content(
            model="gemma-3-12b-it",
            contents=conversation_history,
            config=types.GenerateContentConfig(
                temperature=0.35,
            ),
        )

        function_calls = getattr(response, "function_calls", None)

        if function_calls:
            for function_call in function_calls:
                print(f"Calling function: {function_call.name}({function_call.args})")
        else:
            bot_response = response.text
            print(f"Chatbot: {bot_response}")
        return

    # Interactive loop
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Chatbot: Goodbye!")
            break

        conversation_history.append(
            types.Content(role="user", parts=[types.Part(text=user_input)])
        )

        response = client.models.generate_content(
            model="gemma-3-12b-it",
            contents=conversation_history,
            config=types.GenerateContentConfig(
                temperature=0.35,
            ),
        )

        function_calls = getattr(response, "function_calls", None)

        if function_calls:
            for function_call in function_calls:
                print(f"Calling function: {function_call.name}({function_call.args})")
        else:
            bot_response = response.text
            conversation_history.append(
                types.Content(role="model", parts=[types.Part(text=bot_response)])
            )
            print(f"Chatbot: {bot_response}")


if __name__ == "__main__":
    main()
