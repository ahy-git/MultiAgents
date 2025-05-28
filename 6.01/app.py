import os
import streamlit as st
from datetime import time

from utils.group_controller import GroupController 
from utils.groups_util import GroupUtils 

# Instância do controlador de grupos
control = GroupController()
groups = control.fetch_groups()

ut = GroupUtils()  # Instância da classe de utilitários
group_map, options = ut.map(groups)

# Configurações de layout em colunas
col1, col2 = st.columns([1, 1])


# Coluna 1: Seletor de grupo
with col1:
    st.header("Selecione um Grupo")
    if group_map:
        selected_group_id = st.selectbox(
            "Escolha um grupo:",
            options,
            format_func=lambda x: x[0]
        )[1]
 
        selected_group = group_map[selected_group_id]
        head_group = ut.head_group(selected_group.name, selected_group.picture_url)
        st.markdown(head_group, unsafe_allow_html=True)

        ut.group_details(selected_group)

    else:
        st.warning("Nenhum grupo encontrado!")

# Coluna 2: Detalhes do grupo e configurações
with col2:
    if group_map:
        st.header("Configurações")
        with st.expander("Configurações do Resumo", expanded=True):

            enabled = st.checkbox(
                "Habilitar Geração do Resumo", 
                value=selected_group.enabled  # Valor carregado do objeto
            )

            horario = st.time_input(
                "Horário de Execução do Resumo:", 
                value=time.fromisoformat(selected_group.horario)  # Valor carregado do objeto
            )

            is_links = st.checkbox(
                "Incluir Links no Resumo", 
                value=selected_group.is_links  # Valor carregado do objeto
            )
            is_names = st.checkbox(
                "Incluir Nomes no Resumo", 
                value=selected_group.is_names  # Valor carregado do objeto
            )

            base_dir = os.path.dirname(__file__)  # pega o diretório do arquivo atual
            python_script = os.path.join(base_dir, "utils", "summary.py")
             
            # Salvar configurações atualizadas
            if st.button("Salvar Configurações"): 
                if control.update_summary( 
                    group_id=selected_group.group_id,
                    horario= "16:49",#horario.strftime("%H:%M"),
                    enabled=enabled,
                    is_links=is_links,
                    is_names=is_names,
                    script=python_script
                ):      
                    st.success("Configurações salvas com sucesso!")
                else:
                    st.error("Erro ao salvar as configurações. Tente novamente!")
