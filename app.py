import os
import sys
import time
from datetime import datetime

# -----------------------------------------------------------------------------
# FOOLPROOF DEPENDENCY LOADER
# -----------------------------------------------------------------------------
try:
    from groq import Groq
except ImportError:
    os.system(f"{sys.executable} -m pip install groq")
    from groq import Groq

import streamlit as st

# -----------------------------------------------------------------------------
# INTERFACE DESIGN & VISUAL STYLING (UI/UX DESIGN SYSTEM)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Lumina Translate AI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom injection for professional banking-grade clean design
st.markdown("""
    <style>
    /* Global Background and Typography Framework */
    .stApp {
        background-color: #f8fafc;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    h1, h2, h3 {
        color: #0f172a !important;
        font-family: 'Inter', -apple-system, sans-serif !important;
        font-weight: 700 !important;
    }
    
    /* Layout Workspace Cards */
    .workspace-card {
        background-color: #ffffff;
        padding: 28px;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
        margin-bottom: 24px;
        transition: all 0.3s ease;
    }
    .workspace-card:hover {
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        transform: translateY(-2px);
    }
    
    /* Input Field & Output Frame Customization */
    .stTextArea textarea {
        font-size: 16px !important;
        border-radius: 10px !important;
        border: 1px solid #cbd5e1 !important;
        background-color: #ffffff !important;
        color: #334155 !important;
        transition: all 0.2s ease;
        padding: 12px !important;
    }
    .stTextArea textarea:focus {
        border-color: #2563eb !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15) !important;
    }
    
    /* Dynamic Translation Result Box */
    .translation-output-box {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        min-height: 280px;
        font-size: 16px;
        line-height: 1.7;
        color: #0f172a;
        white-space: pre-wrap;
        transition: all 0.3s ease;
        position: relative;
    }
    .translation-output-box:hover {
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    .translation-empty-state {
        color: #94a3b8;
        font-style: italic;
        display: flex;
        align-items: center;
        justify-content: center;
        height: 220px;
        font-size: 16px;
    }
    
    /* Elegant Custom Badges */
    .badge {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .badge-primary { background-color: #e0f2fe; color: #0369a1; }
    .badge-success { background-color: #dcfce7; color: #15803d; }
    .badge-warning { background-color: #fef3c7; color: #92400e; }
    .badge-error { background-color: #fee2e2; color: #b91c1c; }
    
    /* Action Button Adjustments */
    div.stButton > button:first-child {
        background-color: #2563eb !important;
        color: white !important;
        border-radius: 10px !important;
        padding: 14px 28px !important;
        font-weight: 600 !important;
        border: none !important;
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2) !important;
        transition: all 0.2s ease;
        font-size: 16px;
    }
    div.stButton > button:first-child:hover {
        background-color: #1d4ed8 !important;
        box-shadow: 0 4px 12px -1px rgba(37, 99, 235, 0.3) !important;
        transform: translateY(-1px);
    }
    
    /* Loading Spinner Customization */
    .stSpinner > div {
        border-top-color: #2563eb !important;
        width: 50px !important;
        height: 50px !important;
    }
    
    /* Sidebar Customization */
    .stSidebar {
        background-color: #f1f5f9;
        border-right: 1px solid #e2e8f0;
    }
    
    /* Progress Bar */
    .stProgress > div > div {
        background-color: #2563eb !important;
        height: 8px !important;
        border-radius: 4px !important;
    }
    
    /* Copy Button */
    .copy-button {
        background-color: #f1f5f9 !important;
        color: #64748b !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        font-size: 14px !important;
        cursor: pointer;
        transition: all 0.2s ease;
        font-weight: 500;
    }
    .copy-button:hover {
        background-color: #e2e8f0 !important;
        color: #475569 !important;
    }
    
    /* Status Indicators */
    .status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 10px;
    }
    
    /* Language Selector Styling */
    .stSelectbox {
        border-radius: 10px !important;
        border: 1px solid #cbd5e1 !important;
        font-size: 15px !important;
        padding: 8px 12px !important;
    }
    
    /* Translation Info Bar */
    .translation-info {
        background-color: #f8fafc;
        padding: 12px 16px;
        border-radius: 8px;
        margin-bottom: 16px;
        border: 1px solid #e2e8f0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 14px;
        color: #64748b;
    }
    
    /* Success Animation */
    @keyframes success-pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    .success-animation {
        animation: success-pulse 0.5s ease;
    }
    
    /* Character Counter */
    .char-counter {
        font-size: 12px;
        color: #94a3b8;
        text-align: right;
        margin-top: 4px;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# INITIALIZATION & CREDENTIAL SECURITY
# -----------------------------------------------------------------------------
api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")

if not api_key:
    st.sidebar.markdown("### 🔑 Authentication")
    api_key = st.sidebar.text_input(
        "Groq API Key", 
        type="password", 
        placeholder="gsk_..."
    )
    st.sidebar.caption("Provide your key above or save it in your project's Secrets configuration layout.")

client = None
if api_key:
    client = Groq(api_key=api_key)

# -----------------------------------------------------------------------------
# UX ENGINE PARAMETERS (SIDEBAR OPTIONS)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title("⚙️ Engine Control")
    st.write("Configure model optimization preferences below.")
    
    model_choice = st.selectbox(
        "Model Architecture",
        options=["llama-3.3-70b-versatile", "llama3-8b-8192"],
        index=0,
        help="Llama 3.3 70B represents top-tier structural accuracy for contextual translation processing."
    )
    
    translation_tone = st.select_slider(
        "Stylistic Profile Delivery",
        options=["Literal", "Balanced", "Creative"],
        value="Balanced",
        help="Literal focuses on exact semantic matching. Creative adapts idioms fluently."
    )
    
    st.divider()
    st.markdown("### 🌐 Operational Status")
    if client:
        st.markdown('<span class="badge badge-success">● Engine Connected</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="badge badge-primary">○ Awaiting Key Input</span>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# CORE MAIN APPLICATION WORKSPACE
# -----------------------------------------------------------------------------
# Header with logo and title
st.markdown("""
    <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 24px; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; color: white;">
        <span style="font-size: 32px;">✨</span>
        <div>
            <h1 style="margin: 0; padding: 0; font-size: 28px;">Lumina Translate AI</h1>
            <p style="margin: 0; color: rgba(255,255,255,0.9); font-size: 14px;">Enterprise-grade low latency translation infrastructure</p>
        </div>
    </div>
""", unsafe_allow_html=True)

st.write("")

LANGUAGES = [
    "English", "Burmese", "Thai", "Vietnamese", "Japanese", 
    "Korean", "Chinese (Mandarin)", "French", "Spanish", "German"
]

# Grid Framework Distribution Layout
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="workspace-card">', unsafe_allow_html=True)
    st.markdown('<span class="badge badge-primary">INPUT RESOURCE</span>', unsafe_allow_html=True)
    
    # Selection Inputs grouped elegantly
    source_lang = st.selectbox("Source Language Profile", ["Detect Language"] + LANGUAGES)
    
    input_text = st.text_area(
        "Content Entry Frame", 
        height=280, 
        placeholder="Type, drop, or paste standard text content here to parse translation...",
        key="input_text"
    )
    
    # Character counter
    if input_text:
        char_count = len(input_text)
        st.markdown(f'<div class="char-counter">Characters: {char_count}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="workspace-card">', unsafe_allow_html=True)
    st.markdown('<span class="badge badge-success">FINALIZED TRANSLATION</span>', unsafe_allow_html=True)
    
    target_lang = st.selectbox("Target Target Language", [lang for lang in LANGUAGES if lang != source_lang], index=0)
    
    # Translation info bar
    st.markdown(f'''
        <div class="translation-info">
            <span>Model: {model_choice}</span>
            <span>Style: {translation_tone}</span>
        </div>
    ''', unsafe_allow_html=True)
    
    # Action Controller Execution Trigger
    translate_button = st.button("🚀 Process Translation Pipeline", use_container_width=True)
    
    st.write("")
    output_placeholder = st.empty()
    
    # Initialize UI placeholder state component elegantly
    output_placeholder.markdown(
        '<div class="translation-output-box"><div class="translation-empty-state">Awaiting context generation runtime trigger...</div></div>', 
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# ENGINE RUNTIME COMPILER LOGIC
# -----------------------------------------------------------------------------
if translate_button:
    if not client:
        st.error("⚠️ Active Engine Credentials Required: Please pass a valid Groq API key parameter to continue.")
    elif not input_text.strip():
        st.warning("⚠️ Processing Request Aborted: Source input field cannot be blank.")
    else:
        with st.spinner("Processing pipeline sequence optimization inputs..."):
            try:
                # Show progress bar
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(i + 1)
                
                # System design context payload guidelines
                system_instruction = (
                    f"You are an elite linguistic engine. Translate text explicitly into {target_lang}. "
                    f"Maintain a strict {translation_tone} linguistic framework profile. "
                    "Provide ONLY the pure finalized translation output string. Remove all pleasantries, commentary, and surrounding punctuation markers."
                )
                
                if source_lang != "Detect Language":
                    user_prompt = f"Translate cleanly from {source_lang} to {target_lang}:\n\n{input_text}"
                else:
                    user_prompt = f"Identify origin tongue structures and translate explicitly into {target_lang}:\n\n{input_text}"
                
                temp_map = {"Literal": 0.1, "Balanced": 0.45, "Creative": 0.8}
                
                response = client.chat.completions.create(
                    model=model_choice,
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=temp_map[translation_tone],
                    max_tokens=3072
                )
                
                translated_result = response.choices[0].message.content.strip()
                
                # Hide progress bar
                progress_bar.empty()
                
                # Render beautifully formatted text blocks container
                output_placeholder.markdown(
                    f'''
                    <div class="translation-output-box success-animation">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                            <span style="font-size: 14px; color: #64748b;">Translation Result</span>
                            <button class="copy-button" onclick="navigator.clipboard.writeText('{translated_result.replace("'", "\\'")}'); this.textContent='✓ Copied!'; setTimeout(() => this.textContent='📋 Copy', 2000);">
                                📋 Copy
                            </button>
                        </div>
                        {translated_result}
                    </div>
                    ''', 
                    unsafe_allow_html=True
                )
                
            except Exception as error:
                progress_bar.empty()
                st.error(f"Engine Runtime Exception encountered: {str(error)}")
