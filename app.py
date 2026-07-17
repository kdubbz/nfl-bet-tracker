import streamlit as st
import pandas as pd
import nflreadpy as nfl

# Set page configuration for mobile-first layout
st.set_page_config(page_title="NFL Bets Dashboard", layout="centered")

# --- DATA FETCHING ---
@st.cache_data(ttl=86400)
def load_nfl_data(year):
    try:
        raw_stats = nfl.load_player_stats([year])
        return raw_stats.to_pandas()
    except Exception:
        return pd.DataFrame()

# --- TITLE ---
st.title("🏈 Premium NFL Bet Tracker")

# --- SEASON TOGGLE ---
SEASON = st.radio(
    "Select View:",
    options=["2025 Research & Baselines", "2026 Live Track"],
    horizontal=True,
    help="Toggle between historical research/projections and live 2026 tracking."
)

# --- THE 3-LEG PARLAY DEFINITION ---
PARLAY_BETS = [
    {
        "name": "Rome Odunze",
        "db_name": "R.Odunze",
        "stat": "receiving_yards",
        "line": 799.5,
        "team": "CHI",
        "2025_actual": 661.0,
        "narrative": (
            "**Why the Over hits:** Odunze posted a highly efficient 661 yards on just 44 receptions "
            "as a rookie despite playing behind a crowded target hierarchy and adjusting to a rookie QB. "
            "Entering Year 2, wide receivers historically take their most massive leaps. With "
            "established chemistry with Caleb Williams, an expected increase in snap-share, and his exceptional "
            "15.0 yards-per-reception average, he only needs to average **47.1 yards per game** over 17 games to clear this."
        )
    },
    {
        "name": "Josh Allen",
        "db_name": "J.Allen",
        "stat": "passing_yards",
        "line": 3549.5,
        "team": "BUF",
        "2025_actual": 3668.0,
        "narrative": (
            "**Why the Over hits:** Josh Allen threw for 3,668 yards in 2025 during an incredibly transitionary "
            "year for the Bills' pass-catchers, landing him 3rd in MVP voting. His line for 2026 is set "
            "at a remarkably low 3,549.5 yards. Since 2020, Allen has consistently cleared this mark, "
            "averaging over 4,100 passing yards per season. The Bills’ offense is highly vertical, and even with "
            "heavy run integration, Allen’s volume floor makes **208.8 passing yards per game** a highly achievable bar."
        )
    },
    {
        "name": "Kyren Williams",
        "db_name": "K.Williams",
        "stat": "rushing_yards",
        "line": 999.5,
        "team": "LAR",
        "2025_actual": 1252.0,
        "narrative": (
            "**Why the Over hits:** Kyren remains the focal engine of Sean McVay's highly rated run blocking scheme, "
            "which posted the highest rushing success rate in the league last season. He racked up 1,252 yards in 2025 "
            "averaging a robust 4.8 yards per carry. While Blake Corum will eat some spell snaps, the Rams run-heavy "
            "red zone and neutral script gameplans guarantee Kyren high-value volume. Needing only **58.8 yards per game** "
            "to cross the 1,000-yard mark makes this a prime leg."
        )
    }
]

# --- VIEW 1: 2025 RESEARCH & BASELINES ---
if SEASON == "2025 Research & Baselines":
    st.header("🔬 2025 Baseline & 2026 Narrative Research")
    st.markdown("### **Active Parlay: The Triple-Threat Over**")
    
    # Load historical 2025 data to verify against the API
    stats_2025 = load_nfl_data(2025)
    
    for bet in PARLAY_BETS:
        with st.container(border=True):
            st.subheader(f"⚡ {bet['name']} ({bet['team']})")
            
            # Show the targeted line vs what they did in 2025
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label="2026 Line Target", value=f"{bet['line']:,}")
            with col2:
                # Use live API if pulled, otherwise fall back on validated stats
                api_stat = 0
                if not stats_2025.empty:
                    player_data = stats_2025[stats_2025['player_name'] == bet['db_name']]
                    api_stat = player_data[bet['stat']].sum() if not player_data.empty else 0
                
                display_val = api_stat if api_stat > 0 else bet['2025_actual']
                st.metric(label="2025 Actual Stats", value=f"{display_val:,.0f}")
            with col3:
                diff = bet['line'] - display_val
                st.metric(
                    label="Pace Delta", 
                    value=f"{'+' if diff > 0 else ''}{diff:,.1f}",
                    delta="Yards Needed vs '25" if diff > 0 else "Cleared in '25!"
                )
            
            st.markdown(bet['narrative'])

# --- VIEW 2: 2026 LIVE TRACK ---
else:
    st.header("📊 Active 2026 Tracker")
    st.write("Tracking live stats. Values will update automatically once regular season games begin.")
    
    stats_2026 = load_nfl_data(2026)
    live_active = not stats_2026.empty
    
    for bet in PARLAY_BETS:
        current_total = 0
        if live_active:
            player_data = stats_2026[stats_2026['player_name'] == bet['db_name']]
            current_total = player_data[bet['stat']].sum() if not player_data.empty else 0
            
        pct_complete = min(float(current_total / bet['line']), 1.0) if bet['line'] > 0 else 0.0
        remaining = max(bet['line'] - current_total, 0)
        
        with st.container(border=True):
            st.subheader(f"{bet['name']} — {bet['stat'].replace('_', ' ').title()}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Current 2026 Total", value=f"{current_total:,.1f}")
            with col2:
                if remaining > 0:
                    st.metric(label="Remaining Needed", value=f"{remaining:,.1f}", delta=f"-{remaining:,.1f}")
                else:
                    st.metric(label="Status", value="🎉 OVER HIT!")
                    
            st.progress(pct_complete, text=f"{pct_complete*100:.1f}% of {bet['line']:,} Target")