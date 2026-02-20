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

# Language Personas - Now with a "Detect Language" instruction
personas = {
    "English": "You are VizAI, an expert student counselor. Preferred language: English.",
    "Spanish": "You are VizAI, an expert student counselor. Preferred language: Spanish.",
    "Telugu": "You are VizAI, an expert student counselor. Preferred language: Telugu.",
    "Tamil": "You are VizAI, an expert student counselor. Preferred language: Tamil.",
    "Hindi": "You are VizAI, an expert student counselor. Preferred language: Hindi."
}

selected_lang = st.sidebar.selectbox("Select Language", list(personas.keys()))

# State Selection with Key for Resetting
selected_state = st.sidebar.selectbox(
    "Target US State", 
    us_states, 
    index=None, 
    placeholder="Select a State",
    key="state_selector" 
)

# 4. Final System Instruction Assembly
state_context = selected_state if selected_state else "[Pending Selection]"

final_instructions = (
    f"{personas[selected_lang]} Target State: {state_context}. "
    "SYSTEM RULE: Always respond in the SAME language the user uses for their message, "
    "even if it differs from the persona's 'Preferred language'. "
    "Your personality: You are a student counselor, polite and a little funny too. "
    "BEHAVIOR: Immediately after a state is selected, greet the student warmly and ask what they are looking for. "
    "If they ask about school or colleges, ask them about their next level of education and specific info needed. "
    "DATA FORMAT: Provide public/private school details in a single line with this structure:\n"
    "School: [Name] | Offering Classes: [Grades] | Fee details: [Fees] | Subjects and Syllabus: [Info] | Suggestions: [Advice]\n"
    "After providing the summary, offer to provide detailed information about a specific school."
)

# 5. Session State & Logic
if "history" not in st.session_state or "config" not in st.session_state:
    st.session_state.history = []
    st.session_state.config = f"{selected_lang}-{selected_state}"

# Reset chat if selection changes
if st.session_state.config != f"{selected_lang}-{selected_state}":
    st.session_state.history = []
    st.session_state.config = f"{selected_lang}-{selected_state}"
    st.rerun()

# 6. UI Header
st.title("🎓 Ask VizAI")
st.markdown("<p style='text-align: left;'><i>School & College search, simplified</i></p>", unsafe_allow_html=True)

# Clear Chat logic resets both history and the dropdown
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.history = []
    st.session_state.state_selector = None
    st.rerun()

# 7. Gemini Client
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# 8. Immediate Greeting Logic
# Triggers if a state is selected and no messages exist yet
if selected_state and len(st.session_state.history) == 0:
    with st.spinner("Initializing VizAI..."):
        # We send a hidden prompt to trigger the warm greeting
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            config=types.GenerateContentConfig(system_instruction=final_instructions),
            contents=[f"I have just selected {selected_state}. Greet me warmly in {selected_lang}!"]
        )
        st.session_state.history.append({"role": "assistant", "content": response.text})

# 9. Display Chat History
for message in st.session_state.history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 10. Chat Input
if selected_state:
    if prompt := st.chat_input(f"Ask about education in {selected_state}..."):
        st.session_state.history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = client.models.generate_content(
                model="gemini-2.0-flash-lite",
                config=types.GenerateContentConfig(system_instruction=final_instructions),
                contents=[msg["content"] for msg in st.session_state.history]
            )
            reply = response.text
            st.markdown(reply)
            st.session_state.history.append({"role": "assistant", "content": reply})
else:
    st.info("👋 Please select a Target US State in the sidebar to begin!")

st.sidebar.markdown("---")
st.sidebar.write(f"📍 **Focus:** {selected_state if selected_state else 'Not Selected'}")
st.sidebar.write(f"🌐 **Persona:** {selected_lang}")
st.sidebar.markdown("---")
st.sidebar.markdown("❤️ Made by Vijay")
