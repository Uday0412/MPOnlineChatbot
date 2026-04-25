import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("GEMINI_API_KEY not found in .env")
    exit(1)

genai.configure(api_key=api_key)

try:
    print("Testing embedding with models/embedding-001...")
    result = genai.embed_content(
        model="models/embedding-001",
        content="Hello world",
        task_type="retrieval_document"
    )
    print("Success!")
    print(f"Embedding length: {len(result['embedding'])}")
except Exception as e:
    print(f"Failed: {e}")

try:
    print("\nTesting embedding with models/text-embedding-004...")
    result = genai.embed_content(
        model="models/text-embedding-004",
        content="Hello world",
        task_type="retrieval_document"
    )
    print("Success!")
except Exception as e:
    print(f"Failed: {e}")
