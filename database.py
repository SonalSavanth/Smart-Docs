from flask_sqlalchemy import SQLAlchemy
import chromadb
from chromadb.utils import embedding_functions
from config import Config

# SQLAlchemy instance
db = SQLAlchemy()

# ChromaDB for RAG
chroma_client = chromadb.PersistentClient(path=Config.CHROMA_DB_PATH)
gemini_ef = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
    api_key=Config.GEMINI_API_KEY,
    model_name="models/gemini-embedding-001"
)

def get_vector_collection(user_id: int):
    """Each user gets their own collection"""
    return chroma_client.get_or_create_collection(
        name=f"user_{user_id}_docs",
        embedding_function=gemini_ef
    )

def init_db(app):
    """Initialize database with Flask app"""
    db.init_app(app)
    with app.app_context():
        db.create_all()
