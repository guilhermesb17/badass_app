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
            # estilização do layout
            col1, col2, col3= st.columns([3,3,3])
            with col2:
                with st.container():
                    st.markdown("""
                        <style>
                        [data-testid="stForm"] {
                            margin-top: 25%;
                            width: 80%;
                            border-radius: 2rem;
                            box-shadow: 0px 2px 16px rgba(0, 0, 0, 0.10), 0px 8px 36px rgba(0, 0, 0, 0.06);
                            border: 0px;
                            margin-left: 50px;
                            align-items: center;
                            justify-content: center;
                            }
                        .stButton > button {
                            width: 100%;
                            border-radius: 0.5rem;
                            background-color: transparent;
                            color: black;
                            flex-shrink: unset !important;
                            position: relative;
                            z-index: 1;
                            overflow-x: hidden;
                            box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1), 0px 2px 16px rgba(0, 0, 0, 0.08);
                        }
                        .stButton > button:hover {
                            width: 100%;
                            border-radius: 0.5rem;
                            background-color: black;
                            color: white;
                            box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2), 0px 2px 8px rgba(0, 0, 0, 0.08);
                        }
                        .st-bs {
                            border: transparent;
                            background-color: transparent;
                        }
                        .st-bw {
                            border: transparent;
                            background-color: transparent;
                        }
                        .st-bu {
                            border: transparent;
                            background-color: transparent;
                        }
                        input[aria-label="Email AD"].st-c6 {
                            border-bottom: 1px solid lightgray
                        }
                        </style>
                        """, unsafe_allow_html= True)
                    with st.form('Login'):
                        st.markdown("""<hr style="height:30px;border:none;color:transparent;background-color:transparent;" /> """, unsafe_allow_html=True)

                        #Cria as colunas
                        lc1,lc2,lc3 = st.columns([1,1,1])
                        with lc2:
                            st.image('frontend/img/logo_reduzida.png', use_column_width=True)
                        st.markdown("""<hr style="height:10px;border:none;color:transparent;background-color:transparent;" /> """, unsafe_allow_html=True)

                        # título de boas vindas
                        st.markdown(f"<h2 style='text-align: center; font-size:26px; color:#darkslategray; font-weight:600;'>Iniciar Sessão com Azure AD</h2>",
                        unsafe_allow_html=True)
                        st.markdown("""<hr style="height:10px;border:none;color:transparent;background-color:transparent;" /> """, unsafe_allow_html=True)

                        fc1,fc2,fc3 = st.columns([1,3,1])
                        with fc2:
                            Login_mail = st.text_input('Email AD', placeholder='Email A3Data', label_visibility="collapsed", key='login-mail-input')
                            Login_pwd = st.text_input('Senha AD', type='password', placeholder='Senha', label_visibility="collapsed", key='LoginPWD')
                            st.markdown("""<hr style="height:20px;border:none;color:transparent;background-color:transparent;" /> """, unsafe_allow_html=True)
                            Login_button = st.form_submit_button('Login')
                            st.markdown("""<hr style="height:20px;border:none;color:transparent;background-color:transparent;" /> """, unsafe_allow_html=True)
                        
            if Login_button:
                try:
                    result = self.public_app.acquire_token_by_username_password(
                        username=Login_mail,
                        password=Login_pwd,
                        scopes=self.SCOPE
                    )

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
                    st.experimental_set_query_params(query_params='Login')
                    return True

                except:
                    st.markdown("""<hr style="height:20px;border:none;color:transparent;background-color:transparent;" /> """, unsafe_allow_html=True)
                    c1,c2,c3 = st.columns(3)
                    with c2:
                        st.warning('Verifique as credenciais!')                

        else:
            # Define as variaveis de Session State
            st.session_state.cookie = self.cookie_manager
            st.session_state.name = self.cookie['name']
            st.session_state.mail = self.cookie['mail']
            st.session_state.accounts = self.cookie['accounts']

            return True

    def logout(self):
        #if st.button('Logout'):
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


    
