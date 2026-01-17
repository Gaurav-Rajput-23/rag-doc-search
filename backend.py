import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from config import SYSTEM_PROMPT, EMBEDDING_MODEL_NAME, CHUNK_SIZE, CHUNK_OVERLAP

# --- 1. INITIALIZATION ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except KeyError:
    st.error("API Key not found!")
    st.stop()

genai.configure(api_key=api_key)
llm = genai.GenerativeModel('models/gemini-2.5-flash')

# --- 2. CORE FUNCTIONS ---

def process_documents(file_objects):
    """
    Takes a list of uploaded files, extracts text, splits, and creates vectors.
    """
    full_text = ""
    
    # Loop through all uploaded files
    for file_obj in file_objects:
        reader = PdfReader(file_obj)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
    
    # Split text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, 
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = text_splitter.split_text(full_text)
    
    # Create Embeddings
    # Note: This is where we will add Threading later!
    embedder = SentenceTransformer(EMBEDDING_MODEL_NAME)
    vectors = embedder.encode(chunks)
    
    # Create Index
    dimension = vectors.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(vectors)
    
    return index, embedder, chunks, len(file_objects)

def search_index(query, index, embedder, chunks, top_k=3):
    """
    Searches the vector index for relevant chunks.
    """
    query_vector = embedder.encode([query])
    D, I = index.search(query_vector, k=top_k)
    
    # Map indices back to text
    retrieved_chunks = [chunks[i] for i in I[0]]
    return "\n\n".join(retrieved_chunks)

def generate_answer(query, context):
    """
    Generates the final answer using the LLM.
    """
    prompt = f"{SYSTEM_PROMPT}\n\nCONTEXT:\n{context}\n\nQUESTION:\n{query}\n\nANSWER:"
    
    response = llm.generate_content(prompt)
    return response.text