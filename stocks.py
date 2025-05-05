import streamlit as st
import pandas as pd
import numpy as np
import generate as gen

#st.title("Welcome to PortfoliGo!")

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

# --- Initialize session state ---
if "tickers" not in st.session_state:
    st.session_state.tickers = []
if "names" not in st.session_state:
    st.session_state.names = []

# --- Header ---
st.title("📊 Welcome to PortfolioGo!")
st.write("Please enter the stocks and constraints for your custom-built portfolio. Let's get started!")
st.write("Please enter the base form of tickers (e.g. AAPL, SHOP). Do not include the exchange suffix (e.g. .TO, .NS).")

if "tickers" in st.session_state and len(st.session_state.tickers) < 9:
    st.error("You must add a minumun of 10 stocks to proceed.")
else:
    st.success("Great! You can now proceed to the next step.")

# --- Ticker Input ---
with st.form("add_ticker_form", clear_on_submit=True):
    col1, col2 = st.columns([3, 1])
    with col1:
        new_ticker = st.text_input("Enter a stock ticker you like (e.g. AAPL, TSLA)", key="ticker_input")
    with col2:
        submitted = st.form_submit_button("Add Ticker")
    
    if submitted and new_ticker:
        proceed = True
        clean_ticker = new_ticker.upper().strip().upper()
        if not clean_ticker.isalpha():
            st.error("Please enter a valid ticker symbol (letters only).")
            proceed = False
        elif clean_ticker in st.session_state.tickers:
            st.warning(f"{clean_ticker} is already in your list.")
            proceed = False
        else:
            st.success(f"Added {clean_ticker} to your portfolio!")
        if clean_ticker not in st.session_state.tickers and proceed:
            st.session_state.tickers.append(clean_ticker)
            try:
                name = gen.get_name(clean_ticker)
                st.session_state.names.append(name)
            except Exception as e:
                st.session_state.names.append("Unknown")
                st.warning(f"Could not retrieve name for {clean_ticker}. This stock may be removed when creating your portfolio.")


# --- Display Ticker Table ---
st.subheader("📋 Your Selected Tickers")
if st.session_state.tickers:
    st.dataframe(pd.DataFrame({"Ticker": st.session_state.tickers, "Name": st.session_state.names}), use_container_width=True)
else:
    st.info("No tickers added yet. Add some to get started!")

# --- Continue Button ---
st.markdown("---")
if "tickers" in st.session_state and len(st.session_state.tickers) > 9:
    if st.button("✅ Proceed to Investment Parameters"):
        st.switch_page('param.py')

"""
investment_size = 1000000
min_stocks = 12
max_stocks = 24
flat_fee = 3.95
fee_per_share = 0.001

ticker_file = pd.read_csv('Tickers.csv', header=None)
ticker_file.rename(columns={0: 'name'}, inplace=True)

gen.start(investment_size, max_stocks, flat_fee, fee_per_share, ticker_file)
"""
