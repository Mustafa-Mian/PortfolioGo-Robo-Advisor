import streamlit as st
import pandas as pd
import numpy as np
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
        border: 1px solid #000000;
        background-color: #5e1914;
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
    if st.session_state.min_stocks == st.session_state.max_stocks:
        st.session_state.best_portfolios, st.session_state.back_testing_portfolios = gen.fixed_start(st.session_state.total_investment, st.session_state.min_stocks, st.session_state.flat_fee, st.session_state.fee_per_share, st.session_state.ticker_file)
    else:
        st.session_state.best_portfolios, st.session_state.back_testing_portfolios = gen.start(st.session_state.total_investment, st.session_state.min_stocks, st.session_state.max_stocks, st.session_state.flat_fee, st.session_state.fee_per_share, st.session_state.ticker_file)

st.success("Done! Lets take a look at your portfolios and the best one we found:", icon=':material/check_circle:')

Portfolio_Final = pd.DataFrame()
backtested_final = pd.DataFrame()
Portfolio_with_stats = pd.DataFrame()
count = 0

if st.session_state.min_stocks == st.session_state.max_stocks:
    count = st.session_state.min_stocks
    Portfolio_Final = hp.get_best_port_fixed(st.session_state.best_portfolios[count], st.session_state.min_stocks)
    Portfolio_with_stats = st.session_state.best_portfolios[count]
else:
    Portfolio_Final, count = hp.get_best_port(st.session_state.best_portfolios, st.session_state.max_stocks, st.session_state.min_stocks)
    Portfolio_with_stats = st.session_state.best_portfolios[count]

backtested_final = st.session_state.back_testing_portfolios[st.session_state.min_stocks]
comparison_returns = pd.DataFrame()
best_returns = backtested_final['Portfolio'].pct_change().dropna() * 100
benchmark_returns = hp.get_benchmark_index().ffill().pct_change().dropna() * 100
comparison_returns['Your Portfolio Return'] = best_returns
comparison_returns['S&P 500 Return'] = benchmark_returns['SP Index']

benchmark_real = benchmark_returns['SP Index'] / 100
sp_avg_daily = benchmark_real.mean()
annualized_sp_return = (1 + sp_avg_daily) ** 252 - 1
annualized_sp_return = np.round(annualized_sp_return * 100, 2)

total_df = pd.DataFrame(
    {
        'Weight': str(np.round(Portfolio_Final['Weight'].sum(), 3)) + "%",
        'Shares Bought': Portfolio_Final['Shares'].sum(),
        'Value': "$" + str(Portfolio_Final['Value'].sum()),
        'Average Daily Return (Nov 2023 - Mar 2025)': str(np.round(best_returns.mean(), 3)) + "%",
    },
    index=['Total']
)

st.subheader("Your Portfolio:")
st.dataframe(Portfolio_Final, use_container_width=True)
st.subheader("Total Summary:")
st.dataframe(total_df, use_container_width=True)
st.info("Please note the calculated values for the Total Weight may slightly vary from 100% due to Python's rounding logic. The Total Value may vary from the defined investment amount due to transaction fees (if provided) and similar rounding issues.", icon=':material/info:')

st.subheader("Some key statistics of your portfolio:")
col1, col2, col3 = st.columns(3)
display_return = np.round(Portfolio_with_stats['Portfolio Return'].iloc[-1] * 100, 2)
display_beta = np.round(Portfolio_with_stats['weighted beta'].iloc[-1], 3)
daily_rf, annual_rf = hp.get_rf()
annual_rf = np.round(annual_rf * 100, 2)
col1.metric("Annualized Return", str(display_return) + '%', str(np.round(display_return - annualized_sp_return, 2)) + "% compared to S&P 500")
col2.metric("Portfolio Beta", str(display_beta), str(np.round(display_beta - 1, 3)) + " compared to Market")
col3.metric("Sharpe Ratio", str(np.round(Portfolio_with_stats['Sharpe Ratio'].iloc[-1], 2)), "With a risk-free rate of " + str(annual_rf) + "%")

st.badge("The Annualized Return is the expected return of the portfolio over a year, based on data from Nov 2023 - Mar 2025", icon=":material/finance:", color="green")
st.badge("Beta measures the sensitivity to market shifts. A Higher beta means more movement compared to the market.", icon=":material/whatshot:", color="blue")
st.badge("The Sharpe Ratio measures return per unit of risk. Higher values indicate better risk-adjusted performance.", icon=":material/ifl:", color='violet')

st.subheader("Your portfolio's performance vs the S&P 500:")
st.warning("Your portfolio performace may vary depending on the stocks you selected. Look for overall trends - are your portfolio returns outperforming the market returns on average?", icon=':material/priority_high:')
st.line_chart(comparison_returns, x_label="Date", y_label="Percent Return", height=600, width=900)

st.error("Remember, past performance is not indicative of future results. This is for educational purposes only and should not be considered financial advice.", icon=':material/info:')

st.markdown("---")
st.subheader("With every portfolio comes knowledge - and the chance to")
if st.button("Try Again!", use_container_width=True):
    st.switch_page('stocks.py')

render_footer()