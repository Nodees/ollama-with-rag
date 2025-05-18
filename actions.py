import tiktoken
from langchain_text_splitters import RecursiveCharacterTextSplitter

encoder = tiktoken.get_encoding("cl100k_base")


def splitter() -> RecursiveCharacterTextSplitter:
    return RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=lambda text: len(encoder.encode(text)),
    )


def query_chromadb(collection, question, n_results=3):
    results = collection.query(
        query_texts=[question],
        n_results=n_results
    )
    documents = results['documents'][0]
    return "\n".join(documents)


def build_contextual_prompt(docs: str, question: str) -> str:
    return f"""
                Você é um assistente útil que responde em português com base nas informações abaixo.
            
                Base de conhecimento:
                \"\"\"
                {docs}
                \"\"\"
                
                Pergunta:
                {question}
                
                Resposta:
            """


def get_or_create_collection(client):
    return client.get_or_create_collection(name="doc")
