import os
import argparse
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function
from prompts import system_prompt

def main():
    parser = argparse.ArgumentParser(description="AI coding agent")
    parser.add_argument("user_prompt", type=str, help="Prompt for Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")

    for _ in range(20):
        try:
            final_response = generate_content(client, messages, args.verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                return
        except Exception as e:
            print(f"Error in generate_content: {e}")

    print(f"Maximum iterations (20) reached")
    sys.exit(1)

def generate_content(client, messages, verbose):
     
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
    )
    )

    if not response.usage_metadata:
        raise RuntimeError("No usage metadata available for this response.")

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")

    if response.candidates:
        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)

    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)

        if not function_call_result.parts:
            raise RuntimeError("Function call returned no parts")

        if not function_call_result.parts[0].function_response:
            raise RuntimeError("Function call returned no function_response")

        if not function_call_result.parts[0].function_response.response:
            raise RuntimeError("Function call returned no response data")

        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")

        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting.")
    
    messages.append(types.Content(role="user", parts=function_responses))
    
    return False
    
    
if __name__ == "__main__":
    main()