def chunk_text(pages, chunk_size=500, overlap=100):
    chunks = []
    for page in pages:
        text = page["text"]
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append({
                "text": text[start:end],
                "page": page["page"],
                "category": page["category"],
                "brand": page["brand"],
                "source_pdf": page["source_pdf"]
            })
            start += chunk_size - overlap
    return chunks
