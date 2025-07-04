# 🤖 Enhanced AI Agent with RAG & Memory

A powerful AI chatbot system with **Retrieval-Augmented Generation (RAG)**, **conversation memory**, **PDF processing**, and **smart answer switching**.

## 🌟 Features

### ✅ **Chat History & Memory**
- Maintains conversation context across multiple turns
- Session-based memory management
- Persistent chat history storage

### ✅ **RAG (Retrieval-Augmented Generation)**
- Upload and process PDF documents
- Cohere embeddings for semantic search
- Automatic document chunking and indexing
- Smart retrieval with reranking

### ✅ **Smart Answer Switching**
- Automatically chooses between:
  - Document-based answers (RAG)
  - General knowledge (LLM)
  - Web search results (Tavily)
- Configurable similarity thresholds

### ✅ **Multiple AI Providers**
- **Groq**: Fast inference (Llama, Mixtral models)
- **OpenAI**: High-quality responses (GPT-4o-mini)

### ✅ **Advanced Tools**
- **Cohere**: Embeddings, reranking, and classification
- **Tavily**: Web search integration
- **FAISS**: Vector storage and similarity search

## 🚀 Quick Start

### 1. **Clone & Setup**
```bash
git clone <your-repo>
cd enhanced-ai-agent
```

### 2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 3. **Configure API Keys**
```bash
cp .env.example .env
# Edit .env with your API keys
```

Required API keys:
- `GROQ_API_KEY` - Get from [Groq Console](https://console.groq.com/)
- `OPENAI_API_KEY` - Get from [OpenAI Platform](https://platform.openai.com/)
- `TAVILY_API_KEY` - Get from [Tavily](https://tavily.com/)
- `COHERE_API_KEY` - Get from [Cohere](https://cohere.ai/)

### 4. **Run the Application**

**Linux/Mac:**
```bash
chmod +x run_enhanced.sh
./run_enhanced.sh
```

**Windows:**
```batch
run_enhanced.bat
```

**Manual Start:**
```bash
# Terminal 1: Backend
python backend_enhanced.py

# Terminal 2: Frontend
streamlit run frontend_enhanced.py
```

## 📖 Usage Guide

### **1. Basic Chat**
1. Open the web interface (usually `http://localhost:8501`)
2. Configure your AI model and provider
3. Enter your system prompt to define agent behavior
4. Start chatting!

### **2. PDF Upload & RAG**
1. Go to the sidebar → "Document Management"
2. Upload a PDF file
3. Click "Process PDF" to index the document
4. Ask questions about the document content
5. The agent will automatically use document context when relevant

### **3. Memory & Sessions**
- Each conversation maintains context automatically
- Use "New Session" to start fresh
- "Clear History" removes conversation memory
- Session IDs help organize different conversations

### **4. Smart Answer Switching**
The agent automatically decides how to answer based on:
- **High similarity to documents** → Uses RAG with document context
- **Low similarity to documents** → Uses general LLM knowledge
- **Web search enabled** → Falls back to web search when needed

Adjust the "RAG Similarity Threshold" to control this behavior:
- **Lower (0.3-0.5)**: More likely to use documents
- **Higher (0.7-0.9)**: More strict document matching

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   AI Services   │
│   (Streamlit)   │◄──►│   (FastAPI)     │◄──►│   (LLM/RAG)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
    ┌────▼────┐             ┌────▼────┐             ┌────▼────┐
    │ Session │             │ Memory  │             │ Vector  │
    │ State   │             │ Manager │             │ Store   │
    └─────────┘             └─────────┘             └─────────┘
```

### **Core Components:**

1. **Frontend (`frontend_enhanced.py`)**
   - Streamlit web interface
   - File upload handling
   - Session management
   - Real-time chat interface

2. **Backend (`backend_enhanced.py`)**
   - FastAPI REST API
   - PDF processing endpoints
   - Memory management APIs
   - CORS support

3. **AI Agent (`ai_agent_enhanced.py`)**
   - LangGraph workflow orchestration
   - RAG implementation with Cohere
   - Memory management
   - Smart routing logic

## 🔧 API Endpoints

### **Chat**
```http
POST /chat
Content-Type: application/json

{
  "model_name": "llama-3.3-70b-versatile",
  "model_provider": "Groq",
  "system_prompt": "You are a helpful assistant...",
  "messages": ["Hello, how are you?"],
  "allow_search": true,
  "user_id": "user123",
  "session_id": "session456",
  "similarity_threshold": 0.5
}
```

### **PDF Upload**
```http
POST /upload-pdf
Content-Type: multipart/form-data

file: <pdf_file>
user_id: "user123"
```

### **Chat History**
```http
POST /chat-history
Content-Type: application/json

{
  "session_id": "session456"
}
```

### **Other Endpoints**
- `POST /clear-history` - Clear session history
- `POST /user-documents` - Get user's uploaded documents
- `GET /health` - Health check
- `GET /` - API information

## ⚙️ Configuration

### **Model Options**

**Groq Models:**
- `llama-3.3-70b-versatile` - Latest Llama model
- `mixtral-8x7b-32768` - Mixtral with large context
- `llama3-70b-8192` - Standard Llama 3

**OpenAI Models:**
- `gpt-4o-mini` - Cost-effective GPT-4

### **RAG Settings**
- **Chunk Size**: 1000 characters
- **Chunk Overlap**: 200 characters
- **Retrieval Count**: 3 documents
- **Reranking**: Cohere rerank for relevance

### **Memory Settings**
- **Session History**: Last 10 messages
- **Storage**: In-memory (can be extended to Redis/DB)

## 🛠️ Customization

### **Adding New LLM Providers**
```python
# In ai_agent_enhanced.py
elif provider == "Anthropic":
    llm = ChatAnthropic(model=llm_id)
```

### **Custom Document Processing**
```python
# Extend RAGManager class
def process_custom_format(self, content, format_type):
    # Add support for Word docs, web pages, etc.
    pass
```

### **Persistent Storage**
```python
# Replace in-memory storage with database
class DatabaseMemoryManager:
    def __init__(self, db_url):
        # SQLAlchemy or MongoDB setup
        pass
```

## 🐛 Troubleshooting

### **Common Issues**

1. **"Module not found" errors**
   ```bash
   pip install -r requirements.txt
   ```

2. **API key errors**
   - Check `.env` file exists and has correct keys
   - Verify API keys are valid and have sufficient credits

3. **PDF processing fails**
   - Ensure PDF is not password-protected
   - Check file size (large PDFs may timeout)

4. **Memory issues with large documents**
   - Reduce chunk size in `RAGManager`
   - Implement document pagination

5. **Slow responses**
   - Try different models (Groq is generally faster)
   - Reduce similarity search results
   - Disable web search for faster responses

### **Debug Mode**
Enable debug information in the frontend to see:
- Session state
- API payloads
- Document processing status

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **LangChain** & **LangGraph** for the agent framework
- **Cohere** for embeddings and reran
