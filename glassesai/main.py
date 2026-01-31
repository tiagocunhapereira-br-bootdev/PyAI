import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError(
        "Hey! You haven't set an API key! Try changing .env and putting your API key there!"
    )

client = genai.Client(api_key=api_key)


import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError(
        "Hey! You haven't set an API key! Try changing .env and putting your API key there!"
    )

client = genai.Client(api_key=api_key)


def main():
    print("Welcome to the chatbot! Type 'exit' or 'quit' to end the chat.")

    if len(sys.argv) <= 1:
        print("This agent expects a question as a CLI argument.")
        sys.exit(1)

    user_input = " ".join(sys.argv[1:])

    messages = []
    messages.append(
        types.Content(
            role="user",
            parts=[types.Part(text=user_input)],
        )
    )

    for _ in range(20):
        contents = [
            types.Content(
                role="user",
                parts=[types.Part(text=system_prompt)],
            )
        ] + messages

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=types.GenerateContentConfig(
                temperature=0,
                tools=[available_functions],
            ),
        )

        candidates = getattr(response, "candidates", None) or []
        for cand in candidates:
            if cand.content is not None:
                messages.append(cand.content)

        function_calls = getattr(response, "function_calls", None)
        function_results_parts = []

        if function_calls:
            for function_call in function_calls:
                function_call_result = call_function(function_call, verbose=True)

                if not function_call_result.parts:
                    raise RuntimeError("Function call returned no parts")

                part0 = function_call_result.parts[0]
                if part0.function_response is None:
                    raise RuntimeError("Function call part has no function_response")

                resp = part0.function_response.response
                if resp is None:
                    raise RuntimeError(
                        "Function call function_response.response is None"
                    )

                function_results_parts.append(part0)
                print(f"-> {resp}")

            messages.append(
                types.Content(role="user", parts=function_results_parts)
            )
        else:
            final_text = response.text
            print("Final response:")
            print(final_text)
            return

    print("Error: agent reached maximum iterations without producing a final response.")
    sys.exit(1)


if __name__ == "__main__":
    main()


