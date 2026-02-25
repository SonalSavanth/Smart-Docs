# 🚀 QUICK START GUIDE (No JavaScript Version)

## What You've Got

A **Smart Document Manager** built with:
- ✅ Flask (Python backend)
- ✅ Jinja2 Templates (HTML rendering)
- ✅ **NO JavaScript!** (Server-side only)
- ✅ CRUD operations
- ✅ RAG (AI chat with documents)
- ✅ LLM features (auto-summarization, tagging)
- ✅ **Google Gemini AI** (free tier available!)

## ⚡ 3-Step Setup

### Step 1: Install PostgreSQL

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo service postgresql start
```

**Windows:**
Download from https://www.postgresql.org/download/windows/

### Step 2: Get Gemini API Key

1. Go to https://aistudio.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key (starts with `AIza...`)

### Step 3: Install & Run

```bash
# Install Python packages
pip install -r requirements.txt

# Create database
createdb smart_docs

# Set up environment
cp .env.example .env
# Edit .env with your PostgreSQL credentials and Gemini key

# Run the app
python app.py
```

Open browser: **http://localhost:5000**

## 🎯 How It Works (No JavaScript!)

### Traditional Web App Flow

1. **User Action** → Submits HTML form
2. **Server Receives** → Flask processes data
3. **Server Renders** → Jinja2 creates new HTML
4. **Browser Displays** → Page reloads with new content

**No AJAX, no fetch(), no JSON!**

### Example: Uploading a Document

```
User selects file + clicks "Upload"
          ↓
Form submits to /upload (POST)
          ↓
Flask receives file, processes it
          ↓
Gemini AI generates summary & tags
          ↓
Flask renders index.html with updated data
          ↓
Browser displays new page with document
```

## 📂 File Structure

```
smart-docs-no-js/
├── app.py                    # Flask routes (NO API endpoints)
├── templates/                # Jinja2 HTML templates
│   ├── base.html            # Layout
│   ├── index.html           # Dashboard
│   └── chat.html            # Chat page
├── config.py                # Settings (Gemini API key)
├── models.py                # Database models
├── crud.py                  # Database operations
├── rag.py                   # AI search logic (Gemini 2.5 Flash)
└── llm.py                   # AI features (Gemini 2.5 Flash)
```

## 🎨 What You'll See

### Dashboard Page
- Stats cards (documents, chats, tags)
- Upload form with file selector
- Document list with summaries and tags
- All updates require page refresh

### Chat Page
- Full conversation history
- Text area for questions
- Submit button → page reloads with answer
- No live updates

## 🔑 Key Differences

### From JavaScript Version:

| What | JavaScript Version | This Version |
|------|-------------------|--------------|
| **Updates** | Dynamic (no reload) | Page reload |
| **Forms** | AJAX/fetch() | Traditional POST |
| **Code** | Frontend + Backend | Backend only |
| **Files** | HTML + CSS + JS | HTML + CSS |
| **Learning** | JS + Python | Just Python |

### Why This Is Simpler:

✅ **One Language** - Only Python + HTML  
✅ **No API Layer** - Direct template rendering  
✅ **Fewer Files** - No JavaScript files  
✅ **Traditional** - Classic web development  
✅ **Easier Debug** - See everything in Python  

## 🧪 Test It

### 1. Upload a Document
1. Homepage → Choose file (PDF, TXT, or DOCX)
2. Check "Auto-generate summary"
3. Click "Upload & Analyze"
4. Wait 10-30 seconds (Gemini is processing)
5. Page reloads → See document with AI summary

### 2. Chat with Documents
1. Click "💬 Chat" in navigation
2. Type: "What are the main topics in my documents?"
3. Click "Send"
4. Page reloads → See Gemini AI answer

### 3. View Details
1. Click "View" on any document
2. See full details
3. Click "Translate" → Choose language
4. Submit → Page reloads with translation

## 💡 How Templates Work

### Jinja2 Template Example

```html
<!-- base.html -->
<html>
  <body>
    {% block content %}{% endblock %}
  </body>
</html>

<!-- index.html -->
{% extends "base.html" %}
{% block content %}
  <h1>Documents</h1>
  {% for doc in documents %}
    <div>{{ doc.title }}</div>
  {% endfor %}
{% endblock %}
```

Flask renders these to complete HTML pages!

## 🤖 AI Models Configuration

Make sure your files use the correct Gemini models:

**llm.py and rag.py:**
```python
model = genai.GenerativeModel('models/gemini-2.5-flash')
```

**database.py:**
```python
model_name="models/gemini-embedding-001"
```

## 🔧 Troubleshooting

### "Template Not Found"
→ Check templates are in `templates/` folder

### "404 models/... is not found"
→ Wrong model name! Use:
- Text generation: `models/gemini-2.5-flash`
- Embeddings: `models/gemini-embedding-001`
→ Run `python check_models.py` to verify

### "Secret Key Warning"
→ Add SECRET_KEY to .env file

### "DataError: value too long"
→ Make sure `models.py` has:
```python
file_type = db.Column(db.String(150))
```

### Forms Not Submitting
→ Verify method="POST" in form tag

### Page Not Refreshing
→ Clear browser cache (Ctrl+F5)

### Gemini API Key Not Working
→ Get a new key from https://aistudio.google.com/app/apikey
→ Make sure it's in `.env` as `GEMINI_API_KEY=AIza...`

## 💰 Free Tier Limits

**Gemini 2.5 Flash:**
- 60 requests per minute
- Free for personal use!

**Embeddings:**
- 1500 requests per day
- Perfect for testing and small projects

## 📚 Next Steps

1. Read full README.md
2. Customize templates in `templates/`
3. Modify CSS in `base.html`
4. Add more routes in `app.py`
5. Check model availability: `python check_models.py`

## 🎉 You're All Set!

Start uploading documents and chatting with your Gemini AI assistant!

**Remember:** This version uses traditional web forms, so pages refresh when you submit. That's normal!

---

Built with Flask + Jinja2 + Google Gemini (No JavaScript!) ❤️
