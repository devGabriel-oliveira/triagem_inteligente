import streamlit as st

# Autenticação simples (para demonstração)
USERS = {
    "gabriel": "1234",
    "medico": "senha"
}

def login():
    st.sidebar.title("Login")

    user = st.sidebar.text_input("Usuário")
    pwd = st.sidebar.text_input("Senha", type="password")

    if st.sidebar.button("Entrar"):
        if user in USERS and USERS[user] == pwd:
            st.session_state["auth"] = True
            st.session_state["user"] = user
            st.success("Logado com sucesso!")
        else:
            st.error("Usuário ou senha incorretos.")

    return st.session_state.get("auth", False)
