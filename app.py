import streamlit as st
import openai
import os

# Azure OpenAI setup using Streamlit secrets
openai.api_type = "azure"
openai.api_base = st.secrets["AZURE_OPENAI_ENDPOINT"]
openai.api_version = "2023-05-15"
openai.api_key = st.secrets["AZURE_OPENAI_KEY"]

# --- Helper functions ---
def calculate_bmr(gender, weight, height, age):
    if gender == "Male":
        return 10 * weight + 6.25 * height - 5 * age + 5
    else:
        return 10 * weight + 6.25 * height - 5 * age - 161

def calculate_tdee(bmr, activity_level):
    multipliers = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725
    }
    return bmr * multipliers[activity_level]

def get_deficit_recommendation(tdee, target_weight, current_weight, months):
    weight_to_lose = current_weight - target_weight
    total_deficit_needed = weight_to_lose * 7700  # kcal per kg of fat
    daily_deficit = total_deficit_needed / (months * 30)
    return int(daily_deficit)

def gpt_reply(message, context="You are a friendly fitness coach helping users lose weight. Be supportive and practical."):
    try:
        response = openai.ChatCompletion.create(
            engine=st.secrets["AZURE_OPENAI_DEPLOYMENT"],
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": message}
            ],
            temperature=0.7,
            max_tokens=200
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[GPT Error]: {str(e)}"

# --- Streamlit Chat Setup ---
st.set_page_config(page_title="FitLite Chatbot", layout="centered")
st.title("🏋️ FitLite: AI Weight Loss Chatbot")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    st.session_state.user_data = {
        "age": None, "gender": None, "height": None, "weight": None,
        "target_weight": None, "activity": None, "months": None, "goal_set": False
    }

# Show current chat history
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input bar
if prompt := st.chat_input("Say something to FitLite..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Goal-setting conversation flow
    user_data = st.session_state.user_data

    if not user_data["goal_set"]:
        try:
            if user_data["age"] is None:
                user_data["age"] = int(prompt)
                reply = "Great. Now tell me your gender (Male/Female)."
            elif user_data["gender"] is None and prompt.lower() in ["male", "female"]:
                user_data["gender"] = prompt.capitalize()
                reply = "Cool. What's your height in cm?"
            elif user_data["height"] is None:
                user_data["height"] = int(prompt)
                reply = "Got it. What's your current weight in kg?"
            elif user_data["weight"] is None:
                user_data["weight"] = float(prompt)
                reply = "Nice. What's your target weight in kg?"
            elif user_data["target_weight"] is None:
                user_data["target_weight"] = float(prompt)
                reply = "In how many months do you want to reach your goal?"
            elif user_data["months"] is None:
                user_data["months"] = int(prompt)
                reply = "Finally, what's your activity level? (Sedentary / Lightly Active / Moderately Active / Very Active)"
            elif user_data["activity"] is None and prompt.lower() in ["sedentary", "lightly active", "moderately active", "very active"]:
                user_data["activity"] = prompt.title()
                user_data["goal_set"] = True

                # Calculate and give feedback
                bmr = calculate_bmr(user_data["gender"], user_data["weight"], user_data["height"], user_data["age"])
                tdee = calculate_tdee(bmr, user_data["activity"])
                deficit = get_deficit_recommendation(tdee, user_data["target_weight"], user_data["weight"], user_data["months"])
                target_cal = int(tdee - deficit)

                reply = (
                    f"✅ Thanks! Based on your inputs:\n\n"
                    f"- **TDEE** (maintenance calories): {int(tdee)} kcal/day\n"
                    f"- To hit your goal in {user_data['months']} months, aim for: **{target_cal} kcal/day**\n"
                    f"- Daily deficit: {deficit} kcal\n\n"
                    f"Now, tell me what you ate today and I’ll help you adjust!"
                )
            else:
                reply = "Let’s begin! How old are you?"
        except:
            reply = "Oops, please enter a valid number or response for this step."
    else:
        reply = gpt_reply(prompt)

    # Show GPT reply
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)

# App footer
st.caption("🤖 Powered by Azure OpenAI GPT-3.5 Turbo | FitLite Chat")
