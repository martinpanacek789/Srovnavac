# 01_Srovnání_Půjček.py
import streamlit as st

import pandas as pd
import plotly.graph_objects as go

from modules.loan import Loan
from modules.comparator import Comparator
from modules.change_page import nav_page

@st.cache_data
def load_loan_data():
    df = pd.read_csv('data/in/tables/loan_data_demo.csv')
    return df


def create_pie_chart(labels, values):
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    return fig


hide_table_row_index = """
        <style>
        thead tr th:first-child {display:none}
        tbody th {display:none}
        </style>
        """


def change_callback():
    print("Callback called")


st.title("Srovnání půjček")

with st.sidebar:
    loan_amt = st.number_input('Kolik si chci půjčit:', value=100_000)
    income_amt = st.number_input('Čistý měsíční příjem:', value=100_000)

    calc_type = st.radio("Chci", ('Zadat dobu splácení', 'Zadat kolik můžu splácet'))

    if calc_type == 'Zadat kolik můžu splácet':
        pay_amt = st.number_input('Kolik můžu splácet:', value=1_000, step=1_000)
        pay_time = None
    else:
        pay_time = st.number_input('Doba splácení (měsíce):', value=36)
        pay_amt = None

    special_loan_case = st.radio('Speciální případ', ('Ne', 'Auto', 'Bydlení', 'Studium', 'Konsolidace'))

    show_payment_plan = st.checkbox('Ukázat plán splácení')
    only_banks = st.checkbox('Pouze bankovní půjčky')

    comp = st.button('Zobrazit')


st.write("Rozhodnutí ohledně financí a půjček může být pro mladé lidi obtížné. "
         "S naším nekomerčním porovnávačem spotřebitelských půjček "
         "získáte přehled o nabídkách od různých poskytovatelů."
         "Díky personalizovanému vyhledávání najdete půjčku Vám přesně na míru!")

st.header("Výsledky:")

if 'calculated' not in st.session_state or st.session_state.calculated is False:
    st.write("Nejprve vyplňte formulář a stiskněte tlačítko Zobrazit")
    st.session_state.calculated = False
    st.session_state.available_loans_name = []

if comp:
    # Compare available loans
    comparator = Comparator(load_loan_data(), loan_amt, special_loan_case, only_banks)

    st.session_state.available_loans = comparator.available_loans

    available_loans = comparator.available_loans['product_name'].tolist()

    st.session_state.available_loans_name = comparator.available_loans['product_name'].tolist()

    st.session_state.calculated = True

    int_rate = float(comparator.available_loans['min_rate'][0]/100)

    # Initialize a Loan instance
    loan = Loan(loan_amt, int_rate, loan_length=pay_time, max_monthly_payment=pay_amt)

if st.session_state.calculated:
    # Show the best loans
    st.write(f"Nejlepší půjčky pro vás:")
    st.markdown(hide_table_row_index, unsafe_allow_html=True)
    st.table(st.session_state.available_loans.head(5))

    selected_loan = st.selectbox('Vyberte půjčku', st.session_state.available_loans_name)

    int_rate = float(st.session_state.available_loans[
                   st.session_state.available_loans['product_name'] == selected_loan]['min_rate'].iloc[0])

    loan = Loan(loan_amt, int_rate/100, loan_length=pay_time, max_monthly_payment=pay_amt)

    # Total interest paid
    st.write(f"Měsíční splátka: {round(loan.monthly_payment, 2)}")
    st.write(f"Celkem úrok: {round(loan.total_interest, 2)}")
    st.write(f"Celková splatná částka: {round(loan.total_amount_paid, 2)}")

    fig = create_pie_chart(['Celková splatná částka', 'Celkem úrok'],
                           [round(loan.total_amount_paid, 2), round(loan.total_interest, 2)])

    st.plotly_chart(fig)

    # Display the payment plan
    if show_payment_plan:
        st.subheader("Plán splácení:")
        st.markdown(hide_table_row_index, unsafe_allow_html=True)

        # Display the output table
        st.table(loan.payment_plan)

    if st.button('Více informací'):
        nav_page("FAQ")

