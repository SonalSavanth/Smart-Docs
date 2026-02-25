import google.generativeai as genai
from config import Config

# Configure Gemini
genai.configure(api_key=Config.GEMINI_API_KEY)

# Use the latest stable model
model = genai.GenerativeModel('models/gemini-2.5-flash')

def generate_summary(text: str, max_words: int = 100) -> str:
    """Generate a summary of document content"""
    prompt = f"Summarize the following text in {max_words} words or less:\n\n{text}"
    
    response = model.generate_content(prompt)
    return response.text

def suggest_tags(text: str, max_tags: int = 5) -> list:
    """Auto-generate relevant tags for a document"""
    prompt = f"Generate {max_tags} relevant tags for this document. Return only the tags separated by commas:\n\n{text[:2000]}"
    
    response = model.generate_content(prompt)
    tags = response.text.split(",")
    return [tag.strip().lower() for tag in tags]

def translate_text(text: str, target_language: str) -> str:
    """Translate document content"""
    prompt = f"Translate the following text to {target_language}:\n\n{text}"
    
    response = model.generate_content(prompt)
    return response.text

#OLD

# import google.generativeai as genai
# from config import Config

# # Configure Gemini
# genai.configure(api_key=Config.GEMINI_API_KEY)

# # Initialize the model
# model = genai.GenerativeModel('gemini-1.5-flash')

# def generate_summary(text: str, max_words: int = 100) -> str:
#     """Generate a summary of document content"""
#     prompt = f"Summarize the following text in {max_words} words or less:\n\n{text}"
    
#     response = model.generate_content(prompt)
#     return response.text

# def suggest_tags(text: str, max_tags: int = 5) -> list:
#     """Auto-generate relevant tags for a document"""
#     prompt = f"Generate {max_tags} relevant tags for this document. Return only the tags separated by commas:\n\n{text[:2000]}"
    
#     response = model.generate_content(prompt)
#     tags = response.text.split(",")
#     return [tag.strip().lower() for tag in tags]

# def translate_text(text: str, target_language: str) -> str:
#     """Translate document content"""
#     prompt = f"Translate the following text to {target_language}:\n\n{text}"
    
#     response = model.generate_content(prompt)
#     return response.text