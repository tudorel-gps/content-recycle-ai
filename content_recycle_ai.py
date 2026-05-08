import streamlit as st
import requests

# --- CONFIGURARE PAGINĂ ---
st.set_page_config(page_title="ContentRecycle AI", layout="centered", page_icon="♻️")

# --- DATE ACCES (DIN SECRETS SAU COD) ---
# Am lăsat cheia ta de Groq aici pentru a fi sigur că merge direct
GROQ_API_KEY = "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"
ACCESS_PASSWORD = st.secrets.get("APP_PASSWORD")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# --- ECRAN DE LOGIN ---
if not st.session_state["authenticated"]:
    st.title("♻️ ContentRecycle AI")
    st.subheader("Transformă orice text în postări virale.")
    st.write("---")
    
    pwd = st.text_input("Parola de acces:", type="password")
    if st.button("Deblochează"):
        if pwd == ACCESS_PASSWORD:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Parolă incorectă!")
            st.markdown("### [Cumpără acces aici](https://farcastor.gumroad.com/l/xumhyx)")
    st.stop()

# --- DASHBOARD PRINCIPAL ---
st.title("♻️ ContentRecycle AI - Dashboard")
st.write("Lipește textul mai jos și lasă AI-ul să facă magia.")

source_text = st.text_area("Text sursă:", height=200, placeholder="Ex: Un transcript de YouTube, un articol...")

if st.button("Generează Postări"):
    if source_text:
        with st.spinner("Groq generează postările..."):
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            
            # NOUL PROMPT AGRESIV: Nu pune întrebări, doar execută.
            data = {
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {
                        "role": "system", 
                        "content": "You are a professional social media content generator. Your task: take ANY input and transform it into 3 viral posts (LinkedIn, X, Instagram). Do NOT ask for more info. Do NOT explain yourself. Just output the posts. Even if the input is short or weird, create something viral out of it."
                    },
                    {"role": "user", "content": source_text}
                ],
                "temperature": 0.7
            }
            
            try:
                response = requests.post(url, json=data, headers=headers)
                if response.status_code == 200:
                    result = response.json()
                    st.divider()
                    st.markdown(result['choices'][0]['message']['content'])
                    st.success("Gata! Generat cu succes.")
                else:
                    st.error(f"Eroare Groq: {response.status_code}")
                    st.json(response.json())
            except Exception as e:
                st.error(f"A apărut o eroare: {e}")
    else:
        st.warning("Te rog să introduci un text!")

st.write("---")
if st.button("Logout"):
    st.session_state["authenticated"] = False
    st.rerun()
