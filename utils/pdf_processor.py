import PyPDF2
import io

def extract_text_from_pdf(file):
    if not file:
        return ""
    reader = PyPDF2.PdfReader(file)
    return "\n".join([page.extract_text() for page in reader.pages])