import fitz  # PyMuPDF
from pdfminer.high_level import extract_text
import os

def extract_with_pymupdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text

def extract_with_pdfminer(pdf_path):
    return extract_text(pdf_path)

def save_text(text, filename="misra_raw.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)

pdf_path = "Misra_document.pdf"

try:
    text = extract_with_pymupdf(pdf_path)
    if not text.strip():
        raise ValueError("Empty text from PyMuPDF, trying fallback.")
except Exception as e:
    print("PyMuPDF failed. Trying pdfminer...")
    text = extract_with_pdfminer(pdf_path)

save_text(text)
print("[✓] PDF text extraction complete.")
