import streamlit as st
import requests

# Configurare Pagina
st.set_page_config(page_title="ContentRecycle AI", page_icon="♻️")

# Secrete
api_key = st.secrets.get("GEMINI_API_KEY")
password = st.secrets.get("APP_PASSWORD")

# Login simplu
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    input_pass = st.text_input("Parola:", type="password")
    if st.button("Log In"):
        if input_pass == password:
            st.session_state.auth = True
            st.rerun()
    st.stop()

st.title("♻️ ContentRecycle AI")
source_text = st.text_area("Pune textul aici:", height=200)

if st.button("Generate"):
    if not source_text:
        st.warning("Pune text!")
    else:
        # APEL DIRECT HTTP - Ignoram libraria oficiala care da erori
        # Folosim versiunea v1 (nu beta) si modelul cel mai stabil
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={api_key}"
        
        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [{
                "parts": [{"text": f"Transforma in 3 postari social media: {source_text}"}]
            }]
        }
        
        with st.spinner("Se genereaza..."):
            response = requests.post(url, json=payload, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                # Extragem textul din raspunsul JSON
                try:
                    generated_text = result['candidates'][0]['content']['parts'][0]['text']
                    st.success("Gata!")
                    st.markdown(generated_text)
                except:
                    st.error("Google a raspuns dar formatul e ciudat. Verifica cheia API.")
            else:
                st.error(f"Eroare Google: {response.status_code}")
                st.json(response.json()) # Vedem exact de ce urla Google
