import streamlit as st 
from streamlit_option_menu import option_menu
from images._my_images import Image
from paginas.welcome import render_welcome
from paginas.post import render_post_page
from paginas.uploadPDF import render_upload_page

# Carrega os ícones do Font Awesome
st.markdown("""
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
""", unsafe_allow_html=True)

# Topbar customizado com HTML + CSS
st.markdown("""
    <style>
        .topbar {
            background-color: #0E1117;
            padding: 10px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: white;
            font-family: sans-serif;
            position: sticky;
            top: 0;
            z-index: 999;
        }

        .topbar a {
            color: white;
            text-decoration: none;
            margin: 0 15px;
            font-size: 16px;
        }

        .topbar a:hover {
            text-decoration: underline;
        }

        .menu-item {
            display: flex;
            align-items: center;
        }

        .menu-item i {
            margin-right: 6px;
        }
    </style>

    <div class="topbar">
        <div class="menu-item">
            <a href="https://example.com/home" target="_blank"><i class="fas fa-home"></i> Home</a>
            <a href="https://example.com/agents" target="_blank"><i class="fas fa-robot"></i> Agentes</a>
            <a href="https://example.com/config" target="_blank"><i class="fas fa-cog"></i> Configurações</a>
        </div>
    </div>
""", unsafe_allow_html=True)


st.sidebar.image(
    Image.LOGO,
    use_container_width = True
)

with st.sidebar:
    selected = option_menu(
        menu_title = 'Agentic Plataform',
        options = ['Home', 'Post Agent', 'Summary PDF'],
        icons=['house', 'file-earmark-text', 'cloud-upload'],
        menu_icon = 'robot',
        default_index=0,
        orientation='vertical'
    )

st.sidebar.image(
    Image.POWERED,
    use_container_width=False,
    width=400
)

if selected == 'Home':
    render_welcome()
elif selected == 'Post Agent':
    render_post_page()
elif selected == 'Summary PDF':
    render_upload_page()
    