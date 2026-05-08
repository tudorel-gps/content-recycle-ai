import streamlit as st
import requests

# --- CONFIGURARE PAGINĂ ---
st.set_page_config(page_title="ContentRecycle AI", layout="centered", page_icon="♻️")

# --- SECRETS ---
# Asigură-te că ai APP_PASSWORD în Streamlit Secrets
GROQ_API_KEY = "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"
ACCESS_PASSWORD = st.secrets.get("APP_PASSWORD")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# --- LOGIN ---
if not st.session_state["authenticated"]:
    st.title("♻️ ContentRecycle AI")
    st.info("Introdu parola pentru a folosi AI-ul pe Groq.")
    pwd = st.text_input("Parola:", type="password")
    if st.button("Unlock"):
        if pwd == ACCESS_PASSWORD:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Parolă greșită!")
    st.stop()

# --- MAIN APP ---
st.title("♻️ ContentRecycle AI (Groq Edition) 🚀")
source_text = st.text_area("Paste content here:", height=200)

if st.button("Generate Social Posts"):
    if source_text:
        with st.spinner("Groq is thinking fast..."):
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": "You are a social media expert. Create 3 viral posts (LinkedIn, X, Instagram) from the given text."},
                    {"role": "user", "content": source_text}
                ]
            }
            
            try:
                response = requests.post(url, json=data, headers=headers)
                if response.status_code == 200:
                    result = response.json()
                    st.markdown(result['choices'][0]['message']['content'])
                    st.success("Gata! Generat cu Llama 3 pe Groq.")
                else:
                    st.error(f"Eroare Groq: {response.status_code}")
                    st.json(response.json())
            except Exception as e:
                st.error(f"A apărut o problemă: {e}")
    else:
        st.warning("Pune text, boss!")
