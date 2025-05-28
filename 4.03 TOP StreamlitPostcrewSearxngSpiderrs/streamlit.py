import streamlit as st
from postCrew import crewPost

crew_post = crewPost()

st.title('sistema de postagem crewai')
tema = st.text_input('Digite o topico para postagem','IA na geologia')

if st.button('Iniciar processo'):
    with st.spinner ('Executando tarefas do Crew...'):
        result = crew_post.kickoff(inputs={'topic' : tema})
        st.success('Post gerado')
        st.subheader('Post Gerado')
        st.write(result)

