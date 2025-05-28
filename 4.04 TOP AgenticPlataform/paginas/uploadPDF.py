import os 
import time
import streamlit as st 
from crews.pdfResumo import CrewPDFResumo


TEMP_DIR = 'temp'
os.makedirs(TEMP_DIR, exist_ok=True)

def render_upload_page():
    st.title('Resumidor de PDF')
    st.write('Upload a pdf to summarize its contents')
    uploaded_file = st.file_uploader('Choose pdf file', type='pdf')
    
    if uploaded_file is not None:
        try:
            temp_file_path = os.path.join(TEMP_DIR,uploaded_file.name)
            with open (temp_file_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            
            st.success(f'Upload realizado com sucesso: {uploaded_file.name}')
            st.info('Resumindo pdf com agentes')
            st.info(f'{temp_file_path}')
            
            with st.spinner('Executando tarefas do Crew...'):
                crew = CrewPDFResumo(temp_file_path)
                
                resultado = crew.kickoff()
                
                st.text_area("Resumo via agentes:", resultado, height=300)
        except Exception as e:
            st.error(f'Erro ao processar arquivo: {e}')
        
    