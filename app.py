import streamlit as st

st.set_page_config(page_title="Break-even Revenue Simulator", layout='wide')
st.title("Break-even Revenue Simulator")
st.header("Input")

revenue = st.number_input("Revenue", min_value=0, value=None)
variable = st.number_input("Variable Cost", min_value=0, value=None)
fixed = st.number_input("Fixed Cost", min_value=0, value=None)
contribution = revenue - variable

calculate = st.button("Calculate")

if calculate:
    if revenue is None or variable is None or fixed is None:
        st.warning("Please enter Revenue, Variable Cost, and Fixed Cost")
    elif revenue <= 0:
        st.error("Revenue must be greater than 0")
    elif variable >= revenue:
        st.error("Variable Cost must be lower than Revenue")
    elif fixed >= revenue:
        st.error("Fixed Cost must be lower than Revenue.")
    else:
        contribution_margin = contribution/revenue
        break_even_revenue = fixed/contribution_margin
        profit = contribution - fixed
        margin_of_safety = revenue - break_even_revenue
        st.header("Result")
        st.metric("Contribution", f"{contribution:,.2f}")
        st.metric("Contribution Margin", f"{contribution_margin:,.2f}")
        st.metric("Break-even Revenue", f"{break_even_revenue:,.2f}")
        st.metric("Profit", f"{profit:,.2f}")
        st.metric("Margin of Safety", f"{margin_of_safety:,.2f}")