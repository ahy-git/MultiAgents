import streamlit as st
from crews.postCrew import crewPost

def render_post_page():
    st.title('Sistema de postagem com crewAI')
    
    tema = st.text_input('Digite o topico para postagem', 'IA na saude')
    
    if st.button('Iniciar Processo'):
        with st.spinner('Executando Crew'):
            crew_postagem = crewPost()
            result = crew_postagem.kickoff(inputs={'topic' : tema})
            st.success('Processo concluido!')
            
            st.subheader('Postagem Gerada')
            st.write(result)
