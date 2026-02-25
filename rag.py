import google.generativeai as genai
import PyPDF2
from database import get_vector_collection
from config import Config
from typing import List, Optional

# Configure Gemini
genai.configure(api_key=Config.GEMINI_API_KEY)
model = genai.GenerativeModel('models/gemini-2.5-flash')  # Latest stable model

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF"""
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """Split text into overlapping chunks"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
    return chunks

def index_document(user_id: int, document_id: int, text: str):
    """Add document to vector database"""
    collection = get_vector_collection(user_id)
    
    # Split into chunks
    chunks = chunk_text(text)
    
    # Add to ChromaDB
    collection.add(
        documents=chunks,
        ids=[f"doc_{document_id}_chunk_{i}" for i in range(len(chunks))],
        metadatas=[{"document_id": document_id, "chunk_index": i} for i in range(len(chunks))]
    )
    
    return len(chunks)

def search_documents(user_id: int, question: str, 
                    document_ids: Optional[List[int]] = None, 
                    n_results: int = 5):
    """RAG: Retrieve relevant chunks and generate answer"""
    collection = get_vector_collection(user_id)
    
    # Build filter for specific documents if provided
    where_filter = None
    if document_ids:
        where_filter = {"document_id": {"$in": document_ids}}
    
    # Retrieve relevant chunks
    results = collection.query(
        query_texts=[question],
        n_results=n_results,
        where=where_filter
    )
    
    if not results["documents"][0]:
        return {
            "answer": "I couldn't find any relevant information in your documents.",
            "sources": [],
            "chunks_used": 0
        }
    
    # Combine chunks as context
    context = "\n\n".join(results["documents"][0])
    source_docs = [meta["document_id"] for meta in results["metadatas"][0]]
    
    # Generate answer using Gemini
    prompt = f"""You are a helpful assistant. Answer the question based ONLY on the provided context. If the answer is not in the context, say so.

Context:
{context}

Question: {question}

Answer:"""
    
    response = model.generate_content(prompt)
    answer = response.text
    
    return {
        "answer": answer,
        "sources": list(set(source_docs)),
        "chunks_used": len(results["documents"][0])
    }

def delete_document_from_vector_db(user_id: int, document_id: int):
    """Remove document chunks from vector database"""
    collection = get_vector_collection(user_id)
    
    # Get all chunk IDs for this document
    results = collection.get(
        where={"document_id": document_id}
    )
    
    if results["ids"]:
        collection.delete(ids=results["ids"])


#OLD

# import google.generativeai as genai
# import PyPDF2
# from database import get_vector_collection
# from config import Config
# from typing import List, Optional

# # Configure Gemini
# genai.configure(api_key=Config.GEMINI_API_KEY)
# model = genai.GenerativeModel('gemini-1.5-flash')

# def extract_text_from_pdf(file_path: str) -> str:
#     """Extract text from PDF"""
#     with open(file_path, 'rb') as file:
#         pdf_reader = PyPDF2.PdfReader(file)
#         text = ""
#         for page in pdf_reader.pages:
#             text += page.extract_text()
#     return text

# def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
#     """Split text into overlapping chunks"""
#     chunks = []
#     start = 0
#     while start < len(text):
#         end = start + chunk_size
#         chunk = text[start:end]
#         chunks.append(chunk)
#         start = end - overlap
#     return chunks

# def index_document(user_id: int, document_id: int, text: str):
#     """Add document to vector database"""
#     collection = get_vector_collection(user_id)
    
#     # Split into chunks
#     chunks = chunk_text(text)
    
#     # Add to ChromaDB (ChromaDB will handle embeddings)
#     collection.add(
#         documents=chunks,
#         ids=[f"doc_{document_id}_chunk_{i}" for i in range(len(chunks))],
#         metadatas=[{"document_id": document_id, "chunk_index": i} for i in range(len(chunks))]
#     )
    
#     return len(chunks)

# def search_documents(user_id: int, question: str, 
#                     document_ids: Optional[List[int]] = None, 
#                     n_results: int = 5):
#     """RAG: Retrieve relevant chunks and generate answer"""
#     collection = get_vector_collection(user_id)
    
#     # Build filter for specific documents if provided
#     where_filter = None
#     if document_ids:
#         where_filter = {"document_id": {"$in": document_ids}}
    
#     # Retrieve relevant chunks
#     results = collection.query(
#         query_texts=[question],
#         n_results=n_results,
#         where=where_filter
#     )
    
#     if not results["documents"][0]:
#         return {
#             "answer": "I couldn't find any relevant information in your documents.",
#             "sources": [],
#             "chunks_used": 0
#         }
    
#     # Combine chunks as context
#     context = "\n\n".join(results["documents"][0])
#     source_docs = [meta["document_id"] for meta in results["metadatas"][0]]
    
#     # Generate answer using Gemini
#     prompt = f"""You are a helpful assistant. Answer the question based ONLY on the provided context. If the answer is not in the context, say so.

# Context:
# {context}

# Question: {question}

# Answer:"""
    
#     response = model.generate_content(prompt)
#     answer = response.text
    
#     return {
#         "answer": answer,
#         "sources": list(set(source_docs)),
#         "chunks_used": len(results["documents"][0])
#     }

# def delete_document_from_vector_db(user_id: int, document_id: int):
#     """Remove document chunks from vector database"""
#     collection = get_vector_collection(user_id)
    
#     # Get all chunk IDs for this document
#     results = collection.get(
#         where={"document_id": document_id}
#     )
    
#     if results["ids"]:
#         collection.delete(ids=results["ids"])