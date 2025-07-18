import requests
from bs4 import BeautifulSoup

def extract_text_from_url(url):
    if not url.startswith(('http://', 'https://')):
        return "Invalid URL"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return ' '.join([p.get_text() for p in soup.find_all('p')])
    except:
        return "Failed to extract content"