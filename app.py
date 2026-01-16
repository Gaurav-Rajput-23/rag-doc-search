import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Doc Search", layout="wide")
st.title("RAG based doc search ")

# --- LOAD SECRETS ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except KeyError:
    st.error("API Key not found! Please check .streamlit/secrets.toml")
    st.stop()

# --- CONFIGURE GOOGLE AI ---
genai.configure(api_key=api_key)
model = genai.GenerativeModel('models/gemini-2.5-flash')

# --- MAIN APP ---
st.write("### Chat Interface")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# 1. Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 2. Chat Input 
if user_input := st.chat_input("Ask a question about your PDF..."):
    
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    #  A SEARCH MEMORY (RAG) ---
    context_text = ""
    if "index" in st.session_state and "docs" in st.session_state and "embedder" in st.session_state:
        st.write("Entering Rag searching mode ")
        #convert user question to Vector
        query_vector = st.session_state.embedder.encode([user_input])
        
        # Search the ind for  top 3 similar chunks
        D, I = st.session_state.index.search(query_vector, k=3)
        
        #taking the text ofchunks
        retrieved_chunks = [st.session_state.docs[i] for i in I[0]] 
        
        #chuck in string 
        context_text = "\n\n".join(retrieved_chunks)
        
        # what we found 
        with st.expander(" Source Material"):
            st.write(context_text)
    else:
        st.warning("Please upload a PDF first to enable RAG search.")

    #  B-genarating ans -
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # promt here 
            if context_text:
                prompt = f"""
                You are a helpful assistant. 
                Answer the user's question using ONLY the context provided below.
                If the answer is not in the context, say "I don't know based on the document."
                
                CONTEXT:
                {context_text}
                
                QUESTION:
                {user_input}
                
                ANSWER:
                """
            else:
                prompt = user_input # Just chat normally if no PDF

            response = model.generate_content(prompt)
            ai_reply = response.text
            message_placeholder.markdown(ai_reply)
            
        except Exception as e:
            ai_reply = f"Error: {str(e)}"
            message_placeholder.markdown(ai_reply)

    # 4. Save assistant message
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})

# ---pdf prossesing section ---
st.markdown("---")
st.subheader(" Doc Loader")
uploaded_file = st.file_uploader("Upload a PDF to process", type=["pdf"])

if uploaded_file is not None:
    # -Checking if we already processed this exact file ---
    current_file_name = uploaded_file.name
    
    # Check if we processed a file AND if it's the same filename
    if "processed_file_name" not in st.session_state or st.session_state.processed_file_name != current_file_name:
        
        # Only run this if it's a new file
        st.write(f"Processing {current_file_name} for the first time...")
        
        reader = PdfReader(uploaded_file)
        full_text = ""
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                full_text += text + "\n"
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_text(full_text)
        
        st.session_state.docs = chunks
        
        with st.spinner("Creating Memory (Embeddings)..."):
            embedder = SentenceTransformer('all-MiniLM-L6-v2')
            vectors = embedder.encode(chunks)
            dimension = vectors.shape[1]
            index = faiss.IndexFlatL2(dimension)
            index.add(vectors)
            
            st.session_state.index = index
            st.session_state.embedder = embedder

        # we processed this file
        st.session_state.processed_file_name = current_file_name

        st.success("Document Indexed Successfully!")
        st.info(f"Created {len(chunks)} vectors.")
    else:
        st.info(f" done '{current_file_name}' is already loaded. No re-indexing needed.")

