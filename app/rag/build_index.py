import os
from app.rag.pdf_loader import load_pdf
from app.rag.chunking import chunk_text
from app.rag.vector_store import VectorStore

PDF_DIR = "data/pdfs"

texts = []
metadata = []

for pdf in os.listdir(PDF_DIR):
    if not pdf.endswith(".pdf"):
        continue

    pages = load_pdf(os.path.join(PDF_DIR, pdf))
    chunks = chunk_text(pages)

    for chunk in chunks:
        texts.append(chunk["text"])
        metadata.append(chunk)

vs = VectorStore()
vs.build(texts, metadata)
vs.save()

print("FAISS index built successfully.")
