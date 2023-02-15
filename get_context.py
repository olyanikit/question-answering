from bs4 import BeautifulSoup
import requests
import os 

API_KEY = os.environ['API_KEY']
SEARCH_ENGINE_ID = os.environ['SEARCH_ENGINE_ID']

def get_context(query):
    start = 1
    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}"
    data = requests.get(url).json()
    search_items = data.get("items")
    for i, search_item in enumerate(search_items[:1], start=1):
        snippet = search_item.get("snippet")
        link = search_item.get("link")
        resp = requests.get(link)
        context = get_context_from_page(resp.content, snippet)

    return context, snippet


def get_context_from_page(response_content, snippet):    
    soup = BeautifulSoup(response_content, 'html.parser')
    text = soup.find_all(lambda tag: snippet in tag.text)

    cleaned_text = ''
    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head', 
        'input',
        'script',
        'style',
        ]
    for item in text:
        if item.parent.name not in blacklist:
            cleaned_text += '{} '.format(item)
            
    return cleaned_text.replace('\t', '').strip()
