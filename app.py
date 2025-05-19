import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv("azure_keys.env")

openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_version = "2023-05-15"
openai.api_key = os.getenv("AZURE_OPENAI_KEY")

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
    total_deficit_needed = weight_to_lose * 7700
    daily_deficit = total_deficit_needed / (months * 30)
    return int(daily_deficit)

def gpt_reply(message, context="You are a fitness coach helping a user lose weight. Be supportive and practical."):
    try:
        response = openai.ChatCompletion.create(
            engine=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
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

st.set_page_config(page_title="FitLite Chatbot", layout="centered")
st.title("🏋️ FitLite: AI Weight Loss Chatbot")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    st.session_state.user_data = {
        "age": None, "gender": None, "height": None, "weight": None,
        "target_weight": None, "activity": None, "months": None, "goal_set": False
    }

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Say something to FitLite..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    user_data = st.session_state.user_data
    if not user_data["goal_set"]:
        if user_data["age"] is None and prompt.isdigit():
            user_data["age"] = int(prompt)
            reply = "Great. Now tell me your gender (Male/Female)."
        elif user_data["gender"] is None and prompt.lower() in ["male", "female"]:
            user_data["gender"] = prompt.capitalize()
            reply = "Cool. What's your height in cm?"
        elif user_data["height"] is None:
            try:
                user_data["height"] = int(prompt)
                reply = "Got it. What's your current weight in kg?"
            except:
                reply = "Please enter height in cm (numbers only)."
        elif user_data["weight"] is None:
            try:
                user_data["weight"] = float(prompt)
                reply = "What's your target weight in kg?"
            except:
                reply = "Please enter a valid weight."
        elif user_data["target_weight"] is None:
            try:
                user_data["target_weight"] = float(prompt)
                reply = "In how many months do you want to achieve this?"
            except:
                reply = "Please enter a valid target weight."
        elif user_data["months"] is None:
            try:
                user_data["months"] = int(prompt)
                reply = "And finally, what's your activity level? (Sedentary / Lightly Active / Moderately Active / Very Active)"
            except:
                reply = "Enter number of months as a whole number."
        elif user_data["activity"] is None and prompt.lower() in ["sedentary", "lightly active", "moderately active", "very active"]:
            user_data["activity"] = prompt.title()
            user_data["goal_set"] = True
            bmr = calculate_bmr(user_data["gender"], user_data["weight"], user_data["height"], user_data["age"])
            tdee = calculate_tdee(bmr, user_data["activity"])
            deficit = get_deficit_recommendation(tdee, user_data["target_weight"], user_data["weight"], user_data["months"])
            target_cal = int(tdee - deficit)
            reply = f"✅ Thanks! Based on your info, you need about **{int(tdee)} kcal/day** to maintain weight.\nTo reach your goal in {user_data['months']} months, aim for **{target_cal} kcal/day** (deficit: {deficit} kcal).\nWhat did you eat today? I can help suggest improvements."
        else:
            reply = "Let’s begin! How old are you?"
    else:
        reply = gpt_reply(prompt)

    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)

st.caption("🤖 Powered by Azure OpenAI + Streamlit | FitLite Chat")
