import streamlit as st
import google.generativeai as genai

# Page Config
st.set_page_config(page_title="ContentRecycle AI", layout="centered", page_icon="♻️")

# --- ACCESS SYSTEM ---
# Make sure to set APP_PASSWORD in your Streamlit Secrets
ACCESS_PASSWORD = st.secrets.get("APP_PASSWORD")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("♻️ ContentRecycle AI")
    st.subheader("Transform long content into viral social media posts in seconds.")
    st.write("---")
    st.info("🔒 This is a premium AI tool. Please enter your access password below.")
    
    pwd = st.text_input("Enter Password:", type="password")
    
    if st.button("Unlock Access"):
        if pwd == ACCESS_PASSWORD:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Invalid password!")
            # REPLACE THE LINK BELOW WITH YOUR GUMROAD LINK
            st.markdown(f"### [Don't have a password? Get it for $2 here](https://farcastor.gumroad.com/l/xumhyx)")
    
    st.write("---")
    st.caption("Powered by Google Gemini AI")
    st.stop()

# --- MAIN APP (Visible only after login) ---
st.title("♻️ ContentRecycle AI - Dashboard")
st.write("Welcome! Paste your article, transcript, or ideas below.")

api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("API Key missing. Check Streamlit Secrets.")
else:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    source_text = st.text_area("Paste your source content here:", height=250, placeholder="E.g., A YouTube transcript, a blog post, or a long thought...")
    
    if st.button("Generate Social Posts"):
        if source_text:
            with st.spinner("AI is crafting your posts..."):
                try:
                    prompt = (
                        "Convert the following text into 3 distinct social media posts:\n"
                        "1. Professional & Insightful (for LinkedIn)\n"
                        "2. Short & Punchy (for X/Twitter)\n"
                        "3. Engaging & Visual-focused (for Instagram/Threads)\n"
                        f"Text: {source_text}"
                    )
                    response = model.generate_content(prompt)
                    st.divider()
                    st.markdown(response.text)
                    st.success("Done! You can now copy-paste these to your socials.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.warning("Please provide some text first!")

st.write("---")
if st.button("Logout"):
    st.session_state["authenticated"] = False
    st.rerun()
