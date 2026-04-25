import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("GEMINI_API_KEY not found in .env")
    exit(1)

genai.configure(api_key=api_key)

print("Available models:")
for m in genai.list_models():
    if 'embedContent' in m.supported_generation_methods:
        print(f"{m.name} supported: {m.supported_generation_methods}")
