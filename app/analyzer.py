import os
import requests
import fitz
from docx import Document

LLM_API_URL = os.getenv('TINYLLAMA_API_URL', 'http://localhost:11434/api/generate')
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'pdf', 'docx'}
LLM_MODEL = "tinyllama"


class Analyzer():
    def __init__(self):
        """ Initializes the Analyzer class, setting up the upload folder."""
        self.upload_folder = UPLOAD_FOLDER
        self.llm_api_url = LLM_API_URL
        self.allowed_extensions = ALLOWED_EXTENSIONS
        self.llm_model = LLM_MODEL
        
        os.makedirs(self.upload_folder, exist_ok=True)
        
    def allowed_file(self, filename):
        """ Check if the file has an allowed extension."""
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.allowed_extensions
        
    def extract_text_from_pdf(self, file_path):
        """Extract text from a PDF file."""
        text = ""
        with fitz.open(file_path) as pdf_document:
            for page in pdf_document:
                text += page.get_text()
        return text
    
    def extract_text_from_docx(self, file_path):
        """Extract text from a DOCX file."""
        text = ""
        doc = Document(file_path)
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
            
        return text
    
    def analyze_text(self, text):
        print(text)
        prompt = f"""
        You are a professional text analyst.
        Analyze the following text and return:
        1. Strengths
        2. Weaknesses
        3. Recommendations for improvement.
    
        Text:
        {text}
    
        Please respond in JSON:
        {{
            "strengths": [...],
            "weaknesses": [...],
            "recommendations": [...]
        }}
        """
        
        response = requests.post(self.llm_api_url, json={"prompt": prompt, "model": self.llm_model, "stream": False})
        if response.status_code != 200:
            return {"error": "Failed to analyze text", "details": response.text}
        return response.json()
    
    
analyzer = Analyzer()