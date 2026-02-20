import streamlit as st
from google import genai
from google.genai import types

# 1. Page Config & Custom Styling
st.set_page_config(page_title="VizAI - College Search", page_icon="🎓", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stChatMessage { border-radius: 15px; padding: 12px; margin-bottom: 10px; border: 1px solid #e0e0e0; }
    h1 { color: #1E3A8A; font-family: 'Inter', sans-serif; text-align: center; }
    .stButton>button { width: 100%; border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 2. US States List
us_states = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", 
    "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", 
    "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", 
    "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", 
    "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", 
    "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", 
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", 
    "Wisconsin", "Wyoming"
]

# 3. Sidebar Persona & State Selection
st.sidebar.title("🎨 Customize VizAI")

# Language Selection
personas = {
    "English": "You are VizAI, an expert college counselor. Help users find colleges in ",
    "Spanish": "Eres VizAI, un consejero universitario experto. Ayuda a los usuarios a encontrar universidades en ",
    "Telugu": "మీరు VizAI, కళాశాల కౌన్సెలర్. అండర్ గ్రాడ్యుయేట్ కళాశాల వివరాలను ఇక్కడ కనుగొనడంలో సహాయపడండి: ",
    "Tamil": "நீங்கள் VizAI, ஒரு கல்லூரி ஆலோசகர். கல்லூரிகளைக் கண்டறிய உதவவும்: ",
    "Hindi": "आप VizAI हैं, एक विशेषज्ञ कॉलेज काउंसलर। यहां कॉलेज खोजने में मदद करें: "
}
selected_lang = st.sidebar.selectbox("Select Language", list(personas.keys()))

# State Selection (The new dropdown)
selected_state = st.sidebar.selectbox("Target US State", us_states, index=42) # Default to Texas

# Final System Instruction Assembly
final_instructions = f"{personas[selected_lang]} {selected_state}. Simplify details and use tables for comparisons."

# 4. Session State & Logic
if "history" not in st.session_state or "config" not in st.session_state:
    st.session_state.history = []
    st.session_state.config = f"{selected_lang}-{selected_state}"

# Reset chat if Language or State changes to keep context fresh
if st.session_state.config != f"{selected_lang}-{selected_state}":
    st.session_state.history = []
    st.session_state.config = f"{selected_lang}-{selected_state}"
    st.rerun()

# 5. UI Header
st.title("🎓 Ask VizAI")
st.markdown("<p style='text-align: center;'><i>Undergrad college search, simplified</i></p>", unsafe_allow_html=True)

if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.history = []
    st.rerun()

# 6. Gemini Client (API Key from st.secrets)
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# 7. Chat Display & Input
for message in st.session_state.history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input(f"Ask about colleges in {selected_state}..."):
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(system_instruction=final_instructions),
            contents=[msg["content"] for msg in st.session_state.history]
        )
        reply = response.text
        st.markdown(reply)
        st.session_state.history.append({"role": "assistant", "content": reply})

st.sidebar.markdown("---")
st.sidebar.write(f"📍 **Focus:** {selected_state}")
st.sidebar.write(f"🌐 **Language:** {selected_lang}")

st.sidebar.markdown("---")
st.sidebar.markdown("❤️ Made by [Build Fast with AI](https://buildfastwithai.com)")
