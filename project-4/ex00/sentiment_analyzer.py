import os
import google.generativeai as genai
from dotenv import load_dotenv
import re

load_dotenv()

example_github_comments = [
	{
    	"text": "A implementação deste método não é performatica",
    	"sentiment": "Negativo"
	},
	{
    	"text": "Podemos reescrever este trecho de código de outra forma para melhor a legibilidade.",
    	"sentiment": "Positivo"
	},
	{
    	"text": "Vamos adicionar essa técnica na classe ABC para aumentar a leitura",
    	"sentiment": "Positivo"
	},
	{
    	"text": "Isso reduziu o tempo de resposta em 40ms. Poderia explicar como chegou nesta solução?",
    	"sentiment": "Positivo"
	},
	{
    	"text": "Não faça dessa forma porque vai degradar muito o servidor. Reverta a alteração",
    	"sentiment": "Negativo"
	},
    {
    	"text": "A alteração pode causar um bug no método A, reveja os cenários de teste",
    	"sentiment": "Negativo"
	},
]

github_comments = [
	{
    	"text": "Ótimo trabalho na implementação desta feature! O código está limpo e bem documentado. Isso vai ajudar muito nossa produtividade.",
    	"sentiment": ""
	},
	{
    	"text": "Esta mudança quebrou a funcionalidade X. Por favor, reverta o commit imediatamente.",
    	"sentiment": ""
	},
	{
    	"text": "Podemos discutir uma abordagem alternativa para este problema? Acho que a solução atual pode causar problemas de desempenho no futuro.",
    	"sentiment": ""
	},
	{
    	"text": "Obrigado por relatar este bug. Vou investigar e atualizar a issue assim que tiver mais informações.",
    	"sentiment": ""
	},
	{
    	"text": "Este pull request não segue nossas diretrizes de estilo de código. Por favor, revise e faça as correções necessárias.",
    	"sentiment": ""
	},
	{
    	"text": "Excelente ideia! Isso resolve um problema que estávamos enfrentando há semanas. Mal posso esperar para ver isso implementado.",
    	"sentiment": ""
	},
	{
    	"text": "Esta issue está aberta há meses sem nenhum progresso. Podemos considerar fechá-la se não for mais relevante?",
    	"sentiment": ""
	},
	{
    	"text": "O novo recurso está causando conflitos com o módulo Y. Precisamos de uma solução urgente para isso.",
    	"sentiment": ""
	},
	{
    	"text": "Boa captura! Este edge case não tinha sido considerado. Vou adicionar testes para cobrir este cenário.",
    	"sentiment": ""
	},
	{
    	"text": "Não entendo por que estamos priorizando esta feature. Existem problemas mais críticos que deveríamos estar abordando.",
    	"sentiment": ""
	}
]


def create_prompt(comment):
    global example_github_comments
    examples = "".join([f"<example>\nComentário: {c['text']}\nSentimento: {c['sentiment']}\n</example>\n" for c in example_github_comments])
    return f"""
Classifique os comentarios em Positivo ou Negativo, para o sentimento do comentário do desenvolvedor relacionado a alterações realizadas dentro do PR do github.

<examples>
{examples}
</examples>

Comentário: {comment}
Sentimento:
    """


def call_llm(text):
    # Implementar chamada ao modelo com exemplos (multishot)
    genai.configure(api_key=os.environ['GEMINI_API_KEY'])
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(create_prompt(text))
    return response.text


def parse_llm_response(response):
    # print(response)
    regex = r"Sentimento: (.*)"
    m = re.match(regex, response)
    return m.groups()[0].strip().replace('*','')


def analyze_sentiments(comments):
    for comment in comments:
        llm_response = call_llm(comment["text"])
        comment["sentiment"] = parse_llm_response(llm_response)



analyze_sentiments(github_comments)

# Imprimir resultados
for comment in github_comments:
    print(f"Texto: {comment['text']}")
    print(f"Sentimento: {comment['sentiment']}")
    print("-" * 50)