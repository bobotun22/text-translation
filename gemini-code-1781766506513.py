import os
import streamlit as st
from google import genai
from google.genai import types

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION & THEME (UI/UX)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Translation Workspace",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling for an elegant, distraction-free layout
st.markdown("""
    <style>
    .main {
        background-color: #fcfcfc;
    }
    .stTextArea textarea {
        font-size: 16px !important;
        border-radius: 8px !important;
        line-height: 1.5;
    }
    .translation-output {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        min-height: 160px;
        font-size: 16px;
        line-height: 1.6;
        color: #1a202c;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# INITIALIZATION & API CLIENT
# -----------------------------------------------------------------------------
# Checks Streamlit Secrets first, then local environment variables
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

# Fallback UI if the API key is not configured in the host environment
if not api_key:
    api_key = st.sidebar.text_input(
        "🔑 Enter Gemini API Key", 
        type="password", 
        help="Get a key from Google AI Studio to unlock translation features."
    )

client = None
if api_key:
    # Initializing the modern standard Client
    client = genai.Client(api_key=api_key)

# -----------------------------------------------------------------------------
# SIDEBAR CONTROLS
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title("⚙️ Workspace Options")
    st.caption("Control AI and translation behaviors")
    
    # Model configuration choice
    model_choice = st.selectbox(
        "AI Engine Profile",
        options=["gemini-2.5-flash", "gemini-2.5-pro"],
        index=0,
        help="Flash offers hyper-fast responses. Pro delivers maximum reasoning power for long documents."
    )
    
    # Context tone selection
    translation_tone = st.select_slider(
        "Stylistic Tone",
        options=["Literal", "Balanced", "Creative"],
        value="Balanced"
    )
    
    st.write("---")
    st.subheader("📦 Repository & Deployment")
    st.markdown("""
    **To deploy this workspace via GitHub:**
    1. Create a GitHub repo and add this file as `app.py`.
    2. Add a `requirements.txt` file listing your dependencies.
    3. Link the repository directly on **Streamlit Community Cloud**.
    """)
    st.link_button("🌐 Connect via GitHub", "https://github.com", use_container_width=True)

# -----------------------------------------------------------------------------
# MAIN LAYOUT INTERFACE
# -----------------------------------------------------------------------------
st.title("🌐 AI Translation Workspace")
st.markdown("Context-aware processing engine powered by Google Gemini.")

# Supported core languages
LANGUAGES = [
    "English", "Burmese", "Thai", "Vietnamese", "Japanese", 
    "Korean", "Chinese (Mandarin)", "French", "Spanish", "German"
]

# Structural 2-column distribution layout
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("### 📥 Source Selection")
    source_lang = st.selectbox("From language:", ["Detect Language"] + LANGUAGES)
    input_text = st.text_area(
        "Source Text Element", 
        height=280, 
        placeholder="Type or paste text content to process..."
    )

with col2:
    st.markdown("### 📤 Output Translation")
    target_lang = st.selectbox("To language:", [lang for lang in LANGUAGES if lang != source_lang], index=0)
    
    # Operational Action Trigger Button
    translate_button = st.button("🚀 Process Translation", type="primary", use_container_width=True)
    
    # Clean output state management container
    output_placeholder = st.empty()
    output_placeholder.markdown(
        '<div class="translation-output" style="color: #a0aec0; font-style: italic;">Processed output will populate here...</div>', 
        unsafe_allow_html=True
    )

# -----------------------------------------------------------------------------
# RUNTIME TRANSLATION LOGIC
# -----------------------------------------------------------------------------
if translate_button:
    if not client:
        st.error("⚠️ Active API key credentials required. Please input a valid API Key to initialize the client.")
    elif not input_text.strip():
        st.warning("⚠️ Text processing cancelled: The source field is empty.")
    else:
        with st.spinner("Analyzing context parameters and translating text..."):
            try:
                # System configuration instructions to eliminate conversational dialogue from the AI response
                system_instruction = (
                    f"You are an expert native translator translating directly into {target_lang}. "
                    f"Adhere strictly to a {translation_tone} tone structure. "
                    "Output only the finalized clean translation results. Do not provide conversational prefaces, feedback, or notes."
                )
                
                # Context parsing based on language detection settings
                if source_lang != "Detect Language":
                    user_prompt = f"Translate the text accurately from {source_lang} to {target_lang}:\n\n{input_text}"
                else:
                    user_prompt = f"Identify the source language automatically and translate into {target_lang}:\n\n{input_text}"
                
                # Dynamic mapping of the temperature configuration based on structural preference
                temp_map = {"Literal": 0.2, "Balanced": 0.5, "Creative": 0.85}
                
                # Running client execution matching current GenAI specifications
                response = client.models.generate_content(
                    model=model_choice,
                    contents=user_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=temp_map[translation_tone],
                    )
                )
                
                # Update UI container gracefully with structural result text
                output_placeholder.markdown(
                    f'<div class="translation-output">{response.text}</div>', 
                    unsafe_allow_html=True
                )
                
            except Exception as error:
                st.error(f"Runtime Processing Exception encountered: {str(error)}")
