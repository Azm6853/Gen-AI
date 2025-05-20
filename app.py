import streamlit as st
import openai

# Azure OpenAI setup using Streamlit secrets
openai.api_type = "azure"
openai.api_base = st.secrets["AZURE_OPENAI_ENDPOINT"]
openai.api_version = "2023-05-15"
openai.api_key = st.secrets["AZURE_OPENAI_KEY"]

# Streamlit page config
st.set_page_config(page_title="FitLite Chatbot", layout="centered")
st.title("🏋️ FitLite: Interactive GPT Fitness Coach")

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
                "After getting the details, help them calculate TDEE, calorie target, and make suggestions. "
                "Never ask more than one question at a time."
            )
        }
    ]

# Display previous chat messages (except system prompt)
for msg in st.session_state.chat_history[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Say something to FitLite..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call GPT with full chat history
    try:
        response = openai.ChatCompletion.create(
            engine=st.secrets["AZURE_OPENAI_DEPLOYMENT"],
            messages=st.session_state.chat_history,
            temperature=0.7,
            max_tokens=300
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        reply = f"[GPT Error]: {str(e)}"

    # Show and store GPT reply
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)

# Footer
st.caption("🤖 Powered by Azure OpenAI GPT-3.5 Turbo | FitLite Chat")
