import os
import streamlit as st
from datetime import time, timedelta, datetime

from utils.group_controller import GroupController
from utils.groups_util import GroupUtils

# Instância do controlador de grupos
control = GroupController()
ut = GroupUtils()

# Cacheando os grupos para evitar recarregamento pesado
@st.cache_data
def load_groups():
    groups = control.fetch_groups()
    return ut.map(groups)

group_map, options = load_groups()

col1, col2 = st.columns([1, 1])

# Coluna 1: Seletor de grupo
with col1:
    st.header("Selecione um Grupo")
    if group_map:
        selected_option = st.selectbox(
            "Escolha um grupo:",
            options,
            format_func=lambda x: x[0]
        )
        selected_group_id = selected_option[1]
        selected_group = group_map[selected_group_id]

        head_group = ut.head_group(selected_group.name, selected_group.picture_url)
        st.markdown(head_group, unsafe_allow_html=True)
        ut.group_details(selected_group)

    else:
        st.warning("Nenhum grupo encontrado!")

# Coluna 2: Configurações
with col2:
    if group_map:
        st.header("Configurações")
        with st.expander("Configurações do Resumo", expanded=True):

            enabled = st.checkbox(
                "Habilitar Geração do Resumo", 
                value=selected_group.enabled
            )
            horario = st.time_input(
                "Horário de Execução do Resumo:", 
                value=time.fromisoformat(selected_group.horario)
            )
            is_links = st.checkbox(
                "Incluir Links no Resumo", 
                value=selected_group.is_links
            )
            is_names = st.checkbox(
                "Incluir Nomes no Resumo", 
                value=selected_group.is_names
            )

            base_dir = os.path.dirname(__file__)
            python_script = os.path.join(base_dir, "utils", "summary.py")

            if st.button("Salvar Configurações"): 
                if control.update_summary(
                    group_id=selected_group.group_id,
                    horario=horario.strftime("%H:%M"),
                    enabled=enabled,
                    is_links=is_links,
                    is_names=is_names,
                    script=python_script
                ):
                    st.success("Configurações salvas com sucesso!")
                else:
                    st.error("Erro ao salvar as configurações. Tente novamente!")

# NOVO: Agendamento batch para vários grupos
st.header("Agendamento Batch de Grupos")

selected_groups = st.multiselect(
    "Selecione os grupos para agendar",
    options,
    format_func=lambda x: x[0]
)

if st.button("Agendar Batch"):
    if selected_groups:
        now = datetime.now()
        first_schedule = now.replace(second=0, microsecond=0) + timedelta(minutes=5)  # Começa daqui 5 min
        for index, group in enumerate(selected_groups):
            group_id = group[1]
            horario_agendado = (first_schedule + timedelta(minutes=10 * index)).time()

            control.update_summary(
                group_id=group_id,
                horario=horario_agendado.strftime("%H:%M"),
                enabled=True,
                is_links=True,
                is_names=True,
                script=os.path.join(base_dir, "utils", "summary.py")
            )

        st.success(f"{len(selected_groups)} grupos agendados em batch com separação de 10 minutos.")
    else:
        st.warning("Selecione pelo menos um grupo para agendar.")
