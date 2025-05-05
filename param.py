import streamlit as st

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

# --- Investment Parameters ---
st.subheader("💰 Investment Constraints")

st.write("Let's talk about the fine details. What are your investment parameters?")

investment_size = st.number_input("Total Investment Amount (USD)", min_value=1000.0, step=100.0, value=10000.0)
if "total_investment" not in st.session_state:
    st.session_state.total_investment = investment_size
st.markdown("---")
fee_box = st.checkbox("I have transaction fees", value=False)
if fee_box:
    flat_fees = st.number_input("Flat Transaction Fee per Purchase ($)", min_value=0.0, step=1.0, value=9.99)
    per_share_fees = st.number_input("Fee per Share ($)", min_value=0.0, step=0.01, value=0.00)
st.markdown("---")

# st.write(len(st.session_state.tickers))

if len(st.session_state.tickers) == 10:
    st.write("Since you have only chosen 10 stocks, your portfilio will include all 10. Add more stocks and PortfolioGo will automatically decide the best to use!")
    if st.button("Go back to add more stocks!"):
        st.switch_page('stocks.py')
else:
    fixed = st.checkbox("I want to fix the number of stocks in my portfolio", value=False)
    if fixed:
        st.write("How many companies do you want to hold in your portfolio? Pick a number and we'll figure out the best ones and how many shares to buy!")
        num_stocks = st.number_input("Number of Stocks", min_value=10, max_value=len(st.session_state.tickers), value=10)
    else:
        stock_count = len(st.session_state.tickers)

        # Edge case: Only 11 stocks
        if stock_count == 11:
            min_stocks = 10
            max_stocks = 11
            st.info("You have only provided 11 stocks. PortfolioGo will use a minimum of 10 and a maximum of 11 when generating potential portfolios. By adding more stocks, you can increase the range.", icon=":material/info:")
            if st.button("Go back to add more stocks!"):
                st.switch_page('stocks.py')
        else:
            # Show min slider safely
            min_slider_max = stock_count - 1
            min_stocks = st.slider("Minimum Number of Stocks", min_value=10, max_value=min_slider_max, value=10)

            # Show max slider only if valid range exists
            if min_stocks + 1 == stock_count:
                st.info(f"The only possible range is {min_stocks} to {stock_count}. PortfolioGo will use a minimum of {min_stocks} and a maximum of {stock_count}.", icon=":material/info:")
            else:
                max_stocks = st.slider("Maximum Number of Stocks", min_value=min_stocks + 1, max_value=stock_count, value=stock_count)

# --- Continue Button ---
st.markdown("---")
if st.button("✅ Proceed to Optimization"):

    # Save total investment
    st.session_state.total_investment = investment_size

    # Save fee information
    if fee_box:
        st.session_state.flat_fee = flat_fees
        st.session_state.fee_per_share = per_share_fees
    else:
        st.session_state.flat_fee = 0.0
        st.session_state.fee_per_share = 0.0

    # Save stock count preferences
    if len(st.session_state.tickers) == 10:
        st.session_state.min_stocks = 10
        st.session_state.max_stocks = 10
    elif fixed:
        st.session_state.min_stocks = num_stocks
        st.session_state.max_stocks = num_stocks
    else:
        st.session_state.min_stocks = min_stocks
        st.session_state.max_stocks = max_stocks

    st.success("Running optimization (backend logic goes here)...")
    st.switch_page('result.py')
