import wikipedia
from googlesearch import search

def get_wikipedia_url(keyword):
    try:
        page = wikipedia.page(keyword)
        return page.url
    except(wikipedia.DisambiguationError, wikipedia.exceptions.PageError):
        return None

def get_google_first_result(keyword):
    try:
        result = next(search(keyword, num_results=1))
        return result
    except StopIteration:
        return None
    
def get_relevant_url(keyword):
    wiki_url = get_wikipedia_url(keyword)
    if wiki_url:
        return wiki_url
    return get_google_first_result(keyword)
