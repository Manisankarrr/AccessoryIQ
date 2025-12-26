import os
from pypdf import PdfReader

def extract_metadata_from_filename(filename: str):
    name = filename.lower()

    if "iphone" in name or "galaxy" in name:
        category = "mobile"
    elif "tv" in name:
        category = "tv"
    elif "laptop" in name:
        category = "laptop"
    elif "playstation" in name:
        category = "gaming"
    else:
        category = "unknown"

    brand = name.split("_")[0]

    return {
        "category": category,
        "brand": brand,
        "source_pdf": filename
    }


def load_pdf(path: str):
    reader = PdfReader(path)
    filename = os.path.basename(path)
    base_metadata = extract_metadata_from_filename(filename)

    pages = []
    for i, page in enumerate(reader.pages):
        pages.append({
            "text": page.extract_text(),
            "page": i + 1,
            **base_metadata
        })
    return pages
