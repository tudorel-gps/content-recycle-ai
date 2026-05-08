import streamlit as st
import google.generativeai as genai

# Configurare pagina
st.set_page_config(page_title="ContentRecycle AI", layout="centered", page_icon="♻️")

# Secrete
ACCESS_PASSWORD = st.secrets.get("APP_PASSWORD")
api_key = st.secrets.get("GEMINI_API_KEY")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("♻️ ContentRecycle AI")
    pwd = st.text_input("Parola:", type="password")
    if st.button("Unlock"):
        if pwd == ACCESS_PASSWORD:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Gresit!")
    st.stop()

# --- APP LOGIC ---
st.title("♻️ ContentRecycle AI")

if api_key:
    # AICI E CHEIA: Fortam comunicarea prin REST, nu prin gRPC (care da eroarea 404)
    genai.configure(api_key=api_key, transport='rest')
    
    # Folosim numele scurt al modelului
    model = genai.GenerativeModel('gemini-1.5-flash')

    text_input = st.text_area("Pune textul aici:")
    if st.button("Generate"):
        if text_input:
            try:
                # Generare postari
                response = model.generate_content(f"Transforma in 3 postari social media: {text_input}")
                st.markdown(response.text)
            except Exception as e:
                # Daca tot da eroare, incercam modelul PRO ca fallback
                try:
                    model_pro = genai.GenerativeModel('gemini-1.5-pro')
                    response = model_pro.generate_content(text_input)
                    st.markdown(response.text)
                except Exception as e2:
                    st.error(f"Eroare persistenta: {e2}")
else:
    st.error("Lipseste API Key in Secrets!")
