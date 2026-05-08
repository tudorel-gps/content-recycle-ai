import streamlit as st
import requests

# Setări de bază
st.set_page_config(page_title="ContentRecycle AI", page_icon="♻️")

# Preluăm secretele
api_key = st.secrets.get("GEMINI_API_KEY")
password = st.secrets.get("APP_PASSWORD")

# Logare simplă
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("♻️ ContentRecycle AI")
    input_pass = st.text_input("Introdu parola de acces:", type="password")
    if st.button("Intră în aplicație"):
        if input_pass == password:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Parolă greșită!")
    st.stop()

# Aplicația principală
st.title("♻️ ContentRecycle AI - Dashboard")
source_text = st.text_area("Lipește textul tău aici:", height=200)

if st.button("Generează Postări"):
    if not source_text:
        st.warning("Pune un text mai întâi!")
    else:
        # ATENȚIE: Folosim URL-ul direct pentru Gemini 1.5 Flash
        # Am pus v1 (nu v1beta) pentru stabilitate maximă
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        payload = {
            "contents": [{
                "parts": [{"text": f"Transformă acest text în 3 postări de social media (LinkedIn, X, Instagram): {source_text}"}]
            }]
        }
        
        with st.spinner("Se lucrează..."):
            res = requests.post(url, json=payload)
            
            if res.status_code == 200:
                try:
                    output = res.json()['candidates'][0]['content']['parts'][0]['text']
                    st.success("Gata!")
                    st.markdown(output)
                except Exception:
                    st.error("Eroare la procesarea răspunsului de la Google.")
            else:
                st.error(f"Eroare Google: {res.status_code}")
                st.json(res.json()) # Aici o să vedem exact ce nu-i convine
