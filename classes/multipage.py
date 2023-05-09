# Imports
import hydralit as st
import streamlit_option_menu as opt
from PIL import Image
from classes.auth import Autenticar
import hydralit_components as hc

hc.hydralit_experimental(True)

class MultiPage:
    """Framework para combinar multiplas aplicações com streamlit"""

    def __init__(self):
        """Constructor class que gera uma lista que vai armazena todas as aplicações como variaveis instanciaveis"""
        self.pages = []
        self.selected = None
        self.auth = Autenticar()
    
    def add_page(self, title, icon, func):
        """
        Args: 
            title ([str]): Titulo da página que está adicionado na lista de apps
            func: Função python que será renderizada na página em Streamlit
        """

        self.pages.append(
            {
                "title": title,
                "icon": icon,
                "function": func
            }
        )

    def run(self):
        """Estiliza a sidebar e seleciona a página a ser renderizada"""

        title = [page["title"] for page in self.pages]
        icon = [page["icon"] for page in self.pages]

        c1, c2, c3, c4 = st.columns([0.1,8,3,1])
        with c2:
            st.image('frontend/img/logo_reduzida.png', width=120)

        with c3:
            self.selected = opt.option_menu(
                menu_title= None, 
                options= title,
                orientation='horizontal',
                icons=icon, 
                menu_icon="cast", 
                default_index=0,
                styles={
                    "nav": {
                        "gap": "1rem",
                        },
                    "container": {
                        "padding": "0!important",
                        "background-color": "transparent",
                        "margin": 0,
                        },
                    "icon": {
                        "font-size": "18px"
                        }, 
                    "nav-link": {
                        "font-size": "14px",
                        "text-align": "left", 
                        "margin":"0px",
                        "--hover-color": "lightgray",
                        "align-items": "center",
                        "justify-content": "center",
                        "gap": "1rem",
                        "padding-left": "auto",
                        "border-radius": "8px"
                        },
                    "nav-link-selected": {
                        "background-color": "black",
                        "color": "white",
                        "box-shadow":"0px 2px 4px rgba(0, 0, 0, 0.2), 0px 2px 8px rgba(0, 0, 0, 0.08)",
                        },
                }
            )

        with c4:
            # Adicione um botão no aplicativo para acionar o modal
            modal_code = f"""
            <div>
            <!-- Botão para acionar modal -->
            <button type="button" class="btn btn-primary my-btn" data-toggle="modal" data-target="#LogoutModal">
                <i class="bi" style="padding-right: 10px; padding-top: 0px">
                    <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" fill="currentColor" class="bi bi-power" viewBox="0 0 16 16">
                        <path d="M7.5 1v7h1V1h-1z"/>
                        <path d="M3 8.812a4.999 4.999 0 0 1 2.578-4.375l-.485-.874A6 6 0 1 0 11 3.616l-.501.865A5 5 0 1 1 3 8.812z"/>
                    </svg>
                </i>
                <span style="padding-top: 3px;">Sair</span>
            </button>
            <!-- Modal -->
            <div class="modal fade" id="LogoutModal" tabindex="-1" role="dialog" aria-labelledby="LogoutModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-sm modal-dialog-centered" role="document">
                <div class="modal-content">
                <div class="modal-body">
                    <div class="container">
                    <h2 class="text-center">Deseja Sair?</h2>
                    <form class="form-horizontal" action="/">
                        <div class="form-group">        
                        <div class="col-sm-offset-2 col-sm-10"></div>
                        </div>
                        <div class="form-group">        
                        <div class="d-flex justify-content-center">
                            <button type="button" class="btn btn-secondary mx-2" data-dismiss="modal">Voltar</button> 
                            <button type="submit" id="submit-btn" class="btn btn-primary" id="sair" name="sair" value="sair">Sair</button> 
                        </div>
                        </div>
                    </form>
                    </div>
                </div>
                </div>
            </div>
            </div>


            """
            st.markdown(modal_code,unsafe_allow_html=True)
            status_modal = st.experimental_get_query_params()

        st.markdown("""<hr style="height:1px;border:none;color:transparent;background-color:transparent;" /> """, unsafe_allow_html=True)
        st.markdown("""<hr style="height:2px;border:none;color:gray;background-color:gray;" /> """, unsafe_allow_html=True)
        st.markdown("""<hr style="height:2px;border:none;color:transparent;background-color:transparent;" /> """, unsafe_allow_html=True)

        if status_modal:
            try:
                if status_modal['sair'][0] == 'sair':
                    self.auth.logout()
                    st.experimental_set_query_params(query_params='Logout')
            except:
                pass

        # Seleciona a página a ser renderizada  
        for page in self.pages:
            if page["title"] == self.selected:
                page["function"]()
