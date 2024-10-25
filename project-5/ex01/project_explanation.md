# Análise de currículos com RAG

## Visão geral do sistema
Este sistema é uma aplicação Streamlit para análise de currículos utilizando Retrieval-Augmented Generation (RAG). Ele permite aos usuários fazer upload de currículos em PDF, armazená-los em um banco de dados vetorial (Chroma), e realizar consultas sobre os candidatos usando processamento de linguagem natural.

## Componentes principais
1. Interface do usuário (Streamlit)
- Fornece uma interface web interativa para upload de currículos e realização de consultas.

2. Processamento de PDF (pdfplumber)
- Extrai texto de arquivos PDF de currículos.

3. Banco de dados vetorial (ChromaDB)
- Armazena e indexa o texto dos currículos para busca eficiente.

4. Modelo de linguagem (Groq)
- Utiliza um modelo de linguagem avançado para analisar currículos e responder perguntas.

5. Gerenciamento de ambiente (dotenv)
- Carrega variáveis de ambiente para configuração segura.

## Conceitos principais
- RAG (Retrieval-Augmented Generation): Técnica que combina recuperação de informações com geração de texto para produzir respostas mais precisas e contextualizadas.
- Embedding: Representação vetorial de texto que captura significado semântico, usado para busca eficiente.
- Prompt Engineering: Técnica de construção de instruções para modelos de linguagem para obter respostas desejadas.

## Fluxo de funcionamento
1. O usuário faz upload de currículos PDF através da interface Streamlit.
2. Os PDFs são processados, o texto é extraído e armazenado no ChromaDB.
3. O usuário faz uma pergunta sobre os candidatos.
4. O sistema recupera os currículos mais relevantes do ChromaDB.
5. Um prompt é construído com a pergunta e os currículos recuperados.
6. O prompt é enviado ao modelo Groq para análise.
7. A resposta do modelo é exibida ao usuário na interface Streamlit.