from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

def query_groq(prompt: str) -> str:
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


def run_prompt_chain():
    prompt = f"""Quem foi Claude Elwood Shannon?"""
    response_1 = query_groq(prompt)
    
    prompt = f"""Quais foram suas principais contribuições para a teoria da informação?
    <shannon_summary>
    {response_1}
    </shannon_summary>
    """
    response_2 = query_groq(prompt)

    prompt = f"""E os impactos que essas contribuições trouxeram para a computação moderna e nas tecnologias da computação
    <main_contributions>
    {response_2}
    </main_contributions>
    """
    response_3 = query_groq(prompt)

    prompt = f"""Sintetize as informações e monte um resumo sobre Claude Elwood Shannon e sua influencia na tecnologia
    <shannon_summary>
    {response_1}
    </shannon_summary>
    <main_contributions>
    {response_2}
    </main_contributions>
    <contributions_impacts>
    {response_3}
    </contributions_impacts>
    """
    print(query_groq(prompt))


if __name__ == "__main__":
    run_prompt_chain()