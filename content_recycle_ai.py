import streamlit as st
import requests

# --- PAGE CONFIG ---
st.set_page_config(page_title="ContentRecycle AI", layout="centered", page_icon="♻️")

# --- DATA ACCESS ---
# Using your Groq API Key
GROQ_API_KEY = "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"
ACCESS_PASSWORD = st.secrets.get("APP_PASSWORD")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# --- LOGIN SCREEN ---
if not st.session_state["authenticated"]:
    st.title("♻️ ContentRecycle AI")
    st.subheader("Transform any content into viral social media posts.")
    st.write("---")
    
    pwd = st.text_input("Access Password:", type="password")
    if st.button("Unlock Access"):
        if pwd == ACCESS_PASSWORD:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Invalid Password!")
            st.markdown("### [Get access here](https://farcastor.gumroad.com/l/xumhyx)")
    st.stop()

# --- MAIN DASHBOARD ---
st.title("♻️ ContentRecycle AI - Dashboard")
st.write("Paste your content below and let the AI do the magic.")

source_text = st.text_area("Source Content:", height=200, placeholder="E.g., YouTube transcript, blog article, or raw notes...")

if st.button("Generate Posts"):
    if source_text:
        with st.spinner("AI is crafting your posts..."):
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            
            # THE PROMPT (English instructions)
            data = {
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {
                        "role": "system", 
                        "content": "You are a professional social media content generator. Your task: take ANY input and transform it into 3 viral posts (LinkedIn, X, and Instagram). Do NOT ask for more info. Do NOT explain yourself. Just output the posts in English. Even if the input is short, weird, or in another language, create high-quality viral posts in English based on it."
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
                    st.success("Success! Posts generated.")
                else:
                    st.error(f"Groq Error: {response.status_code}")
                    st.json(response.json())
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please provide some text first!")

st.write("---")
if st.button("Logout"):
    st.session_state["authenticated"] = False
    st.rerun()
