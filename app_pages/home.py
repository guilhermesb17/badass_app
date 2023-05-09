import streamlit as st

def app():
    st.markdown("""
    <style>
        .center {
            display: flex;
            padding-left: 25px;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        .icon {
            margin-bottom: 5px;
        }
    </style>"""+ f"""
    <h1 class="center" style='text-align: center; font-size:28px; color:#2c2c2c; font-weight:700;'>
        <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" fill="currentColor" class="bi bi-person-workspace icon" viewBox="0 0 16 16">
            <path d="M4 16s-1 0-1-1 1-4 5-4 5 3 5 4-1 1-1 1H4Zm4-5.95a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5Z"/>
            <path d="M2 1a2 2 0 0 0-2 2v9.5A1.5 1.5 0 0 0 1.5 14h.653a5.373 5.373 0 0 1 1.066-2H1V3a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v9h-2.219c.554.654.89 1.373 1.066 2h.653a1.5 1.5 0 0 0 1.5-1.5V3a2 2 0 0 0-2-2H2Z"/>
        </svg>
        Bem-vindo {st.session_state.name}
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <h2 style='text-align: center; font-size:20px; color:darkslategray; font-weight:700;'>
        Template Streamlit A3Data
    </h2>
    """, unsafe_allow_html=True)

