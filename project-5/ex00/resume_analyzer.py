import chromadb
from chromadb.utils import embedding_functions
import os
import pdfplumber
import glob
import re

def process_pdf_directory(pdf_directory, collection: chromadb.Collection):
    pdf_files = glob.glob(os.path.join(pdf_directory, "**", "*.pdf"), recursive=True)
    print(f"Encontrados {len(pdf_files)} arquivos PDF no diretório.")

    for i, name in enumerate(pdf_files):
        filename = f"{name}"
        if not name.endswith(".pdf"): continue

        r = collection.get(
            ids=[name],
            where={"source": name},
        )
        
        print(f"Processando PDF {i + 1}/{len(pdf_files)}: {name}")

        if len(r['ids']) > 0:
            continue
        
        print(f"Extracting {name}")

        pdftext = ""
        with pdfplumber.open(filename) as f:
            for page in f.pages:
                pdftext += page.extract_text()

        # pdftext = pdftext.replace(r"Página \d de \d", "")
        pdftext = re.sub(r"Página \d de \d\n", "", pdftext)

        collection.add(
            ids=[name],
            metadatas=[{"source": name}],
            documents=[pdftext]
        )


def interactive_query_loop(collection: chromadb.Collection):
    while True:
        query = input("\nConsulta: ")
        if query.lower() == 'sair':
            break
        results = collection.query(
            query_texts=[query],
            n_results=3,
            include=['documents', 'metadatas']
        )
        
        print("\nResultados:")
        for document, metadata in zip(results['documents'][0], results['metadatas'][0]):
            print(f"Documento: {metadata['source']}")
            print(f"Trecho: {document[:200]}...") # Apenas os 200 primeiros caracteres
            print()

def main():
    persist_directory = "./chroma_data"
    pdf_directory = "./pdfs"
    
    # TODO: Configurar ChromaDB com persistência local
    chroma_client = chromadb.PersistentClient(path=persist_directory)
    
    # TODO: Criar embedding function
    # Dica: Experimente com diferentes modelos, como "paraphrase-multilingual-MiniLM-L12-v2"
    embedding_function = embedding_functions.DefaultEmbeddingFunction()
    
    # TODO: Criar ou obter uma coleção existente
    collection_name = 'curriculos'
    collection = chroma_client.get_or_create_collection(collection_name, embedding_function=embedding_function)
    
    # TODO: Implementar a função process_pdf_directory
    process_pdf_directory(pdf_directory, collection)
    
    # TODO: Implementar a função interactive_query_loop
    interactive_query_loop(collection)

if __name__ == "__main__":
    main()

