import os
from dotenv import load_dotenv
from openai import OpenAI

# Load the environment
load_dotenv()

api_key = os.getenv("GROK_API_KEY")
print(f"DEBUG: Checking API Key... Found: {bool(api_key)}")
if api_key:
    print(f"DEBUG: Key prefix: {api_key[:10]}...")

try:
    print("DEBUG: Initializing Client...")
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.x.ai/v1",
    )

    print("DEBUG: Sending test request to Grok...")
    completion = client.chat.completions.create(
        model="grok-beta",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello!"}
        ],
    )
    print("\nSUCCESS! Grok Replied:")
    print(completion.choices[0].message.content)

except Exception as e:
    print("\nFAILED TO CONNECT.")
    print(f"ERROR TYPE: {type(e).__name__}")
    print(f"ERROR MESSAGE: {e}")
