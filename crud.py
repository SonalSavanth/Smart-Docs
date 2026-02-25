from database import db
from models import User, Folder, Document, Tag, DocumentTag, ChatMessage

# ============ USERS ============
def create_user(email: str, name: str):
    user = User(email=email, name=name)
    db.session.add(user)
    db.session.commit()
    return user

def get_user(user_id: int):
    return User.query.get(user_id)

def get_user_by_email(email: str):
    return User.query.filter_by(email=email).first()

def get_all_users(skip: int = 0, limit: int = 100):
    return User.query.offset(skip).limit(limit).all()

def delete_user(user_id: int):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return user

# ============ FOLDERS ============
def create_folder(name: str, user_id: int, parent_folder_id: int = None):
    folder = Folder(
        name=name,
        user_id=user_id,
        parent_folder_id=parent_folder_id
    )
    db.session.add(folder)
    db.session.commit()
    return folder

def get_user_folders(user_id: int):
    return Folder.query.filter_by(user_id=user_id).all()

def get_folder(folder_id: int):
    return Folder.query.get(folder_id)

def update_folder(folder_id: int, name: str):
    folder = Folder.query.get(folder_id)
    if folder:
        folder.name = name
        db.session.commit()
    return folder

def delete_folder(folder_id: int):
    folder = Folder.query.get(folder_id)
    if folder:
        db.session.delete(folder)
        db.session.commit()
    return folder

# ============ DOCUMENTS ============
def create_document(title: str, user_id: int, file_path: str, 
                   file_type: str, folder_id: int = None):
    doc = Document(
        title=title,
        user_id=user_id,
        folder_id=folder_id,
        file_path=file_path,
        file_type=file_type
    )
    db.session.add(doc)
    db.session.commit()
    return doc

def get_user_documents(user_id: int, folder_id: int = None):
    query = Document.query.filter_by(user_id=user_id)
    if folder_id:
        query = query.filter_by(folder_id=folder_id)
    return query.all()

def get_document(document_id: int):
    return Document.query.get(document_id)

def update_document(document_id: int, title: str = None, 
                   summary: str = None, folder_id: int = None):
    doc = Document.query.get(document_id)
    if doc:
        if title:
            doc.title = title
        if summary:
            doc.summary = summary
        if folder_id is not None:
            doc.folder_id = folder_id
        db.session.commit()
    return doc

def delete_document(document_id: int):
    doc = Document.query.get(document_id)
    if doc:
        db.session.delete(doc)
        db.session.commit()
    return doc

# ============ TAGS ============
def add_tag_to_document(document_id: int, tag_name: str):
    # Get or create tag
    tag = Tag.query.filter_by(name=tag_name).first()
    if not tag:
        tag = Tag(name=tag_name)
        db.session.add(tag)
        db.session.commit()
    
    # Check if already linked
    existing = DocumentTag.query.filter_by(
        document_id=document_id,
        tag_id=tag.id
    ).first()
    
    if not existing:
        doc_tag = DocumentTag(document_id=document_id, tag_id=tag.id)
        db.session.add(doc_tag)
        db.session.commit()
    
    return tag

def get_document_tags(document_id: int):
    doc = Document.query.get(document_id)
    return [tag.name for tag in doc.tags] if doc else []

# ============ CHAT MESSAGES ============
def create_chat_message(user_id: int, question: str, answer: str, source_docs: list):
    msg = ChatMessage(
        user_id=user_id,
        question=question,
        answer=answer,
        source_documents=source_docs
    )
    db.session.add(msg)
    db.session.commit()
    return msg

def get_chat_history(user_id: int, limit: int = 50):
    return ChatMessage.query\
        .filter_by(user_id=user_id)\
        .order_by(ChatMessage.created_at.desc())\
        .limit(limit)\
        .all()
