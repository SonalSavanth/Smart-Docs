import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://user:password@localhost/smart_docs'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # GEMINI
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'your-gemini-key')
    
    # Flask secret key for sessions and flash messages
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # File uploads
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}
    
    # ChromaDB
    CHROMA_DB_PATH = './chroma_db'
