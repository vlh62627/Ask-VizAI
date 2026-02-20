import streamlit as st
from google import genai
from google.genai import types

# --- Page config ---
st.set_page_config(
    page_title="Gemini Chatbot with System Prompt",
    page_icon="💬",
    layout="wide"
)

# --- App Header ---
st.markdown(
    """
    <div style='text-align:center; background-color:#f0f2f6; padding:20px; border-radius:10px'>
        <h1>💬 Ask VizAI</h1>
        <p style='font-size:16px; color:#555;'>College search, simplified</p>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Initialize Gemini client ---
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# --- Sidebar for system prompt and customization ---
st.sidebar.title("⚙️ Custom Instructions")
st.sidebar.write("Modify the system prompt or choose a persona for the AI.")

# Persona dropdown
persona = st.sidebar.selectbox(
    "Choose AI Persona 🌐",
    ["English", "Spanish", "Telugu", "Tamil", "Hindi"],
    index=0,
    help="Select a persona/language for the AI assistant."
)

# Map persona to default system prompt
persona_prompts = {
    "English": "You are a helpful assistant who communicates in English.",
    "Spanish": "Eres un asistente útil que comunica en español.",
    "Telugu": "మీరు సహాయక చాట్ అసిస్టెంట్, తెలుగు లో సమాధానాలు ఇవ్వండి.",
    "Tamil": "நீங்கள் உதவியாளராக இருக்கின்றீர்கள் மற்றும் தமிழ் மொழியில் பதிலளிக்கின்றீர்கள்.",
    "Hindi": "आप एक सहायक हैं और हिंदी में उत्तर देते हैं।"
}

# System prompt text area
system_prompt = st.sidebar.text_area(
    "System Prompt",
    value=persona_prompts[persona],
    height=150,
    help="The system prompt sets the behavior and personality of the AI assistant."
)

st.sidebar.info(
    "💡 **Tip:** Try prompts like:\n- 'You are a friendly pirate'\n- 'Respond only in haikus'\n- 'You are a coding tutor'"
)

# Reset chat when system prompt changes
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = system_prompt
    st.session_state.history = []

if st.session_state.system_prompt != system_prompt:
    st.session_state.system_prompt = system_prompt
    st.session_state.history = []
    st.experimental_rerun()

# --- Display chat history ---
for message in st.session_state.history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat input ---
if prompt := st.chat_input("Type your message here..."):
    # Add user message to history
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Create chat with system prompt
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(system_instruction=system_prompt)
    )
    
    # Replay previous messages
    for msg in st.session_state.history[:-1]:
        if msg["role"] == "user":
            chat.send_message(msg["content"])

    # Get response from Gemini
    with st.chat_message("assistant"):
        response = chat.send_message(prompt)
        reply = response.text
        st.markdown(reply)

    # Add assistant message to history
    st.session_state.history.append({"role": "assistant", "content": reply})

# --- Sidebar Footer ---
st.sidebar.markdown("---")
st.sidebar.markdown("❤️ Made by Vijay")
