import io
import os
import pickle
import hashlib
from concurrent.futures import ThreadPoolExecutor
import streamlit as st
import PIL.Image
import pandas as pd
import requests
from bs4 import BeautifulSoup
from google import genai
from google.genai import types
from pypdf import PdfReader
import pdfplumber
import pytesseract
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from rank_bm25 import BM25Okapi
from config import (
    SYSTEM_PROMPT, EMBEDDING_MODEL_NAME, CHUNK_SIZE, CHUNK_OVERLAP, CACHE_DIR,
    PDF_EXTENSIONS, IMAGE_EXTENSIONS, AUDIO_EXTENSIONS, SPREADSHEET_EXTENSIONS
)

CANDIDATE_MODELS = ['gemini-3.8-flash', 'gemini-3.5-flash', 'gemini-2.5-flash', 'gemini-1.5-flash']

# --- 1. INITIALIZATION ---
def get_ai_client():
    api_key = None
    try:
        api_key = st.secrets.get("GOOGLE_API_KEY")
    except Exception:
        pass
    
    if not api_key:
        api_key = os.environ.get("GOOGLE_API_KEY")
        
    if not api_key:
        return None
    return genai.Client(api_key=api_key)

@st.cache_resource
def get_embedder():
    return SentenceTransformer(EMBEDDING_MODEL_NAME)

# --- 2. CACHING & PERSISTENCE ---
def get_cache_key(file_objects):
    hasher = hashlib.md5()
    for file_obj in file_objects:
        hasher.update(file_obj.name.encode('utf-8'))
        hasher.update(str(file_obj.size).encode('utf-8'))
    return hasher.hexdigest()

def get_cache_paths(cache_key):
    os.makedirs(CACHE_DIR, exist_ok=True)
    index_path = os.path.join(CACHE_DIR, f"{cache_key}.index")
    meta_path = os.path.join(CACHE_DIR, f"{cache_key}.pkl")
    return index_path, meta_path

def save_to_cache(cache_key, index, bm25, chunks, processed_files):
    index_path, meta_path = get_cache_paths(cache_key)
    faiss.write_index(index, index_path)
    with open(meta_path, "wb") as f:
        pickle.dump({"bm25": bm25, "chunks": chunks, "processed_files": processed_files}, f)

def load_from_cache(cache_key):
    index_path, meta_path = get_cache_paths(cache_key)
    if os.path.exists(index_path) and os.path.exists(meta_path):
        try:
            index = faiss.read_index(index_path)
            with open(meta_path, "rb") as f:
                meta = pickle.load(f)
            return index, meta.get("bm25"), meta["chunks"], meta["processed_files"]
        except Exception:
            return None
    return None

def clear_disk_cache():
    if os.path.exists(CACHE_DIR):
        for fname in os.listdir(CACHE_DIR):
            fpath = os.path.join(CACHE_DIR, fname)
            if os.path.isfile(fpath):
                try:
                    os.remove(fpath)
                except Exception:
                    pass

# --- 3. MULTIMODAL & SPREADSHEET & WEB EXTRACTION ---

def extract_pdf_chunks(file_obj, file_bytes, text_splitter):
    chunks_with_meta = []
    fname = file_obj.name
    
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page_idx, page in enumerate(pdf.pages, start=1):
                page_text = page.extract_text() or ""
                tables = page.extract_tables()
                if tables:
                    table_strs = []
                    for table in tables:
                        clean_table = [[str(cell or "").strip() for cell in row] for row in table if any(row)]
                        if clean_table:
                            table_str = "\n".join([" | ".join(row) for row in clean_table])
                            table_strs.append(table_str)
                    if table_strs:
                        page_text += "\n\n--- Table Data ---\n" + "\n\n".join(table_strs)
                
                if len(page_text.strip()) < 20:
                    try:
                        img = page.to_image().original
                        ocr_text = pytesseract.image_to_string(img)
                        if ocr_text.strip():
                            page_text += "\n" + ocr_text.strip()
                    except Exception:
                        pass
                
                if page_text.strip():
                    page_chunks = text_splitter.split_text(page_text)
                    for c in page_chunks:
                        chunks_with_meta.append({
                            "text": c,
                            "source": fname,
                            "page": page_idx,
                            "type": "pdf"
                        })
    except Exception:
        try:
            reader = PdfReader(io.BytesIO(file_bytes))
            for page_idx, page in enumerate(reader.pages, start=1):
                t = page.extract_text()
                if t:
                    page_chunks = text_splitter.split_text(t)
                    for c in page_chunks:
                        chunks_with_meta.append({
                            "text": c,
                            "source": fname,
                            "page": page_idx,
                            "type": "pdf"
                        })
        except Exception:
            pass
            
    return chunks_with_meta

def extract_spreadsheet_chunks(file_obj, file_bytes, text_splitter):
    fname = file_obj.name
    ext = os.path.splitext(fname)[1].lower()
    chunks_with_meta = []
    
    try:
        if ext == ".csv":
            df_dict = {"Sheet1": pd.read_csv(io.BytesIO(file_bytes))}
        else:
            df_dict = pd.read_excel(io.BytesIO(file_bytes), sheet_name=None)
            
        for sheet_name, df in df_dict.items():
            if df.empty:
                continue
            table_markdown = f"--- Spreadsheet Sheet: {sheet_name} ({fname}) ---\n"
            table_markdown += df.to_markdown(index=False)
            
            c_list = text_splitter.split_text(table_markdown)
            for c in c_list:
                chunks_with_meta.append({
                    "text": c,
                    "source": fname,
                    "page": sheet_name,
                    "type": "spreadsheet"
                })
    except Exception as e:
        chunks_with_meta.append({
            "text": f"Error parsing spreadsheet {fname}: {str(e)}",
            "source": fname,
            "page": "Sheet1",
            "type": "spreadsheet"
        })
        
    return chunks_with_meta

def extract_audio_chunks(file_obj, file_bytes, text_splitter):
    fname = file_obj.name
    ext = os.path.splitext(fname)[1].lower()
    mime_map = {".mp3": "audio/mp3", ".wav": "audio/wav", ".m4a": "audio/m4a", ".ogg": "audio/ogg"}
    mime_type = mime_map.get(ext, "audio/mp3")
    
    audio_part = types.Part.from_bytes(data=file_bytes, mime_type=mime_type)
    prompt = f"Provide a clean, complete, and accurate transcription of this audio recording ({fname})."
    
    transcript, err = call_gemini_simple([audio_part, prompt])
    if err:
        transcript = f"[Audio Transcription Notice for {fname}: {err}]"
        
    audio_chunks = text_splitter.split_text(transcript)
    return [{
        "text": c,
        "source": fname,
        "page": "Voice Note",
        "type": "audio"
    } for c in audio_chunks]

def extract_image_chunks(file_obj, file_bytes, text_splitter):
    fname = file_obj.name
    ext = os.path.splitext(fname)[1].lower()
    mime_map = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}
    mime_type = mime_map.get(ext, "image/jpeg")
    
    ocr_text = ""
    try:
        img = PIL.Image.open(io.BytesIO(file_bytes))
        ocr_text = pytesseract.image_to_string(img).strip()
    except Exception:
        pass
        
    img_part = types.Part.from_bytes(data=file_bytes, mime_type=mime_type)
    prompt = (
        f"Describe the contents of this image ({fname}) in detail. "
        "Include all visible text, charts, tables, diagrams, colors, key objects, and visual structure present."
    )
    vision_desc, err = call_gemini_simple([img_part, prompt])
    
    combined = ""
    if ocr_text:
        combined += f"Extracted Text (OCR):\n{ocr_text}\n\n"
    if vision_desc:
        combined += f"Visual Description:\n{vision_desc}\n"
    elif err:
        combined += f"Visual Analysis Notice: {err}\n"
        
    image_chunks = text_splitter.split_text(combined or "Image uploaded.")
    return [{
        "text": c,
        "source": fname,
        "page": "Image Visual",
        "type": "image"
    } for c in image_chunks]

def scrape_web_url_chunks(url):
    """
    Fetches and parses text content from a web URL.
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        
        soup = BeautifulSoup(resp.text, 'html.parser')
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
            
        page_text = soup.get_text(separator=' ', strip=True)
        title = soup.title.string.strip() if soup.title else url
        
        chunks = text_splitter.split_text(f"--- Web Page Content ({title}) ---\n" + page_text)
        return [{
            "text": c,
            "source": title or url,
            "page": "Web URL",
            "type": "web"
        } for c in chunks]
    except Exception as e:
        return [{
            "text": f"Failed to fetch Web URL ({url}): {str(e)}",
            "source": url,
            "page": "Web URL",
            "type": "web"
        }]

def call_gemini_simple(contents):
    ai_client = get_ai_client()
    if not ai_client:
        return None, "API Key missing."
    for model_name in CANDIDATE_MODELS:
        try:
            res = ai_client.models.generate_content(model=model_name, contents=contents)
            if res and res.text:
                return res.text, None
        except Exception as e:
            if "PERMISSION_DENIED" in str(e) or "403" in str(e):
                return None, "403 PERMISSION_DENIED: API Key restricted."
            continue
    return None, "Generation failed."

def extract_chunks_from_single_file(file_obj):
    file_bytes = file_obj.getvalue() if hasattr(file_obj, "getvalue") else file_obj.read()
    ext = os.path.splitext(file_obj.name)[1].lower()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    
    if ext in PDF_EXTENSIONS:
        return extract_pdf_chunks(file_obj, file_bytes, text_splitter)
    elif ext in SPREADSHEET_EXTENSIONS:
        return extract_spreadsheet_chunks(file_obj, file_bytes, text_splitter)
    elif ext in AUDIO_EXTENSIONS:
        return extract_audio_chunks(file_obj, file_bytes, text_splitter)
    elif ext in IMAGE_EXTENSIONS:
        return extract_image_chunks(file_obj, file_bytes, text_splitter)
    else:
        text = file_bytes.decode('utf-8', errors='ignore')
        c_list = text_splitter.split_text(text)
        return [{"text": c, "source": file_obj.name, "page": 1, "type": "text"} for c in c_list]

def process_documents(file_objects, extra_chunks=None):
    cache_key = get_cache_key(file_objects)
    cached_data = load_from_cache(cache_key)
    embedder = get_embedder()
    
    if cached_data and not extra_chunks:
        index, bm25, chunks, processed_files = cached_data
        return index, bm25, embedder, chunks, len(file_objects), True

    with ThreadPoolExecutor(max_workers=min(8, max(1, len(file_objects)))) as executor:
        results = list(executor.map(extract_chunks_from_single_file, file_objects))
    
    chunks = [c for r in results for c in r]
    if extra_chunks:
        chunks.extend(extra_chunks)
        
    if not chunks:
        chunks = [{"text": "No extractable text found.", "source": "None", "page": 0, "type": "none"}]
    
    # 1. FAISS Cosine Similarity Index
    chunk_texts = [c["text"] for c in chunks]
    vectors = embedder.encode(chunk_texts, batch_size=32, show_progress_bar=False, normalize_embeddings=True)
    vectors = np.array(vectors, dtype=np.float32)
    faiss.normalize_L2(vectors)
    
    dimension = vectors.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(vectors)
    
    # 2. BM25 Sparse Keyword Index
    tokenized_corpus = [t.lower().split() for t in chunk_texts]
    bm25 = BM25Okapi(tokenized_corpus)
    
    current_files = [f.name for f in file_objects]
    if not extra_chunks:
        save_to_cache(cache_key, index, bm25, chunks, current_files)
    
    return index, bm25, embedder, chunks, len(file_objects), False

# --- 4. HYBRID SEARCH & STREAMING ---

def hybrid_search_index(query, index, bm25, embedder, chunks, top_k=7):
    N = len(chunks)
    
    query_vector = embedder.encode([query], normalize_embeddings=True)
    query_vector = np.array(query_vector, dtype=np.float32)
    faiss.normalize_L2(query_vector)
    _, faiss_indices = index.search(query_vector, k=min(20, N))
    faiss_list = [i for i in faiss_indices[0] if 0 <= i < N]
    
    query_tokens = query.lower().split()
    bm25_scores = bm25.get_scores(query_tokens) if bm25 else np.zeros(N)
    bm25_list = np.argsort(bm25_scores)[::-1][:min(20, N)].tolist()
    
    rrf_scores = {}
    k_constant = 60
    
    for rank, idx in enumerate(faiss_list):
        rrf_scores[idx] = rrf_scores.get(idx, 0.0) + 1.0 / (k_constant + rank + 1)
        
    for rank, idx in enumerate(bm25_list):
        rrf_scores[idx] = rrf_scores.get(idx, 0.0) + 1.0 / (k_constant + rank + 1)
        
    sorted_indices = sorted(rrf_scores.keys(), key=lambda x: rrf_scores[x], reverse=True)[:top_k]
    retrieved_chunks = [chunks[i] for i in sorted_indices]
    
    context_parts = []
    citations = []
    for c in retrieved_chunks:
        context_parts.append(f"[{c['source']} | Page/Section: {c['page']}]\n{c['text']}")
        citations.append({"source": c['source'], "page": c['page'], "type": c['type']})
        
    unique_citations = []
    seen = set()
    for cit in citations:
        key = (cit['source'], str(cit['page']))
        if key not in seen:
            seen.add(key)
            unique_citations.append(cit)
            
    return "\n\n".join(context_parts), unique_citations

def generate_answer_stream(query, context):
    ai_client = get_ai_client()
    if not ai_client:
        yield "API Key not found in Streamlit secrets or environment variables."
        return
        
    prompt = f"{SYSTEM_PROMPT}\n\nCONTEXT:\n{context}\n\nQUESTION:\n{query}\n\nANSWER:"
    
    for model_name in CANDIDATE_MODELS:
        try:
            response_stream = ai_client.models.generate_content_stream(
                model=model_name,
                contents=prompt
            )
            for chunk in response_stream:
                if chunk.text:
                    yield chunk.text
            return
        except Exception as e:
            if "PERMISSION_DENIED" in str(e) or "403" in str(e):
                yield "\n\n⚠️ **API Key Permission Denied (403)**: Please update your key at https://aistudio.google.com/ in `.streamlit/secrets.toml`."
                return
            continue
            
    yield "Error: Unable to generate response with candidate models."