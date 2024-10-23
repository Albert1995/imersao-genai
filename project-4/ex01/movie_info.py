import json
import os
from dotenv import load_dotenv
import google.generativeai as genai
from groq import Groq

load_dotenv()

def create_prompt(movie):
    return f"""
    Provide information about the movie "{movie}" in JSON format.
    Start your response with:
    {{
    "title": "{movie}",
    """

def query_gemini(prompt):
    genai.configure(api_key=os.environ['GEMINI_API_KEY'])
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text


def query_groq(prompt) -> str:
    client = Groq(api_key=os.environ['GROQ_API_KEY'])
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
            {
                'role': 'assistant',
                'content': '{'
            }
        ],
        model="llama3-8b-8192",
    )
    return '{' + chat_completion.choices[0].message.content



def get_movie_info(movie):
    try:
        user_prompt = create_prompt(movie)
        model_response = query_groq(user_prompt)
        if model_response.startswith('{') and model_response.endswith('}'):
            return json.loads(model_response)
        return None
    except Exception:
        return None



movie_titles = ["The Matrix", "Inception", "Pulp Fiction", "The Shawshank Redemption", "The Godfather"]
for title in movie_titles:
    print(f"\nAnalyzing: {title}")
    result = get_movie_info(title)
    if result:
        for key, value in result.items():
            if key not in ['name', 'year', 'director', 'genre', 'plot_summary']: continue
            print(f"{key}: {value}")
    else:
        print('Error: Failed to generate valid JSON')
    print("-" * 50)
