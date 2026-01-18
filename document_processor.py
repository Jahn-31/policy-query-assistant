import PyPDF2
import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter
import config
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import os

# Set tesseract path for Windows (adjust if needed)
if os.name == 'nt':  # Windows
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class DocumentProcessor:
    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP
        )
    
    def extract_text(self, pdf_path):
        """Extract text from PDF (with OCR fallback for scanned PDFs)"""
        text = ""
        
        # Try regular text extraction first
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text() or ""
                    text += page_text
        except:
            try:
                with open(pdf_path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    for page in reader.pages:
                        text += page.extract_text()
            except:
                pass
        
        # If no text extracted or very little text, it's likely a scanned PDF
        if len(text.strip()) < 100:
            print(f"⚠️  PDF appears to be scanned. Running OCR...")
            text = self.extract_text_with_ocr(pdf_path)
        
        return text
    
    def extract_text_with_ocr(self, pdf_path):
        """Extract text from scanned PDF using OCR"""
        try:
            # Convert PDF pages to images
            images = convert_from_path(pdf_path, dpi=300)
            
            text = ""
            for i, image in enumerate(images):
                print(f"  Processing page {i+1}/{len(images)} with OCR...")
                # Extract text from image using Tesseract
                page_text = pytesseract.image_to_string(image, lang='eng')
                text += f"\n\n--- Page {i+1} ---\n\n{page_text}"
            
            print(f"✓ OCR completed. Extracted {len(text)} characters")
            return text
            
        except Exception as e:
            print(f"✗ OCR failed: {e}")
            return ""
    
    def process(self, pdf_path, metadata):
        """Process PDF into chunks with metadata"""
        text = self.extract_text(pdf_path)
        
        if not text.strip():
            print(f"⚠️  No text extracted from {pdf_path}")
            return []
        
        chunks = self.splitter.split_text(text)
        
        result = []
        for i, chunk in enumerate(chunks):
            result.append({
                "text": chunk,
                "metadata": {**metadata, "chunk_id": i, "total_chunks": len(chunks)}
            })
        return result