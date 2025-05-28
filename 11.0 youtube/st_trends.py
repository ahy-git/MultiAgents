import streamlit as st 
import json
import time
from crew_trends_analyzer import YoutubeTrendAnalyzer

with open("yt_categories.json", "r",encoding="utf-8") as f:
    categories_data = json.load(f)

with open ("yt_regions.json","r",encoding="utf-8") as f:
    region_data = json.load(f)

category_mapping = {item["id"]: item["snippet"]["title"] for item in categories_data["items"]}
region_mapping = {item["id"]: item["snippet"]["name"] for item in region_data["items"]}

category_reverse_mappping = {v: k for k,v in category_mapping.items()}
region_reverse_mapping = {v: k for k,v in region_mapping.items()}

st.title("Youtube Trend analyzer")
st.header("Analisis Config")

category_name = st.selectbox("categoria:", list(category_mapping.values()))
category_id = category_reverse_mappping[category_name]

# Campo de seleção para região
region_name = st.selectbox("Escolha a Região", list(region_mapping.values()))
region_id = region_reverse_mapping[region_name]  # Obter o ID correspondente

max_results = st.number_input("Quantidade de vídeos a buscar", min_value=1, max_value=50, value=10)
num_comments = st.number_input("Quantidade de comentários a analisar por vídeo", min_value=1, max_value=100, value=5)

if st.button("Executar Analise"):
    with st.spinner("Buscando trends"):
        time.sleep(2)
        
        analyzer = YoutubeTrendAnalyzer()
        inputs = {
            "category": category_id,
            "region": region_id,
            "max_results": max_results,
            "num_comments": num_comments            
        }
        resultado = analyzer.kickoff(inputs=inputs)
    
        st.success("Analise concluida")
        st.write("Relatorio:")
        st.text(resultado)
    
    