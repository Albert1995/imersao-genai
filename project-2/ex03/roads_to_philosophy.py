import requests
import bs4
import sys
import re

WIKIPEDIA_URL="https://en.wikipedia.org/"
TARGET="Philosophy"
INFINITY=float('inf')

def parse_arguments() -> str:
    """
    Valida se o argumento de pesquisa está presente
    """
    
    if len(sys.argv) < 2:
        raise Exception("Should pass a term to search")
    return sys.argv[1]

def find_link(href):
    return href and (href.startswith("/wiki") or href.startswith("https://en.wikipedia"))

def road_to_philosophy(url: str, i: int = 1, visited: list = list()):
    response = requests.get(url)

    if not response.ok:
        raise Exception('fail to request to wikipedia')

    html = response.text
    b = bs4.BeautifulSoup(html, features='html.parser')

    current = b.find(id='firstHeading').text
    print(current)

    if current.lower() == 'philosophy':
        return i
    
    if current in visited:
        return INFINITY

    visited.append(b.find(id='firstHeading').text)

    next_link = None
    b = b.find(id='mw-content-text')
    list_p = b.find_all('p')

    for p in list_p:
        next_link = p.find(href=find_link)
        if next_link: break

    if not next_link:
        next_link = b.find(href=find_link)

    if not next_link:
        return -1
    
    return road_to_philosophy(f"{WIKIPEDIA_URL}{next_link.attrs['href']}", i + 1, visited)
    

def main():
    term = parse_arguments()
    cleaned_term = term.strip().replace(' ', '_')
    if term.lower() == 'philosophy':
        return f'0 roads from {term} to philosophy!'
    
    try:
        i = road_to_philosophy(f"{WIKIPEDIA_URL}wiki/{cleaned_term}")
    except Exception as exc:
        print(f'Error: {exc}. Unable to continue')
        return
    
    print()
    if i == -1:
        print('It leads to a dead end!')
    elif i == INFINITY:
        print('It leads to an infinite loop!')
    else:
        print(f'{i} roads from {term} to philosophy!')
    
main()