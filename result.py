import streamlit as st

st.write("Hello")

st.write(st.session_state.total_investment)
st.write(st.session_state.flat_fee)
st.write(st.session_state.fee_per_share)
st.write(st.session_state.min_stocks)
st.write(st.session_state.max_stocks)


