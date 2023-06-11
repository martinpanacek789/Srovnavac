import pandas as pd
import numpy as np
import numpy_financial as npf


class Loan:
    def __init__(self, loan_amount, interest_rate, loan_length=None, max_monthly_payment=None):
        """
        Initialize a Loan instance.

        Args:
            loan_amount (float): The total loan amount.
            interest_rate (float): The annual interest rate (as a decimal).
            loan_length (int, optional): The length of the loan in months. Defaults to None.
            max_monthly_payment (float, optional): The maximum amount the user can pay monthly. Defaults to None.
        """
        self.loan_amount = loan_amount
        self.interest_rate = interest_rate

        if loan_length is None and max_monthly_payment is None:
            raise ValueError("Either loan_length or max_monthly_payment must be provided.")

        if loan_length is not None and max_monthly_payment is not None:
            raise ValueError("Only one of loan_length or max_monthly_payment can be provided.")

        if loan_length is not None:
            self.loan_length = loan_length
            self.monthly_payment = self.calculate_monthly_payment()
        else:
            self.max_monthly_payment = max_monthly_payment
            self.loan_length = npf.nper(self.interest_rate / 12, -self.max_monthly_payment, self.loan_amount)
            self.loan_length = int(np.ceil(self.loan_length))
            self.monthly_payment = self.calculate_monthly_payment()

        self.payment_plan = self.calculate_payment_plan()
        self.total_interest = self.payment_plan["Interest Paid"].sum()
        self.total_amount_paid = self.total_interest + self.loan_amount

    def calculate_payment_plan(self):
        """
        Calculate the monthly payment plan based on loan amount, interest rate, and loan length.

        Returns:
            pd.DataFrame: A pandas DataFrame representing the payment plan.
                         Each row contains the month number, monthly payment, interest paid, principal paid, and remaining balance.
        """
        monthly_interest_rate = self.interest_rate / 12
        monthly_payment = self.monthly_payment

        plan = []
        remaining_balance = self.loan_amount

        for month in range(1, self.loan_length + 1):
            interest_paid = remaining_balance * monthly_interest_rate
            principal_paid = min(monthly_payment - interest_paid, remaining_balance)
            remaining_balance -= principal_paid

            payment_details = {
                "Month": month,
                "Monthly Payment": round(monthly_payment, 2),
                "Interest Paid": round(interest_paid, 2),
                "Principal Paid": round(principal_paid, 2),
                "Remaining Balance": round(remaining_balance, 2)
            }

            plan.append(payment_details)

        payment_plan_df = pd.DataFrame(plan)
        return payment_plan_df

    def calculate_monthly_payment(self):
        """
        Calculate the maximum monthly payment based on loan amount, interest rate, and loan length.

        Returns:
            float: The maximum monthly payment amount.
        """
        monthly_interest_rate = self.interest_rate / 12
        max_monthly_payment = (self.loan_amount * monthly_interest_rate) /\
                              (1 - (1 + monthly_interest_rate) ** -self.loan_length)
        return max_monthly_payment
