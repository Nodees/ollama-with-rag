import os
from uuid import uuid4

import psycopg2
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader

from actions import splitter, get_or_create_collection
from utils import chroma_connect

DB_CONFIG = {
    "host": "localhost",
    "port": "5433",
    "dbname": "ollama",
    "user": "ollama",
    "password": "ollama"
}

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def save_file(uploaded_file):
    file_path = os.path.join(UPLOAD_DIR, f"{uploaded_file.name}")
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return str(uploaded_file.name)


def insert_file_record(file_name):
    collection = get_or_create_collection(chroma_connect())
    loader = PyPDFLoader(f'./{UPLOAD_DIR}/{file_name}', extract_images=False)
    splits = loader.load_and_split(text_splitter=splitter())

    if len(splits) == 0:
        st.warning("O arquivo está vazio ou não pode ser processado")
        return

    collection_identifier = str(uuid4())
    for i, chunk in enumerate(splits):
        collection.add(
            documents=[chunk.page_content],
            metadatas=[{
                "file_name": file_name,
                "chunk_index": i,
                "collection_identifier": collection_identifier
            }],
            ids=[str(uuid4())]
        )

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
                INSERT INTO training (name, code) VALUES ('{file_name}', '{collection_identifier}');
            """)
        conn.commit()


def list_uploaded_files():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name FROM training ORDER BY id;")
            rows = cur.fetchall()
    return [{"id": str(row[0]), "name": row[1]} for row in rows]


def training():
    st.title("Upload de Arquivos PDF com Registro no PostgreSQL")
    uploaded_file = st.file_uploader("Selecione um arquivo PDF", type=["pdf"])
    if uploaded_file is not None:
        file_name = save_file(uploaded_file)
        insert_file_record(file_name)
        st.success(f"Arquivo '{file_name}' enviado e registrado com sucesso!")

    st.subheader("Treinamentos")
    files = list_uploaded_files()
    if files:
        st.table(files)
    else:
        st.info("Nenhum treinamento ainda.")


if __name__ == '__main__':
    training()
