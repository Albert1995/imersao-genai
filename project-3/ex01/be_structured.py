import ollama
import os
import google.generativeai as genai
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

def format_prompt(input: str) -> str:
    return f"""Extract information from job description below to fill the required fields. Job Descriptions could be english or portuguese. 
Should complete all fields, if not found any information add 'Not Specified'.

Fields to be filled:
- Name of Role,
- Working Hours,
- Country,
- Tech Skills

Job Description:
{input}

"""

def query_qwen(prompt: str) -> str:
    print('Consultando Ollama - qwen2:1.5b')
    response = ollama.chat(
        model='qwen2:1.5b',
        messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ]
    )
    return response['message']['content']

def query_groq(prompt: str) -> str:
    print('Consultando Groq')
    client = Groq(api_key=os.environ['GROQ_API_KEY'])
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content

def query_gemini(prompt: str) -> str:
    print('Consultando Gemini')
    genai.configure(api_key=os.environ['GEMINI_API_KEY'])
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text


def query_all_models(prompt: str) -> dict[str, str]:
    return {
        'qwen2:1.5b': query_qwen(prompt),
        'llama': query_groq(prompt),
        'gemini': query_gemini(prompt)
    }

def main():
    with open("job_description.txt", "r") as file:
        job_description = file.read()

    formatted_prompt = format_prompt(job_description)
    results = query_all_models(formatted_prompt)

    for model, response in results.items():
        print(f"\nAnálise do {model}:")
        print(response)
        print("-" * 50)

if __name__ == "__main__":
    main()