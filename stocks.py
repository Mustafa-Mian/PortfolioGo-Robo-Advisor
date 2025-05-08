import streamlit as st
import pandas as pd
import numpy as np
import generate as gen
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

# --- Initialize session state ---
if "tickers" not in st.session_state:
    st.session_state.tickers = []
if "names" not in st.session_state:
    st.session_state.names = []
if "use_predefined" not in st.session_state:
    st.session_state.use_predefined = False
if "fixed_tickers" not in st.session_state:
    st.session_state.fixed_tickers = ['AAPL', 'MFC', 'SHOP', 'RY', 'NKE', 'MSFT', 'PG', 'NVDA', 'F', 'PFE', 'Afg', 'GOLD', 'BMO', 'SQ', 'TD', 'RCI', 'T', 'JPM', 'ENB', 'YO', 'BA', 'LLY', 'META', 'SPOT']
if "fixed_names" not in st.session_state:
    st.session_state.fixed_names = ['Apple Inc.', 'Manulife Financial Corporation', 'Shopify Inc.', 'Royal Bank of Canada', 'NIKE, Inc.', 'Microsoft Corporation', 'The Procter & Gamble Company', 'NVIDIA Corporation', 'Ford Motor Company', 'Pfizer Inc.', 'American Financial Group, Inc.', 'Barrick Gold Corporation', 'Bank of Montreal', 'Unknown', 'The Toronto-Dominion Bank', 'Rogers Communications Inc.', 'AT&T Inc.', 'JPMorgan Chase & Co.', 'Enbridge Inc.', 'Unknown', 'The Boeing Company', 'Eli Lilly and Company', 'Meta Platforms, Inc.', 'Spotify Technology S.A.']

render_header()

# --- Header ---
st.subheader("Welcome to PortfolioGo!", divider='grey')
container = st.container(border=True)
container.write("Our goal is to make you a strong, investment-worthy portfolio. You provide the stocks, we'll handle the analysis.")
container.write('Please enter the stocks and constraints for your custom-built portfolio.')
container.badge("Let's go!", icon=":material/rocket_launch:", color="green")

use_predefined_now = st.checkbox(
    "Can't think of enough stocks? Click here and we'll use a pre-defined set to show you how PortfolioGo works. (Note selecting this option will overwrite any previously written tickers)",
    value=st.session_state.use_predefined
)

if use_predefined_now and not st.session_state.use_predefined:
    st.session_state.tickers = st.session_state.fixed_tickers.copy()
    st.session_state.names = st.session_state.fixed_names.copy()
    st.session_state.use_predefined = True
elif not use_predefined_now and st.session_state.use_predefined:
    st.session_state.tickers = []
    st.session_state.names = []
    st.session_state.use_predefined = False


# --- Ticker Input ---
with st.form("add_ticker_form", clear_on_submit=True):
    col1, col2 = st.columns([3, 1])
    with col1:
        new_ticker = st.text_input("Enter the ticker for a stock you like (e.g. AAPL, NKE):", key="ticker_input")
    with col2:
        submitted = st.form_submit_button("Add Ticker")
    
    if submitted and new_ticker:
        proceed = True
        clean_ticker = new_ticker.upper().strip().upper()
        if not clean_ticker.isalpha():
            st.error("Please enter a valid ticker symbol (letters only). Unfortunately, numbers and special characters are not allowed. We understand this might mean leaving out certain exchanges, and are working to improve this in the future.")
            proceed = False
        elif clean_ticker in st.session_state.tickers:
            st.warning(f"{clean_ticker} is already in your list.")
            proceed = False
        else:
            st.success(f"Added {clean_ticker} to your portfolio!")
        if clean_ticker not in st.session_state.tickers and proceed:
            st.session_state.tickers.append(clean_ticker)
            try:
                name = gen.get_name_cached(clean_ticker)
                st.session_state.names.append(name)
            except Exception as e:
                st.session_state.names.append("Unknown")
                st.warning(f"Could not retrieve name for {clean_ticker}. This stock may be removed when creating your portfolio.")

# --- Display Ticker Table ---
st.subheader("📋 Your Selected Tickers")
if st.session_state.use_predefined:
    st.write("Some of these tickers may represent unlisted/non-existent companies. That's okay! The goal is to show you how PortfolioGo works and filters out these stocks when creating your portfolio.")

if st.session_state.tickers:
    st.dataframe(pd.DataFrame({"Ticker": st.session_state.tickers, "Name": st.session_state.names}), use_container_width=True)
else:
    st.info("No tickers added yet. Add some to get started!")

# --- Continue Button ---
if len(st.session_state.tickers) < 10:
    st.error("You must add a minimum of 10 stocks to proceed.")
else:
    st.success("Great! You can now proceed to the next step.")
    if st.button("✅ Review provided stocks"):
        st.switch_page('clean.py')
    
render_footer()