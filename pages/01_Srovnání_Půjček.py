# 01_Srovnání_Půjček.py
import streamlit as st
from streamlit_option_menu import option_menu

import pandas as pd
import plotly.graph_objects as go

from modules.loan import Loan
from modules.comparator import Comparator
from modules.change_page import nav_page


@st.cache_data
def load_loan_data():
    df = pd.read_csv('data/in/tables/loan_data_final.csv')
    return df


def create_pie_chart(labels, values):
    pie = go.Figure(data=[go.Pie(labels=labels, values=values)])
    return pie

st.title("Srovnání půjček")

st.write("Rozhodnutí ohledně financí a půjček může být pro mladé lidi obtížné. "
         "S naším nekomerčním porovnávačem spotřebitelských půjček "
         "získáte přehled o nabídkách od různých poskytovatelů."
         "Díky personalizovanému vyhledávání najdete půjčku Vám přesně na míru!\n")


st.write("Zde je možné zadat parametry půjčky a vyhledat odpovídající půjčky "
         "nebo vyzkoušet jednu z přednastavených variant.")

dummy_option = option_menu(None,
                           ['Vlastní parametry', "Bydlení", "Auto", "Studium", "Zahraniční pobyt"],
                           icons=['gear', 'house', 'car-front', "book", "airplane"],
                           menu_icon="cast", default_index=0, orientation="horizontal")

loan_amt_init = 100_000
pay_time_init = 36
pay_amt_init = 5_000
special_loan_case_init = 0

if dummy_option == 'Bydlení':
    loan_amt_init = 500_000
    pay_time_init = 120
    pay_amt_init = 15_000
    special_loan_case_init = 2
elif dummy_option == 'Auto':
    loan_amt_init = 250_000
    pay_time_init = 60
    pay_amt_init = 10_000
    special_loan_case_init = 1
elif dummy_option == 'Studium':
    loan_amt_init = 200_000
    pay_time_init = 48
    pay_amt_init = 5_000
    special_loan_case_init = 3
elif dummy_option == 'Zahraniční pobyt':
    loan_amt_init = 150_000
    pay_time_init = 36
    pay_amt_init = 5_000

with st.sidebar:
    loan_amt = st.number_input('Kolik si chci půjčit:', value=loan_amt_init, step=1_000)
    income_amt = st.number_input('Čistý měsíční příjem:', value=40_000, step=1_000)

    calc_type = st.radio("Chci", ('Zadat dobu splácení', 'Zadat kolik můžu splácet'))

    if calc_type == 'Zadat kolik můžu splácet':
        pay_amt = st.number_input('Kolik můžu splácet:', value=pay_amt_init, step=1_000)
        pay_time = None
    else:
        pay_time = st.number_input('Doba splácení (měsíce):', value=pay_time_init, step=1)
        pay_amt = None

    special_loan_case = st.radio('Speciální případ', ('Ne', 'Auto', 'Bydlení', 'Studium', 'Konsolidace'),
                                 index=special_loan_case_init)

    show_payment_plan = st.checkbox('Ukázat plán splácení')
    only_banks = st.checkbox('Pouze bankovní půjčky')

    comp = st.button('Zobrazit')

    st.markdown('<br>' * 3, unsafe_allow_html=True)

st.header("Výsledky:")

if 'calculated' not in st.session_state or st.session_state.calculated is False:
    if dummy_option == "Vlastní parametry":
        st.write("Nejprve vyplňte formulář a stiskněte tlačítko Zobrazit")
    else:
        st.write("Stiskněte tlačítko Zobrazit, případně nejdříve upravte parametry půjčky")
    st.session_state.calculated = False
    st.session_state.available_loans_name = []

if comp:
    # Compare available loans
    comparator = Comparator(load_loan_data(), loan_amt, special_loan_case, only_banks, pay_time)

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

    loan = Loan(loan_amt, int_rate/100, loan_length=pay_time, max_monthly_payment=pay_amt)

    # Total interest paid
    st.write(f"Měsíční splátka: {round(loan.monthly_payment, 2)}")
    st.write(f"Celkem úrok: {round(loan.total_interest, 2)}")
    st.write(f"Celková splatná částka: {round(loan.total_amount_paid, 2)}")
    st.write(f"Počet splátek: {round(loan.payment_plan.Month.max(), 0)}")
    st.write(f"Procent z příjmů: {round((loan.monthly_payment / income_amt) * 100, 1)} %")

    fig = create_pie_chart(['Celková splatná částka', 'Celkem úrok'],
                           [round(loan.total_amount_paid, 2), round(loan.total_interest, 2)])

    st.plotly_chart(fig, use_container_width=True)

    # Display the payment plan
    if show_payment_plan:
        st.subheader("Plán splácení:")

        # Display the output table
        st.dataframe(data=loan.payment_plan,
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
