import streamlit as st
import pickle
import pandas as pd
import webbrowser

# Load Model
try:
    with open('pipe.pkl', 'rb') as model_file:
        pipe = pickle.load(model_file)
except FileNotFoundError:
    st.error("🚨 Error: 'pipe.pkl' not found! Please upload the model file.")
    uploaded_file = st.file_uploader("Upload 'pipe.pkl'", type=["pkl"])
    if uploaded_file is not None:
        pipe = pickle.load(uploaded_file)
    else:
        st.stop()

# Teams and Cities Data
teams = [
    "Sunrisers Hyderabad", "Mumbai Indians", "Royal Challengers Bangalore", 
    "Kolkata Knight Riders", "Punjab Kings", "Chennai Super Kings", 
    "Rajasthan Royals", "Delhi Capitals"
]

cities = [
    'Hyderabad', 'Bengaluru', 'Mumbai', 'Kolkata', 'Delhi',
    'Jaipur', 'Chennai', 'Ahmedabad', 'Dharamsala', 'Visakhapatnam',
    'Guwahati', 'Lucknow', 'Mullanpur', 'Chandigarh', 'Pune', 'Raipur', 'Ranchi', 'Indore', 'Cuttack', 'Nagpur', 'Mohali'
]

# UI Design
st.set_page_config(page_title="IPL Win Predictor", layout="wide")
st.markdown("<h1 style='text-align: center; color: #FF5733;'>🏏 IPL Win Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size:18px;'>Predict the winning probability of an IPL team based on match conditions!</p>", unsafe_allow_html=True)
st.markdown("---")

# Team Selection
col1, col2 = st.columns(2)
with col1:
    batting_team = st.selectbox("🏏 **Select the Batting Team**", sorted(teams))
with col2:
    bowling_team = st.selectbox("🎯 **Select the Bowling Team**", sorted(teams))

if batting_team == bowling_team:
    st.error("🚨 Wrong team selection! The batting and bowling teams cannot be the same.")
    st.stop()

# Venue and Target Score
selected_city = st.selectbox("📍 **Select Match Venue**", sorted(cities))
target = st.number_input("🎯 **Enter the Target Score**", min_value=1, step=1)
st.markdown("---")

# Match Progress Input
st.subheader("📊 Match Progress")
col3, col4, col5 = st.columns(3)
with col3:
    score = st.number_input("🏏 **Current Score**", min_value=0, step=1)
with col4:
    overs = st.number_input("⏳ **Overs Completed**", min_value=0.0, max_value=20.0, step=0.1, format="%.1f")
with col5:
    wickets = st.number_input("❌ **Wickets Fallen**", min_value=0, max_value=10, step=1)

# Adjust overs function
def adjust_overs(overs):
    full_overs = int(overs)
    balls = round((overs - full_overs) * 10)
    balls = min(balls, 5)  # Ensure max of 5 balls
    return full_overs + balls / 10.0

overse = adjust_overs(overs)
balls_left = max(120 - (int(overs) * 6 + round((overs - int(overs)) * 10)), 0)

# Prediction Button
if st.button("🔮 **Predict Probability**"):
    if overs == 0:
        st.warning("⚠️ Overs cannot be zero! Please enter a valid number of overs.")
    elif target == score and wickets == 10:
         st.warning("⚠️ Score achieved and 10 wicket falls ! what ?")
    elif wickets == 10:
        st.success(f"✅ {bowling_team} has won the match! All wickets have fallen.")
    elif score >= target:
        st.success(f"✅ {batting_team} has won the match! Target achieved.")
    elif score == target - 1 and balls_left == 0:
        st.success("🏏 It is a draw! Enjoy the Super Over!")
    elif balls_left == 0:
        st.success(f"✅ {bowling_team} has won the match! No balls left.")
    else:
        runs_left = target - score
        wickets_left = 10 - wickets
        crr = score / overs if overs > 0 else 0
        rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0
        input_df = pd.DataFrame({
            'batting_team': [batting_team],
            'bowling_team': [bowling_team],
            'city': [selected_city],
            'runs_left': [runs_left],
            'balls_left': [balls_left],
            'wickets': [wickets_left],
            'total_runs_x': [target],
            'crr': [crr],
            'rrr': [rrr]
        })
        result = pipe.predict_proba(input_df)
        win_prob, loss_prob = result[0][1], result[0][0]
        st.markdown("---")
        st.subheader("📊 **Winning Probability**")
        col6, col7 = st.columns(2)
        with col6:
            st.metric(label=f"✅ {batting_team} Win Probability", value=f"{round(win_prob * 100, 2)}%")
        with col7:
            st.metric(label=f"❌ {bowling_team} Win Probability", value=f"{round(loss_prob * 100, 2)}%")
        st.progress(win_prob)

# Live Score Search
if st.button("📺 Watch Live Score"):
    search_url = f"https://www.google.com/search?q=Live+score+{batting_team}+vs+{bowling_team}"
    webbrowser.open(search_url)

# Download IPL Schedule
with open("sc.pdf", "rb") as file:
    st.download_button(label="📄 Download IPL 2025 Schedule", data=file, file_name="IPL_2025_Schedule.pdf", mime="application/pdf")

# Footer
st.markdown("""
    <hr>
    <p style='text-align: center; font-size:16px;'>Created by <b>Diwanshu</b> with ❤️</p>
    <p style='text-align: center;'>
        <a href='https://www.linkedin.com/in/diwanshu-gangwar/' target='_blank' 
        style='text-decoration: none; font-size:16px; color: #0077b5; font-weight: bold;'>
            Connect with me on LinkedIn
        </a>
    </p>
""", unsafe_allow_html=True)
