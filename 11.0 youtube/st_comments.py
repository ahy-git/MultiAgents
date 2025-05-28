import streamlit as st
from crew_comments import YouTubeCommentsAnalyzer
import time

st.title("Youtube Comments Analyzer")
st.write("Links para analizar")
video_links_input = st.text_area(
    "Adicione os links",
    height=150,
    placeholder="https://www.youtube.com/watch?v=xxxxxxx\nhttps://www.youtube.com/watch?v=yyyyyyy"
)

video_links = [link.strip() for link in video_links_input.split("\n") if link.strip()]

if st.button("🔍 Analisar Comentários"):
    if not video_links:
        st.warning("⚠️ Por favor, insira pelo menos um link de vídeo do YouTube.")
    else:
        st.info("🔄 Processando análise, aguarde...")

        # Adicionando um Loader
        with st.spinner("🔎 Extraindo e analisando comentários... Isso pode levar alguns segundos..."):
            time.sleep(2)  # Simulação de tempo de espera
            analyzer = YouTubeCommentsAnalyzer()
            resultado = analyzer.kickoff(video_links=video_links)

        st.success("✅ Análise concluída!")
        st.write("### 📜 Relatório de Insights")
        st.text(resultado)  # Exibir relatório no formato de texto
