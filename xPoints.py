import streamlit as st
import numpy as np
from scipy.stats import poisson

# Page config
st.set_page_config(page_title="xPoints Calculator", layout="centered")

st.title("⚽ xPoints Calculator")

# ---------- FUNCTION ----------
def calculate_xpoints(home_metric, away_metric):

    home_goal_probs = [poisson.pmf(i, home_metric) for i in range(6)]
    away_goal_probs = [poisson.pmf(i, away_metric) for i in range(6)]

    match_probs = np.outer(home_goal_probs, away_goal_probs)

    p_home_win = np.sum(np.tril(match_probs, -1))
    p_draw = np.sum(np.diag(match_probs))
    p_away_win = np.sum(np.triu(match_probs, 1))

    xpoints_home = p_home_win * 3 + p_draw
    xpoints_away = p_away_win * 3 + p_draw

    return xpoints_home, xpoints_away


# =========================================================
# SECTION 1 — xG MODEL
# =========================================================

st.header("📊 Home vs Away xG Model")

home_xg = st.number_input("Home xG", min_value=0.0, step=0.01, value=1.50, key="home_xg")
away_xg = st.number_input("Away xG", min_value=0.0, step=0.01, value=1.20, key="away_xg")

if st.button("Calculate xPoints (xG)"):

    home_xp, away_xp = calculate_xpoints(home_xg, away_xg)

    st.success(f"Home xPoints (xG model): {home_xp:.3f}")
    st.success(f"Away xPoints (xG model): {away_xp:.3f}")


# =========================================================
# SECTION 2 — xGOT MODEL
# =========================================================

st.header("🎯 Home vs Away xGOT Model")

home_xgot = st.number_input("Home xGOT", min_value=0.0, step=0.01, value=1.40, key="home_xgot")
away_xgot = st.number_input("Away xGOT", min_value=0.0, step=0.01, value=1.10, key="away_xgot")

if st.button("Calculate xPoints (xGOT)"):

    home_xp_got, away_xp_got = calculate_xpoints(home_xgot, away_xgot)

    st.success(f"Home xPoints (xGOT model): {home_xp_got:.3f}")
    st.success(f"Away xPoints (xGOT model): {away_xp_got:.3f}")
