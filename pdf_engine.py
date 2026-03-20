from pypdf import PdfReader

def get_pdf_content(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for i, page in enumerate(reader.pages):
        content = page.extract_text()
        text += f"\n--- PAGE {i+1} ---\n{content}"
    return text
