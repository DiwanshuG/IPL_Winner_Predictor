# IPL Win Predictor

A machine learning–based web application that predicts the winning probability of IPL teams based on real-time match conditions such as score, overs, wickets, venue, and teams.

The project demonstrates an end-to-end ML workflow including data preprocessing, feature encoding, model training, evaluation, and deployment using Streamlit.

---

##  Live Demo
👉 https://ipl-win-predictor-2025.streamlit.app/

---

##  Problem Statement
Predict the probability of a batting team winning an IPL match given the current match situation.  
This helps analyze how match factors like score, wickets, and overs influence match outcomes.

---

##  Dataset
- Historical IPL match data [2008-2024]
- Includes team names, venue, target score, current score, overs, and wickets
- Categorical and numerical features required preprocessing

---

##  Approach
- Cleaned and prepared match-level data using Pandas
- Encoded categorical features (teams, venue) using One-Hot Encoding
- Built an ML pipeline using Scikit-learn to combine preprocessing and modeling
- Trained a Logistic Regression model to estimate win probability
- Evaluated model performance using train-test split
- Saved the trained model using Pickle for deployment

---

##  Features
- Real-time win probability prediction
- Inputs:
  - Batting & bowling teams
  - Match venue
  - Target score, current score, overs, wickets
- Handles match-end edge cases (all out, overs completed, etc.)
- Interactive UI with metrics and progress visualization
- Deployed using Streamlit

---

##  Tech Stack
- Python  
- Pandas, NumPy  
- Scikit-learn  
- Streamlit  
- Pickle  
- Matplotlib, Seaborn  

---

## Learnings
- End-to-end machine learning workflow on real-world tabular data
- Handling categorical variables using pipelines
- Importance of proper preprocessing in ML models
- Deploying ML models as interactive web applications

---

## Run Locally
```bash
git clone https://github.com/your-username/IPL-Win-Predictor.git
cd IPL-Win-Predictor
pip install -r requirements.txt
streamlit run app.py
```

## Author 
### Diwanshu Gangwar [ LinkedIn: https://www.linkedin.com/in/diwanshu-gangwar/]
