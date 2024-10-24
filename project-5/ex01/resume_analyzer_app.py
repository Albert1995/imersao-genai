import streamlit as st
import pdfplumber
import chromadb
import re
from chromadb.utils import embedding_functions
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

collection: chromadb.Collection = None

def open_chroma():
    global collection
    persist_directory = "./chroma_data"
    chroma_client = chromadb.PersistentClient(path=persist_directory)
    embedding_function = embedding_functions.DefaultEmbeddingFunction()
    collection_name = 'curriculos'
    collection = chroma_client.get_or_create_collection(collection_name, embedding_function=embedding_function)

def process_pdf_file(pdf_file):
    global collection

    name = pdf_file.name

    r = collection.get(
        ids=[name],
        where={"source": name},
    )
    
    print(f"Processando PDF: {name}")

    if len(r['ids']) > 0:
        return
    
    pdftext = ""
    with pdfplumber.open(pdf_file) as f:
        for page in f.pages:
            pdftext += page.extract_text()

    # pdftext = pdftext.replace(r"Página \d de \d", "")
    pdftext = re.sub(r"Página \d de \d\n", "", pdftext)

    collection.add(
        ids=[name],
        metadatas=[{"source": name}],
        documents=[pdftext]
    )

def create_prompt(query, resumes):
    resumes = "\n".join([f"<resume>{r}</resume>" for r in resumes])
    return f"""
    <resumes>
    {resumes}
    </resumes>

    <question>
    {query}
    </question>

    Você irá atuar como um recrutador de uma empresa. Sua principal tarefa é avaliar os currículos presentes <resumes>.
    E depois de avaliar deverá decidir quais destes currículos responde melhor a pergunta <question></question>
    """

def query_groq(prompt) -> str:
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


def intro():
    import streamlit as st

    st.write("# Pesquisar Candidatos")
    st.sidebar.success("Select a demo above.")
    query = st.text_input("Faça uma pergunta sobre os candidatos:")
    if query:
        with st.spinner("Buscando resposta..."):
            global collection

            results = collection.query(
                query_texts=[query],
                n_results=3,
                include=['documents']
            )

            prompt = create_prompt(query, results['documents'][0])
            answer = query_groq(prompt)
            st.write(answer)

def upload_resumes():
    import streamlit as st

    st.markdown(f"# Subir Currículos")
    pdf_files = st.file_uploader("Escolhas os currículos em PDF", type="pdf", accept_multiple_files=True)

    if pdf_files:
        with st.spinner("Subindo currículos..."):
            for pdf_file in pdf_files:
                process_pdf_file(pdf_file)
        st.success("Currículos processados com sucesso!")

open_chroma()
page_names_to_funcs = {
    "Pesquisar Candidato": intro,
    "Subir Currículos": upload_resumes,
}

demo_name = st.sidebar.selectbox("Choose a demo", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()