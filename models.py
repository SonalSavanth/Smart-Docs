from database import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY

class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    name = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    folders = db.relationship("Folder", back_populates="user", cascade="all, delete-orphan")
    documents = db.relationship("Document", back_populates="user", cascade="all, delete-orphan")
    chat_messages = db.relationship("ChatMessage", back_populates="user", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'created_at': self.created_at.isoformat()
        }

class Folder(db.Model):
    __tablename__ = "folders"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    parent_folder_id = db.Column(db.Integer, db.ForeignKey("folders.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship("User", back_populates="folders")
    documents = db.relationship("Document", back_populates="folder")
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'parent_folder_id': self.parent_folder_id,
            'created_at': self.created_at.isoformat()
        }

class Document(db.Model):
    __tablename__ = "documents"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    folder_id = db.Column(db.Integer, db.ForeignKey("folders.id"), nullable=True)
    title = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500))
    file_type = db.Column(db.String(100))
    summary = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship("User", back_populates="documents")
    folder = db.relationship("Folder", back_populates="documents")
    tags = db.relationship("Tag", secondary="document_tags", back_populates="documents")
    
    def to_dict(self, include_tags=True):
        result = {
            'id': self.id,
            'title': self.title,
            'folder_id': self.folder_id,
            'file_type': self.file_type,
            'summary': self.summary,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        if include_tags:
            result['tags'] = [tag.name for tag in self.tags]
        return result

class Tag(db.Model):
    __tablename__ = "tags"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    
    documents = db.relationship("Document", secondary="document_tags", back_populates="tags")

class DocumentTag(db.Model):
    __tablename__ = "document_tags"
    
    document_id = db.Column(db.Integer, db.ForeignKey("documents.id"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)

class ChatMessage(db.Model):
    __tablename__ = "chat_messages"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    source_documents = db.Column(ARRAY(db.String))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship("User", back_populates="chat_messages")
    
    def to_dict(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'source_documents': self.source_documents,
            'created_at': self.created_at.isoformat()
        }
