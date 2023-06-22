# 02_Textové_Vyhledávání.py
import streamlit as st

import pandas as pd
import plotly.graph_objects as go
import openai

from modules.comparator import Comparator
from modules.loan import Loan
from modules.change_page import nav_page


@st.cache_data
def load_loan_data():
    df = pd.read_csv('data/in/tables/loan_data_final.csv')
    return df


openai.api_key = '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'

@st.cache_data
def process_text_input(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user",
             "content": f'"Extract the loan amount and loan length in months and/or max possible repayment '
                        f'from the following sentence, return only numbers separated by semicolon.'
                        f'"If some of the variables is not in the text, return 0 for it"'
                        f' \n\n {text}'}
        ])

    return response['choices'][0]['message']['content'].split(";")

def create_pie_chart(labels, values):
    pie = go.Figure(data=[go.Pie(labels=labels, values=values)])
    return pie


hide_table_row_index = """
        <style>
        thead tr th:first-child {display:none}
        tbody th {display:none}
        </style>
        """


if 'calculated' not in st.session_state or st.session_state.calculated is False:
    st.session_state.calculated = False
    st.session_state.available_loans_name = []

st.title("Textové vyhledávání")

st.write("Zde je možné zadat textový popis a vyhledat odpovídající půjčku.")

input_text = st.text_input('Enter a value:', value=1.0, key='a')

if st.button('Vyhledat'):

    # res = process_text_input(input_text)

    res = ['100000', '36', '5000']

    if len(res) != 3:
        st.write("Někde se stala chyba, zkuste to znova.")
    elif res[0] == '0':
        st.write("Text neobsahuje částku půjčky, zkuste to znova.")
        loan_amt = res[0]
        pay_time = res[1]
        pay_amt = res[2]

        st.write(f"Castka: {loan_amt}")
        st.write(f"Doba: {pay_time}")
        st.write(f"Min splatka: {pay_amt}")
    elif res[1] == '0' and res[2] == '0':
        st.write("Někde se stala chyba, zkuste to znova.")
        loan_amt = res[0]
        pay_time = res[1]
        pay_amt = res[2]

        st.write(f"Castka: {loan_amt}")
        st.write(f"Doba: {pay_time}")
        st.write(f"Min splatka: {pay_amt}")
    else:
        loan_amt = float(res[0])
        pay_time = int(res[1])
        pay_amt = float(res[2])

        st.write(f"Castka: {loan_amt}")
        st.write(f"Doba: {pay_time}")
        st.write(f"Min splatka: {pay_amt}")

        comparator = Comparator(load_loan_data(), loan_amt, only_banks=True)

        st.session_state.available_loans = comparator.available_loans

        available_loans = comparator.available_loans['product_name'].tolist()

        st.session_state.available_loans_name = comparator.available_loans['product_name'].tolist()

        st.session_state.calculated = True

        int_rate = float(comparator.available_loans['min_rate'][0]/100)

if st.session_state.calculated:
    # Show the best loans
    st.write(f"Nejlepší půjčky pro vás:")

    st.dataframe(data=st.session_state.available_loans,
                 hide_index=True,
                 # use_container_width=True,
                 column_config={
                     "product_name": "Název Produktu",
                     "zk_award": st.column_config.TextColumn(
                         "Ocenění ZK",
                         width="medium"),
                     "delay": "Odklad",
                     "min_amt": st.column_config.NumberColumn(
                        "Minimální částka",
                         format="%.0f Kč"
                     ),
                     "max_amt": st.column_config.NumberColumn(
                        "Maximální částka",
                         format="%.0f Kč"
                     ),
                     "min_len": None,
                     "max_len": None,
                     "min_rate": "Minimální úrok",
                     "non_bank": None,
                     "online": "Sjednání online",
                     "special_cat": None,
                     "link": st.column_config.LinkColumn(
                         "Odkaz"
                     ),
                 })

    selected_loan = st.selectbox('Vyberte půjčku', st.session_state.available_loans_name)

    int_rate = float(st.session_state.available_loans[
                   st.session_state.available_loans['product_name'] == selected_loan]['min_rate'].iloc[0])

    if pay_time > 0 and pay_amt > 0:
        pay_time_2 = pay_time
        pay_amt_2 = None

    loan = Loan(loan_amt, int_rate/100, loan_length=pay_time_2, max_monthly_payment=pay_amt_2)

    # Total interest paid
    st.write(f"Měsíční splátka: {round(loan.monthly_payment, 2)}")
    st.write(f"Celkem úrok: {round(loan.total_interest, 2)}")
    st.write(f"Celková splatná částka: {round(loan.total_amount_paid, 2)}")
    st.write(f"Počet splátek: {round(loan.payment_plan.Month.max(), 0)}")

    fig = create_pie_chart(['Celková splatná částka', 'Celkem úrok'],
                           [round(loan.total_amount_paid, 2), round(loan.total_interest, 2)])

    st.plotly_chart(fig, use_container_width=True)

    # Display the payment plan
    st.subheader("Plán splácení:")
    st.markdown(hide_table_row_index, unsafe_allow_html=True)

    # Display the output table
    st.table(loan.payment_plan)

    if st.button('Více informací'):
        nav_page("FAQ")