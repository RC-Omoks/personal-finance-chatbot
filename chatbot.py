# File: requirements.txt
#streamlit
#openai
#python-dotenv

# File: .env.example
# Rename to .env and fill with your OpenAI key
#OPENAI_API_KEY=your_openai_api_key

# File: chatbot.py
import os
import streamlit as st
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configure Streamlit page
st.set_page_config(page_title="Financial Assistant", page_icon="💬", layout="centered")

st.header("💬 Personal Financial Assistant")

# Initialize session state for messages
if 'messages' not in st.session_state:
    st.session_state.messages = []

# System prompt
SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "You are a knowledgeable personal financial assistant. "
        "Provide clear, concise financial advice, explain concepts simply, "
        "and offer actionable tips."
    )
}

# Query OpenAI LLM
def query_financial_llm(conversation):
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=conversation,
        temperature=0.7,
    )
    return response.choices[0].message.content

# Display chat history
for msg in st.session_state.messages:
    role = msg['role']
    content = msg['content']
    st.chat_message(role).write(content)

# Accept user input via Streamlit's chat_input
if user_input := st.chat_input("Type your finance question..."):
    # Display user message immediately
    st.chat_message("user").write(user_input)
    # Append user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Build conversation and query
    conversation = [SYSTEM_PROMPT] + st.session_state.messages
    assistant_reply = query_financial_llm(conversation)

    # Append assistant message and display
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
    st.chat_message("assistant").write(assistant_reply)