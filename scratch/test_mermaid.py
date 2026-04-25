import base64
import urllib.request
import zlib
import json

mermaid_code = """graph TD
    User([User]) -->|Interacts with UI| Frontend[Frontend React/Vite]
    Frontend -->|REST API Calls| Backend[Backend FastAPI]
    
    subgraph Backend System
        Backend -->|Extract Text| OCR[Tesseract OCR]
        Backend -->|Store Uploads| FS[Local File System]
        Backend -->|Query| RAG[RAG Pipeline]
        RAG -->|Generate Embeddings| GenAI[Gemini AI Model]
        Backend -->|Store Vectors| DB[(MongoDB)]
    end"""

# mermaid.ink uses base64 encoded string, but the recommended way is base64(pako.deflate(str)) for large strings or just base64(str)

# Using pako-like string encoding:
# It's actually a JSON string: {"code": mermaid_code, "mermaid": {"theme": "default"}}
state = json.dumps({"code": mermaid_code, "mermaid": {"theme": "default"}})
b64 = base64.urlsafe_b64encode(state.encode('utf-8')).decode('utf-8')

url_png = f"https://mermaid.ink/img/{b64}"
url_pdf = f"https://mermaid.ink/svg/{b64}" # Wait, let's see if pdf is supported. There is usually /img and /svg. 
# actually crocxz mermaid.ink does not officially support /pdf natively. Some forks do.

# Let's write the string directly and check
print(f"B64: {b64}")
