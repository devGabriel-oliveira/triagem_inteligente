import streamlit as st
from dotenv import load_dotenv
import os
from auth import login
from database import get_patient_data, init_db
from agent import run_triage_agent

# Inicializa banco
init_db()

# Carrega variáveis de ambiente
load_dotenv()

st.set_page_config(page_title="Triagem Inteligente", layout="wide")
st.title("🩺 Sistema Inteligente de Triagem com CrewAI")

# --- LOGIN ---
if not login():
    st.stop()

st.subheader("Buscar Paciente")

# Entrada do ID
patient_id = st.number_input("ID do paciente", min_value=1, step=1)

# Carregar dados
if st.button("Carregar dados"):
    data = get_patient_data(patient_id)

    if not data:
        st.error("Paciente não encontrado.")
    else:
        st.success("Dados carregados com sucesso!")

        # Data vem como → (id, name, age, symptoms)
        pid, name, age, symptoms = data

        st.write("### Dados do Paciente")
        st.write(f"**Nome:** {name}")
        st.write(f"**Idade:** {age}")
        st.write(f"**Sintomas:** {symptoms}")

        # Monta um texto organizado para enviar ao agente
        patient_info = f"""
        Paciente:
        - ID: {pid}
        - Nome: {name}
        - Idade: {age}
        - Sintomas: {symptoms}

        Gere uma triagem clínica com possíveis diagnósticos e próximos passos.
        """

        st.subheader("Gerar Análise")

        if st.button("Executar agente"):
            try:
                with st.spinner("Analisando com CrewAI..."):
                    result = run_triage_agent(data)

                st.subheader("Resultado da Triagem")
                st.write(result)

            except Exception as e:
                st.error("❌ ERRO AO EXECUTAR O AGENTE")
                st.exception(e)
