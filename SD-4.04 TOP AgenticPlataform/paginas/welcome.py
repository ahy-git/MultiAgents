import streamlit as st

def render_welcome():
    st.write('Este eh o conteudo da Home')
    st.title('Bem-vindo a nossa Agentic Plataform')
    st.write(
    """
    Esta é uma aplicação de demonstração criada
    com **Streamlit** combinada com o **CrewAI**.
    Utilize o menu lateral para navegar entre as
    páginas disponíveis:
    - **Post Agent:** Crie e gerencie suas
    postagens com Agentes de IA.
    - **Summary PDF:** Faça upload de arquivos
    PDF para os agentes resumirem.
    Sinta-se à vontade para explorar !
    """
    )
    st.markdown("""
                ---
                Desenvolvido por [AHY](https://github.com/ahy-git)
                """)