import streamlit as st

pages = {
    "": [
        st.Page("chat.py", title="Assistente virtual"),
        st.Page("training.py", title="Treinamento"),
    ]
}

pg = st.navigation(pages)
pg.run()
