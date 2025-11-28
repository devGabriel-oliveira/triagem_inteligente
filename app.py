import streamlit as st
from dotenv import load_dotenv
import os
from auth import login
from database import get_patient_data, init_db
from agent import run_triage_agent

init_db()
load_dotenv()

st.set_page_config(page_title="Triagem Inteligente", layout="wide")
st.title("🩺 Sistema Inteligente de Triagem com CrewAI")

# login
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

        # Serializa dados corretamente
        patient_data_str = (
            f"ID: {data[0]}\n"
            f"Nome: {data[1]}\n"
            f"Idade: {data[2]}\n"
            f"Sintomas: {data[3]}"
        )

        st.subheader("Gerar Análise")

        if st.button("Executar agente"):
            with st.spinner("Analisando com AI..."):
                result = run_triage_agent(patient_data_str)

            st.subheader("Resultado da Triagem")

            if "❌" in result:
                st.error(result)
            else:
                st.success("Análise concluída!")
                st.write(result)
