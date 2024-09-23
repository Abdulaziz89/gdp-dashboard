import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def calculate_mortgage(property_value, initial_pay_percent, interest_rate, loan_term):
    down_payment = property_value * (initial_pay_percent / 100)
    loan_amount = property_value - down_payment
    monthly_rate = interest_rate / 100 / 12
    number_of_payments = loan_term * 12

    monthly_payment = (loan_amount * 
                       (monthly_rate * (1 + monthly_rate) ** number_of_payments) / 
                       ((1 + monthly_rate) ** number_of_payments - 1))

    schedule = []
    balance = loan_amount
    total_interest = 0

    for month in range(1, int(number_of_payments) + 1):
        interest_payment = balance * monthly_rate
        principal_payment = monthly_payment - interest_payment
        balance -= principal_payment
        total_interest += interest_payment

        if month <= 5 or month > number_of_payments - 5:
            schedule.append({
                'Month': month,
                'Payment': monthly_payment,
                'Principal': principal_payment,
                'Interest': interest_payment,
                'Remaining Balance': max(0, balance)
            })

    return monthly_payment, loan_amount, total_interest, schedule

st.title('Saudi Mortgage Calculator')

col1, col2 = st.columns(2)

with col1:
    property_value = st.number_input('Property Value (SAR)', min_value=0.0, value=500000.0, step=10000.0)
    initial_pay_percent = st.number_input('Initial Payment (%)', min_value=0.0, max_value=100.0, value=20.0, step=1.0)

with col2:
    interest_rate = st.number_input('Annual Interest Rate (%)', min_value=0.0, max_value=30.0, value=5.0, step=0.1)
    loan_term = st.number_input('Loan Term (Years)', min_value=1, max_value=30, value=25, step=1)

if st.button('Calculate'):
    monthly_payment, loan_amount, total_interest, schedule = calculate_mortgage(
        property_value, initial_pay_percent, interest_rate, loan_term)

    st.subheader('Results')
    col1, col2, col3 = st.columns(3)
    col1.metric('Loan Amount', f'{loan_amount:,.2f} SAR')
    col2.metric('Monthly Payment', f'{monthly_payment:,.2f} SAR')
    col3.metric('Total Interest', f'{total_interest:,.2f} SAR')

    # Payment Breakdown Pie Chart
    fig = go.Figure(data=[go.Pie(
        labels=['Principal', 'Total Interest'],
        values=[loan_amount, total_interest],
        hole=.3
    )])
    fig.update_layout(title='Payment Breakdown')
    st.plotly_chart(fig)

    # Amortization Schedule
    st.subheader('Amortization Schedule')
    df = pd.DataFrame(schedule)
    df = df.style.format({
        'Payment': '{:,.2f}',
        'Principal': '{:,.2f}',
        'Interest': '{:,.2f}',
        'Remaining Balance': '{:,.2f}'
    })
    st.dataframe(df)

    # Additional information
    st.info(f"This schedule shows the first 5 and last 5 payments of your {loan_term}-year mortgage.")