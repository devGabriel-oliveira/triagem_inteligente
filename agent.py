import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# 1 - tenta pegar chave do .env
api_key = os.getenv("OPENAI_API_KEY")

# 2 - tenta pegar do secrets
if not api_key:
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
    except Exception:
        api_key = None

# 3 - erro caso não exista chave
if not api_key:
    print("❌ ERRO: OPENAI_API_KEY não encontrada.")
    raise ValueError("Nenhuma chave OPENAI_API_KEY encontrada.")

client = OpenAI(api_key=api_key)

from crewai import Agent, Task, Crew


def run_triage_agent(patient_data: str):

    # Tratamento de erro de entrada
    if not patient_data or not isinstance(patient_data, str):
        return "❌ Erro: dados do paciente inválidos para análise."

    try:
        agent = Agent(
            role="Assistente de Triagem",
            goal="Gerar triagem médica baseada nos dados do paciente.",
            backstory="Você é um agente clínico experiente.",
            model="gpt-4o-mini",
            verbose=False
        )

        task = Task(
            description=(
                f"Analise os dados do paciente:\n\n{patient_data}\n\n"
                "Gere uma triagem resumida, achados e condutas."
            ),
            agent=agent
        )

        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=False
        )

        # EXECUÇÃO COM TRY
        result = crew.kickoff()

        # Alguns retornam obj — garantimos string
        return str(result)

    except Exception as e:
        import traceback
        error_log = traceback.format_exc()
        print("❌ ERRO AO EXECUTAR AGENTE:")
        print(error_log)

        # Retorno seguro para o Streamlit
        return (
            "❌ Não foi possível gerar a triagem no momento.\n"
            "O erro foi registrado nos logs para análise."
        )
