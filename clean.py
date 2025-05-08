import streamlit as st
import pandas as pd
import generate as gen
from components import render_header, render_footer

ticker_df = pd.DataFrame(st.session_state.tickers)
ticker_df.rename(columns={0: 'name'}, inplace=True)

st.session_state.ticker_file = ticker_df

render_header()

with st.spinner("Hang on - We're cleaning your provided stocks", show_time=False):
    st.session_state.ticker_file = gen.clean_data(st.session_state.ticker_file)

if len(st.session_state.ticker_file) < 10:
    st.write("Unfortunately, there are not enough stocks to create a portfolio after removing stocks we couldn't find data for. Please add more stocks and try again.")
    st.markdown("---")
    st.dataframe(st.session_state.ticker_file, use_container_width=True)
    if st.button("Go back to add more stocks!"):
        st.switch_page('stocks.py')
elif len(st.session_state.ticker_file) != len(ticker_df):
    st.write("We went ahead and removed any stocks we couldn't fetch data for (or had concerningly low trading volumes). Here's what made the cut:")
    st.markdown("---")
    st.dataframe(st.session_state.ticker_file, use_container_width=True)
    st.markdown("---")
    if st.button("✅ Proceed to Investment Parameters"):
        st.switch_page('param.py')
else:
    st.write("All your stocks are good to go! Just to confirm, here's what we have:")
    st.markdown("---")
    st.dataframe(st.session_state.ticker_file, use_container_width=True)
    st.markdown("---")
    if st.button("✅ Proceed to Investment Parameters"):
        st.switch_page('param.py')

render_footer()