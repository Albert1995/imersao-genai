from flask import Flask, request, jsonify, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_bcrypt import Bcrypt
from functools import wraps
import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
import uuid
import os
from werkzeug.utils import secure_filename
import pdfplumber
import re

app = Flask(__name__)
bcrypt = Bcrypt(app)
limiter = Limiter(get_remote_address, app=app, default_limits=["200 per day", "50 per hour"])

# Configurações para autenticação e autorização
USERS = {
    'admin': {'password': bcrypt.generate_password_hash('admin123').decode('utf-8'), 'role': 'admin'},
    'recruiter': {'password': bcrypt.generate_password_hash('recruiter123').decode('utf-8'), 'role': 'recruiter'},
    'candidate': {'password': bcrypt.generate_password_hash('candidate123').decode('utf-8'), 'role': 'candidate'}
}

# Iniciando o ChromaDB
client = chromadb.PersistentClient()
collection = client.get_or_create_collection('curriculos')

def check_role(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth = request.authorization
            if not auth or not USERS.get(auth.username) or not bcrypt.check_password_hash(USERS[auth.username]['password'], auth.password):
                return abort(401)
            if USERS[auth.username]['role'] not in role and 'any' not in role:
                return abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def chunk_text_recursive(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    return splitter.split_text(text)

def clean_text(text):
    page_number_pattern = r"Página\s+\d+\s+de\s+\d+\n"
    return re.sub(page_number_pattern, '', text)

@app.route('/upload_pdf', methods=['POST'])
@check_role(['candidate', 'admin'])
@limiter.limit("5 per minute")
def upload_pdf():
    if not request.files:
        return jsonify({'error': 'No file provided'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and file.filename.endswith('.pdf'):
        filename = secure_filename(file.filename)
        file_path = os.path.join("/tmp", filename)
        file.save(file_path)

        extracted_text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                extracted_text += clean_text(page.extract_text()) + "\n"

        # Fazer chunk do texto
        chunks = chunk_text_recursive(extracted_text)

        # Armazenar no ChromaDB
        doc_id = str(uuid.uuid4())
        collection.add(
            documents=chunks, 
            metadatas=[{'doc_id': doc_id, "chunk_id": i} for i in range(len(chunks))], 
            ids=[str(uuid.uuid4()) for _ in range(len(chunks))]
        )

        return jsonify({'message': 'PDF uploaded and processed', 'id': doc_id}), 201
    return jsonify({'error': 'Invalid file format, only PDFs are allowed'}), 400

@app.route('/search', methods=['GET'])
@check_role(['any'])
@limiter.limit("10 per minute")
def search():
    query = request.args.get('q')
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400
    
    # Realiza a busca semântica no ChromaDB
    results = collection.query(query_texts=[query], n_results=5)
    
    objects = [
        {
            "document": results['metadatas'][0][index]['doc_id'],
            "chunk_id": results['metadatas'][0][index]['chunk_id'],
            "content": results['documents'][0][index]
        }
        for index in range(len(results['ids'][0]))
    ]
    return jsonify(objects), 200

@app.route('/curriculum/<id>', methods=['DELETE'])
@check_role(['admin'])
def delete_curriculum(id):
    collection.delete(where={"doc_id": id})
    return jsonify({'message': 'Curriculum deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True)
