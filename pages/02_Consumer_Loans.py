# 02_Consumer_Loans.py
import streamlit as st
import pandas as pd
from modules.loan import Loan
from modules.comparator import Comparator

@st.cache_data
def load_loan_data():
    df = pd.read_csv('in/tables/loan_data_demo.csv')
    return df


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

    calc_type = st.radio("Chci", ('Zadat kolik můžu splácet', 'Zadat dobu splácení'))

    if calc_type == 'Zadat kolik můžu splácet':
        pay_amt = st.number_input('Kolik můžu splácet:', value=1_000)
        pay_time = None
    else:
        pay_time = st.number_input('Doba splácení:', value=36)
        pay_amt = None

    special_loan_case = st.radio('Speciální případ',
                                    ('Ne','Auto', 'Bydlení', 'Studium', 'Konsolidace'))

    show_payment_plan = st.checkbox('Ukázat plán splácení')
    only_banks = st.checkbox('Pouze bankovní půjčky')

    comp = st.button('Zobrazit')


st.write("Some text here")

st.header("Výsledky:")

if 'calculated' not in st.session_state:
    st.write("Loading data...")
    st.session_state.calculated = False
    st.write(st.session_state.calculated)
    st.session_state.available_loans_name = []

if comp:
    # Compare available loans
    comparator = Comparator(load_loan_data(), loan_amt, special_loan_case, only_banks)

    st.session_state.available_loans = comparator.available_loans

    # selected_loan = st.selectbox('Vyberte půjčku', comparator.available_loans['product_name'])

    available_loans = comparator.available_loans['product_name'].tolist()

    st.session_state.available_loans_name = comparator.available_loans['product_name'].tolist()

    st.session_state.calculated = True

    # interest_rate = comparator.available_loans[comparator.available_loans['product_name'] == selected_loan]['min_rate']/100

    int_rate = float(comparator.available_loans['min_rate'][0]/100)

    # Initialize a Loan instance
    loan = Loan(loan_amt, int_rate, loan_length=pay_time, max_monthly_payment=pay_amt)

    # Total interest paid
    st.write(f"Monthly payment: {round(loan.monthly_payment, 2)}")
    st.write(f"Total interest paid: {round(loan.total_interest, 2)}")
    st.write(f"Total amount paid: {round(loan.total_amount_paid, 2)}")


if st.session_state.calculated:
    # Show the best loans
    st.write(f"Nejlepší půjčky pro vás:")
    st.markdown(hide_table_row_index, unsafe_allow_html=True)
    st.table(st.session_state.available_loans.head(5))

    selected_loan = st.selectbox('Vyberte půjčku', st.session_state.available_loans_name)

    st.write(selected_loan)

    int_rate = float(st.session_state.available_loans[
                   st.session_state.available_loans['product_name'] == selected_loan]['min_rate'])

    st.write(int_rate)

    loan = Loan(loan_amt, int_rate/100, loan_length=pay_time, max_monthly_payment=pay_amt)

    # Total interest paid
    st.write(f"Monthly payment: {round(loan.monthly_payment, 2)}")
    st.write(f"Total interest paid: {round(loan.total_interest, 2)}")
    st.write(f"Total amount paid: {round(loan.total_amount_paid, 2)}")

    # Display the payment plan
    if show_payment_plan:
        st.markdown(hide_table_row_index, unsafe_allow_html=True)

        # Display the output table
        st.table(loan.payment_plan)

st.header("FAQ:")

