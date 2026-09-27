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

# --- FUTURISTIC AI GLASSMORPHISM THEME (LIGHT & DARK BROWSER PROOF) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Force App Background Regardless of Browser Theme */
    .stApp, [data-testid="stAppViewContainer"] {
        background-color: #0B0F17 !important;
        background-image: 
            radial-gradient(circle at 15% 15%, rgba(99, 102, 241, 0.15) 0%, transparent 45%),
            radial-gradient(circle at 85% 85%, rgba(168, 85, 247, 0.12) 0%, transparent 45%) !important;
        color: #F3F4F6 !important;
    }
    
    .main .block-container {
        padding: 2.5rem 2rem 3rem 2rem;
        max-width: 900px;
    }
    
    #MainMenu, footer {visibility: hidden;}
    
    [data-testid="stHeader"] {
        background: transparent !important;
    }
    
    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapseButton"],
    button[kind="header"] {
        color: #818CF8 !important;
        background: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 8px !important;
        backdrop-filter: blur(10px) !important;
        visibility: visible !important;
        z-index: 999999 !important;
    }
    
    /* AI Badge & Header Styling */
    .ai-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.25) 0%, rgba(168, 85, 247, 0.25) 100%);
        border: 1px solid rgba(168, 85, 247, 0.5);
        box-shadow: 0 0 15px rgba(99, 102, 241, 0.25);
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 700;
        color: #D8B4FE !important;
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
        color: #9CA3AF !important;
        font-size: 0.95rem;
        font-weight: 400;
        margin-bottom: 1.75rem;
    }
    
    /* Glassmorphism Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0E131F !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {
        color: #E5E7EB !important;
    }
    
    [data-testid="stSidebar"] h3 {
        font-size: 0.78rem;
        font-weight: 700;
        color: #818CF8 !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.75rem;
    }
    
    /* High Contrast Inputs & Text Areas (Light Mode Proof) */
    input, textarea, [data-testid="stChatInput"] textarea, .stChatInputContainer textarea {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        background-color: #161D2F !important;
        border: 1px solid rgba(129, 140, 248, 0.4) !important;
        border-radius: 12px !important;
        font-size: 0.95rem !important;
        opacity: 1 !important;
    }
    
    input:focus, textarea:focus, [data-testid="stChatInput"] textarea:focus {
        border-color: #A855F7 !important;
        box-shadow: 0 0 20px rgba(168, 85, 247, 0.35) !important;
        background-color: #1C253B !important;
    }
    
    ::placeholder, textarea::placeholder, input::placeholder {
        color: #9CA3AF !important;
        -webkit-text-fill-color: #9CA3AF !important;
        opacity: 1 !important;
    }
    
    /* File Uploader Container */
    [data-testid="stFileUploader"] {
        border: 1.5px dashed #4F46E5 !important;
        border-radius: 14px !important;
        padding: 1.25rem !important;
        background: #141A29 !important;
    }
    
    [data-testid="stFileUploader"] label {
        color: #F3F4F6 !important;
    }
    
    /* Glass Stat Cards */
    .stat-container {
        background: #141A29 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.75rem;
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
        color: #9CA3AF !important;
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
        background: rgba(99, 102, 241, 0.2) !important;
        border: 1px solid rgba(129, 140, 248, 0.4) !important;
        border-radius: 8px;
        padding: 0.3rem 0.75rem;
        font-size: 0.78rem;
        font-weight: 600;
        color: #E0E7FF !important;
        margin-right: 0.45rem;
        margin-top: 0.45rem;
    }
    
    /* Modern Glass Buttons */
    .stButton > button {
        background: #1E293B !important;
        color: #F8FAFC !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 10px !important;
        padding: 0.6rem 1.2rem !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%) !important;
        border-color: #A855F7 !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.35) !important;
    }
    
    /* Chat Messages */
    .stChatMessage {
        background: transparent !important;
        padding: 1.5rem 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06) !important;
    }
    
    .stChatMessage[data-testid*="assistant"] {
        background: #131A29 !important;
        border-radius: 16px !important;
        padding: 1.25rem 1.5rem !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        margin-bottom: 1rem !important;
    }
    
    [data-testid="stChatMessageContent"] {
        color: #F3F4F6 !important;
    }
    
    [data-testid="stChatMessageContent"] p {
        color: #F3F4F6 !important;
    }
    
    [data-testid="chatAvatarIcon-user"] {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%) !important;
    }
    
    [data-testid="chatAvatarIcon-assistant"] {
        background: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%) !important;
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
