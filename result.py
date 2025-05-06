import streamlit as st
import pandas as pd
import generate as gen
import helpers as hp
from components import render_header, render_footer

# --- Custom CSS for style ---
st.markdown("""
    <style>
    .main {
        background-color: #f7f9fc;
    }
    .stButton>button {
        border-radius: 10px;
        border: 1px solid #4a90e2;
        background-color: #4a90e2;
        color: white;
    }
    .stTextInput>div>div>input {
        border-radius: 8px;
    }
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
    }
    </style>
""", unsafe_allow_html=True)

render_header()

st.write("It's time to create your portfolio! Let's see what we can do with the stocks you provided.")
if 'best_portfolios' not in st.session_state:
    st.session_state.best_portfolios = pd.DataFrame()
if 'back_testing_portfolios' not in st.session_state:
    st.session_state.back_testing_portfolios = {}

with st.spinner("Hang on - We're generating your portfolio. Please note this may take some time. We are generating over 10000 portfolios and backtesting them on over a year's worth of data to find the best one for you.", show_time=False):
    st.session_state.best_portfolios, st.session_state.back_testing_portfolios = gen.start(st.session_state.total_investment, st.session_state.min_stocks, st.session_state.max_stocks, st.session_state.flat_fee, st.session_state.fee_per_share, st.session_state.ticker_file)

st.success("Done! Lets take a look at your portfolios and the best ones we found:", icon=':material/check_circle:')

Portfolio_Final, count = hp.get_best_port(st.session_state.best_portfolios, st.session_state.max_stocks, st.session_state.min_stocks)
backtested_final = st.session_state.back_testing_portfolios[count]
comparison_returns = pd.DataFrame()
best_returns = backtested_final['Portfolio'].pct_change().dropna() * 100

benchmark_returns = hp.get_benchmark_index().pct_change().dropna() * 100
comparison_returns['Your Portfolio Return'] = best_returns
comparison_returns['S&P 500 Return'] = benchmark_returns['SP Index']

total_df = pd.DataFrame(
    {
        'Weight': str(Portfolio_Final['Weight'].sum()) + "%",
        'Shares Bought': Portfolio_Final['Shares'].sum(),
        'Value': "$" + str(Portfolio_Final['Value'].sum()),
        'Average Return (Nov 2023 - Mar 2025)': str(best_returns.mean()) + "%",
    },
    index=['Total']
)

st.write("Your best portfolio:")
st.dataframe(Portfolio_Final, use_container_width=True)
st.write("Total Summary:")
st.dataframe(total_df, use_container_width=True)
st.info("Please note the calculated values for the Total Weight may slightly vary from 100% due to Python's rounding logic. The Total Value may vary from the defined investment amount due to transaction fees (if provided) and similar rounding issues.", icon=':material/info:')
st.write("Your portfolio's performance vs the S&P 500:")
st.info("Your portfolio performace may vary depending on the stocks you selected. Look for overall trends - are your portfolio returns outperforming the market returns on average?", icon=':material/priority_high:')
st.line_chart(comparison_returns, x_label="Date", y_label="Percent Return", height=600, width=900)

st.error("Remember, past performance is not indicative of future results. This is for educational purposes only and should not be considered financial advice.", icon=':material/info:')
render_footer()