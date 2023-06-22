import pandas as pd
import streamlit as st


class Comparator:
    def __init__(self,  loan_data, loan_amount, special_type=None, only_banks=False, pay_timme=None):
        """
        Initialize a Loan instance.

        Args:
            loan_data (pd.DataFrame): The loan data table (as a pandas DataFrame)
            loan_amount (float): The total loan amount.
            special_type (str): The special type of loan, defaults to none.
            only_banks (bool): Whether to only show loans from banks, defaults to False.
        """

        self.loan_amount = loan_amount
        self.special_type = special_type
        self.loan_data = loan_data # pd.read_csv('/Users/martinpanacek/Srovnavac/data/loan_data_demo.csv', sep=';')
        self.only_banks = only_banks

        self.available_loans = self.compare_loans(self.loan_data, self.loan_amount, self.special_type, self.only_banks)
        self.recommended_loan = self.available_loans.iloc[0]

    @staticmethod
    @st.cache_data
    def compare_loans(loan_data, loan_amount, special_type='none', only_banks=False, pay_time=None):
        """
        Select suitable loans based on loan amount and special type, then sort them by interest rate.

        Returns:
            pd.DataFrame: A pandas DataFrame with suitable loans sorted by interest rate.
        """

        if special_type == 'none':
            loans = loan_data.query('special_cat=="none"')
        else:
            loans = loan_data.query('special_cat=="none" or special_cat==@special_type')

        if only_banks:
            loans = loans.query('non_bank==0')

        if pay_time is not None:
            loans = loans.query('max_len>=@pay_time and min_len<=@pay_time')

        loans = loans.query('max_amt>=@loan_amount and min_amt<=@loan_amount') \
            .sort_values('min_rate') \
            .reset_index(drop=True)

        return loans
