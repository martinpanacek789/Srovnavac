import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.title("Srovnávač půjček")

if st.button("Srovnat půjčky"):
    switch_page("Srovnání půjček")

st.header("O projektu")

st.markdown("Jsme skupina studentů z FIS VŠE, kteři se v rámci datového projektu věnovali vytvoření srovnávače půjček "
            "pro mladé lidi ve spolupráci s neziskovým projektem Zlatá Koruna.\n")

st.markdown("Aplikace je založena na moderních technologiích, obsahuje textové vyhledávání využívající umělou "
            "inteligenci a další funkce, které umožnují uživateli snadno a rychle najít odpovídaící půjčku.\n")

st.markdown("Děkujeme, že jste navštívili naši aplikaci a doufáme, že se Vám bude líbit.\n"
            "Tým studentů datové analytiky FIS VŠE")





