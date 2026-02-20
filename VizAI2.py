import streamlit as st
from google import genai
from google.genai import types

# 1. Page Config & Custom Styling
st.set_page_config(page_title="VizAI - College Search", page_icon="🎓", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stChatMessage { border-radius: 15px; padding: 12px; margin-bottom: 10px; border: 1px solid #e0e0e0; }
    h1 { color: #1E3A8A; font-family: 'Inter', sans-serif; text-align: left; }
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
    "English": "You are VizAI, an expert student counselor. Help users find schools and colleges in ",
    "Spanish": "Eres VizAI, un consejero estudiantil experto. Ayuda a los usuarios a encontrar escuelas y universidades en ",
    "Telugu": "మీరు VizAI, విద్యార్థి కౌన్సెలర్. ఇక్కడ పాఠశాలలు మరియు కళాశాలలను కనుగొనడంలో సహాయపడండి: ",
    "Tamil": "நீங்கள் VizAI, ஒரு மாணவர் ஆலோசகர். பள்ளிகள் மற்றும் கல்லூரிகளைக் கண்டறிய உதவவும்: ",
    "Hindi": "आप VizAI हैं, एक विशेषज्ञ छात्र परामर्शदाता। यहां स्कूल और कॉलेज खोजने में मदद करें: "
}
selected_lang = st.sidebar.selectbox("Select Language", list(personas.keys()))

# State Selection (Set index=None for a blank/placeholder start)
selected_state = st.sidebar.selectbox(
    "Target US State", 
    us_states, 
    index=None, 
    placeholder="Select a State"
)

# 4. Final System Instruction Assembly
# Only include state context if a state is selected
state_context = selected_state if selected_state else "[Pending Selection]"

final_instructions = (
    f"{personas[selected_lang]} {state_context}. "
    "Your personality: You are a student counselor, polite and a little funny too. "
    "CRITICAL RULE: If the student has just selected a state, greet them warmly and enthusiastically. "
    "Based on the selection of State and Language, greet him and ask what he is looking for. "
    "If he asks about school or colleges, ask the student about his next level of education and information he is looking for. "
    "Provide the all the public and private school details in a single line with precise and perfect details. "
    "Use the following structure:\n"
    "School: \nOffering Classes: \nFee details: \nSubjects and Syllabus: \nSuggestions: \n"
    "Based on the response provide detailed information about that school/college."
)

# 5. Session State & Logic
if "history" not in st.session_state or "config" not in st.session_state:
    st.session_state.history = []
    st.session_state.config = f"{selected_lang}-{selected_state}"

# Reset chat if Language or State changes to keep context fresh
if st.session_state.config != f"{selected_lang}-{selected_state}":
    st.session_state.history = []
    st.session_state.config = f"{selected_lang}-{selected_state}"
    st.rerun()

# 6. UI Header
st.title("🎓 Ask VizAI")
st.markdown("<p style='text-align: left;'><i>School & College search, simplified</i></p>", unsafe_allow_html=True)

if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.history = []
    st.rerun()

# 7. Gemini Client (API Key from st.secrets)
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# 8. Chat Display & Input
for message in st.session_state.history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Only show chat input if a state is selected
if selected_state:
    if prompt := st.chat_input(f"Ask about education in {selected_state}..."):
        st.session_state.history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = client.models.generate_content(
                model="google/gemini-2.5-flash-lite",
                config=types.GenerateContentConfig(system_instruction=final_instructions),
                contents=[msg["content"] for msg in st.session_state.history]
            )
            reply = response.text
            st.markdown(reply)
            st.session_state.history.append({"role": "assistant", "content": reply})
else:
    st.info("👋 Please select a Target US State in the sidebar to start your consultation!")

st.sidebar.markdown("---")
st.sidebar.write(f"📍 **Focus:** {selected_state if selected_state else 'Not Selected'}")
st.sidebar.write(f"🌐 **Language:** {selected_lang}")
st.sidebar.markdown("---")
st.sidebar.markdown("❤️ Made by Vijay")
