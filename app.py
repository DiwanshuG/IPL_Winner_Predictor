import streamlit as st
import pickle
import pandas as pd
import webbrowser

# Load the trained model
try:
    with open('pipe.pkl', 'rb') as model_file:
        pipe = pickle.load(model_file)
except FileNotFoundError:
    st.error("🚨 Error: 'pipe.pkl' not found! Please ensure the model file is in the correct location.")
    st.stop()

# IPL Teams
teams = [
    "Sunrisers Hyderabad", "Mumbai Indians", "Royal Challengers Bangalore", 
    "Kolkata Knight Riders", "Punjab Kings", "Chennai Super Kings", 
    "Rajasthan Royals", "Delhi Capitals"
]

# IPL Host Cities
cities = [
    'Hyderabad', 'Bengaluru', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
    'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
    'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
    'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
    'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
    'Sharjah', 'Mohali'
]

st.markdown("<h1 style='text-align: center; color: #FF5733;'>🏏 IPL Win Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size:18px;'>Predict the winning probability of an IPL team based on match conditions!</p>", unsafe_allow_html=True)

# Team Selection
st.markdown("---")
col1, col2 = st.columns([1, 1])
with col1:
    batting_team = st.selectbox("🏏 **Select the Batting Team**", sorted(teams))
with col2:
    bowling_team = st.selectbox("🎯 **Select the Bowling Team**", sorted(teams))

if batting_team == bowling_team:
    st.error("🚨 Wrong team selection! The batting and bowling teams cannot be the same.")
    st.stop()

# Select Match Venue
selected_city = st.selectbox("📍 **Select Match Venue**", sorted(cities))

# Input Target Score
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
        st.warning("⚠️ Overs cannot be zero! Please enter a valid number of overs.")
    elif score > target:
        st.warning("⚠️ Score cannot be greater than the target!")
    elif overs * 6 >= 120:
        st.warning("⚠️ Maximum 20 overs (120 balls) allowed!")
    else:
        runs_left = target - score
        balls_left = 120 - int(overs * 6)
        wickets_left = 10 - wickets

        # Avoid division by zero errors
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

        # Get prediction probabilities
        result = pipe.predict_proba(input_df)
        loss_prob = result[0][0]
        win_prob = result[0][1]

        # Display Results at the Top
        st.markdown("---")
        st.subheader("📊 **Winning Probability**")

        col6, col7 = st.columns([1, 1])
        with col6:
            st.metric(label=f"✅ {batting_team} Win Probability", value=f"{round(win_prob * 100, 2)}%")
        with col7:
            st.metric(label=f"❌ {bowling_team} Win Probability", value=f"{round(loss_prob * 100, 2)}%")

        # Progress Bar Representation
        st.progress(win_prob)

# Watch Live Score Button
if st.button("📺 Watch Live Score"):
    search_query = f"Live score {batting_team} vs {bowling_team}"
    search_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
    webbrowser.open(search_url)
    st.success("✅ Redirecting to Live Score...")

# Download IPL 2025 Schedule
with open("sc.pdf", "rb") as file:
    st.download_button(
        label="📄 Download IPL 2025 Schedule",
        data=file,
        file_name="sc.pdf",
        mime="application/pdf"
    )

# Footer
st.markdown("""
    <hr>
    <p style='text-align: center; font-size:16px;'>Created by <b>Diwanshu</b> with ❤️</p>
    <p style='text-align: center;'>
        <a href='https://www.linkedin.com/in/diwanshu-gangwar/' target='_blank' 
        style='text-decoration: none; font-size:16px; color: #0077b5; font-weight: bold; display: inline-flex; align-items: center;'>
            <img src='https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png' 
            width='20px' style='vertical-align: middle; margin-right: 5px;' />
            Connect with me
        </a>
    </p>
""", unsafe_allow_html=True)
