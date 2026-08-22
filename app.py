import streamlit as st
import pandas as pd
import nflreadpy as nfl

# Set page configuration for mobile-first layout
st.set_page_config(page_title="NFL Bet Portfolio", layout="centered")

# --- CUSTOM CSS FOR MODERN CARDS ---
st.html("""
<style>
.st-key-parlay-card {
    border: 2px solid #31333F !important;
    border-radius: 12px !important;
    padding: 20px !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
}
.metric-box {
    background-color: #1E222A;
    border-left: 4px solid #FFD700;
    padding: 12px 16px;
    border-radius: 8px;
    margin-top: 10px;
    margin-bottom: 15px;
}
</style>
""")

# --- DATA FETCHING ---
@st.cache_data(ttl=86400)
def load_nfl_data(year):
    try:
        raw_stats = nfl.load_player_stats([year])
        return raw_stats.to_pandas()
    except Exception:
        return pd.DataFrame()

# --- TITLE ---
st.title("🏈 NFL Bet Portfolio")

# --- SEASON TOGGLE ---
VIEW_MODE = st.radio(
    "Select View Mode:",
    options=["🔬 2025 Research & Baselines", "📊 Live 2026 Tracking Tracker"],
    horizontal=True,
    help="Toggle between historical research/projections and live 2026 tracking."
)

def get_stat_label(stat_key):
    mapping = {
        "passing_yards": "Passing Yards",
        "rushing_yards": "Rushing Yards",
        "receiving_yards": "Receiving Yards",
        "passing_touchdowns": "Passing TDs",
        "rushing_touchdowns": "Rushing TDs",
        "receiving_touchdowns": "Receiving TDs"
    }
    return mapping.get(stat_key, "Units")

# --- PORTFOLIO DEFINITIONS ---
PARLAYS = [
    {
        "id": 0,
        "title": "Total Yards Over",
        "wager": "BONUS BET",
        "payout": "$148.94",
        "legs": [
            {
                "name": "Rome Odunze",
                "team": "Chicago Bears",
                "db_name": "R.Odunze",
                "stat": "receiving_yards",
                "line": 799.5,
                "type": "player",
                "2025_actual": 661.0,
                "narrative": "Requires clearing **799.5 receiving yards** (averaging 47.1 yards/game over a 17-game season)."
            },
            {
                "name": "Josh Allen",
                "team": "Buffalo Bills",
                "db_name": "J.Allen",
                "stat": "passing_yards",
                "line": 3549.5,
                "type": "player",
                "2025_actual": 3668.0,
                "narrative": "Requires clearing **3,549.5 passing yards** (averaging 208.8 yards/game)."
            },
            {
                "name": "Kyren Williams",
                "team": "Los Angeles Rams",
                "db_name": "K.Williams",
                "stat": "rushing_yards",
                "line": 999.5,
                "type": "player",
                "2025_actual": 1252.0,
                "narrative": "Requires clearing **999.5 rushing yards** (averaging 58.8 yards/game)."
            }
        ]
    },
    {
        "id": 1,
        "title": "Maye there be Love",
        "wager": "BONUS BET",
        "payout": "$39.53",
        "legs": [
            {"name": "Jordan Love", "db_name": "J.Love", "stat": "passing_yards", "line": 3500.0, "type": "player", "2025_actual": 3381.0, "narrative": "Requires clearing **3,500.0 passing yards**."},
            {"name": "Drake Maye", "db_name": "D.Maye", "stat": "rushing_touchdowns", "line": 5.0, "type": "player", "2025_actual": 4.0, "narrative": "Requires reaching **5 rushing touchdowns**."}
        ]
    },
    {
        "id": 2,
        "title": "TD Machines",
        "wager": "BONUS BET",
        "payout": "$141.23",
        "legs": [
            {"name": "Aaron Rodgers", "db_name": "A.Rodgers", "stat": "passing_touchdowns", "line": 21.5, "type": "player", "2025_actual": 24.0, "narrative": "Requires clearing **21.5 passing touchdowns**."},
            {"name": "George Pickens", "db_name": "G.Pickens", "stat": "receiving_touchdowns", "line": 6.5, "type": "player", "2025_actual": 9.0, "narrative": "Requires clearing **6.5 receiving touchdowns**."},
            {"name": "Jonathan Taylor", "db_name": "J.Taylor", "stat": "rushing_touchdowns", "line": 11.5, "type": "player", "2025_actual": 18.0, "narrative": "Requires clearing **11.5 rushing touchdowns**."}
        ]
    },
    {
        "id": 3,
        "title": "Division Winners",
        "wager": "$10.00",
        "payout": "$40.19",
        "legs": [
            {"name": "Baltimore Ravens", "type": "division", "target": "1st place in AFC North", "2025_result": "8-9", "place": "2nd", "playoffs": "Missed", "narrative": "Requires 1st place finish in AFC North."},
            {"name": "Philadelphia Eagles", "type": "division", "target": "1st place in NFC East", "2025_result": "11-6", "place": "1st", "playoffs": "Made", "narrative": "Requires 1st place finish in NFC East."}
        ]
    },
    {
        "id": 4,
        "title": "Division Winners",
        "wager": "$5.00",
        "payout": "$54.33",
        "legs": [
            {"name": "Green Bay Packers", "type": "division", "target": "1st place in NFC North", "2025_result": "9-7-1", "place": "2nd", "playoffs": "Made", "narrative": "Requires 1st place finish in NFC North."},
            {"name": "Jacksonville Jaguars", "type": "division", "target": "1st place in AFC South", "2025_result": "13-4", "place": "1st", "playoffs": "Made", "narrative": "Requires 1st place finish in AFC South."}
        ]
    },
    {
        "id": 5,
        "title": "Playoffs or Bust",
        "wager": "BONUS BET",
        "payout": "$166.35",
        "legs": [
            {"name": "Green Bay Packers", "type": "playoff", "target": "Make Playoffs", "2025_result": "9-7-1", "place": "2nd", "playoffs": "Made", "narrative": "Requires Playoff Berth."},
            {"name": "Buffalo Bills", "type": "playoff", "target": "Make Playoffs", "2025_result": "12-5", "place": "2nd", "playoffs": "Made", "narrative": "Requires Playoff Berth."},
            {"name": "Kansas City Chiefs", "type": "playoff", "target": "Make Playoffs", "2025_result": "6-11", "place": "3rd", "playoffs": "Missed", "narrative": "Requires Playoff Berth."},
            {"name": "Baltimore Ravens", "type": "playoff", "target": "Make Playoffs", "2025_result": "8-9", "place": "2nd", "playoffs": "Missed", "narrative": "Requires Playoff Berth."},
            {"name": "Los Angeles Rams", "type": "playoff", "target": "Make Playoffs", "2025_result": "12-5", "place": "2nd", "playoffs": "Made", "narrative": "Requires Playoff Berth."},
            {"name": "Philadelphia Eagles", "type": "playoff", "target": "Make Playoffs", "2025_result": "11-6", "place": "1st", "playoffs": "Made", "narrative": "Requires Playoff Berth."}
        ]
    }
]

# --- SLIDE STATE ---
if "parlay_index" not in st.session_state:
    st.session_state.parlay_index = 0

def prev_slide():
    if st.session_state.parlay_index > 0:
        st.session_state.parlay_index -= 1

def next_slide():
    if st.session_state.parlay_index < len(PARLAYS) - 1:
        st.session_state.parlay_index += 1

idx = st.session_state.parlay_index
current_parlay = PARLAYS[idx]
stats_df = load_nfl_data(2025 if "2025" in VIEW_MODE else 2026)

# =========================================================
# 🔬 VIEW 1: 2025 RESEARCH & BASELINES
# =========================================================
if "2025" in VIEW_MODE:
    st.header("🔬 Analytical Research & Baseline Metrics")
    
    with st.container(border=True, key="parlay-card"):
        st.subheader(f"⚡ {current_parlay['title']}")
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"**Wager:** `{current_parlay['wager']}`")
        with col_b:
            st.markdown(f"**Est. Payout:** `{current_parlay['payout']}`")
        st.divider()
        
        for leg in current_parlay['legs']:
            st.markdown(f"#### 🎯 {leg['name']}")
            
            if leg['type'] == 'player':
                stat_name = get_stat_label(leg['stat'])
                
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric(label=f"2026 Target ({stat_name})", value=f"{leg['line']:,}")
                with c2:
                    db_name = leg['db_name'].replace(" ", "")
                    api_stat = 0
                    if not stats_df.empty and 'player_name' in stats_df.columns:
                        player_data = stats_df[stats_df['player_name'] == db_name]
                        if not player_data.empty and leg['stat'] in stats_df.columns:
                            api_stat = player_data[leg['stat']].sum()
                    display_val = api_stat if api_stat > 0 else leg['2025_actual']
                    st.metric(label=f"2025 {stat_name}", value=f"{display_val:,.0f}")
                with c3:
                    diff = leg['line'] - display_val
                    st.metric(label="Target Variance vs '25", value=f"{'+' if diff > 0 else ''}{diff:,.1f}")

            else:
                target_label = f"Objective: **{leg['target']}**" if leg['type'] == 'division' else f"Target: **{leg['target']}**"
                st.markdown(target_label)
                st.markdown(f"**2025 Baseline context:** {leg['2025_result']} | {leg['place']} | {leg['playoffs']}")
            
            st.markdown(leg['narrative'])
            st.markdown("---")

# =========================================================
# 📊 VIEW 2: 2026 LIVE TRACK (DYNAMIC TRACKING)
# =========================================================
else:
    st.header("📊 Active 2026 Parlay Progress Tracker")
    
    with st.container(border=True, key="parlay-card"):
        st.subheader(f"⚡ {current_parlay['title']}")
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"**Wager:** `{current_parlay['wager']}`")
        with col_b:
            st.markdown(f"**Est. Payout:** `{current_parlay['payout']}`")
        st.divider()
        
        for leg in current_parlay['legs']:
            st.markdown(f"##### 👤 {leg['name']}")
            
            if leg['type'] == 'player':
                current_total = 0.0
                games_played = 0
                
                if not stats_df.empty and 'player_name' in stats_df.columns:
                    db_name = leg['db_name'].replace(" ", "")
                    player_data = stats_df[stats_df['player_name'] == db_name]
                    if not player_data.empty and leg['stat'] in stats_df.columns:
                        current_total = float(player_data[leg['stat']].sum())
                        if 'games' in player_data.columns:
                            games_played = int(player_data['games'].sum())
                        elif 'week' in player_data.columns:
                            games_played = int(player_data['week'].nunique())

                # Strict check specifically targeting the TD parlay ID (2) or any touchdown stat key
                is_td_leg = current_parlay['id'] == 2 or "touchdown" in leg['stat'] or leg['stat'].endswith("_tds")

                units_remaining = max(0.0, leg['line'] - current_total)
                games_remaining = max(1, 17 - games_played)
                needed_per_game = units_remaining / games_remaining if units_remaining > 0 else 0.0
                
                pct_complete = min(float(current_total / leg['line']), 1.0) if leg['line'] > 0 else 0.0
                stat_name = get_stat_label(leg['stat'])
                
                # Metrics layout
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric(label=f"Current {stat_name}", value=f"{current_total:,.0f}" if is_td_leg else f"{current_total:,.1f}")
                with c2:
                    st.metric(label=f"Goal {stat_name}", value=f"{leg['line']:,}")
                with c3:
                    if is_td_leg:
                        st.metric(
                            label="TDs Remaining", 
                            value=f"{units_remaining:,.1f}", 
                            delta=f"{games_remaining} games left"
                        )
                    else:
                        st.metric(
                            label="Needed / Game", 
                            value=f"{needed_per_game:.1f}", 
                            delta=f"{games_remaining} games left"
                        )
                
                # Progress Bar display
                progress_label = f"{pct_complete*100:.1f}% Completed ({units_remaining:,.1f} {stat_name.lower()} remaining)"
                st.progress(pct_complete, text=progress_label)
            
            else:
                c1, c2 = st.columns([2, 1])
                with c1:
                    target_label = f"Objective: **{leg['target']}**" if leg['type'] == 'division' else f"🎯 Objective: **{leg['target']}**"
                    st.markdown(target_label)
                with c2:
                    st.markdown("Status: `Pending` ⏳")
            
            st.markdown("<br>", unsafe_allow_html=True)

# --- DYNAMIC BOTTOM NAVIGATION ---
st.write("---")
col_prev, col_indicator, col_next = st.columns([1, 2, 1])
with col_prev:
    if idx > 0:
        st.button("◀ Previous", on_click=prev_slide, use_container_width=True)
with col_indicator:
    st.markdown(f"<h4 style='text-align: center; margin-top: 5px;'>Parlay {idx + 1} of {len(PARLAYS)}</h4>", unsafe_allow_html=True)
with col_next:
    if idx < len(PARLAYS) - 1:
        st.button("Next ▶", on_click=next_slide, use_container_width=True)
st.write("---")
