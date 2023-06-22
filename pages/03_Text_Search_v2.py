import streamlit as st
from streamlit_option_menu import option_menu

import pandas as pd
import plotly.graph_objects as go
import openai

from modules.loan import Loan
from modules.comparator import Comparator
from modules.change_page import nav_page


@st.cache_data
def load_loan_data():
    df = pd.read_csv('data/in/tables/loan_data_final.csv')
    return df


openai.api_key = st.secrets["OPENAI_API_KEY"]

#'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'

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


st.title("Srovnání půjček")

loan_amt_2 = 100_000
pay_time_2 = 36
pay_amt_2 = None
special_loan_case_2 = 0

if 'calculated_2' not in st.session_state or st.session_state.calculated_2 is False:
    st.write("Enter a value:")
    st.session_state.calculated_2 = False
    st.session_state.available_loans_name_2 = []


st.write("Zde je možné zadat textový popis a vyhledat odpovídající půjčku.")

input_query = st.text_input('Zadejte popis:')

gpt_output = None

if st.button('Vyhledat'):
    gpt_output = process_text_input(input_query)


st.write(input_query)
st.write(gpt_output)

comp2 = st.checkbox('Zobrazit')

if comp2:
    comparator_2 = Comparator(load_loan_data(), loan_amt_2, only_banks=True)

    st.session_state.available_loans_2 = comparator_2.available_loans

    available_loans_2 = comparator_2.available_loans['product_name'].tolist()

    st.session_state.available_loans_name_2 = comparator_2.available_loans['product_name'].tolist()

    int_rate = float(comparator_2.available_loans['min_rate'][0]/100)

    # Initialize a Loan instance
    loan_2 = Loan(loan_amt_2, int_rate, loan_length=pay_time_2, max_monthly_payment=pay_amt_2)

    st.session_state.calculated_2 = True
else:
    st.session_state.calculated_2 = False

if st.session_state.calculated_2:
    # Show the best loans
    st.write(f"Nejlepší půjčky pro vás:")

    st.dataframe(data=st.session_state.available_loans_2,
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

    selected_loan_2 = st.selectbox('Vyberte půjčku', st.session_state.available_loans_name_2)

    int_rate = float(st.session_state.available_loans_2[
                   st.session_state.available_loans_2['product_name'] == selected_loan_2]['min_rate'].iloc[0])

    loan_2 = Loan(loan_amt_2, int_rate/100, loan_length=pay_time_2, max_monthly_payment=pay_amt_2)

    # Total interest paid
    st.write(f"Měsíční splátka: {round(loan_2.monthly_payment, 2)}")
    st.write(f"Celkem úrok: {round(loan_2.total_interest, 2)}")
    st.write(f"Celková splatná částka: {round(loan_2.total_amount_paid, 2)}")
    st.write(f"Počet splátek: {round(loan_2.payment_plan.Month.max(), 0)}")

    fig = create_pie_chart(['Celková splatná částka', 'Celkem úrok'],
                           [round(loan_2.total_amount_paid, 2), round(loan_2.total_interest, 2)])

    st.plotly_chart(fig, use_container_width=True)

    # Display the payment plan
    if st.checkbox('Zobrazit plán splácení'):
        st.subheader("Plán splácení:")

        st.dataframe(data=loan_2.payment_plan,
                     hide_index=True,
                     use_container_width=True,
                     column_config={
                        "Month": "Měsíc",
                        "Monthly Payment": st.column_config.NumberColumn("Měsíční splátka", format="%.2f Kč"),
                        "Interest Paid": st.column_config.NumberColumn("Úrok", format="%.2f Kč"),
                        "Principal Paid": st.column_config.NumberColumn("Jistina", format="%.2f Kč"),
                        "Remaining Balance": st.column_config.NumberColumn("Zbývající dluh", format="%.2f Kč")
                     })

    if st.button('Více informací'):
        nav_page("FAQ")

