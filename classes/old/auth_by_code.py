# Estilização
import streamlit as st
# Cookies
import extra_streamlit_components as stx
# Autenticação
from datetime import datetime, timedelta
from msal import PublicClientApplication
import jwt
import requests

class Autenticar:
    """Classe para realizar autenticação com Azure Ad via Biblioteca MSAL"""
        
    def __init__(self) -> None:
        """Construtor class para compartilhar variáveis entre as funções"""

        # Credenciais do Azure AD
        self.CLIENT_ID = st.secrets['azure']['client_id']
        self.TENANT_ID = st.secrets['azure']['tenant_id']
        self.CLIENT_SECRET = st.secrets['azure']['client_secret']
        self.REDIRECT_URI = st.secrets['azure']['redirect_uri']
        self.AUTHORITY = f'https://login.microsoftonline.com/{self.TENANT_ID}'
        self.SCOPE = ["https://graph.microsoft.com/.default"]

        # Define o cookie manager
        self.cookie_manager = None
        self.cookie_name = None
        self.cookie_exp_day = None
        self.cookie_key = None
        self.cookie_exp_date = None
        self.cookie = None

        # Configura o client do MSAL
        self.public_app = None
        # Recebe informações do usuário
        self.accounts = None


    def check_session(self):
    # Define todas as variáveis do session_state
        if 'mail' not in st.session_state:
            st.session_state.mail = None
        if 'name' not in st.session_state:
            st.session_state.name = None
        if 'accounts' not in st.session_state:
            st.session_state.accounts = None
        if 'cookie' not in st.session_state:
            st.session_state.cookie = None
        if 'cname' not in st.session_state:
            st.session_state.cname = None

    
    def set_cookie(self):
        self.check_session()
        # Define as variáveis do cookies
        self.cookie_manager = stx.CookieManager()
        self.cookie_name = st.secrets['auth_config']['name']
        self.cookie_exp_day = st.secrets['auth_config']['expiry_days']
        self.cookie_key = st.secrets['auth_config']['key']
        self.cookie_exp_date = (datetime.now() + timedelta(days=self.cookie_exp_day)).timestamp()
        self.cookie = self.cookie_manager.get(self.cookie_name)
        st.session_state.cname = self.cookie_name


    def set_public_app(self):
        # Configura o client do MSAL
        self.public_app = PublicClientApplication(
            self.CLIENT_ID,
            authority=self.AUTHORITY
        )


    def check_cookie(self):
        """Verifica e configura os cookies"""
        
        self.set_cookie()

        if self.cookie is not None:
            try:
                self.cookie = jwt.decode(self.cookie, key=self.cookie_key, algorithms=['HS256'])
            except:
                self.cookie = False
        
        if self.cookie is None:
            return False

        if self.cookie['exp_date'] > datetime.utcnow().timestamp() and ('name' and 'mail' in self.cookie):
            st.session_state.name = self.cookie['name']
            st.session_state.mail = self.cookie['mail']
            st.session_state.accounts = self.cookie['accounts']
            return True
        else: 
            return False    


    def login(self):
        """Define a função de login"""
        self.set_public_app()

        if self.check_cookie() is False:
            # título de boas vindas
            st.markdown(f"<h1 style='text-align: center; font-size:60px; color:#FF7A00'>Bem vindo!</h1>", 
            unsafe_allow_html=True)
            # título do console
            st.markdown("<h3 style='text-align: center; color:darkslategray'>CRC - Console de Regras Chronos</h3>", 
            unsafe_allow_html=True)
            # estilização do layout
            col1, col2, col3= st.columns([3,3,3])
            with col2:
                if st.button('Login'):
                    flow = self.public_app.initiate_device_flow(scopes=self.SCOPE)
                    st.write("Para fazer login, acesse: " + flow['verification_uri'])
                    st.write("E insira o código: " + flow['user_code'])
                    result = self.public_app.acquire_token_by_device_flow(flow)
                    access_token = result["access_token"]

                    self.accounts = self.public_app.get_accounts()

                    # Obtém informações do usuário com o token de acesso
                    response = requests.get(
                        "https://graph.microsoft.com/v1.0/me",
                        headers={"Authorization": f"Bearer {access_token}"},
                    )
                    user_data = response.json()
                    user_name = user_data['displayName']

                    if user_data['mail'] is None:
                        user_mail = user_data['userPrincipalName']
                    else:
                        user_mail = user_data['mail']

                    # Define as variaveis de Session State
                    st.session_state.name = user_name
                    st.session_state.mail = user_mail
                    st.session_state.accounts = self.accounts 

                    # Cria o token 
                    token = jwt.encode(
                        {
                            'name':st.session_state['name'],
                            'mail':st.session_state['mail'],
                            'accounts' : st.session_state['accounts'],
                            'exp_date':self.cookie_exp_date},
                        key=self.cookie_key,
                        algorithm='HS256'
                    )
                    # Configura cookies
                    self.cookie_manager.set(
                        self.cookie_name,
                        token,
                        expires_at=datetime.now() + timedelta(days=self.cookie_exp_day))

                    st.session_state.cookie = self.cookie_manager

                    return True

        else:
            # Define as variaveis de Session State
            st.session_state.name = self.cookie['name']
            st.session_state.mail = self.cookie['mail']
            st.session_state.mail = self.cookie['accounts']

            return True
        

    def logout(self):
        if st.button('Logout'):
            self.set_public_app()
            self.cookie_manager = st.session_state.cookie

            # Limpa as variaveis de Cookie
            self.cookie_manager.delete(st.session_state.cname)

            # Limpa o cache de token do aplicativo MSAL
            self.public_app.remove_account(st.session_state.accounts[0])
            
            # Limpa as variaveis de Session State
            st.session_state.mail = None
            st.session_state.accounts = None

            return True


    
