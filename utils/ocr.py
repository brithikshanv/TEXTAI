import pytesseract
from PIL import Image

def extract_text_from_image(file):
    if not file:
        return ""
    image = Image.open(file)
    return pytesseract.image_to_string(image)