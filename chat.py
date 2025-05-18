import streamlit as st
from ollama import Client
from openai import OpenAI

from actions import build_contextual_prompt, query_chromadb, get_or_create_collection
from utils import chroma_connect

llama_client = Client(
    host='http://127.0.0.1:11434'
)

openai_client = OpenAI(
    api_key="<your-api-key-here>"
)


def generate_prompt(message):
    collection = get_or_create_collection(chroma_connect())
    docs = query_chromadb(collection, message)
    return build_contextual_prompt(docs, message)


def openai_answer(message):
    prompt = generate_prompt(message)
    print(prompt)
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                'role': 'system',
                'content': 'You are a userful assistant to respond every question in Portuguese Brazil'
            },
            {
                'role': 'user',
                'content': prompt
            }
        ]
    )

    return response.choices[0].message.content


def llama_answer(message):
    prompt = generate_prompt(message)
    print(prompt)
    response = llama_client.chat(
        model='llama3',
        messages=[
            {
                'role': 'system',
                'content': 'You are a userful assistant to respond every question in Portuguese Brazil'
            },
            {
                'role': 'user',
                'content': prompt
            }
        ]
    )
    return response['message']['content']


def display_messages_from_history():
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])


def app():
    get_response = {
        'LLaMA': llama_answer,
        'GPT-4o': openai_answer
    }

    model = st.radio(
        'Escolha o modelo:',
        options=['LLaMA', 'GPT-4o'],
        index=0,
        horizontal=True
    )

    if 'messages' not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({'role': 'assistant', 'content': 'Olá, como posso ajudar?'})

    display_messages_from_history()

    if user_message := st.chat_input('Type your message here...'):
        st.session_state.messages.append({'role': 'user', 'content': user_message})
        with st.chat_message('user'):
            st.write(user_message)

        with st.spinner('Processing...'):
            print(model)
            response = get_response.get(model, 'O modelo utilizado não foi encontrado ou não existe.')(user_message)

            st.session_state.messages.append({'role': 'assistant', 'content': response})
            with st.chat_message('assistant'):
                st.write(response)


if __name__ == '__main__':
    app()
