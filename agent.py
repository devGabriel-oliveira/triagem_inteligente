import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# Carrega .env localmente (não afeta Streamlit Cloud)
load_dotenv()

# 1️⃣ Tenta pegar do ambiente local (.env)
api_key = os.getenv("OPENAI_API_KEY")

# 2️⃣ Se não existir, tenta pegar do Streamlit Secrets
if not api_key:
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
    except Exception:
        api_key = None

# 3️⃣ Se ainda for None → ERRO CLARO
if not api_key:
    raise ValueError(
        "\n❌ ERRO: Nenhuma chave OPENAI_API_KEY foi encontrada.\n"
        "➡️ Local: verifique seu arquivo .env\n"
        "➡️ Cloud: adicione a chave em Settings → Secrets\n"
    )

# 4️⃣ Criar cliente OpenAI com a API correta
client = OpenAI(api_key=api_key)


# --- SUA LÓGICA DO AGENTE CREWAI ---
from crewai import Agent, Task, Crew

def run_triage_agent(patient_data: str):
    agent = Agent(
        role="Assistente de Triagem",
        goal="Analisar dados clínicos e gerar insights para o médico.",
        backstory="Você é um agente de saúde especializado em triagens rápidas.",
        model="gpt-4o-mini",
        verbose=True
    )

    task = Task(
        description=f"Analise os dados do paciente:\n{patient_data}\n\n"
                    "Gere uma triagem resumida, suspeitas clínicas e próximos passos.",
        agent=agent
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=True
    )

    result = crew.kickoff()
    return result
