# agent.py
import os
import streamlit as st
from dotenv import load_dotenv

# Carrega .env localmente
load_dotenv()

# Pegar API key (local .env ou Streamlit secrets)
api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY", None)

if not api_key:
    # Não lançamos erro aqui para evitar crash automático — funções que chamam devem checar
    def run_triage_agent(patient_data: str):
        return "❌ Nenhuma OPENAI_API_KEY configurada. Configure LOCAL (.env) ou Streamlit Secrets."
    # exporta função e sai
    __all__ = ["run_triage_agent"]
else:
    # Temos API key — configurar cliente OpenAI (oficial)
    try:
        from openai import OpenAI
        openai_client = OpenAI(api_key=api_key)
    except Exception:
        openai_client = None

    # Tenta importar crewai (se disponível). Se não, fallback para OpenAI diretamente.
    try:
        from crewai import Agent, Task, Crew
        CREWAI_AVAILABLE = True
    except Exception:
        CREWAI_AVAILABLE = False

    def _call_openai_chat(prompt: str) -> str:
        """Fallback: chama a API OpenAI Chat completions e retorna texto."""
        try:
            if openai_client is None:
                return "❌ OpenAI client não inicializado."
            # Usar o método compatível com openai-python v1+ (OpenAI.chat.completions)
            resp = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Você é um assistente médico que faz triagens clínicas. Seja claro e prático."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500
            )
            # Extrair texto
            if resp and getattr(resp, "choices", None):
                # depending on client return structure
                choice0 = resp.choices[0]
                if hasattr(choice0, "message") and hasattr(choice0.message, "content"):
                    return choice0.message.content
                if isinstance(choice0, dict) and "message" in choice0 and "content" in choice0["message"]:
                    return choice0["message"]["content"]
                # fallback to str
                return str(resp)
            return "⚠️ OpenAI retornou resposta vazia."
        except Exception as e:
            return f"❌ Erro ao chamar OpenAI: {e}"

    def run_triage_agent(patient_data: str) -> str:
        """
        Recebe patient_data como string ou dicionário. Retorna texto com a triagem.
        Esta função tenta usar CrewAI se disponível, senão faz fallback para OpenAI.
        """
        # Normalizar patient_data para texto
        if isinstance(patient_data, dict):
            parts = []
            for k, v in patient_data.items():
                parts.append(f"{k}: {v}")
            prompt_body = "\n".join(parts)
        else:
            prompt_body = str(patient_data)

        prompt = (
            "Você é um assistente de triagem médica. Baseado nas informações abaixo, "
            "gere um resumo clínico curto, principais riscos, sinais de alarme e recomendações iniciais. "
            "Seja objetivo e coloque bullets quando fizer sentido.\n\n"
            f"{prompt_body}\n\n"
            "Responda de forma clara e prática."
        )

        # Try CrewAI first
        if CREWAI_AVAILABLE:
            try:
                agent = Agent(
                    role="Assistente de Triagem",
                    goal="Gerar uma triagem clínica e recomendações a partir de dados estruturados.",
                    backstory="Agente para apoiar médicos com triagem inicial.",
                    model="gpt-4o-mini",
                    verbose=False
                )

                task = Task(
                    description=prompt,
                    agent=agent
                )

                crew = Crew(
                    agents=[agent],
                    tasks=[task],
                    verbose=False
                )

                result = crew.kickoff()

                # result pode ter .raw ou outra estrutura
                if hasattr(result, "raw"):
                    return result.raw
                # se for dict/obj com choices/messages
                try:
                    return str(result)
                except Exception:
                    return "⚠️ Agente retornou formato inesperado; verifique logs."
            except Exception as e:
                # fallback para OpenAI
                fallback_text = _call_openai_chat(prompt)
                return f"(Fallback OpenAI devido a erro CrewAI) \n\n{fallback_text}"
        else:
            # direct OpenAI
            return _call_openai_chat(prompt)
