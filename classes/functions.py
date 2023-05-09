import streamlit as st

class Functions:
    def style_sidebar():
        st.markdown("""
            <style>
                /* Define a classe sidebar */
                .css-vk3wp9.e1fqkh3o11 {
                    position: fixed;
                    top: 0;
                    left: 0;
                    height: 100%;
                    width: 80px;
                    background-color: #f0f0f0;
                    overflow: hidden;
                    transition: width 0.3s ease-in-out;
                    z-index: 999;
                }
                
                /* Define o estilo do link dentro da sidebar */
                .css-vk3wp9.e1fqkh3o11 a {
                    display: block;
                    color: #333;
                    text-decoration: none;
                    padding: 10px;
                }
                
                /* Define o estilo do link ativo na sidebar */
                .css-vk3wp9.e1fqkh3o11 a.active {
                    font-weight: bold;
                    background-color: #ddd;
                }
                
                /* Define o estilo da barra de menu para expandir/retrair a sidebar */
                .sidebar-menu {
                    height: 50px;
                    background-color: #ddd;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }
                
                /* Define o estilo do ícone para expandir/retrair a sidebar */
                .sidebar-menu i {
                    font-size: 24px;
                    cursor: pointer;
                }
                
                /* Define o estilo da classe sidebar-expand para expandir a sidebar */
                .sidebar-expand {
                    width: 200px;
                }
            </style>
        """, unsafe_allow_html=True)