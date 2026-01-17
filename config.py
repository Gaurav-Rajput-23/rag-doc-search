
# System Prompt 
SYSTEM_PROMPT = """
You are a helpful technical assistant. 
Answer the user's question using ONLY the context provided below.
- If the answer is not in the context, strictly say "I don't know based on the provided document."
- Do not use outside knowledge.
- Be concise and accurate.
"""

#embedding Model
EMBEDDING_MODEL_NAME = 'all-MiniLM-L6-v2'

# Chunk Settings
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200