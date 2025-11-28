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

        # Converter tuple do banco para texto
        patient_data_str = (
            f"ID: {data[0] if isinstance(data, tuple) else data['id']}\n"
            f"Nome: {data[1] if isinstance(data, tuple) else data['name']}\n"
            f"Idade: {data[2] if isinstance(data, tuple) else data['age']}\n"
            f"Sintomas: {data[3] if isinstance(data, tuple) else data['symptoms']}"
        )


        if st.button("Executar agente"):
            patient_data_str = (
                f"ID: {data[0]}\n"
                f"Nome: {data[1]}\n"
                f"Idade: {data[2]}\n"
                f"Sintomas: {data[3]}"
            )

            with st.spinner("Analisando com CrewAI..."):
                result = run_triage_agent(patient_data_str)

            st.subheader("Resultado da Triagem")
            st.write(result)


