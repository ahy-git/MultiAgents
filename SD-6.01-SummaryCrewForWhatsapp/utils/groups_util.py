import pandas as pd
import base64
import requests
import streamlit as st
from PIL import Image
from io import BytesIO
from datetime import datetime 
import re

class GroupUtils:
    """
    Classe de utilitários para manipulação de imagens, datas e grupos.
    """
    @staticmethod
    def remove_think_section(output: str) -> str:
        """Remove trechos de raciocínio intermediário como <think>...</think> ou 'Thought: ...' da resposta final."""
        import re
        if not output or not isinstance(output, str):
            return ""

        try:
            # Remove blocos <think>...</think>
            output = re.sub(r"<think>.*?</think>", "", output, flags=re.DOTALL)

            # Remove linhas que começam com 'Thought:' (case-insensitive)
            output = re.sub(r"(?i)^thought:.*$", "", output, flags=re.MULTILINE)

            # Limpa espaços em branco extras
            return output.strip()
        except Exception as e:
            # Em caso de falha inesperada, retorna a resposta original
            print(f"[Aviso] Erro ao limpar raciocínio intermediário: {e}")
            return output
        
    
    def resized_image_to_base64(self, image):
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

    
    def format_date(self, timestamp):
        try:
            dt = datetime.fromtimestamp(int(timestamp))
            return dt.strftime("%d-%m-%Y %H:%M")
        except (ValueError, TypeError):
            return "Data inválida"

    
    def get_image(self, url, size=(30, 30)):
        try:
            if not url:
                raise ValueError("URL vazio")
            response = requests.get(url, stream=True, timeout=5)
            image = Image.open(response.raw).convert("RGBA").resize(size)
            return image
        except Exception:
            return Image.new("RGBA", size, (200, 200, 200))  # Imagem padrão

    
    def map(self, groups):
        self.group_map = {group.group_id: group for group in groups}
        self.options = [(group.name, group.group_id) for group in groups]
        return self.group_map, self.options
    
    def head_group(self, title, url_image):
        
        resized_image = self.get_image(url_image)
        
        image_title = f"""
        <div style="display: flex; align-items: center;">
            <img src="data:image/png;base64,{self.resized_image_to_base64(resized_image)}" 
             alt="Grupo" 
             style="width:30px; height:30px; border-radius: 50%; margin-right: 10px;">
            <h3 style="margin: 0;">{title}</h3>
        </div>
        """
        return image_title
    
        # Função para retornar apenas os ícones
    def status_icon(self,value):
        return "✅" if value else "❌"
    
    def group_details(self, selected_group):
        
        with st.expander("Informações Gerais", expanded=False):
            st.write("**Criador:**", selected_group.owner)
            st.write("**Tamanho do Grupo:**", selected_group.size)
            st.write("**Data de Criação:**", self.format_date(selected_group.creation))
            st.write(f"**Grupo Restrito:** {self.status_icon(selected_group.restrict)}")
            st.write(f"**Modo Apenas Administradores:** {self.status_icon(selected_group.announce)}")
            st.write(f"**É Comunidade:** {self.status_icon(selected_group.is_community)}")
            st.write(f"**É Comunidade de Anúncios:** {self.status_icon(selected_group.is_community_announce)}")
            