import streamlit as st
from query_processor import process_query

# Set Streamlit Page Configuration
st.set_page_config(page_title="SQLite Chat Assistant", page_icon="💬", layout="wide")

# Custom CSS for Styling
st.markdown("""
    <style>
        body { background-color: #F0F2F6; }
        .stChatMessage { border-radius: 10px; padding: 10px; margin-bottom: 10px; }
        .user { background-color: #DCF8C6; text-align: left; color: black; }
        .assistant { background-color: #E3E3E3; text-align: left; color: black; }
        .message-box { padding: 20px; border-radius: 10px; margin-bottom: 10px; }
        .stTextInput>div>div>input { background-color: #f7f7f7 !important; }
    </style>
""", unsafe_allow_html=True)

# Sidebar for Info and Controls
with st.sidebar:
    st.header("📊 Database Info")
    st.write("💡 You can ask queries like:")
    st.code("""
    - List all employees in Sales.
    - Who is the manager of Engineering?
    - List all employees hired after 2022-01-01.
    """, language="plaintext")
    st.write("📌 **Tips:** Use natural language to interact!")

# Title and Description
st.title("💬 SQLite Chat Assistant")
st.markdown("🤖 **Ask me questions related to the Employee Database!**")

# Chat History Storage
if "messages" not in st.session_state:
    st.session_state.messages = []

# Two-column Layout
col1, col2 = st.columns([2, 5])

# Display Chat Messages
with col2:
    for message in st.session_state.messages:
        role_class = "user" if message["role"] == "user" else "assistant"
        with st.chat_message(message["role"]):
            st.markdown(f"<div class='message-box {role_class}'>{message['content']}</div>", unsafe_allow_html=True)

# Chat Input
user_input = st.chat_input("🔍 Type your query...")

if user_input:
    # Add User Message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(f"<div class='message-box user'>{user_input}</div>", unsafe_allow_html=True)

    # Process Query
    response = process_query(user_input)

    # Add Assistant Response
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(f"<div class='message-box assistant'>{response}</div>", unsafe_allow_html=True)
