import numpy as np
from scipy.stats import poisson

# Expected goals for each team
team_a_xg = .47
team_b_xg = 1.82

# Goal probability distributions for each team
team_a_goal_probs = [poisson.pmf(i, team_a_xg) for i in range(6)]
team_b_goal_probs = [poisson.pmf(i, team_b_xg) for i in range(6)]

# Probability matrix for match outcomes6
match_probs = np.outer(team_a_goal_probs, team_b_goal_probs)

# Calculating probabilities for each team
p_win_a = np.sum(np.tril(match_probs, -1))  # Team A wins
p_draw = np.sum(np.diag(match_probs))        # Draw
p_win_b = np.sum(np.triu(match_probs, 1))    # Team B wins

# xPoints for each team
xPoints_a = p_win_a * 3 + p_draw * 1 + p_win_b * 0
xPoints_b = p_win_b * 3 + p_draw * 1 + p_win_a * 0

# Output xPoints for each team
print("Team A xPoints:", round(xPoints_a, 3))
print("Team B xPoints:", round(xPoints_b, 3))
