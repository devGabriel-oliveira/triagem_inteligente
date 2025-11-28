# app.py
import streamlit as st
from dotenv import load_dotenv
import os
from auth import login
from database import get_patient_data, init_db
from agent import run_triage_agent

# Inicializa DB (cria se não existir)
init_db()

# Carrega .env local (para desenvolvimento)
load_dotenv()

st.set_page_config(page_title="Triagem Inteligente", layout="wide")
st.title("🩺 Sistema Inteligente de Triagem com CrewAI")

# Autenticação simples
if not login():
    st.stop()

st.subheader("Buscar Paciente")

# ID input
patient_id = st.number_input("ID do paciente", min_value=1, step=1, key="patient_id_input")

# Carregar dados (mantém em session_state)
if st.button("Carregar dados"):
    try:
        data = get_patient_data(patient_id)
        if not data:
            st.error("Paciente não encontrado.")
            st.session_state["patient_loaded"] = False
            st.session_state.pop("patient_data", None)
        else:
            # data expected as dict: {"id":..., "name":..., "age":..., "symptoms":...}
            st.success("Dados carregados com sucesso!")
            st.session_state["patient_loaded"] = True
            st.session_state["patient_data"] = data
    except Exception as e:
        st.error("Erro ao carregar dados do paciente")
        st.exception(e)
        st.session_state["patient_loaded"] = False
        st.session_state.pop("patient_data", None)

# Mostrar dados carregados
if st.session_state.get("patient_loaded", False):
    patient = st.session_state.get("patient_data", {})
    st.write("### Dados do Paciente")
    st.write(f"**ID:** {patient.get('id')}")
    st.write(f"**Nome:** {patient.get('name')}")
    st.write(f"**Idade:** {patient.get('age')}")
    st.write(f"**Sintomas:** {patient.get('symptoms')}")

    # Monta patient_info texto para enviar ao agente
    patient_info = (
        f"ID: {patient.get('id')}\n"
        f"Nome: {patient.get('name')}\n"
        f"Idade: {patient.get('age')}\n"
        f"Sintomas: {patient.get('symptoms')}\n"
    )

    st.subheader("Análise automática (IA)")
    # Botão que executa o agente; botão separado do carregar dados evita perda de estado
    if st.button("Executar Agente"):
        try:
            with st.spinner("Analisando com CrewAI..."):
                # chama agente (garante retorno em string)
                result = run_triage_agent(patient_info)

            # Mostrar resultado (se vazio, avisar)
            if result and str(result).strip():
                st.subheader("Resultado da Triagem")
                st.write(result)
            else:
                st.warning("O agente não retornou texto. Verifique logs.")
        except Exception as e:
            st.error("❌ ERRO AO EXECUTAR O AGENTE")
            st.exception(e)
else:
    st.info("Carregue os dados do paciente (ID) e então execute a análise.")
