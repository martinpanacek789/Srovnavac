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
    # Create a Pandas DataFrame from the input value
    input_df = pd.DataFrame({'Input': [input_value]})

    # Perform calculations on the input data
    output_df = load_loan_data()

    hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

    st.markdown(hide_table_row_index, unsafe_allow_html=True)

    # Display the output table
    st.table(output_df)
