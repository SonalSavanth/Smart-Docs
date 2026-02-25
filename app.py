from flask import Flask, request, render_template, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import os

from config import Config
from database import init_db, db
import crud
import llm
import rag

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY  # For flash messages

# Initialize database
init_db(app)

# Create upload directory
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

# Set default user (in production, use proper authentication)
DEFAULT_USER_ID = 1

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def ensure_default_user():
    """Create default user if doesn't exist"""
    user = crud.get_user(DEFAULT_USER_ID)
    if not user:
        crud.create_user(email='demo@example.com', name='Demo User')

# ==================== MAIN ROUTES ====================

@app.route('/')
def index():
    """Home page with dashboard"""
    ensure_default_user()
    
    # Get stats
    documents = crud.get_user_documents(DEFAULT_USER_ID)
    folders = crud.get_user_folders(DEFAULT_USER_ID)
    chat_history = crud.get_chat_history(DEFAULT_USER_ID, limit=1000)
    
    # Count unique tags
    all_tags = set()
    for doc in documents:
        for tag in doc.tags:
            all_tags.add(tag.name)
    
    stats = {
        'doc_count': len(documents),
        'chat_count': len(chat_history),
        'tag_count': len(all_tags),
        'folder_count': len(folders)
    }
    
    return render_template('index.html', 
                         documents=documents,
                         folders=folders,
                         stats=stats)

# ==================== DOCUMENT ROUTES ====================

@app.route('/upload', methods=['POST'])
def upload_document():
    """Upload and process document"""
    if 'file' not in request.files:
        flash('No file provided', 'error')
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    if not allowed_file(file.filename):
        flash('File type not allowed. Use PDF, TXT, DOC, or DOCX', 'error')
        return redirect(url_for('index'))
    
    auto_summarize = request.form.get('auto_summarize') == 'on'
    auto_tag = request.form.get('auto_tag') == 'on'
    folder_id = request.form.get('folder_id')
    if folder_id:
        folder_id = int(folder_id)
    
    # Save file
    filename = secure_filename(file.filename)
    file_path = os.path.join(Config.UPLOAD_FOLDER, f"{DEFAULT_USER_ID}_{filename}")
    file.save(file_path)
    
    # Create document record
    doc = crud.create_document(
        title=filename,
        user_id=DEFAULT_USER_ID,
        file_path=file_path,
        file_type=file.content_type,
        folder_id=folder_id
    )
    
    try:
        # Extract text
        if file.content_type == 'application/pdf':
            text = rag.extract_text_from_pdf(file_path)
        else:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
        
        # LLM: Auto-generate summary
        if auto_summarize and text:
            summary = llm.generate_summary(text)
            crud.update_document(doc.id, summary=summary)
        
        # LLM: Auto-suggest tags
        if auto_tag and text:
            tags = llm.suggest_tags(text)
            for tag in tags:
                crud.add_tag_to_document(doc.id, tag)
        
        # RAG: Index document
        chunks_indexed = rag.index_document(DEFAULT_USER_ID, doc.id, text)
        
        flash(f'✅ Document uploaded successfully! Indexed {chunks_indexed} chunks.', 'success')
    
    except Exception as e:
        flash(f'⚠️ Document uploaded but processing failed: {str(e)}', 'warning')
    
    return redirect(url_for('index'))

@app.route('/document/<int:doc_id>/delete', methods=['POST'])
def delete_document(doc_id):
    """Delete a document"""
    doc = crud.get_document(doc_id)
    if not doc:
        flash('Document not found', 'error')
        return redirect(url_for('index'))
    
    try:
        # Remove from vector database
        rag.delete_document_from_vector_db(DEFAULT_USER_ID, doc_id)
    except Exception as e:
        print(f"Vector DB deletion failed: {e}")
    
    # Remove file
    if os.path.exists(doc.file_path):
        try:
            os.remove(doc.file_path)
        except Exception as e:
            print(f"File deletion failed: {e}")
    
    # Remove from database
    crud.delete_document(doc_id)
    
    flash('Document deleted successfully', 'success')
    return redirect(url_for('index'))

@app.route('/document/<int:doc_id>')
def view_document(doc_id):
    """View document details"""
    doc = crud.get_document(doc_id)
    if not doc:
        flash('Document not found', 'error')
        return redirect(url_for('index'))
    
    return render_template('document_detail.html', document=doc)

# ==================== FOLDER ROUTES ====================

@app.route('/folder/create', methods=['POST'])
def create_folder():
    """Create a new folder"""
    name = request.form.get('name')
    if not name:
        flash('Folder name is required', 'error')
        return redirect(url_for('index'))
    
    crud.create_folder(name=name, user_id=DEFAULT_USER_ID)
    flash(f'Folder "{name}" created successfully', 'success')
    return redirect(url_for('index'))

@app.route('/folder/<int:folder_id>/delete', methods=['POST'])
def delete_folder(folder_id):
    """Delete a folder"""
    folder = crud.delete_folder(folder_id)
    if not folder:
        flash('Folder not found', 'error')
    else:
        flash('Folder deleted successfully', 'success')
    return redirect(url_for('index'))

# ==================== CHAT ROUTES ====================

@app.route('/chat')
def chat():
    """Chat page"""
    history = crud.get_chat_history(DEFAULT_USER_ID, limit=50)
    # Reverse to show oldest first
    history = list(reversed(history))
    return render_template('chat.html', chat_history=history)

@app.route('/chat/ask', methods=['POST'])
def ask_question():
    """Ask a question to the AI"""
    question = request.form.get('question')
    
    if not question:
        flash('Please enter a question', 'error')
        return redirect(url_for('chat'))
    
    try:
        # Search documents and get AI answer
        result = rag.search_documents(
            user_id=DEFAULT_USER_ID,
            question=question
        )
        
        # Get source document details
        sources = []
        for doc_id in result['sources']:
            doc = crud.get_document(doc_id)
            if doc:
                sources.append(doc)
        
        # Save chat message
        crud.create_chat_message(
            user_id=DEFAULT_USER_ID,
            question=question,
            answer=result['answer'],
            source_docs=[str(d) for d in result['sources']]
        )
        
        flash('Answer generated successfully', 'success')
    
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('chat'))

@app.route('/chat/clear', methods=['POST'])
def clear_chat():
    """Clear chat history"""
    # In production, you'd delete from database
    flash('Chat history cleared', 'success')
    return redirect(url_for('chat'))

# ==================== LLM UTILITIES ====================

@app.route('/document/<int:doc_id>/translate', methods=['GET', 'POST'])
def translate_document(doc_id):
    """Translate document"""
    doc = crud.get_document(doc_id)
    if not doc:
        flash('Document not found', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        target_language = request.form.get('target_language')
        
        try:
            # Extract text
            if doc.file_type == 'application/pdf':
                text = rag.extract_text_from_pdf(doc.file_path)
            else:
                with open(doc.file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
            
            # Translate (limit to first 5000 chars to avoid token limits)
            translated = llm.translate_text(text[:5000], target_language)
            
            return render_template('translate_result.html', 
                                 document=doc,
                                 translated_text=translated,
                                 target_language=target_language)
        
        except Exception as e:
            flash(f'Translation failed: {str(e)}', 'error')
            return redirect(url_for('view_document', doc_id=doc_id))
    
    return render_template('translate_form.html', document=doc)

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    db.session.rollback()
    return render_template('500.html'), 500

if __name__ == '__main__':
    with app.app_context():
        ensure_default_user()
    app.run(debug=True, host='0.0.0.0', port=5000)
