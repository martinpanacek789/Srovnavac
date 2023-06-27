import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.title("Srovnávač půjček")

st.write("Přejít na")

col1, col2 = st.columns(2)
with col1:
    if st.button("Srovnání půjček", key="srovnani_pujcek", use_container_width=True):
        switch_page("Srovnání půjček")
        # st.write("Srovnání půjček")

with col2:
    if st.button("Textové vyhledávání", key="textove_vyhledavani", use_container_width=True):
        switch_page("Textové vyhledávání")
        # st.write("Textové vyhledávání")

st.header("O projektu")

st.markdown("Jsme skupina studentů z FIS VŠE, kteři se v rámci datového projektu věnovali vytvoření srovnávače půjček "
            "pro mladé lidi ve spolupráci s neziskovým projektem Zlatá Koruna.\n")

st.markdown("Aplikace je založena na moderních technologiích, obsahuje textové vyhledávání využívající umělou "
            "inteligenci a další funkce, které umožnují uživateli snadno a rychle najít odpovídající půjčku.\n")

st.markdown("Děkujeme, že jste navštívili naši aplikaci a doufáme, že se Vám bude líbit.\n"
            "Tým studentů datové analytiky FIS VŠE")

st.image('data/in/files/ZK_logo.png', use_column_width=True)


