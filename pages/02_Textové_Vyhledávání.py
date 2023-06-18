# 02_Textové_Vyhledávání.py
import streamlit as st

import pandas as pd

st.title("Textové vyhledávání")

st.write("Zde je možné zadat textový popis a vyhledat odpovídající půjčku.")

input_value = st.text_input('Enter a value:', value=1.0, key='a')

@st.cache_data
def load_loan_data():
    df = pd.read_csv('data/loan_data_demo.csv', sep=';')
    return df


if st.button('Vyhledat'):
    st.write('Hledám půjčky pro Vás...')
