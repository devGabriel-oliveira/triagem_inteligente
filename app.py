import streamlit as st
from dotenv import load_dotenv
import os
from auth import login
from database import get_patient_data
from agent import run_triage_agent
from database import init_db

init_db()

load_dotenv()

st.set_page_config(page_title="Triagem Inteligente", layout="wide")
st.title("🩺 Sistema Inteligente de Triagem com CrewAI")

if not login():
    st.stop()

st.subheader("Buscar Paciente")

patient_id = st.number_input("ID do paciente", min_value=1, step=1)

if st.button("Carregar dados"):
    data = get_patient_data(patient_id)

    if not data:
        st.error("Paciente não encontrado.")
    else:
        st.success("Dados carregados!")
        st.json(data)

        st.subheader("Gerar Análise")
        
        if st.button("Executar agente"):
            with st.spinner("Analisando com CrewAI..."):
                result = run_triage_agent(patient_id)
            
            st.subheader("Resultado da Triagem")
            st.write(result)
