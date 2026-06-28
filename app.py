import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Break-even Revenue Simulator", layout='wide')
st.title("Break-even Revenue Simulator")
st.caption("Interactive tool for break-even analysis and business scenario evaluation")

st.sidebar.header("Input")

revenue = st.sidebar.number_input("Revenue", min_value=0, value=100)
variable = st.sidebar.number_input("Variable Cost", min_value=0, value=60)
fixed = st.sidebar.number_input("Fixed Cost", min_value=0, value=20)

st.sidebar.divider()
st.sidebar.markdown("""
<small>
<b>Built by W. Navin</b><br>
<i>Turning Operational Data into Better Decisions.</i><br>
🌐 <a href="https://callmenavin.github.io/Portfolio/">Portfolio</a> •
💻 <a href="https://github.com/CallmeNavin?tab=repositories">GitHub</a> •
💼 <a href="https://www.linkedin.com/in/navin826/">LinkedIn</a>

</small>
""", unsafe_allow_html=True)

if revenue is None or variable is None or fixed is None:
    st.warning("Missing Number")
elif revenue <= 0:
    st.error("Revenue must be greater than 0")
elif variable >= revenue:
    st.error("Variable Cost must be lower than Revenue")
elif fixed >= revenue:
    st.error("Fixed Cost must be lower than Revenue.")
else:
    contribution = revenue - variable
    contribution_margin = contribution/revenue
    break_even_revenue = fixed/contribution_margin
    profit = contribution - fixed
    margin_of_safety = revenue - break_even_revenue
    margin_of_safety_pct = margin_of_safety/revenue
    tab1, tab2, tab3 = st.tabs(["Calculator", "Scenario Analysis", "Business Insights"])
    with tab1:
        st.subheader("Current Business Performance")
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        col1.metric("Revenue", f"{revenue:,.2f}")
        col2.metric("Profit", f"{profit:,.2f}")
        col3.metric("Contribution", f"{contribution:,.2f}")
        col4.metric("Contribution Margin", f"{contribution_margin:.1%}")
        col5.metric("Break-even Revenue", f"{break_even_revenue:,.2f}")
        col6.metric("Margin of Safety", f"{margin_of_safety:,.2f}")
        st.subheader("Profit vs Revenue")
        revenue_range = list(range(0, int(revenue * 2) + 10, 10))
        df_chart = pd.DataFrame({"Revenue": revenue_range})
        variable_ratio = variable / revenue
        df_chart["Profit"] = (df_chart["Revenue"] - df_chart["Revenue"] * variable_ratio - fixed)
        positive_area = (
            alt.Chart(df_chart[df_chart["Profit"] >= 0])
            .mark_area(color="green", opacity=0.35)
            .encode(
                x=alt.X("Revenue:Q", title="Revenue"),
                y=alt.Y("Profit:Q", title="Profit"),
                tooltip=["Revenue", "Profit"]
            )
        )
        negative_area = (
            alt.Chart(df_chart[df_chart["Profit"] < 0])
            .mark_area(color="red", opacity=0.35)
            .encode(
                x="Revenue:Q",
                y="Profit:Q",
                tooltip=["Revenue", "Profit"]
            )
        )
        profit_line = (alt.Chart(df_chart).mark_line(color="#1565C0", point=True, strokeWidth=3).encode(x="Revenue:Q",y="Profit:Q",tooltip=["Revenue", "Profit"]))
        break_even_rule = (alt.Chart(pd.DataFrame({"Break Even Revenue": [break_even_revenue]})).mark_rule(strokeDash=[6, 6]).encode(x="Break Even Revenue:Q")) # tạo df mới chỉ có 1 dòng là cái break-even revenue, strokedash: đường nét đứt
        current_revenue_rule = (alt.Chart(pd.DataFrame({"Revenue": [revenue]})).mark_rule().encode(x="Revenue:Q"))
        st.altair_chart((positive_area + negative_area  + profit_line + break_even_rule + current_revenue_rule).properties(height=350),use_container_width=True) # combine 3 cái layer trên thành 1 cái chart. Properties height 350: chart cao 350 pixel, use_container_width=True: chart rộng bằng container, nếu k thì chart sẽ có chiều dài mặc định
    with tab2:
        st.subheader("Scenario Analysis")
        revenue_growth = st.slider("Revenue Growth (%)", -50, 100, 0) # st.slider(label,min,max,default)
        variable_cost_change = st.slider("Variable Cost Change (%)", -50, 100, 0)
        fixed_cost_change = st.slider("Fixed Cost Change (%)", -50, 100, 0)
        scenario_revenue = revenue * (1 + revenue_growth / 100)
        scenario_variable = variable * (1 + variable_cost_change / 100)
        scenario_fixed = fixed * (1 + fixed_cost_change / 100)
        scenario_contribution = scenario_revenue - scenario_variable
        scenario_profit = scenario_contribution - scenario_fixed
        col1, col2, col3 = st.columns(3)
        col1.metric("Scenario Revenue",f"{scenario_revenue:,.2f}",f"{scenario_revenue - revenue:,.2f}") # col1.metric("Scenario Revenue",value,delta
        col2.metric("Scenario Variable Cost",f"{scenario_variable:,.2f}",f"{scenario_variable - variable:,.2f}")
        col3.metric("Scenario Profit",f"{scenario_profit:,.2f}",f"{scenario_profit - profit:,.2f}")
        df_scenario = pd.DataFrame({"Case": ["Current", "Scenario"],"Profit": [profit, scenario_profit]})
        scenario_chart = (alt.Chart(df_scenario).mark_bar().encode(x=alt.X("Case:N", title="Case"),y=alt.Y("Profit:Q", title="Profit"),tooltip=["Case", "Profit"]))
        st.altair_chart(scenario_chart.properties(height=350), use_container_width=True)
    with tab3:
        st.subheader("Business Insights")
        if profit < 0:
            st.error("The business is currently below break-even") # Lời hay lỗ, nếu lỗ thì error sẽ là box màu đỏ
            st.write("Revenue is not enough to cover variable and fixed costs") # Giải thích nguyên nhân
        elif margin_of_safety_pct < 0.1: # Tại sao phải có cái này, vì có lời rồi nhưng có an toàn không?
            st.warning("The business is profitable, but the margin of safety is low") # Nên phải hiển thị warning box
            st.write("A small drop in revenue may push the business into loss")
        else:
            st.success("The business is operating above break-even") # Ổn thì hiện màu xanh
            st.write("Current revenue provides a reasonable safety buffer") # Giải thích
            st.markdown("### Key Concepts")
        with st.expander("What is Contribution Margin?"):
            st.write("Contribution Margin shows how much of each revenue unit remains after variable cost")
        with st.expander("What is Break-even Revenue?"):
            st.write("Break-even Revenue is the revenue level where profit equals zero")
        with st.expander("What is Margin of Safety?"):
            st.write("Margin of Safety shows how far current revenue is above break-even revenue")