import hydralit as st
import hydralit_components as hc

# Imports de Autenticação
from classes.auth import Autenticar

from classes.functions import Functions

# Imports do Framework de Multipáginas
from classes.multipage import MultiPage
from app_pages import home, dashboard


hc.hydralit_experimental(True)

# Estilizando com CSS
try:
    st.set_page_config(
        layout="wide",
        page_title="APP"
        )
except:
    st.experimental_rerun()

with open("frontend/css/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html= True)

# Criando instâncias dos app's
app = MultiPage()
auth = Autenticar()

if auth.login(): #Autenticação

    # Adicionando páginas da aplicação
    c1,c2,c3 = st.columns([0.3,8,0.3])

    with c2:
        st.write('')
        app.add_page(title="Home", icon='house-fill', func=home.app)
        app.add_page(title="Pag 1", icon='house', func=dashboard.app)

        # Rodando a aplicação
        app.run()
