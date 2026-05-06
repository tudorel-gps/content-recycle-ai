"""
╔══════════════════════════════════════════════════════════════════╗
║              ContentRecycle AI — MVP cu Streamlit                ║
║  Transformă orice text în postări optimizate pentru rețele sociale║
╚══════════════════════════════════════════════════════════════════╝

INSTRUCȚIUNI DE PORNIRE:
─────────────────────────
1. Instalează dependențele:
       pip install streamlit anthropic

2. ⚠️  INTRODU CHEIA API (vezi secțiunea CONFIG mai jos)

3. Rulează aplicația:
       streamlit run content_recycle_ai.py

Notă: Poți folosi fie Anthropic (recomandat), fie OpenAI.
"""

import streamlit as st
import anthropic

# ─────────────────────────────────────────────────────────────────
# ░░░  ZONA DE CONFIGURARE — EDITEAZĂ DOAR ACEASTĂ SECȚIUNE  ░░░
# ─────────────────────────────────────────────────────────────────

# OPȚIUNEA 1 (Recomandat): Introdu direct cheia API Anthropic
# Obții cheia de la: https://console.anthropic.com/settings/keys
ANTHROPIC_API_KEY = "sk-ant-INTRODU_CHEIA_TA_AICI"

# OPȚIUNEA 2 (Mai sigur — pentru producție): Folosește variabile de mediu
# Setează în terminal: export ANTHROPIC_API_KEY="sk-ant-..."
# Apoi decomentează linia de mai jos și comentează linia de deasupra:
# import os
# ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

# Modelul Claude folosit (nu modifica dacă ești la început)
MODEL = "claude-opus-4-5"

# ─────────────────────────────────────────────────────────────────
# ░░░          CONFIGURARE INTERFAȚĂ STREAMLIT                 ░░░
# ─────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="ContentRecycle AI",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# CSS personalizat pentru un design minimalist și curat
st.markdown("""
<style>
    /* Import font elegant */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Syne:wght@700;800&display=swap');

    /* Reset și bază */
    .stApp {
        background: #0f0f13;
        font-family: 'Inter', sans-serif;
    }

    /* Header principal */
    .main-header {
        text-align: center;
        padding: 2.5rem 0 1.5rem 0;
        margin-bottom: 2rem;
    }

    .main-header h1 {
        font-family: 'Syne', sans-serif;
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #a8edea, #fed6e3, #c3cfe2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem;
    }

    .main-header p {
        color: #666880;
        font-size: 1.05rem;
        font-weight: 300;
        letter-spacing: 0.02em;
    }

    /* Card-uri pentru output */
    .output-card {
        background: #16161f;
        border: 1px solid #2a2a3a;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: border-color 0.3s ease;
    }

    .output-card:hover {
        border-color: #444466;
    }

    .platform-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: #1e1e2e;
        border-radius: 8px;
        padding: 0.35rem 0.8rem;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 1rem;
        border: 1px solid #2a2a3a;
    }

    /* Textarea styling */
    .stTextArea textarea {
        background: #16161f !important;
        border: 1px solid #2a2a3a !important;
        border-radius: 12px !important;
        color: #d0d0e0 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.95rem !important;
        padding: 1rem !important;
    }

    .stTextArea textarea:focus {
        border-color: #a8edea !important;
        box-shadow: 0 0 0 3px rgba(168, 237, 234, 0.1) !important;
    }

    /* Buton principal */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #a8edea, #c3cfe2) !important;
        color: #0f0f13 !important;
        border: none !important;
        border-radius: 12px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        padding: 0.8rem 2rem !important;
        letter-spacing: 0.03em;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 30px rgba(168, 237, 234, 0.25) !important;
    }

    /* Statistici mici */
    .stat-chip {
        background: #1e1e2e;
        border: 1px solid #2a2a3a;
        border-radius: 20px;
        padding: 0.3rem 0.9rem;
        font-size: 0.75rem;
        color: #666880;
        display: inline-block;
        margin: 0.2rem;
    }

    /* Label-uri */
    .stTextArea label, .stSelectbox label {
        color: #888899 !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase !important;
    }

    /* Divider */
    hr {
        border-color: #2a2a3a !important;
        margin: 1.5rem 0 !important;
    }

    /* Textul din output */
    .output-text {
        color: #c8c8d8;
        font-size: 0.95rem;
        line-height: 1.7;
        white-space: pre-wrap;
        font-family: 'Inter', sans-serif;
    }

    /* Success/error messages */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 10px !important;
    }

    /* Ascunde elementele Streamlit implicite */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# ░░░           FUNCȚII PRINCIPALE — LOGICA APLICAȚIEI         ░░░
# ─────────────────────────────────────────────────────────────────

def build_prompt(text: str, tone_level: str) -> str:
    """
    Construiește prompt-ul trimis către Claude.
    Returnează un singur string cu instrucțiuni clare pentru
    generarea celor 3 formate de postare.
    """
    tone_instruction = {
        "Echilibrat": "Menține un ton natural și autentic.",
        "Formal / Corporativ": "Folosește un limbaj formal, profesional și corporativ.",
        "Casual / Prietenos": "Folosește un ton cald, casual și conversațional.",
    }.get(tone_level, "Menține un ton natural.")

    prompt = f"""
Ești un expert în social media marketing. Vei transforma textul de mai jos în 3 postări optimizate.
{tone_instruction}

REGULI STRICTE:
- Răspunde EXCLUSIV cu cele 3 postări, fără explicații suplimentare
- Folosește limba textului original (dacă textul e în română, postările vor fi în română)
- Respectă exact formatul de mai jos

TEXT ORIGINAL:
\"\"\"
{text}
\"\"\"

---

[LINKEDIN]
(Postare profesională de 150-250 cuvinte. Include un hook puternic în prima linie, paragraf de context, 2-3 insight-uri cheie, o concluzie cu call-to-action și 3-5 hashtag-uri relevante. Fără emoji-uri excesive.)

[TWITTER/X]
(Postare virală de maxim 280 caractere. Hook direct, mesaj clar, opțional un emoji relevant, 2-3 hashtag-uri. Poate fi o serie de 2-3 tweet-uri numerotate dacă subiectul o cere.)

[INSTAGRAM]
(Postare vizuală cu 4-6 bullet points cu emoji-uri, un caption introductiv de 1-2 propoziții, și o întrebare la final pentru engagement. Încheie cu 5-8 hashtag-uri populare.)
"""
    return prompt


def generate_content(text: str, tone_level: str) -> dict:
    """
    Apelează API-ul Anthropic Claude și returnează un dicționar
    cu postările pentru fiecare platformă.
    """
    # Inițializare client Anthropic cu cheia API definită mai sus
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    # Construim prompt-ul
    prompt = build_prompt(text, tone_level)

    # Apel API către Claude
    # Ajustează max_tokens dacă vrei răspunsuri mai lungi/scurte
    message = client.messages.create(
        model=MODEL,
        max_tokens=1500,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # Extragem răspunsul text
    raw_response = message.content[0].text

    # Parsăm răspunsul în secțiunile celor 3 platforme
    results = parse_response(raw_response)
    return results


def parse_response(raw_text: str) -> dict:
    """
    Parsează răspunsul brut de la Claude și îl împarte
    în 3 secțiuni corespunzătoare platformelor.
    """
    sections = {
        "linkedin": "",
        "twitter": "",
        "instagram": "",
    }

    # Căutăm delimitatorii și extragem conținutul dintre ei
    markers = {
        "linkedin": "[LINKEDIN]",
        "twitter": "[TWITTER/X]",
        "instagram": "[INSTAGRAM]",
    }

    text = raw_text.strip()

    for i, (key, marker) in enumerate(markers.items()):
        start_idx = text.find(marker)
        if start_idx == -1:
            continue

        start_idx += len(marker)

        # Găsim sfârșitul acestei secțiuni (începutul următoarei)
        next_markers = list(markers.values())[i + 1:]
        end_idx = len(text)
        for next_marker in next_markers:
            nm_idx = text.find(next_marker, start_idx)
            if nm_idx != -1:
                end_idx = nm_idx
                break

        sections[key] = text[start_idx:end_idx].strip()

    # Fallback: dacă parsarea nu funcționează, returnăm textul brut
    if not any(sections.values()):
        sections["linkedin"] = raw_text
        sections["twitter"] = "⚠️ Nu s-a putut parsa automat. Verifică răspunsul complet în câmpul LinkedIn."
        sections["instagram"] = "⚠️ Nu s-a putut parsa automat."

    return sections


def count_words(text: str) -> int:
    """Numără cuvintele dintr-un text."""
    return len(text.split()) if text.strip() else 0


def count_chars(text: str) -> int:
    """Numără caracterele dintr-un text."""
    return len(text)


# ─────────────────────────────────────────────────────────────────
# ░░░                   INTERFAȚA UTILIZATOR                   ░░░
# ─────────────────────────────────────────────────────────────────

# Header
st.markdown("""
<div class="main-header">
    <h1>♻️ ContentRecycle AI</h1>
    <p>Transformă orice text în postări optimizate pentru LinkedIn, X și Instagram</p>
</div>
""", unsafe_allow_html=True)

# ── Validare cheie API ──────────────────────────────────────────
if not ANTHROPIC_API_KEY or "INTRODU_CHEIA" in ANTHROPIC_API_KEY:
    st.warning(
        "⚠️  **Cheia API lipsește!** Deschide fișierul Python și înlocuiește "
        "`ANTHROPIC_API_KEY` cu cheia ta reală de la [console.anthropic.com](https://console.anthropic.com/settings/keys)."
    )

st.markdown("---")

# ── Layout principal: Input (stânga) | Output (dreapta) ────────
col_input, col_output = st.columns([1, 1.3], gap="large")

# ── COLOANA STÂNGA: Input ──────────────────────────────────────
with col_input:
    st.markdown("#### ✍️ Textul tău")

    # Zona de input pentru textul utilizatorului
    user_text = st.text_area(
        label="TEXT SURSĂ",
        placeholder=(
            "Lipește aici transcriptul, articolul sau orice text lung...\n\n"
            "Exemple:\n"
            "• Un transcript de podcast\n"
            "• Un articol de blog\n"
            "• Note de la un eveniment\n"
            "• Un raport sau o analiză"
        ),
        height=280,
        label_visibility="collapsed",
    )

    # Afișăm statistici despre textul introdus
    if user_text:
        words = count_words(user_text)
        chars = count_chars(user_text)
        st.markdown(
            f'<span class="stat-chip">📝 {words} cuvinte</span>'
            f'<span class="stat-chip">🔡 {chars} caractere</span>',
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Selector pentru tonul postărilor
    tone = st.selectbox(
        label="TON",
        options=["Echilibrat", "Formal / Corporativ", "Casual / Prietenos"],
        help="Alege tonul care se potrivește cu brandul tău personal sau al companiei."
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Butonul de generare
    generate_btn = st.button(
        "✨ Generează Postările",
        disabled=not user_text or not user_text.strip(),
        use_container_width=True,
    )

    # Tips pentru utilizator
    with st.expander("💡 Sfaturi pentru rezultate mai bune"):
        st.markdown("""
        - **Lungime optimă**: 300–2000 de cuvinte funcționează cel mai bine
        - **Context clar**: Cu cât textul e mai structurat, cu atât postările sunt mai relevante
        - **Limbă**: Aplicația detectează automat limba textului
        - **Iterează**: Poți regenera de mai multe ori pentru variații diferite
        """)


# ── COLOANA DREAPTA: Output ────────────────────────────────────
with col_output:
    st.markdown("#### 🚀 Postările generate")

    # Inițializăm session state pentru a păstra rezultatele între reruns
    if "results" not in st.session_state:
        st.session_state.results = None
    if "is_loading" not in st.session_state:
        st.session_state.is_loading = False

    # ── Declanșăm generarea la click pe buton ──
    if generate_btn and user_text.strip():
        st.session_state.is_loading = True

        with st.spinner("🤖 Claude generează postările tale..."):
            try:
                # Apelăm funcția principală de generare
                st.session_state.results = generate_content(user_text, tone)
                st.success("✅ Postările au fost generate cu succes!")
            except anthropic.AuthenticationError:
                st.error(
                    "❌ **Cheie API invalidă.** Verifică că ai introdus corect "
                    "cheia Anthropic în variabila `ANTHROPIC_API_KEY`."
                )
                st.session_state.results = None
            except anthropic.RateLimitError:
                st.error(
                    "⏱️ **Limită API depășită.** Ai atins limita de requests. "
                    "Încearcă din nou în câteva secunde."
                )
                st.session_state.results = None
            except Exception as e:
                st.error(f"❌ **Eroare neașteptată:** {str(e)}")
                st.session_state.results = None

        st.session_state.is_loading = False

    # ── Afișăm rezultatele dacă există ──
    if st.session_state.results:
        results = st.session_state.results

        # ── LinkedIn ─────────────────────────────────────────
        st.markdown("""
        <div class="output-card">
            <div class="platform-badge" style="color: #0A66C2; border-color: #0A66C2;">
                🔷 LinkedIn
            </div>
        </div>
        """, unsafe_allow_html=True)

        linkedin_text = results.get("linkedin", "")
        if linkedin_text:
            # Text area editabil cu postarea LinkedIn
            edited_linkedin = st.text_area(
                "LinkedIn Post",
                value=linkedin_text,
                height=200,
                label_visibility="collapsed",
                key="linkedin_output"
            )
            li_words = count_words(edited_linkedin)
            st.markdown(
                f'<span class="stat-chip">{li_words} cuvinte</span>',
                unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Twitter / X ──────────────────────────────────────
        st.markdown("""
        <div class="output-card">
            <div class="platform-badge" style="color: #e0e0e0; border-color: #444;">
                𝕏 Twitter / X
            </div>
        </div>
        """, unsafe_allow_html=True)

        twitter_text = results.get("twitter", "")
        if twitter_text:
            edited_twitter = st.text_area(
                "Twitter/X Post",
                value=twitter_text,
                height=130,
                label_visibility="collapsed",
                key="twitter_output"
            )
            tw_chars = count_chars(edited_twitter)
            tw_color = "🟢" if tw_chars <= 280 else "🔴"
            st.markdown(
                f'<span class="stat-chip">{tw_color} {tw_chars}/280 caractere</span>',
                unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Instagram ─────────────────────────────────────────
        st.markdown("""
        <div class="output-card">
            <div class="platform-badge" style="color: #E1306C; border-color: #E1306C;">
                📸 Instagram
            </div>
        </div>
        """, unsafe_allow_html=True)

        instagram_text = results.get("instagram", "")
        if instagram_text:
            edited_instagram = st.text_area(
                "Instagram Post",
                value=instagram_text,
                height=200,
                label_visibility="collapsed",
                key="instagram_output"
            )
            ig_words = count_words(edited_instagram)
            st.markdown(
                f'<span class="stat-chip">{ig_words} cuvinte</span>',
                unsafe_allow_html=True
            )

        # ── Buton de resetare ────────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Resetează și generează din nou", use_container_width=True):
            st.session_state.results = None
            st.rerun()

    else:
        # Stare goală — înainte de prima generare
        st.markdown("""
        <div style="text-align:center; padding: 4rem 2rem; color: #444466;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">✨</div>
            <div style="font-size: 1rem; font-weight: 500; margin-bottom: 0.5rem; color: #666880;">
                Postările tale apar aici
            </div>
            <div style="font-size: 0.85rem; color: #444466; line-height: 1.6;">
                Introdu textul în stânga și<br>apasă butonul de generare
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── Footer ──────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<p style="text-align:center; color: #333344; font-size: 0.8rem;">'
    'ContentRecycle AI · Powered by Anthropic Claude · MVP v1.0'
    '</p>',
    unsafe_allow_html=True
)
