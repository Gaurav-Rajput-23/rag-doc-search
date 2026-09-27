import os
import streamlit as st
import backend as backend

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Nexus Multimodal AI RAG",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- FUTURISTIC AI GLASSMORPHISM THEME ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Dark Theme with Glowing Ambient Background */
    .stApp {
        background-color: #0B0F17;
        background-image: 
            radial-gradient(circle at 15% 15%, rgba(99, 102, 241, 0.12) 0%, transparent 45%),
            radial-gradient(circle at 85% 85%, rgba(168, 85, 247, 0.09) 0%, transparent 45%);
        color: #F3F4F6;
    }
    
    .main .block-container {
        padding: 2.5rem 2rem 3rem 2rem;
        max-width: 900px;
    }
    
    /* Hide MainMenu & Footer, but Keep Transparent Header & Sidebar Toggle Button Visible */
    #MainMenu, footer {visibility: hidden;}
    
    [data-testid="stHeader"] {
        background: transparent !important;
    }
    
    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapseButton"],
    button[kind="header"] {
        color: #818CF8 !important;
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        backdrop-filter: blur(10px) !important;
        visibility: visible !important;
        z-index: 999999 !important;
    }
    
    [data-testid="collapsedControl"]:hover,
    [data-testid="stSidebarCollapseButton"]:hover {
        background: rgba(99, 102, 241, 0.25) !important;
        border-color: rgba(168, 85, 247, 0.6) !important;
        color: #FFFFFF !important;
    }
    
    /* AI Badge & Header Styling */
    .ai-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(168, 85, 247, 0.2) 100%);
        border: 1px solid rgba(168, 85, 247, 0.4);
        box-shadow: 0 0 15px rgba(99, 102, 241, 0.2);
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 700;
        color: #C084FC;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 0.75rem;
    }
    
    .main-header-title {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #FFFFFF 0%, #A5B4FC 50%, #C084FC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.03em;
        margin: 0 0 0.25rem 0;
    }
    
    .main-header-sub {
        color: #9CA3AF;
        font-size: 0.95rem;
        font-weight: 400;
        margin-bottom: 1.75rem;
    }
    
    /* Glassmorphism Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(13, 18, 28, 0.85) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    [data-testid="stSidebar"] h3 {
        font-size: 0.75rem;
        font-weight: 700;
        color: #818CF8;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.75rem;
    }
    
    /* Glass File Uploader */
    [data-testid="stFileUploader"] {
        border: 1px dashed rgba(99, 102, 241, 0.4);
        border-radius: 14px;
        padding: 1.25rem;
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(10px);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: rgba(168, 85, 247, 0.7);
        background: rgba(99, 102, 241, 0.05);
        box-shadow: 0 0 20px rgba(99, 102, 241, 0.15);
    }
    
    /* Glass Stat Cards */
    .stat-container {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(12px);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        transition: all 0.25s;
    }
    
    .stat-container:hover {
        border-color: rgba(129, 140, 248, 0.4);
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    
    .stat-number {
        background: linear-gradient(135deg, #818CF8 0%, #C084FC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 1.65rem;
        display: block;
    }
    
    .stat-label {
        color: #9CA3AF;
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-top: 0.25rem;
    }
    
    /* Glowing Citation Badges */
    .citation-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(99, 102, 241, 0.12);
        border: 1px solid rgba(129, 140, 248, 0.35);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25);
        border-radius: 8px;
        padding: 0.3rem 0.75rem;
        font-size: 0.78rem;
        font-weight: 500;
        color: #C7D2FE;
        margin-right: 0.45rem;
        margin-top: 0.45rem;
        transition: all 0.2s;
    }
    
    .citation-badge:hover {
        background: rgba(168, 85, 247, 0.25);
        border-color: rgba(168, 85, 247, 0.6);
        color: #FFFFFF;
        transform: translateY(-1px);
    }
    
    /* Modern Glass Buttons */
    .stButton > button {
        background: rgba(255, 255, 255, 0.04);
        color: #E5E7EB;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 10px;
        padding: 0.6rem 1.2rem;
        font-size: 0.85rem;
        font-weight: 600;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.3) 0%, rgba(168, 85, 247, 0.3) 100%);
        border-color: rgba(168, 85, 247, 0.5);
        color: #FFFFFF;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.25);
    }
    
    /* Chat Messages */
    .stChatMessage {
        background: transparent;
        padding: 1.5rem 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.04);
    }
    
    .stChatMessage[data-testid*="assistant"] {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 16px;
        padding: 1.25rem 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.06);
        margin-bottom: 1rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }
    
    [data-testid="chatAvatarIcon-user"] {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
    }
    
    [data-testid="chatAvatarIcon-assistant"] {
        background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%);
    }
    
    /* Glowing Inputs */
    .stChatInputContainer {
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        padding-top: 1.25rem;
        background: #0B0F17;
    }
    
    .stChatInputContainer textarea {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 14px;
        color: #F3F4F6;
        font-size: 0.95rem;
        padding: 0.875rem 1.25rem;
        transition: all 0.25s;
    }
    
    .stChatInputContainer textarea:focus {
        border-color: #818CF8;
        box-shadow: 0 0 22px rgba(99, 102, 241, 0.35);
        background: rgba(255, 255, 255, 0.05);
    }
</style>
""", unsafe_allow_html=True)

# --- AI BRANDING HEADER ---
st.markdown("""
<div class="ai-badge">✦ AI Multimodal RAG Engine</div>
<h1 class="main-header-title">Nexus Multimodal Search</h1>
<div class="main-header-sub">Hybrid BM25 + FAISS Cosine RAG Search across PDFs, Spreadsheets, Voice Notes, Images & Web URLs</div>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### Upload Sources")
    
    uploaded_files = st.file_uploader(
        "Upload files",
        type=["pdf", "csv", "xlsx", "png", "jpg", "jpeg", "webp", "mp3", "wav", "m4a", "ogg"],
        accept_multiple_files=True,
        help="Upload PDFs, Spreadsheets (CSV/Excel), Images, or Audio"
    )
    
    st.markdown("---")
    st.markdown("### Web URL Ingestion")
    web_url_input = st.text_input("Index Web URL", placeholder="https://example.com/docs")
    fetch_url_btn = st.button("Fetch & Index URL", use_container_width=True)
    
    if fetch_url_btn and web_url_input.strip():
        with st.spinner("Scraping and indexing Web URL..."):
            url_chunks = backend.scrape_web_url_chunks(web_url_input.strip())
            if "extra_chunks" not in st.session_state:
                st.session_state.extra_chunks = []
            st.session_state.extra_chunks.extend(url_chunks)
            
            files = uploaded_files or []
            index, bm25, embedder, chunks, count, _ = backend.process_documents(files, extra_chunks=st.session_state.extra_chunks)
            st.session_state.index = index
            st.session_state.bm25 = bm25
            st.session_state.embedder = embedder
            st.session_state.chunks = chunks
            st.success(f"Indexed URL successfully! Added {len(url_chunks)} web chunks.")
    
    # Stats
    if "processed_files" in st.session_state or "extra_chunks" in st.session_state:
        st.markdown("---")
        
        proc_files = st.session_state.get("processed_files", [])
        file_count = len(proc_files)
        chunk_count = len(st.session_state.chunks) if "chunks" in st.session_state else 0
        
        pdf_cnt = sum(1 for f in proc_files if f.lower().endswith(".pdf"))
        sheet_cnt = sum(1 for f in proc_files if f.lower().endswith(".csv") or f.lower().endswith(".xlsx"))
        img_cnt = sum(1 for f in proc_files if any(f.lower().endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".webp"]))
        audio_cnt = sum(1 for f in proc_files if any(f.lower().endswith(ext) for ext in [".mp3", ".wav", ".m4a", ".ogg"]))
        web_cnt = len(st.session_state.get("extra_chunks", []))
        
        st.markdown(f"""
        <div class="stat-container">
            <span class="stat-number">{file_count + (1 if web_cnt else 0)}</span>
            <div class="stat-label">Files Indexed ({pdf_cnt} 📄 | {sheet_cnt} 📊 | {audio_cnt} 🎙️ | {img_cnt} 🖼️ | {1 if web_cnt else 0} 🌐)</div>
        </div>
        <div class="stat-container">
            <span class="stat-number">{chunk_count}</span>
            <div class="stat-label">Hybrid Vector Chunks</div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("Indexed Sources"):
            for i, filename in enumerate(proc_files, 1):
                ext = os.path.splitext(filename)[1].lower()
                icon = "📄" if ext == ".pdf" else ("📊" if ext in [".csv", ".xlsx"] else ("🎙️" if ext in [".mp3", ".wav", ".m4a", ".ogg"] else "🖼️"))
                st.markdown(f"`{i}.` {icon} {filename}")
            if web_cnt:
                st.markdown(f"`•` 🌐 Web URL Content")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    with col2:
        if st.button("Clear Cache", use_container_width=True):
            backend.clear_disk_cache()
            for key in ["processed_files", "index", "chunks", "bm25", "extra_chunks"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.toast("Disk cache cleared!")
            st.rerun()

# --- PROCESS DOCUMENTS ---
process_now = False
if uploaded_files:
    current_files = [f.name for f in uploaded_files]
    if "processed_files" not in st.session_state or st.session_state.processed_files != current_files:
        process_now = True

if process_now:
    with st.spinner("Processing sources (Building BM25 + FAISS Hybrid Index)..."):
        try:
            extra = st.session_state.get("extra_chunks")
            index, bm25, embedder, chunks, file_count, is_cached = backend.process_documents(uploaded_files, extra_chunks=extra)
            
            st.session_state.index = index
            st.session_state.bm25 = bm25
            st.session_state.embedder = embedder
            st.session_state.chunks = chunks
            st.session_state.processed_files = current_files
            
            if is_cached:
                st.info(f"Loaded {file_count} file{'s' if file_count != 1 else ''} from disk cache ⚡")
            else:
                st.success(f"Indexed {file_count} file{'s' if file_count != 1 else ''} (Hybrid Search Active)")
        except Exception as e:
            st.error(f"Error processing documents: {str(e)}")

# --- CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome message
if not st.session_state.messages and ("processed_files" in st.session_state or "extra_chunks" in st.session_state):
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hello! I've indexed your sources using **Hybrid BM25 + FAISS Search**. Ask me anything across your PDFs, Spreadsheets, Voice Notes, Images, or Web URLs!",
        "citations": []
    })

# Display messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("citations"):
            st.markdown("**Sources Referenced:**")
            badges_html = ""
            for cit in message["citations"]:
                ctype = cit.get("type")
                icon = "📄" if ctype == "pdf" else ("📊" if ctype == "spreadsheet" else ("🎙️" if ctype == "audio" else ("🖼️" if ctype == "image" else "🌐")))
                page_str = f"Page {cit['page']}" if isinstance(cit['page'], int) else str(cit['page'])
                badges_html += f'<span class="citation-badge">{icon} {cit["source"]} ({page_str})</span>'
            st.markdown(badges_html, unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Ask about your PDFs, spreadsheets, voice notes, images, or web URLs..."):
    st.session_state.messages.append({"role": "user", "content": prompt, "citations": []})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        if "index" in st.session_state:
            context, citations = backend.hybrid_search_index(
                prompt,
                st.session_state.index,
                st.session_state.get("bm25"),
                st.session_state.embedder,
                st.session_state.chunks
            )
            
            full_response = st.write_stream(backend.generate_answer_stream(prompt, context))
            
            if citations:
                st.markdown("**Sources Referenced:**")
                badges_html = ""
                for cit in citations:
                    ctype = cit.get("type")
                    icon = "📄" if ctype == "pdf" else ("📊" if ctype == "spreadsheet" else ("🎙️" if ctype == "audio" else ("🖼️" if ctype == "image" else "🌐")))
                    page_str = f"Page {cit['page']}" if isinstance(cit['page'], int) else str(cit['page'])
                    badges_html += f'<span class="citation-badge">{icon} {cit["source"]} ({page_str})</span>'
                st.markdown(badges_html, unsafe_allow_html=True)
                
            st.session_state.messages.append({
                "role": "assistant",
                "content": full_response,
                "citations": citations
            })
        else:
            msg = "Please upload files or index a Web URL to get started."
            st.markdown(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg, "citations": []})

# Empty state
if not uploaded_files and "extra_chunks" not in st.session_state:
    st.info("Upload PDFs, Spreadsheets (CSV/Excel), Voice Notes, Images, or enter a Web URL to begin hybrid searching")