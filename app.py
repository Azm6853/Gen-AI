import streamlit as st

# ----- Utility Functions -----
def calculate_bmr(gender, weight, height, age):
    if gender == "Male":
        return 10 * weight + 6.25 * height - 5 * age + 5
    else:
        return 10 * weight + 6.25 * height - 5 * age - 161

def get_activity_multiplier(level):
    return {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725,
        "Super Active": 1.9
    }.get(level, 1.2)

def estimate_deficit_days(current_weight, target_weight, daily_deficit):
    if daily_deficit <= 0:
        return float('inf')
    return ((current_weight - target_weight) * 7700) / daily_deficit

# ----- Streamlit UI -----
st.set_page_config(page_title="FitLite - AI Weight Planner", layout="centered")
st.title("🏋️ FitLite – Smart Weight-Cut Planner")
st.markdown("Helping you reach your fitness goals with intelligent tracking and tips.")

# Inputs
col1, col2 = st.columns(2)
with col1:
    age = st.number_input("Age", 10, 100, 25)
    gender = st.selectbox("Gender", ["Male", "Female"])
    height = st.number_input("Height (cm)", 100, 250, 170)
with col2:
    weight = st.number_input("Current Weight (kg)", 30.0, 200.0, 70.0)
    target_weight = st.number_input("Target Weight (kg)", 30.0, 200.0, 65.0)
    activity = st.selectbox("Activity Level", [
        "Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Super Active"
    ])

# Daily Calorie Intake
daily_calories = st.number_input("Estimated Daily Calorie Intake (kcal)", 1000, 5000, 2200)

# Calculate
if st.button("Calculate My Plan"):
    bmr = calculate_bmr(gender, weight, height, age)
    tdee = bmr * get_activity_multiplier(activity)
    deficit = tdee - daily_calories
    days_needed = estimate_deficit_days(weight, target_weight, deficit)

    st.subheader("📊 Results")
    st.markdown(f"**Your BMR:** {int(bmr)} kcal/day")
    st.markdown(f"**Your TDEE (maintenance):** {int(tdee)} kcal/day")
    if deficit > 0:
        st.markdown(f"**Daily Calorie Deficit:** {int(deficit)} kcal/day")
        st.markdown(f"**Estimated Time to Goal:** {int(days_needed)} days (~{int(days_needed/7)} weeks)")
        st.success("Stay consistent and monitor weekly!")
    else:
        st.warning("You're not in a calorie deficit. Increase activity or reduce intake.")

    st.markdown("---")
    st.subheader("🧠 Smart Suggestions")
    if deficit < 300:
        st.info("Try a 20-min walk or reduce 1 chapati to increase deficit.")
    elif deficit > 1000:
        st.warning("Too large a deficit may not be sustainable. Consider eating a bit more.")
    else:
        st.success("You're in a healthy calorie deficit range. Keep going!")
