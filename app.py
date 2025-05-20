import streamlit as st
from openai import AzureOpenAI

# Streamlit page setup
st.set_page_config(page_title="FitLite Chatbot", layout="centered")
st.title("🏋️ FitLite: Interactive GPT Fitness Coach")

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_key=st.secrets["AZURE_OPENAI_KEY"],
    api_version="2023-05-15",
    azure_endpoint=st.secrets["AZURE_OPENAI_ENDPOINT"]
)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "system",
            "content": (
                "You are FitLite, an empathetic and intelligent AI fitness coach. "
                "Greet the user and ask them questions naturally to help build a personalized weight loss plan. "
                "Collect information like age, gender, height, weight, goal weight, timeframe, and activity level step-by-step, just like a conversation. "
                "Respond casually and warmly, and encourage them to continue. "
                "Never ask more than one question at a time."
            )
        }
    ]

# Display previous messages (skip system prompt)
for msg in st.session_state.chat_history[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input + GPT response
if prompt := st.chat_input("Say something to FitLite..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        response = client.chat.completions.create(
            model=st.secrets["AZURE_OPENAI_DEPLOYMENT"],
            messages=st.session_state.chat_history,
            temperature=0.7,
            max_tokens=300
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        reply = f"[GPT Error]: {str(e)}"

    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)

st.caption("🤖 Powered by Azure OpenAI | FitLite Chatbot")
