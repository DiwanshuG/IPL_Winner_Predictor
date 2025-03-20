import streamlit as st
import pickle
import pandas as pd
import webbrowser

# Load the trained model
try:
    with open('pipe.pkl', 'rb') as model_file:
        pipe = pickle.load(model_file)
except FileNotFoundError:
    st.error("🚨 Error: 'pipe.pkl' not found! Ensure the model file is in the correct location.")
    st.stop()

# IPL Teams & Cities
teams = [
    "Sunrisers Hyderabad", "Mumbai Indians", "Royal Challengers Bangalore", 
    "Kolkata Knight Riders", "Punjab Kings", "Chennai Super Kings", 
    "Rajasthan Royals", "Delhi Capitals"
]

cities = [
    'Hyderabad', 'Bengaluru', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
    'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
    'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
    'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
    'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
    'Sharjah', 'Mohali'
]

# UI Header
st.markdown("""
    <h1 style='text-align: center; color: #FF5733;'>🏏 IPL Win Predictor</h1>
    <p style='text-align: center; font-size:18px;'>Predict the winning probability of an IPL team based on match conditions!</p>
""", unsafe_allow_html=True)

# Team Selection
st.markdown("---")
col1, col2 = st.columns([1, 1])
with col1:
    batting_team = st.selectbox("🏏 **Select the Batting Team**", sorted(teams))
with col2:
    bowling_team = st.selectbox("🎯 **Select the Bowling Team**", sorted(teams))

if batting_team == bowling_team:
    st.error("🚨 Batting and Bowling teams cannot be the same!")
    st.stop()

# Venue Selection
selected_city = st.selectbox("📍 **Select Match Venue**", sorted(cities))

# Target Input
target = st.number_input("🎯 **Enter the Target Score**", min_value=1, step=1)

# Match Progress Inputs
st.markdown("---")
st.subheader("📊 Match Progress")
col3, col4, col5 = st.columns([1, 1, 1])
with col3:
    score = st.number_input("🏏 **Current Score**", min_value=0, step=1)
with col4:
    overs = st.number_input("⏳ **Overs Completed**", min_value=0.0, max_value=20.0, step=0.1)
with col5:
    wickets = st.number_input("❌ **Wickets Fallen**", min_value=0, max_value=10, step=1)

# Prediction Button
if st.button("🔮 **Predict Probability**"):
    if overs == 0:
        st.warning("⚠️ Overs cannot be zero!")
    elif score > target:
        st.warning("⚠️ Score cannot exceed target!")
    elif overs * 6 >= 120:
        st.warning("⚠️ Max 20 overs (120 balls) allowed!")
    else:
        runs_left = target - score
        balls_left = 120 - int(overs * 6)
        wickets_left = 10 - wickets
        
        crr = score / overs if overs > 0 else 0
        rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0
        
        # **Hardcoded Winning Conditions**
        if wickets == 10:
            win_prob = 0.0
            result_message = f"❌ {batting_team} Lost! (All Out)"
        elif score >= target:
            win_prob = 1.0
            result_message = f"🎉 {batting_team} Won! (Target Achieved)"
        else:
            # Model Prediction
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
            win_prob = result[0][1]  # Batting Team Win Probability
            result_message = f"Predicted using AI Model"
        
        # Display Results
        st.markdown("---")
        st.subheader("📊 **Winning Probability**")
        col6, col7 = st.columns([1, 1])
        with col6:
            st.metric(label=f"✅ {batting_team} Win Probability", value=f"{round(win_prob * 100, 2)}%")
        with col7:
            st.metric(label=f"❌ {bowling_team} Win Probability", value=f"{round((1 - win_prob) * 100, 2)}%")
        
        # Progress Bar
        st.progress(win_prob)
        st.markdown(f"**📢 {result_message}**")

# Watch Live Score Button
if st.button("📺 Watch Live Score"):
    search_url = f"https://www.google.com/search?q=Live+score+{batting_team}+vs+{bowling_team}".replace(" ", "+")
    st.markdown(f"[📺 Click here to Watch Live Score]({search_url})", unsafe_allow_html=True)

# Download IPL Schedule
with open("sc.pdf", "rb") as file:
    st.download_button(
        label="📄 Download IPL 2025 Schedule",
        data=file,
        file_name="IPL_2025_Schedule.pdf",
        mime="application/pdf"
    )

# Footer
st.markdown("""
    <hr>
    <p style='text-align: center; font-size:16px;'>Created by <b>Diwanshu</b> with ❤️</p>
    <p style='text-align: center;'>
        <a href='https://www.linkedin.com/in/diwanshu-gangwar/' target='_blank' 
        style='text-decoration: none; font-size:16px; color: #0077b5; font-weight: bold;'>
            🔗 Connect with me on LinkedIn
        </a>
    </p>
""", unsafe_allow_html=True)
