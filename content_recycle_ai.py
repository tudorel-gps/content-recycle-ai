import streamlit as st
import google.generativeai as genai

# Configurare Pagina
st.set_page_config(page_title="ContentRecycle AI", layout="centered")
st.title("♻️ ContentRecycle AI")
st.subheader("Transformă transcriptul în postări virale (Gratis prin Gemini)")

# Preluare Cheie API din Secrets
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("Lipsește cheia API! Pune GEMINI_API_KEY în Streamlit Secrets.")
else:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-1.5-flash')

    text_input = st.text_area("Introdu transcriptul sau textul lung aici:", height=200)

    if st.button("Generează Postări"):
        if text_input:
            with st.spinner('AI-ul lucrează pentru tine...'):
                prompt = f"Transformă următorul text în 3 postări diferite: 1. LinkedIn (profesional), 2. X/Twitter (scurt/viral), 3. Instagram (bullet points). Iată textul: {text_input}"
                
                response = model.generate_content(prompt)
                
                st.divider()
                st.markdown(response.text)
        else:
            st.warning("Te rog introdu un text mai întâi.")
