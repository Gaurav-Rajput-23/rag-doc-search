import os

# System Prompt given to the AI model
SYSTEM_PROMPT = """
You are a helpful technical assistant. 
Answer the user's question using ONLY the context provided below based on the given instructions.
Instructions:
- Base your answer strictly on the context (which may include PDFs, spreadsheets, voice transcripts, image analyses, and indexed web URLs); if context does not fully cover what was asked, say "I don't know" and explain briefly why.
- Be concise, accurate, and relevant; aim for 2-4 sentences maximum.
- Strictly focus on the prompt or question provided by the user.
- Quote or reference specific parts of the context or source files to support your answer when applicable.
- If the request requires tables or formatted presentation, provide them accordingly.
"""

# Embedding Model
EMBEDDING_MODEL_NAME = 'all-MiniLM-L6-v2'

# Chunk Settings
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 300

# Cache & Storage Settings
CACHE_DIR = os.path.join(os.path.dirname(__file__), ".cache")

# Extension Categories
PDF_EXTENSIONS = [".pdf"]
IMAGE_EXTENSIONS = [".png", ".jpg", ".jpeg", ".webp"]
AUDIO_EXTENSIONS = [".mp3", ".wav", ".m4a", ".ogg"]
SPREADSHEET_EXTENSIONS = [".csv", ".xlsx"]
ALLOWED_EXTENSIONS = PDF_EXTENSIONS + IMAGE_EXTENSIONS + AUDIO_EXTENSIONS + SPREADSHEET_EXTENSIONS