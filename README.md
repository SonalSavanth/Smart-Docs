# Smart Document Manager (No JavaScript Version) 📚

An AI-powered document management system built with **Flask + Jinja2 templates** - NO JavaScript required!

This version combines **CRUD operations**, **RAG (Retrieval-Augmented Generation)**, and **LLM features** using server-side rendering only.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![Gemini](https://img.shields.io/badge/Google-Gemini--2.5-blue.svg)
![No JavaScript](https://img.shields.io/badge/JavaScript-None-red.svg)

## 🌟 Features

### CRUD Operations
- ✅ **Create** - Upload documents with HTML forms
- ✅ **Read** - View documents with server-rendered pages
- ✅ **Update** - Rename and organize documents
- ✅ **Delete** - Remove documents with form submissions

### RAG (Retrieval-Augmented Generation)
- 🔍 **Semantic Search** - Find relevant information across documents
- 💬 **AI Chat** - Ask questions and get answers (no AJAX!)
- 📊 **Source Attribution** - See which documents were used
- 🧠 **Vector Embeddings** - ChromaDB for fast retrieval

### LLM Features
- 📝 **Auto-Summarization** - AI generates summaries on upload
- 🏷️ **Smart Tagging** - Automatic tag suggestions
- 🌍 **Translation** - Translate documents to different languages
- 💡 **Context-Aware** - All AI features understand content

## 💡 Why No JavaScript?

**Simpler Development:**
- ✅ Only need to know Python + HTML
- ✅ No API layer needed
- ✅ Fewer files to manage
- ✅ Traditional web development approach

**How It Works:**
- HTML forms submit data to Flask
- Flask processes and returns new HTML page
- Jinja2 templates render dynamic content
- No AJAX, no fetch(), no JSON parsing

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│  Browser                            │
│  - HTML Forms                       │
│  - Server-rendered pages            │
└─────────────────────────────────────┘
                ↓
         HTTP Form Submission
                ↓
┌─────────────────────────────────────┐
│  Flask (Jinja2 Templates)           │
│  - Process forms                    │
│  - Render HTML                      │
│  - Return complete pages            │
└─────────────────────────────────────┘
         ↓              ↓
┌──────────────┐  ┌─────────────────┐
│ PostgreSQL   │  │ ChromaDB        │
│ - Users      │  │ - Embeddings    │
│ - Documents  │  │ - Vector Search │
│ - Folders    │  │                 │
│ - Chat Logs  │  │                 │
└──────────────┘  └─────────────────┘
         ↓
┌─────────────────────────────────────┐
│  Google Gemini API                  │
│  - Gemini 2.5 Flash for text gen    │
│  - gemini-embedding-001 for vectors │
└─────────────────────────────────────┘
```

## 📋 Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))

## 🚀 Quick Start

### 1. Set Up PostgreSQL

```bash
# Create database
createdb smart_docs
```

### 2. Install Python Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install packages
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit with your settings
nano .env
```

Update `.env`:
```env
DATABASE_URL=postgresql://your_user:your_password@localhost/smart_docs
GEMINI_API_KEY=your-gemini-api-key-here
SECRET_KEY=your-random-secret-key-here
```

### 4. Run the Application

```bash
python app.py
```

Open browser: **http://localhost:5000**

## 📖 Usage Guide

### Uploading Documents

1. Go to the homepage
2. Click "Choose File" and select a PDF, TXT, or DOCX file
3. Check/uncheck auto-summarize and auto-tag options
4. Click "Upload & Analyze"
5. Page reloads with your new document

### Asking Questions (RAG)

1. Click "💬 Chat" in the navigation
2. Type your question in the text area
3. Click "Send"
4. Page reloads with AI answer and sources

### Managing Documents

- **View Details** - Click "View" button on any document
- **Delete** - Click "Delete" button (confirms before deleting)
- **Translate** - Click "Translate" on document detail page

## 📁 Project Structure

```
smart-docs-no-js/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── database.py            # Database setup (Gemini embeddings)
├── models.py              # SQLAlchemy models
├── crud.py                # CRUD operations
├── rag.py                 # RAG logic (Gemini 2.5 Flash)
├── llm.py                 # LLM utilities (Gemini 2.5 Flash)
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── templates/            # Jinja2 templates
│   ├── base.html         # Base template
│   ├── index.html        # Main dashboard
│   ├── chat.html         # Chat page
│   ├── document_detail.html
│   ├── translate_form.html
│   ├── translate_result.html
│   ├── 404.html
│   └── 500.html
├── uploads/              # Uploaded documents (auto-created)
└── chroma_db/            # Vector database (auto-created)
```

## 🔧 How Forms Work

### Upload Form
```html
<form action="/upload" method="POST" enctype="multipart/form-data">
    <input type="file" name="file">
    <input type="checkbox" name="auto_summarize">
    <button type="submit">Upload</button>
</form>
```

Flask receives the form data and processes it directly.

### Chat Form
```html
<form action="/chat/ask" method="POST">
    <textarea name="question"></textarea>
    <button type="submit">Ask</button>
</form>
```

Question is sent to Flask, which queries the AI and returns the answer in a new page.

## 🎯 Key Differences from JavaScript Version

| Feature | With JavaScript | Without JavaScript (This) |
|---------|----------------|---------------------------|
| **Page Updates** | Dynamic (AJAX) | Full page reload |
| **Form Handling** | fetch() API | Traditional POST |
| **Code Files** | HTML + CSS + JS + Python | HTML + CSS + Python only |
| **Complexity** | Higher | Lower |
| **Learning Curve** | Need JS + Python | Just Python + HTML |
| **User Experience** | Smoother (no reload) | Traditional (reloads) |

## 🤖 AI Models Used

| Component | Model | Purpose |
|-----------|-------|---------|
| Text Generation | `models/gemini-2.5-flash` | Summaries, tags, chat, translation |
| Embeddings | `models/gemini-embedding-001` | Vector search for RAG |

## 🐛 Troubleshooting

### Database Connection Error
```
Error: could not connect to server
```
**Solution:** Ensure PostgreSQL is running and DATABASE_URL is correct

### Gemini API Error
```
Error: 404 models/... is not found
```
**Solution:** 
1. Check your GEMINI_API_KEY in .env file
2. Verify you're using correct model names:
   - Text: `models/gemini-2.5-flash`
   - Embeddings: `models/gemini-embedding-001`
3. Run `python check_models.py` to see available models

### Secret Key Warning
```
WARNING: Using default secret key
```
**Solution:** Set a random SECRET_KEY in .env (important for production!)

### File Type Error
```
DataError: value too long for type character varying(50)
```
**Solution:** Make sure `models.py` has `file_type = db.Column(db.String(150))`

### Form Not Submitting
**Solution:** Check that method="POST" is set on the form tag

## 🚀 Deployment

### Production Checklist

1. ✅ Use a production WSGI server (Gunicorn)
2. ✅ Set `debug=False` in app.py
3. ✅ Generate a strong SECRET_KEY
4. ✅ Set up HTTPS
5. ✅ Configure database backups
6. ✅ Monitor API usage (Gemini has free tier limits)

### Example Gunicorn Command

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🎨 Customizing Templates

All HTML is in `templates/` folder. Modify Jinja2 templates to change layout:

```html
{% extends "base.html" %}

{% block content %}
  <h1>My Custom Page</h1>
{% endblock %}
```

## 💰 Cost Considerations

**Google Gemini Pricing (as of 2026):**
- **Gemini 2.5 Flash:** Free tier available (60 requests/minute)
- **Embeddings:** Free tier available (1500 requests/day)
- **Paid tier:** Very affordable compared to other LLMs

**Estimated costs for 100 documents:**
- Indexing: Free (within free tier limits)
- Queries: Free for moderate usage
- Ideal for personal projects and small businesses!

## 🔑 Getting Your Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key
5. Add to your `.env` file

## 🤝 Contributing

Contributions are welcome! This is a great project for learning server-side rendering.

## 📄 License

MIT License

## 🙏 Acknowledgments

- Flask for the web framework
- Jinja2 for templating
- **Google Gemini** for powerful AI capabilities
- ChromaDB for vector storage
- PostgreSQL for reliable data management

---

**Built with ❤️ using Flask, Jinja2, Google Gemini, and ChromaDB - NO JavaScript!**
