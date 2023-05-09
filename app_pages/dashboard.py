import hydralit as st
import hydralit_components as hc
from streamlit_elements import elements, mui, html

hc.hydralit_experimental(True)

def app():
    st.markdown("""
    <style>
        .center {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        .icon {
            margin-bottom: 5px;
        }
    </style>
    <h1 class="center" style='text-align: center; font-size:28px; color:#2c2c2c; font-weight:700;'>
        <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="currentColor" class="bi bi-bar-chart-fill icon" viewBox="0 0 16 16">
            <path d="M1 11a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1v-3zm5-4a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V7zm5-5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1V2z"/>
        </svg>
        Dashboard
    </h1>
    """, unsafe_allow_html=True)