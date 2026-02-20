import streamlit as st
from google import genai
from google.genai import types

# 1. Page Config & Custom Styling
st.set_page_config(page_title="VizAI - College Search", page_icon="🎓", layout="wide")

# Injecting Custom CSS for a modern, clean look
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stChatMessage { border-radius: 15px; padding: 10px; margin-bottom: 10px; border: 1px solid #e0e0e0; }
    .st-emotion-cache-1c7n2ka { max-width: 800px; margin: auto; } /* Center content */
    div[data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #ddd; }
    h1 { color: #1E3A8A; font-family: 'Inter', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar Persona Logic
st.sidebar.title("🎨 VizAI Customization")

personas = {
    "English": "You are VizAI, a helpful college counselor. Simplify undergrad search details. Use tables for comparisons.",
    "Spanish": "Eres VizAI, un consejero universitario experto. Simplifica la búsqueda de universidades en español.",
    "Telugu": "మీరు VizAI, కళాశాల కౌన్సెలర్. అండర్ గ్రాడ్యుయేట్ కళాశాల వివరాలను తెలుగులో సులభతరం చేయండి.",
    "Tamil": "நீங்கள் VizAI, ஒரு கல்லூரி ஆலோசகர். இளங்கலை கல்லூரி விவரங்களை தமிழில் எளிமைப்படுத்துங்கள்.",
    "Hindi": "आप VizAI हैं, एक कॉलेज काउंसलर। स्नातक कॉलेज विवरणों को हिंदी में सरल बनाएं।"
}

selected_lang = st.sidebar.selectbox("Choose Language Persona", list(personas.keys()))
custom_instructions = st.sidebar.text_area("Refine Instructions", value=personas[selected_lang], height=100)

# 3. Session State Management
if "history" not in st.session_state or "current_persona" not in st.session_state:
    st.session_state.history = []
    st.session_state.current_persona = selected_lang

# Reset chat if persona changes
if st.session_state.current_persona != selected_lang:
    st.session_state.history = []
    st.session_state.current_persona = selected_lang
    st.rerun()

# 4. Header
st.title("🎓 Ask VizAI")
st.markdown("##### *Undergrad college search, simplified*")

# 5. Initialize Client (Ensure GEMINI_API_KEY is in your .streamlit/secrets.toml)
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# 6. Display History
for message in st.session_state.history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. Chat Interaction
if prompt := st.chat_input("Ask about Texas colleges, tuition, or rankings..."):
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # We use 'gemini-2.0-flash' or 'gemini-1.5-flash' depending on your tier access
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                system_instruction=custom_instructions
            ),
            contents=[msg["content"] for msg in st.session_state.history]
        )
        reply = response.text
        st.markdown(reply)
        st.session_state.history.append({"role": "assistant", "content": reply})

# Sidebar Footer
st.sidebar.markdown("---")
st.sidebar.markdown("🚀 **VizAI v2.0**")
st.sidebar.info("Tip: Switching languages resets the chat to keep context consistent.")
