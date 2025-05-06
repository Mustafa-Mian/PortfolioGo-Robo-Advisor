import streamlit as st
import base64

def get_img_as_base64(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# def render_header():
#     st.markdown("""
#         <div style='background-color:#5e1914; padding: 1rem; border-radius: 8px;'>
#             <img src="assets/PortfolioGo_Logo.png" alt="PortfolioGo Logo" style='width: 100px; height: auto; display: block; margin: auto;'>
#             <h1 style='color: white; text-align: center;'>PortfolioGo</h1>
#         </div>
#         <br>
#     """, unsafe_allow_html=True)

def render_header():
    logo_base64 = get_img_as_base64("assets/PortfolioGo_Logo.png")
    st.markdown(f"""
        <div style='
            background-color: #5e1914;
            padding: 1.5rem;
            border-radius: 8px;
            text-align: center;
        '>
            <div style='display: flex; align-items: center; justify-content: center; gap: 1rem;'>
                <img src="data:image/png;base64,{logo_base64}" width="100" style='margin: 0;' />
                <h1 style='color: white; margin: 0;'>PortfolioGo</h1>
            </div>
        </div>
        <br>
    """, unsafe_allow_html=True)

def render_footer():
    st.markdown("""
        <br>
        <hr>
        <div style='text-align: center; color: gray; font-size: 0.9rem;'>
            2025 PortfolioGo | Made by Mustafa Mian
            <br></br>
            Always consult a financial advisor before making investment decisions.
        </div>
    """, unsafe_allow_html=True)
