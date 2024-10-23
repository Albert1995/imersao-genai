from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

def create_prompt(role: str, task: str, topic: str, specific_question: str) -> str:
    return f"""Você é um {role}, e como objetivo será {task}.
    E deverá responder a questão relacionada:

    <topic>
        {topic}
    </topic>

    A questão é:

    <specific_question>
        {specific_question}
    </specific_question>
    """

def send_to_gemini(prompt: str) -> str:
    genai.configure(api_key=os.environ['GEMINI_API_KEY'])
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text

# role = "especialista em filosofia e história da ciência"
# task = "explicar o pensamento de Descartes e sua influência para iniciantes em filosofia"
# topic = "René Descartes e o Método Cartesiano"
# specific_question = "Quem foi René Descartes e qual é o significado da frase 'Penso, logo existo'?"
# prompt = create_prompt(role, task, topic, specific_question)
# response = send_to_gemini(prompt)
# print("\nResposta do Gemini 1.5 Flash:")
# print(response)


# role = "assistente especializado em ensinar programação Python para iniciantes"
# task = "explicar conceitos básicos de Python e fornecer exemplos simples e práticos"
# topic = "list comprehensions em Python"
# specific_question = "O que é uma list comprehension e como posso usá-la para criar uma lista de números pares de 0 a 10?"
# prompt = create_prompt(role, task, topic, specific_question)
# response = send_to_gemini(prompt)
# print("\nResposta do Gemini 1.5 Flash:")
# print(response)


role = "historiador da ciência da computação e teoria da informação"
task = "explicar a importância de Claude Shannon e suas contribuições para iniciantes em ciência da computação"
topic = "Claude Shannon e a Teoria da Informação"
specific_question = "Quem foi Claude Shannon e qual foi sua principal contribuição para a ciência da computação e comunicação?"
prompt = create_prompt(role, task, topic, specific_question)
response = send_to_gemini(prompt)
print("\nResposta do Gemini 1.5 Flash:")
print(response)