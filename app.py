import streamlit as st
import pandas as pd
import nfl_data_py as nfl

# Set page configuration for mobile-first layout
st.set_page_config(page_title="NFL Bets Dashboard", layout="centered")

# --- DATA FETCHING & AUTOMATIC WEEKLY REFRESH ---
@st.cache_data(ttl=86400)
def load_nfl_data():
    weekly_player_stats = nfl.import_weekly_data([2026])
    team_desc = nfl.import_team_desc()
    return weekly_player_stats, team_desc

try:
    weekly_stats, teams = load_nfl_data()
except Exception as e:
    st.error("Error fetching live data. Using placeholder mock data for display.")
    weekly_stats = pd.DataFrame(columns=['player_name', 'recent_team', 'passing_yards', 'rushing_yards', 'receiving_yards'])

# --- MOCK USER BETS (Modify these with your actual wagers) ---
PLAYER_BETS = [
    {"name": "B. Nix", "stat": "passing_yards", "line": 3800, "type": "Over"},
    {"name": "D. Henry", "stat": "rushing_yards", "line": 1100, "type": "Over"}
]

DIVISION_BETS = {
    "AFC North": "Ravens",
    "NFC West": "49ers"
}

# --- DASHBOARD UI ---
st.title("🏈 Season-Long Bet Tracker")
st.write("Data automatically refreshes daily.")

# --- SECTION 1: PLAYER STATISTICAL TOTALS ---
st.header("👤 Player Prop Tracker")
for bet in PLAYER_BETS:
    player_data = weekly_stats[weekly_stats['player_name'] == bet['name']]
    current_total = player_data[bet['stat']].sum() if not player_data.empty else 0
    
    pct_complete = min(float(current_total / bet['line']), 1.0) if bet['line'] > 0 else 0.0
    remaining = max(bet['line'] - current_total, 0)
    
    with st.container(border=True):
        st.subheader(f"{bet['name']} — {bet['stat'].replace('_', ' ').title()}")
        st.metric(label="Current Total", value=f"{current_total:,}", delta=f"-{remaining:,} to line")
        st.progress(pct_complete, text=f"{pct_complete*100:.1f}% of {bet['line']:,} Target")

st.divider()

# --- SECTION 2: DIVISIONAL TRACKER ---
st.header("🏆 Divisional Standings")
for division, my_team in DIVISION_BETS.items():
    with st.expander(f"📅 {division} (Your Bet: {my_team})", expanded=True):
        standings_data = {
            "Team": [my_team, "Team B", "Team C", "Team D"],
            "W-L": ["0-0", "0-0", "0-0", "0-0"],
            "Div Record": ["0-0", "0-0", "0-0", "0-0"],
            "Proj. Finish": ["1st", "2nd", "3rd", "4th"]
        }
        df_standings = pd.DataFrame(standings_data)
        
        def highlight_my_team(row):
            return ['background-color: rgba(0, 128, 0, 0.2)' if row.Team == my_team else '' for _ in row]
            
        st.dataframe(
            df_standings.style.apply(highlight_my_team, axis=1),
            hide_index=True,
            use_container_width=True
        )