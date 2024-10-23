import requests
import sys
import wikitextparser as wtp

API_URL = "https://pt.wikipedia.org/w/api.php"

def parse_arguments() -> str:
    """
    Valida se o argumento de pesquisa está presente
    """
    
    if len(sys.argv) < 2:
        raise Exception("Should pass a term to search")
    return sys.argv[1]

def find_suggestion(term: str) -> str:
    """
    Busca uma sugestão válida para o termo
    """

    params = {
        'action': 'query',
        'format': 'json',
        'list': 'search',
        'srlimit': '1',
        'srsearch': term,
        'srinfo': 'suggestion',
    }
    response = requests.get(API_URL, params=params)

    if not response.ok:
        raise Exception("Fail to request to find a suggestion in wikipedia API")

    query_response = response.json()

    if 'searchinfo' in query_response['query']:
        return query_response['query']['searchinfo']['suggestion']
    if 'search' in query_response['query'] and len(query_response['query']['search']) > 0:
        return query_response['query']['search'][0]['title']
    return ''


def get_article(term: str):
    """
    Busca o artigo na Wikipedia e salva no arquivo
    """

    params = {
        'action': 'query',
        'format': 'json',
        'prop': 'revisions',
        'rvprop': 'content',
        'rvslots': '*',
        'titles': term
    }
    response = requests.get(API_URL, params=params)

    if not response.ok:
        raise Exception("Fail to request to get article in wikipedia API")

    query_response = response.json()

    if '-1' in query_response['query']['pages']:
        suggestion = find_suggestion(term)
        if suggestion == '':
            print('Artigo não localizado')
            return
        return get_article(suggestion)
    
    pages = list(query_response['query']['pages'])
    pageid = pages[0]
    content: str = query_response['query']['pages'][pageid]['revisions'][0]['slots']['main']['*']

    if content.startswith("#REDIRECT"):
        return get_article(content.replace("#REDIRECT ", ""))

    content = wtp.parse(content).plain_text()

    save_file(term, content)

def save_file(term, content):
    """
    Cria um novo arquivo para o termo e conteudo
    """
    
    filename = term.lower().replace(' ','_')
    with open(f"{filename}.wiki", "w") as f:
        f.write(content.strip())
    
def main():
    term = parse_arguments()
    # term = "airton senna"
    get_article(term)
    

main()