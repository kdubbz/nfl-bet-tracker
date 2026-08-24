import streamlit as st
import pandas as pd
import nflreadpy as nfl
import time

# Set page configuration for mobile-first layout
st.set_page_config(page_title="NFL Bet Portfolio", layout="centered")

# --- CUSTOM CSS FOR MODERN CARDS & POLISHED UI ---
st.html("""
<style>
/* Card Styling */
.parlay-card {
    border: 2px solid #31333F !important;
    border-radius: 12px !important;
    padding: 20px !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
    background-color: #0E1117 !important;
    margin-bottom: 25px;
}

.metric-box {
    background-color: #1E222A;
    border-left: 4px solid #FFD700;
    padding: 12px 16px;
    border-radius: 8px;
    margin-top: 10px;
    margin-bottom: 15px;
}

/* Custom Progress Bar Colors */
div[data-testid="stProgress"] > div > div > div > div {
    background-color: #FFD700 !important;
}

/* Standings Table Styling */
div[data-testid="stDataFrame"] {
    border-radius: 8px;
    overflow: hidden;
}
</style>
""")

# --- STATIC DATA ---
TEAM_INFO = {
    "BAL": {"Name": "Baltimore Ravens", "Conf": "AFC", "Div": "AFC North"},
    "CIN": {"Name": "Cincinnati Bengals", "Conf": "AFC", "Div": "AFC North"},
    "CLE": {"Name": "Cleveland Browns", "Conf": "AFC", "Div": "AFC North"},
    "PIT": {"Name": "Pittsburgh Steelers", "Conf": "AFC", "Div": "AFC North"},
    "DAL": {"Name": "Dallas Cowboys", "Conf": "NFC", "Div": "NFC East"},
    "NYG": {"Name": "New York Giants", "Conf": "NFC", "Div": "NFC East"},
    "PHI": {"Name": "Philadelphia Eagles", "Conf": "NFC", "Div": "NFC East"},
    "WAS": {"Name": "Washington Commanders", "Conf": "NFC", "Div": "NFC East"},
    "CHI": {"Name": "Chicago Bears", "Conf": "NFC", "Div": "NFC North"},
    "DET": {"Name": "Detroit Lions", "Conf": "NFC", "Div": "NFC North"},
    "GB": {"Name": "Green Bay Packers", "Conf": "NFC", "Div": "NFC North"},
    "MIN": {"Name": "Minnesota Vikings", "Conf": "NFC", "Div": "NFC North"},
    "HOU": {"Name": "Houston Texans", "Conf": "AFC", "Div": "AFC South"},
    "IND": {"Name": "Indianapolis Colts", "Conf": "AFC", "Div": "AFC South"},
    "JAX": {"Name": "Jacksonville Jaguars", "Conf": "AFC", "Div": "AFC South"},
    "TEN": {"Name": "Tennessee Titans", "Conf": "AFC", "Div": "AFC South"},
    "BUF": {"Name": "Buffalo Bills", "Conf": "AFC", "Div": "AFC East"},
    "MIA": {"Name": "Miami Dolphins", "Conf": "AFC", "Div": "AFC East"},
    "NE": {"Name": "New England Patriots", "Conf": "AFC", "Div": "AFC East"},
    "NYJ": {"Name": "New York Jets", "Conf": "AFC", "Div": "AFC East"},
    "DEN": {"Name": "Denver Broncos", "Conf": "AFC", "Div": "AFC West"},
    "KC": {"Name": "Kansas City Chiefs", "Conf": "AFC", "Div": "AFC West"},
    "LV": {"Name": "Las Vegas Raiders", "Conf": "AFC", "Div": "AFC West"},
    "LAC": {"Name": "Los Angeles Chargers", "Conf": "AFC", "Div": "AFC West"},
    "ATL": {"Name": "Atlanta Falcons", "Conf": "NFC", "Div": "NFC South"},
    "CAR": {"Name": "Carolina Panthers", "Conf": "NFC", "Div": "NFC South"},
    "NO": {"Name": "New Orleans Saints", "Conf": "NFC", "Div": "NFC South"},
    "TB": {"Name": "Tampa Bay Buccaneers", "Conf": "NFC", "Div": "NFC South"},
    "ARI": {"Name": "Arizona Cardinals", "Conf": "NFC", "Div": "NFC West"},
    "LA": {"Name": "Los Angeles Rams", "Conf": "NFC", "Div": "NFC West"},
    "LAR": {"Name": "Los Angeles Rams", "Conf": "NFC", "Div": "NFC West"},
    "SF": {"Name": "San Francisco 49ers", "Conf": "NFC", "Div": "NFC West"},
    "SEA": {"Name": "Seattle Seahawks", "Conf": "NFC", "Div": "NFC West"}
}

# --- DATA FETCHING ---
@st.cache_data(ttl=60)
def load_nfl_player_stats(year):
    try:
        raw_stats = nfl.load_player_stats([year])
        return raw_stats.to_pandas()
    except Exception:
        return pd.DataFrame()

@st.cache_data(ttl=60)
def load_nfl_standings(year):
    """Computes live standings and playoff seeding."""
    try:
        schedules = nfl.load_schedules([year]).to_pandas()
        completed = schedules[(schedules['game_type'] == 'REG') & (schedules['result'].notna())]
        
        teams = {abbr: {'W': 0, 'L': 0, 'T': 0} for abbr in TEAM_INFO.keys()}
        for _, game in completed.iterrows():
            home, away = game['home_team'], game['away_team']
            h_score, a_score = game['home_score'], game['away_score']
            
            if home not in teams: teams[home] = {'W': 0, 'L': 0, 'T': 0}
            if away not in teams: teams[away] = {'W': 0, 'L': 0, 'T': 0}
            
            if h_score > a_score:
                teams[home]['W'] += 1
                teams[away]['L'] += 1
            elif a_score > h_score:
                teams[away]['W'] += 1
                teams[home]['L'] += 1
            else:
                teams[home]['T'] += 1
                teams[away]['T'] += 1
                
        df = pd.DataFrame.from_dict(teams, orient='index').reset_index()
        df.rename(columns={'index': 'TeamAbbr'}, inplace=True)
        
        df['TeamName'] = df['TeamAbbr'].apply(lambda x: TEAM_INFO.get(x, {}).get("Name", x))
        df['Conf'] = df['TeamAbbr'].apply(lambda x: TEAM_INFO.get(x, {}).get("Conf", ""))
        df['Div'] = df['TeamAbbr'].apply(lambda x: TEAM_INFO.get(x, {}).get("Div", ""))
        df['PCT'] = df.apply(lambda r: (r['W'] + 0.5 * r['T']) / max(1, r['W'] + r['L'] + r['T']), axis=1)
        
        df['Seed'] = 0
        for conf in ['AFC', 'NFC']:
            conf_df = df[df['Conf'] == conf].copy()
            div_winners = conf_df.sort_values(['PCT', 'W'], ascending=False).groupby('Div').head(1)
            wildcards = conf_df[~conf_df['TeamAbbr'].isin(div_winners['TeamAbbr'])]
            
            div_winners = div_winners.sort_values(['PCT', 'W'], ascending=False)
            wildcards = wildcards.sort_values(['PCT', 'W'], ascending=False)
            
            seed = 1
            for _, row in div_winners.iterrows():
                df.loc[df['TeamAbbr'] == row['TeamAbbr'], 'Seed'] = seed
                seed += 1
            for _, row in wildcards.iterrows():
                df.loc[df['TeamAbbr'] == row['TeamAbbr'], 'Seed'] = seed
                seed += 1
                
        return df
    except Exception:
        return pd.DataFrame()


# --- SIDEBAR: LIVE POLLING ---
st.sidebar.header("🔴 Live Settings")
auto_refresh = st.sidebar.toggle("Live Game Day Polling (60s)", value=False, help="Automatically refreshes the app every 60 seconds to pull live stats.")
if auto_refresh:
    time.sleep(60)
    st.rerun()


# --- PORTFOLIO DEFINITIONS ---
PARLAYS = [
    {
        "id": 0, "title": "Total Yards Over", "wager": "BONUS BET", "payout": "$148.94",
        "legs": [
            {"name": "Rome Odunze", "team": "Chicago Bears", "db_name": "R.Odunze", "stat": "receiving_yards", "line": 799.5, "type": "player", "2025_actual": 661.0, "narrative": "Requires clearing **799.5 receiving yards** (averaging 47.1 yards/game over a 17-game season)."},
            {"name": "Josh Allen", "team": "Buffalo Bills", "db_name": "J.Allen", "stat": "passing_yards", "line": 3549.5, "type": "player", "2025_actual": 3668.0, "narrative": "Requires clearing **3,549.5 passing yards** (averaging 208.8 yards/game)."},
            {"name": "Kyren Williams", "team": "Los Angeles Rams", "db_name": "K.Williams", "stat": "rushing_yards", "line": 999.5, "type": "player", "2025_actual": 1252.0, "narrative": "Requires clearing **999.5 rushing yards** (averaging 58.8 yards/game)."}
        ]
    },
    {
        "id": 1, "title": "Maye there be Love", "wager": "BONUS BET", "payout": "$39.53",
        "legs": [
            {"name": "Jordan Love", "db_name": "J.Love", "stat": "passing_yards", "line": 3500.0, "type": "player", "2025_actual": 3381.0, "narrative": "Requires clearing **3,500.0 passing yards**."},
            {"name": "Drake Maye", "db_name": "D.Maye", "stat": "rushing_touchdowns", "line": 5.0, "type": "player", "2025_actual": 4.0, "narrative": "Requires reaching **5 rushing touchdowns**."}
        ]
    },
    {
        "id": 2, "title": "TD Machines", "wager": "BONUS BET", "payout": "$141.23",
        "legs": [
            {"name": "Aaron Rodgers", "db_name": "A.Rodgers", "stat": "passing_touchdowns", "line": 21.5, "type": "player", "2025_actual": 24.0, "narrative": "Requires clearing **21.5 passing touchdowns**."},
            {"name": "George Pickens", "db_name": "G.Pickens", "stat": "receiving_touchdowns", "line": 6.5, "type": "player", "2025_actual": 9.0, "narrative": "Requires clearing **6.5 receiving touchdowns**."},
            {"name": "Jonathan Taylor", "db_name": "J.Taylor", "stat": "rushing_touchdowns", "line": 11.5, "type": "player", "2025_actual": 18.0, "narrative": "Requires clearing **11.5 rushing touchdowns**."}
        ]
    },
    {
        "id": 3, "title": "Division Winners", "wager": "$10.00", "payout": "$40.19",
        "legs": [
            {"name": "Baltimore Ravens", "type": "division", "division": "AFC North", "target": "1st place in AFC North", "2025_result": "8-9", "place": "2nd", "playoffs": "Missed", "narrative": "Requires 1st place finish in AFC North."},
            {"name": "Philadelphia Eagles", "type": "division", "division": "NFC East", "target": "1st place in NFC East", "2025_result": "11-6", "place": "1st", "playoffs": "Made", "narrative": "Requires 1st place finish in NFC East."}
        ]
    },
    {
        "id": 4, "title": "Division Winners", "wager": "$5.00", "payout": "$54.33",
        "legs": [
            {"name": "Green Bay Packers", "type": "division", "division": "NFC North", "target": "1st place in NFC North", "2025_result": "9-7-1", "place": "2nd", "playoffs": "Made", "narrative": "Requires 1st place finish in NFC North."},
            {"name": "Jacksonville Jaguars", "type": "division", "division": "AFC South", "target": "1st place in AFC South", "2025_result": "13-4", "place": "1st", "playoffs": "Made", "narrative": "Requires 1st place finish in AFC South."}
        ]
    },
    {
        "id": 5, "title": "Playoffs or Bust", "wager": "BONUS BET", "payout": "$166.35",
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

def get_stat_label(stat_key):
    mapping = {
        "passing_yards": "Pass Yds",
        "rushing_yards": "Rush Yds",
        "receiving_yards": "Rec Yds",
        "passing_touchdowns": "Pass TDs",
        "rushing_touchdowns": "Rush TDs",
        "receiving_touchdowns": "Rec TDs"
    }
    return mapping.get(stat_key, "Units")

# --- UI HEADER ---
st.title("🏈 NFL Bet Portfolio")

# --- TABS SETUP ---
tab_research, tab_live = st.tabs(["🔬 2025 Research", "🔴 Live Game Day Tracker"])

# =========================================================
# TAB 1: 2025 RESEARCH (PAGINATED VIEW)
# =========================================================
with tab_research:
    # Load 2025 Data
    stats_df_25 = load_nfl_player_stats(2025)
    standings_df_25 = load_nfl_standings(2025)

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

    with st.container(border=True):
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
                    st.metric(label=f"Target ({stat_name})", value=f"{leg['line']:,}")
                with c2:
                    db_name = leg['db_name'].replace(" ", "")
                    api_stat = 0
                    if not stats_df_25.empty and 'player_name' in stats_df_25.columns:
                        player_data = stats_df_25[stats_df_25['player_name'] == db_name]
                        if not player_data.empty and leg['stat'] in stats_df_25.columns:
                            api_stat = player_data[leg['stat']].sum()
                    display_val = api_stat if api_stat > 0 else leg['2025_actual']
                    st.metric(label=f"2025 {stat_name}", value=f"{display_val:,.0f}")
                with c3:
                    diff = display_val - leg['line']
                    st.metric(label="Variance vs '26 Line", value=f"{'+' if diff > 0 else ''}{diff:,.1f}")

            else:
                target_label = f"Objective: **{leg['target']}**"
                st.markdown(target_label)
                st.markdown(f"**2025 Context:** {leg['2025_result']} | {leg['place']} | Playoffs: {leg['playoffs']}")
            
            st.markdown(f"<div class='metric-box'>{leg['narrative']}</div>", unsafe_allow_html=True)
            st.markdown("---")

    # Pagination navigation
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


# =========================================================
# TAB 2: LIVE 2026 TRACKER (ALL-IN-ONE DASHBOARD)
# =========================================================
with tab_live:
    # Load 2026 Data
    stats_df_26 = load_nfl_player_stats(2026)
    standings_df_26 = load_nfl_standings(2026)

    st.markdown("### 🔴 Active 2026 Progress")
    st.caption("Monitoring all parlays simultaneously. Enable polling in the sidebar for auto-refresh.")
    
    for parlay in PARLAYS:
        with st.container(border=True):
            st.subheader(f"⚡ {parlay['title']}")
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f"**Wager:** `{parlay['wager']}`")
            with col_b:
                st.markdown(f"**Est. Payout:** `{parlay['payout']}`")
            st.divider()
            
            for leg in parlay['legs']:
                st.markdown(f"##### 👤 {leg['name']}")
                
                # --- PLAYER BETS ---
                if leg['type'] == 'player':
                    current_total = 0.0
                    games_played = 0
                    
                    if not stats_df_26.empty and 'player_name' in stats_df_26.columns:
                        db_name = leg['db_name'].replace(" ", "")
                        player_data = stats_df_26[stats_df_26['player_name'] == db_name]
                        if not player_data.empty and leg['stat'] in stats_df_26.columns:
                            current_total = float(player_data[leg['stat']].sum())
                            if 'games' in player_data.columns:
                                games_played = int(player_data['games'].sum())
                            elif 'week' in player_data.columns:
                                games_played = int(player_data['week'].nunique())

                    is_td_leg = parlay['id'] == 2 or "touchdown" in leg['stat'] or leg['stat'].endswith("_tds")
                    units_remaining = max(0.0, leg['line'] - current_total)
                    games_remaining = max(1, 17 - games_played)
                    needed_per_game = units_remaining / games_remaining if units_remaining > 0 else 0.0
                    pct_complete = min(float(current_total / leg['line']), 1.0) if leg['line'] > 0 else 0.0
                    stat_name = get_stat_label(leg['stat'])
                    
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.metric(label=f"Current {stat_name}", value=f"{current_total:,.0f}" if is_td_leg else f"{current_total:,.1f}")
                    with c2:
                        st.metric(label=f"Goal {stat_name}", value=f"{leg['line']:,}")
                    with c3:
                        if is_td_leg:
                            st.metric(label="TDs Remaining", value=f"{units_remaining:,.1f}", delta=f"{games_remaining} games left")
                        else:
                            st.metric(label="Needed / Game", value=f"{needed_per_game:.1f}", delta=f"{games_remaining} games left")
                    
                    st.progress(pct_complete, text=f"{pct_complete*100:.1f}% Completed ({units_remaining:,.1f} {stat_name.lower()} remaining)")
                
                # --- DIVISION BETS ---
                elif leg['type'] == 'division':
                    st.markdown(f"**Objective:** {leg['target']}")
                    div_name = leg.get('division')
                    
                    if div_name and not standings_df_26.empty:
                        div_standings = standings_df_26[standings_df_26['Div'] == div_name].copy()
                        div_standings = div_standings.sort_values(by=['PCT', 'W'], ascending=False).reset_index(drop=True)
                        div_standings['Pos'] = range(1, len(div_standings) + 1)
                        
                        st.dataframe(
                            div_standings[['Pos', 'TeamName', 'W', 'L', 'T']],
                            hide_index=True,
                            use_container_width=True
                        )
                    else:
                        st.info(f"Standings pending season kickoff for {div_name}")

                # --- PLAYOFF BETS ---
                elif leg['type'] == 'playoff':
                    c1, c2 = st.columns([1, 1])
                    with c1:
                        st.markdown(f"🎯 Objective: **{leg['target']}**")
                    with c2:
                        if not standings_df_26.empty:
                            team_data = standings_df_26[standings_df_26['TeamName'] == leg['name']]
                            if not team_data.empty:
                                seed = team_data['Seed'].values[0]
                                conf = team_data['Conf'].values[0]
                                
                                if seed <= 7:
                                    st.success(f"✅ Currently IN (Seed #{seed} {conf})")
                                else:
                                    st.error(f"❌ Currently OUT (Seed #{seed} {conf})")
                            else:
                                st.warning("Status: Matchup Unknown")
                        else:
                            st.info("Status: Pending Kickoff ⏳")
                
                st.markdown("<br>", unsafe_allow_html=True)
                  