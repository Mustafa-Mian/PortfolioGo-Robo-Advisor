import streamlit as st

stocks_page = st.Page("stocks.py", title="Enter your stocks", icon=":material/variable_add:")
clean_page = st.Page("clean.py", title="Cleaning your stocks", icon=":material/mop:")
param_page = st.Page("param.py", title="Define your investment amount", icon=":material/account_balance:")
result_page = st.Page("result.py", title="Create your portfolio", icon=":material/settings:")

pg = st.navigation([stocks_page, clean_page, param_page, result_page], position='hidden')

# --- Page Config ---
st.set_page_config(page_title="PortfolioGo!", layout="centered", page_icon="📈")

pg.run()
