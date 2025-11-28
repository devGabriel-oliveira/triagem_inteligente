import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from crewai import Agent, Task, Crew

load_dotenv()

# Pegando API Key
api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY", None)

if not api_key:
    raise ValueError("❌ Nenhuma OPENAI_API_KEY configurada!")

client = OpenAI(api_key=api_key)

def run_triage_agent(patient_data: str):

    agent = Agent(
        role="Assistente de Triagem",
        goal="Gerar uma triagem clínica precisa baseada nos dados do paciente.",
        backstory="Você é um agente médico treinado para auxiliar triagens hospitalares.",
        model="gpt-4o-mini",
        verbose=False
    )

    task = Task(
        description=(
            "Analise as seguintes informações do paciente e produza um relatório clínico:\n\n"
            f"{patient_data}\n\n"
            "Inclua: sinais de alerta, hipóteses diagnósticas e recomendações médicas."
        ),
        agent=agent
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=False
    )

    result = crew.kickoff()

    # Aqui está a correção!
    if hasattr(result, "raw"):
        return result.raw
    return str(result)
