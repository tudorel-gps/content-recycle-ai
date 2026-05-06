import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="ContentRecycle AI", layout="centered")
st.title("♻️ ContentRecycle AI")

api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("Lipsește cheia API în Secrets!")
else:
    genai.configure(api_key=api_key)
    
    # Găsim automat un model valid care suportă generarea de text
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    if not available_models:
        st.error("Nu am găsit niciun model disponibil pentru această cheie API.")
    else:
        # Alegem primul model disponibil (de obicei gemini-1.5-flash sau gemini-pro)
        target_model = available_models[0]
        model = genai.GenerativeModel(target_model)
        
        st.info(f"Model activat cu succes: {target_model}")

        text_input = st.text_area("Introdu textul pentru reciclare:", height=200)

        if st.button("Generează Postări"):
            if text_input:
                with st.spinner('AI-ul lucrează...'):
                    try:
                        prompt = f"Transformă acest text în 3 postări de social media (LinkedIn, X, Instagram): {text_input}"
                        response = model.generate_content(prompt)
                        st.divider()
                        st.markdown(response.text)
                    except Exception as e:
                        st.error(f"Eroare la generare: {e}")
            else:
                st.warning("Introdu un text mai întâi!")
