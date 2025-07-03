from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import requests
import json
import uuid
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="AI Assistant Pro - RAG & Memory",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #1f77b4;
        --secondary-color: #ff7f0e;
        --success-color: #2ca02c;
        --warning-color: #ff9800;
        --error-color: #d62728;
        --background-color: #f8f9fa;
        --text-color: #2c3e50;
    }

    /* Hide Streamlit branding */
    MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    html, body, [class*="css"] {
        font-family: var(--font-main);
    }

    #MainMenu, header, footer {
        visibility: hidden;
    }

    /* Custom header styling */
    .main-header {
        background: linear-gradient(90deg, #1f77b4 0%, #2ca02c 100%);
        padding: 1rem 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.9;
    }

    .chat-message {
        background: var(--card-bg-color);
        padding: 1rem;
        border-radius: var(--border-radius);
        box-shadow: 0 2px 6px var(--shadow-color);
        margin-bottom: 1rem;
    }

    .user-message {
        border-left: 6px solid var(--primary-color);
    }

    .assistant-message {
        border-left: 6px solid var(--secondary-color);
    }

    .stButton > button {
        background-color: var(--primary-color);
        color: white;
        font-weight: bold;
        border-radius: 6px;
        transition: transform 0.2s, box-shadow 0.2s;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px var(--shadow-color);
    }

    .sidebar-section {
        background: var(--card-bg-color);
        padding: 1rem;
        border-radius: var(--border-radius);
        margin: 1rem 0;
        box-shadow: 0 2px 6px var(--shadow-color);
    }

    .upload-area {
        border: 2px dashed var(--primary-color);
        border-radius: var(--border-radius);
        padding: 2rem;
        text-align: center;
        background: #f0f8ff;
        transition: background 0.3s;
    }

    .upload-area:hover {
        background: #e6f2ff;
    }

    .metric-card {
        background: var(--card-bg-color);
        padding: 1rem;
        border-radius: var(--border-radius);
        border-left: 5px solid var(--accent-color);
        box-shadow: 0 2px 6px var(--shadow-color);
        margin: 0.5rem 0;
    }

    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
    }

    .status-online { background-color: #2ecc71; }
    .status-offline { background-color: #e74c3c; }
    .status-processing { background-color: #f1c40f; }

    .progress-container {
        background: #eee;
        border-radius: var(--border-radius);
        padding: 0.5rem;
        margin: 1rem 0;
        box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    .stMetricValue, .stMetricLabel {
        text-align: center;
    }

    textarea, input, .stTextInput input, .stTextArea textarea {
        border-radius: var(--border-radius);
        border: 1px solid #d1d5db;
        padding: 0.6rem 1rem;
        font-size: 1rem;
    }

    .stExpanderContent {
        padding: 1rem 0;
    }

    .block-container {
        padding: 2rem 3rem;
    }

    .stColumns > div {
        padding: 0 0.75rem;
    }

    .chat-box {
        margin-bottom: 1.5rem;
        background: white;
        padding: 1rem;
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-light);
    }
    
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if 'user_id' not in st.session_state:
    st.session_state.user_id = "default"
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'uploaded_documents' not in st.session_state:
    st.session_state.uploaded_documents = []

# Professional header
st.markdown("""
<div class="main-header">
    <h1>🤖 AI Assistant Pro</h1>
    <p>Advanced RAG-powered AI with Memory & Document Intelligence</p>
</div>
""", unsafe_allow_html=True)

# st.title("🤖 Enhanced AI Chatbot with RAG & Memory")
# st.write("Upload PDFs, maintain conversation history, and get intelligent responses!")

# API Configuration
API_URL = "http://127.0.0.1:9999"

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")

    # User & Session Management
    st.subheader("👤 User & Session")
    user_id = st.text_input("User ID:", value=st.session_state.user_id, key="user_id_input")
    if user_id != st.session_state.user_id:
        st.session_state.user_id = user_id

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 New Session"):
            st.session_state.session_id = str(uuid.uuid4())
            st.session_state.chat_history = []
            st.rerun()

    with col2:
        if st.button("🗑️ Clear History"):
            try:
                response = requests.post(f"{API_URL}/clear-history",
                                         json={"session_id": st.session_state.session_id})
                if response.status_code == 200:
                    st.session_state.chat_history = []
                    st.success("History cleared!")
                else:
                    st.error("Failed to clear history")
            except Exception as e:
                st.error(f"Error: {str(e)}")

    # st.write(f"**Session ID:** `{st.session_state.session_id[:8]}...`")

    # Model Configuration
    st.subheader("🧠 Model Settings")
    MODEL_NAMES_GROQ = ["llama-3.3-70b-versatile", "llama3-70b-8192"]
    MODEL_NAMES_OPENAI = ["gpt-4o-mini"]

    provider = st.radio("Select Provider:", ("Groq", "OpenAI"))

    if provider == "Groq":
        selected_model = st.selectbox("Select Groq Model:", MODEL_NAMES_GROQ)
    elif provider == "OpenAI":
        selected_model = st.selectbox("Select OpenAI Model:", MODEL_NAMES_OPENAI)

    # Agent Configuration
    st.subheader("🎯 Agent Settings")
    allow_web_search = st.checkbox("🔍 Allow Web Search", value=True)
    similarity_threshold = st.slider(
        "📊 RAG Similarity Threshold",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.1,
        help="Higher values = more strict document matching"
    )

    # Document Management
    st.subheader("📚 Document Management")

    # PDF Upload
    uploaded_file = st.file_uploader("Upload PDF", type=['pdf'])

    if uploaded_file is not None:
        if st.button("📤 Process PDF"):
            with st.spinner("Processing PDF..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    data = {"user_id": st.session_state.user_id}
                    response = requests.post(f"{API_URL}/upload-pdf", files=files, data=data)

                    if response.status_code == 200:
                        result = response.json()
                        st.success(f"✅ {result['message']}")
                        st.session_state.uploaded_documents.append(uploaded_file.name)
                    else:
                        error_detail = response.json().get('detail', 'Unknown error')
                        st.error(f"❌ Upload failed: {error_detail}")
                except Exception as e:
                    st.error(f"❌ Error uploading PDF: {str(e)}")

    if st.button("📋 Refresh Documents"):
        try:
            response = requests.post(f"{API_URL}/user-documents",
                                     json={"user_id": st.session_state.user_id})
            if response.status_code == 200:
                result = response.json()
                st.session_state.uploaded_documents = result.get('documents', [])
        except Exception as e:
            st.error(f"Error fetching documents: {str(e)}")

    if st.session_state.uploaded_documents:
        st.write("**📄 Your Documents:**")
        for doc in st.session_state.uploaded_documents:
            st.write(f"• {doc}")
    else:
        st.write("*No documents uploaded yet*")

# Main Chat Interface
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💬 Chat Interface")

    # System Prompt
    system_prompt = st.text_area(
        "🎭 Define your AI Agent:",
        height=100,
        placeholder="You are a helpful AI assistant with access to uploaded documents and web search...",
        value="You are a helpful AI assistant. You can answer questions using uploaded documents or general knowledge. Be clear about your sources."
    )

    # Chat Input
    user_query = st.text_area(
        "💭 Enter your query:",
        height=120,
        placeholder="Ask anything! I can use your uploaded documents or search the web..."
    )

    if st.button("🚀 Ask Agent!", type="primary"):
        if user_query.strip():
            with st.spinner("🤔 Agent is thinking..."):
                payload = {
                    "model_name": selected_model,
                    "model_provider": provider,
                    "system_prompt": system_prompt,
                    "messages": [user_query],
                    "allow_search": allow_web_search,
                    "user_id": st.session_state.user_id,
                    "session_id": st.session_state.session_id,
                    "similarity_threshold": similarity_threshold
                }

                try:
                    response = requests.post(f"{API_URL}/chat", json=payload)
                    if response.status_code == 200:
                        data = response.json()
                        if "error" in data:
                            st.error(f"❌ {data['error']}")
                        else:
                            st.session_state.chat_history.append({
                                "timestamp": datetime.now().strftime("%H:%M:%S"),
                                "user": user_query,
                                "assistant": data['response'],
                                "session_id": data.get('session_id', st.session_state.session_id)
                            })
                            st.rerun()
                    else:
                        st.error("❌ Error: Could not get response from backend.")
                except Exception as e:
                    st.error(f"❌ Exception: {str(e)}")
        else:
            st.warning("⚠️ Please enter a query!")

with col2:
    st.subheader("📜 Chat History")

    if st.button("🔄 Load History"):
        try:
            response = requests.post(f"{API_URL}/chat-history",
                                     json={"session_id": st.session_state.session_id})
            if response.status_code == 200:
                result = response.json()
                history = result.get('history', [])
                st.session_state.chat_history = []

                for i in range(0, len(history), 2):
                    if i + 1 < len(history):
                        user_msg = history[i]
                        ai_msg = history[i + 1]
                        if user_msg.get('type') == 'human' and ai_msg.get('type') == 'ai':
                            st.session_state.chat_history.append({
                                "timestamp": user_msg.get('timestamp', ''),
                                "user": user_msg.get('content', ''),
                                "assistant": ai_msg.get('content', ''),
                                "session_id": st.session_state.session_id
                            })
        except Exception as e:
            st.error(f"Error loading history: {str(e)}")

    if st.session_state.chat_history:
        for i, chat in enumerate(reversed(st.session_state.chat_history[-10:])):
            with st.expander(f"💬 Chat {len(st.session_state.chat_history) - i} - {chat['timestamp']}",
                             expanded=(i == 0)):
                st.write("**👤 You:**")
                st.write(chat['user'])
                st.write("**🤖 Assistant:**")
                st.write(chat['assistant'])
    else:
        st.info("💡 No chat history yet. Start a conversation!")

    # Session Info
    st.divider()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("👤 User ID", st.session_state.user_id)
    # with col2:
    #     st.metric("💬 Session", f"{st.session_state.session_id[:8]}...")
    with col3:
        st.metric("📚 Documents", len(st.session_state.uploaded_documents))

    # Tips & Debug
    with st.expander("🔧 Advanced Features & Tips"):
        st.markdown("""
        ### 🌟 Features Available:

        **1. 🧠 Memory & Context**
        - Maintains conversation history across sessions
        - Context-aware responses based on previous interactions

        **2. 📚 RAG (Retrieval-Augmented Generation)**
        - Upload PDFs and ask questions about their content
        - Smart document retrieval using Cohere embeddings
        - Automatic reranking for better relevance

        **3. 🎯 Smart Answer Switching**
        - Automatically chooses between document content and general knowledge
        - Adjustable similarity threshold for fine-tuning

        **4. 🔍 Web Search Integration**
        - Falls back to web search for questions outside document scope
        - Powered by Tavily Search API

        **5. 🤖 Multiple AI Providers**
        - Groq: Fast inference with Llama and Mixtral models
        - OpenAI: GPT-4o-mini for high-quality responses

        ### 💡 Tips for Best Results:

        **For Document Questions:**
        - Upload relevant PDFs first
        - Use specific questions about document content
        - Lower similarity threshold (0.3-0.5) for broader matching

        **For General Questions:**
        - Higher similarity threshold (0.7-0.9) to avoid document interference
        - Enable web search for current information

        **For Conversations:**
        - Use the same session ID to maintain context
        - System prompts help define agent behavior
        """)

    if st.checkbox("🐛 Show Debug Info"):
        st.subheader("Debug Information")
        st.json({
            # "session_id": st.session_state.session_id,
            "user_id": st.session_state.user_id,
            "chat_history_length": len(st.session_state.chat_history),
            "uploaded_documents": st.session_state.uploaded_documents,
            "selected_model": selected_model,
            "provider": provider,
            "similarity_threshold": similarity_threshold,
            "allow_web_search": allow_web_search
        })

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🤖 <strong>AI Assistant Pro</strong> | Powered by RAG Technology & Advanced Memory Systems</p>
    <p><small>Built with Streamlit • Enhanced with Professional UI/UX</small></p>
</div>
""", unsafe_allow_html=True)


