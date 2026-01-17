import streamlit as st
import backend as backend

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="AI Document Search",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- DARK THEME INSPIRED BY CLAUDE/CHATGPT ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Dark background */
    .stApp {
        background-color: #212121;
    }
    
    .main .block-container {
        padding: 2rem 2rem 2rem 2rem;
        max-width: 850px;
    }
    
    /* Hide streamlit elements */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Headers */
    h1 {
        font-size: 1.75rem;
        font-weight: 600;
        color: #ececec;
        margin-bottom: 0.25rem;
        letter-spacing: -0.02em;
    }
    
    /* Sidebar - dark */
    [data-testid="stSidebar"] {
        background-color: #171717;
        border-right: 1px solid #2d2d2d;
        padding-top: 1.5rem;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding: 0 1.25rem;
    }
    
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        font-size: 0.8rem;
        font-weight: 600;
        color: #a0a0a0;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 1rem;
    }
    
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label {
        color: #b0b0b0;
        font-size: 0.875rem;
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        border: 1.5px dashed #404040;
        border-radius: 10px;
        padding: 1.25rem;
        background: #1a1a1a;
        transition: all 0.2s;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #505050;
        background: #1f1f1f;
    }
    
    [data-testid="stFileUploader"] label {
        color: #d0d0d0;
        font-weight: 500;
    }
    
    /* Chat messages */
    .stChatMessage {
        background-color: transparent;
        padding: 1.75rem 0;
        border-bottom: 1px solid #2d2d2d;
    }
    
    .stChatMessage:last-child {
        border-bottom: none;
    }
    
    /* User message background */
    .stChatMessage[data-testid*="user"] {
        background-color: transparent;
    }
    
    /* Assistant message slight highlight */
    .stChatMessage[data-testid*="assistant"] {
        background-color: #1a1a1a;
    }
    
    /* Avatar styling */
    [data-testid="chatAvatarIcon-user"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="chatAvatarIcon-assistant"] {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    
    /* Message text */
    [data-testid="stChatMessageContent"] {
        color: #ececec;
        font-size: 0.95rem;
        line-height: 1.65;
    }
    
    [data-testid="stChatMessageContent"] p {
        margin-bottom: 0.875rem;
        color: #ececec;
    }
    
    [data-testid="stChatMessageContent"] strong {
        color: #ffffff;
    }
    
    /* Chat input */
    .stChatInputContainer {
        border-top: 1px solid #2d2d2d;
        padding-top: 1.25rem;
        background: #212121;
    }
    
    .stChatInputContainer textarea {
        background-color: #2d2d2d;
        border: 1px solid #404040;
        border-radius: 12px;
        color: #ececec;
        font-size: 0.95rem;
        padding: 0.875rem 1rem;
    }
    
    .stChatInputContainer textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 1px #667eea;
        outline: none;
        background-color: #333333;
    }
    
    .stChatInputContainer textarea::placeholder {
        color: #808080;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #2d2d2d;
        color: #ececec;
        border: 1px solid #404040;
        border-radius: 8px;
        padding: 0.625rem 1.25rem;
        font-size: 0.875rem;
        font-weight: 500;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        background-color: #3a3a3a;
        border-color: #505050;
    }
    
    /* Alert boxes */
    .stAlert {
        background-color: #1a1a1a;
        border: 1px solid #2d2d2d;
        border-radius: 10px;
        padding: 1rem 1.25rem;
        font-size: 0.875rem;
        color: #d0d0d0;
    }
    
    div[data-baseweb="notification"] {
        background-color: #1a3a1a !important;
        border-left: 3px solid #4caf50;
    }
    
    div[data-baseweb="notification"] > div {
        color: #a8e6a8;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-color: #667eea transparent transparent transparent;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #1a1a1a;
        color: #b0b0b0;
        font-size: 0.875rem;
        font-weight: 500;
        border-radius: 6px;
        padding: 0.5rem 0.75rem;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: #252525;
    }
    
    .streamlit-expanderContent {
        background-color: #1a1a1a;
        border: 1px solid #2d2d2d;
        border-top: none;
        color: #b0b0b0;
    }
    
    /* Stats */
    .stat-container {
        background: #1a1a1a;
        border: 1px solid #2d2d2d;
        border-radius: 8px;
        padding: 0.875rem;
        margin-bottom: 0.75rem;
    }
    
    .stat-number {
        color: #ffffff;
        font-weight: 600;
        font-size: 1.5rem;
        display: block;
    }
    
    .stat-label {
        color: #808080;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.25rem;
    }
    
    /* Divider */
    hr {
        border: none;
        border-top: 1px solid #2d2d2d;
        margin: 1.5rem 0;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #171717;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #404040;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #505050;
    }
    
    /* Text selection */
    ::selection {
        background-color: #667eea;
        color: #ffffff;
    }
    
    /* Links */
    a {
        color: #8b9cff;
    }
    
    a:hover {
        color: #a5b4ff;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.title("Document Search")

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### Settings")
    
    uploaded_files = st.file_uploader(
        "Upload documents",
        type=["pdf"],
        accept_multiple_files=True,
        help="Upload PDF files to search"
    )
    
    # Stats
    if "processed_files" in st.session_state:
        st.markdown("---")
        
        file_count = len(st.session_state.processed_files)
        chunk_count = len(st.session_state.chunks) if "chunks" in st.session_state else 0
        
        st.markdown(f"""
        <div class="stat-container">
            <span class="stat-number">{file_count}</span>
            <div class="stat-label">Documents Indexed</div>
        </div>
        <div class="stat-container">
            <span class="stat-number">{chunk_count}</span>
            <div class="stat-label">Text Chunks</div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("Indexed files"):
            for i, filename in enumerate(st.session_state.processed_files, 1):
                st.markdown(f"`{i}.` {filename}")
    
    st.markdown("---")
    
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- PROCESS DOCUMENTS ---
process_now = False
if uploaded_files:
    current_files = [f.name for f in uploaded_files]
    if "processed_files" not in st.session_state or st.session_state.processed_files != current_files:
        process_now = True

if process_now:
    with st.spinner("Processing documents..."):
        try:
            index, embedder, chunks, file_count = backend.process_documents(uploaded_files)
            
            st.session_state.index = index
            st.session_state.embedder = embedder
            st.session_state.chunks = chunks
            st.session_state.processed_files = current_files
            
            st.success(f"Successfully indexed {file_count} document{'s' if file_count != 1 else ''}")
        except Exception as e:
            st.error(f"Error processing documents: {str(e)}")

# --- CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome message
if not st.session_state.messages and "processed_files" in st.session_state:
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hello! I've indexed your documents. Ask me anything about their content."
    })

# Display messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about your documents..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        try:
            if "index" in st.session_state:
                with st.spinner("Searching..."):
                    context = backend.search_index(
                        prompt,
                        st.session_state.index,
                        st.session_state.embedder,
                        st.session_state.chunks
                    )
                    answer = backend.generate_answer(prompt, context)
            else:
                answer = "Please upload PDF documents to get started."
            
            st.markdown(answer)
        except Exception as e:
            answer = f"An error occurred: {str(e)}"
            st.markdown(answer)
    
    st.session_state.messages.append({"role": "assistant", "content": answer})

# Empty state
if not uploaded_files:
    st.info("Upload documents to begin searching")