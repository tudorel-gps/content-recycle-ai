import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="ContentRecycle AI", layout="centered")

# --- LOGICA DE ACCES ---
PAROLA_CORECTA = st.secrets.get("APP_PASSWORD") # O setezi în Secrets

if "access_granted" not in st.session_state:
    st.session_state["access_granted"] = False

if not st.session_state["access_granted"]:
    st.title("🔐 Acces Restricționat")
    st.write("Introdu parola pentru a folosi generatorul de postări.")
    
    parola_introdusa = st.text_input("Parola:", type="password")
    if st.button("Deblochează"):
        if parola_introdusa == PAROLA_CORECTA:
            st.session_state["access_granted"] = True
            st.rerun()
        else:
            st.error("Parolă incorectă!")
            st.write("[Click aici pentru a cumpăra acces](LINK-UL-TAU-DE-PLATA)")
    st.stop() # Oprește restul aplicației aici

# --- CODUL APLICATIEI (Se vede doar după logare) ---
st.title("♻️ ContentRecycle AI - Panou Control")
# Aici vine restul codului tău cu Gemini pe care îl aveam deja...
api_key = st.secrets.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# ... (restul funcționalității tale)
st.success("Ești logat! Spor la generat bani.")
text_input = st.text_area("Introdu textul:", height=200)
# etc.
