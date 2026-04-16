# main.py
import streamlit as st
import threading
from chatbot_core import get_response
from bot import run_bot

# =========================
# 🚀 Start Discord Bot ONCE
# =========================

def start_bot_once():
    if "bot_started" not in st.session_state:
        st.session_state.bot_started = True
        thread = threading.Thread(target=run_bot, daemon=True)
        thread.start()

start_bot_once()

# =========================
# 🎨 Page Config
# =========================
st.set_page_config(
    page_title="EGT.AI",
    page_icon="🤖",
    layout="centered"
)

# =========================
# 🏷 Names
# =========================
USER_NAME = "You"
BOT_NAME = "The Big EGT"

# =========================
# 💬 Chat Title
# =========================
st.title("The Big EGT")

# =========================
# 💾 Chat Memory
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# 🧾 Display Chat (with names)
# =========================
for role, content in st.session_state.messages:
    
    if role == "user":
        name = USER_NAME
    else:
        name = BOT_NAME

    with st.chat_message(role):
        st.markdown(f"**{name}**")
        st.markdown(content)

# =========================
# ⌨️ Chat Input
# =========================
user_input = st.chat_input("Talk to the big EGT")

if user_input:
    # Store user message
    st.session_state.messages.append(("user", user_input))

    with st.chat_message("user"):
        st.markdown(f"**{USER_NAME}**")
        st.markdown(user_input)

    # Generate response
    response = get_response(user_input, user_id="streamlit_user")

    # Typing effect
    with st.chat_message("assistant"):
        st.markdown(f"**{BOT_NAME}**")
        placeholder = st.empty()
        full_text = ""
        
        for char in response:
            full_text += char
            placeholder.markdown(full_text)

    # Store bot response
    st.session_state.messages.append(("assistant", response))
