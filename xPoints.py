import streamlit as st
import numpy as np
from scipy.stats import poisson

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="xPoints Calculator",
    layout="centered"
)

# ----------------------------
# PASSWORD PROTECTION
# ----------------------------
# IMPORTANT:
# Use Streamlit Secrets for security (recommended)
# In Streamlit Cloud → App Settings → Secrets:
# APP_PASSWORD = "yourStrongPassword"

PASSWORD = st.secrets["APP_PASSWORD"]

def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.title("🔒 Private Access")
        password_input = st.text_input("Enter password", type="password")

        if password_input == PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        elif password_input:
            st.error("Incorrect password")

        st.stop()

check_password()

# ----------------------------
# APP CONTENT
# ----------------------------
st.title("⚽ xPoints Calculator (Poisson Model)")

st.markdown("Enter expected goals (xG) for each team.")

team_a_xg = st.number_input(
    "Team A xG",
    min_value=0.0,
    step=0.01,
    value=0.47
)

team_b_xg = st.number_input(
    "Team B xG",
    min_value=0.0,
    step=0.01,
    value=1.82
)

if st.button("Calculate xPoints"):

    # Goal probability distributions
    team_a_goal_probs = [poisson.pmf(i, team_a_xg) for i in range(6)]
    team_b_goal_probs = [poisson.pmf(i, team_b_xg) for i in range(6)]

    # Match outcome matrix
    match_probs = np.outer(team_a_goal_probs, team_b_goal_probs)

    # Outcome probabilities
    p_win_a = np.sum(np.tril(match_probs, -1))
    p_draw = np.sum(np.diag(match_probs))
    p_win_b = np.sum(np.triu(match_probs, 1))

    # xPoints
    xPoints_a = p_win_a * 3 + p_draw
    xPoints_b = p_win_b * 3 + p_draw

    # Output
    st.subheader("📊 Results")
    st.write(f"**Team A Win %:** {p_win_a * 100:.2f}%")
    st.write(f"**Draw %:** {p_draw * 100:.2f}%")
    st.write(f"**Team B Win %:** {p_win_b * 100:.2f}%")

    st.success(f"Team A xPoints: {xPoints_a:.3f}")
    st.success(f"Team B xPoints: {xPoints_b:.3f}")
