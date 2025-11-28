import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# Carrega .env
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
    except Exception:
        api_key = None

if not api_key:
    raise ValueError(
        "\n❌ ERRO: Nenhuma chave OPENAI_API_KEY foi encontrada.\n"
        "➡️ Local: verifique seu arquivo .env\n"
        "➡️ Cloud: adicione a chave em Settings → Secrets\n"
    )

client = OpenAI(api_key=api_key)


# --- CrewAI ---
from crewai import Agent, Task, Crew


def run_triage_agent(patient_data: str):
    try:
        agent = Agent(
            role="Assistente de Triagem",
            goal="Analisar dados clínicos e gerar insights.",
            backstory="Você é um agente clínico especializado em triagem.",
            model="gpt-4o-mini",
            verbose=True
        )

        task = Task(
            description=(
                f"Analise os dados do paciente:\n{patient_data}\n\n"
                "Gere uma triagem resumida com hipóteses e próximos passos."
            ),
            agent=agent
        )

        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=True
        )

        result = crew.kickoff()
        return result

    except Exception as e:
        # Retorno mínimo para evitar crash
        return f"❌ Não foi possível gerar a triagem: {str(e)}"
