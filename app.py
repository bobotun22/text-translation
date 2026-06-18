import os
import streamlit as st
from groq import Groq

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION & THEME (UI/UX)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Groq AI Translation Workspace",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling for an elegant layout
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
# INITIALIZATION & GROQ CLIENT
# -----------------------------------------------------------------------------
api_key = st.secrets.get("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)

if not api_key:
    api_key = st.sidebar.text_input(
        "🔑 Enter Groq API Key", 
        type="password", 
        help="Get a key from your GroqCloud console."
    )

client = None
if api_key:
    client = Groq(api_key=api_key)

# -----------------------------------------------------------------------------
# SIDEBAR CONTROLS
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title("⚡ Groq Options")
    st.caption("Control AI and translation behaviors")
    
    model_choice = st.selectbox(
        "Groq Model Engine",
        options=["llama-3.3-70b-versatile", "llama3-8b-8192"],
        index=0,
        help="Llama 3.3 70B is highly accurate for translation nuances."
    )
    
    translation_tone = st.select_slider(
        "Stylistic Tone",
        options=["Literal", "Balanced", "Creative"],
        value="Balanced"
    )

# -----------------------------------------------------------------------------
# MAIN LAYOUT INTERFACE
# -----------------------------------------------------------------------------
st.title("⚡ Groq Fast Translation Workspace")
st.markdown("Ultra-low latency translation powered by GroqCloud open-source models.")

LANGUAGES = [
    "English", "Burmese", "Thai", "Vietnamese", "Japanese", 
    "Korean", "Chinese (Mandarin)", "French", "Spanish", "German"
]

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
    
    translate_button = st.button("🚀 Process Translation", type="primary", use_container_width=True)
    
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
        st.error("⚠️ Active Groq API key credentials required. Please input your key in the sidebar.")
    elif not input_text.strip():
        st.warning("⚠️ Text processing cancelled: The source field is empty.")
    else:
        with st.spinner("Groq is processing your translation..."):
            try:
                system_instruction = (
                    f"You are an expert native translator translating directly into {target_lang}. "
                    f"Adhere strictly to a {translation_tone} tone structure. "
                    "Output only the finalized clean translation results. Do not provide conversational prefaces, intro sentences, or notes."
                )
                
                if source_lang != "Detect Language":
                    user_prompt = f"Translate the text accurately from {source_lang} to {target_lang}:\n\n{input_text}"
                else:
                    user_prompt = f"Identify the source language automatically and translate into {target_lang}:\n\n{input_text}"
                
                temp_map = {"Literal": 0.1, "Balanced": 0.4, "Creative": 0.75}
                
                response = client.chat.completions.create(
                    model=model_choice,
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=temp_map[translation_tone],
                    max_tokens=2048
                )
                
                translated_result = response.choices[0].message.content
                
                output_placeholder.markdown(
                    f'<div class="translation-output">{translated_result}</div>', 
                    unsafe_allow_html=True
                )
                
            except Exception as error:
                st.error(f"Groq Processing Exception encountered: {str(error)}")
