import pandas as pd
import streamlit as st

# ==========================================
# 1. PAGE CONFIG & CUSTOM ACCENT STYLING
# ==========================================
st.set_page_config(
    page_title="NFL Bet Portfolio", page_icon="🏈", layout="wide"
)

# Custom CSS for UI polish, neon accents, and responsive card grids
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    
    h1, h2, h3 {
        color: #00e676 !important;
        font-family: 'Trebuchet MS', sans-serif;
    }

    /* Bet Container Styling */
    .parlay-card {
        background-color: #1a1f2c;
        border: 1px solid #2d3748;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.4);
    }

    .bet-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background-color: #121621;
        border-left: 4px solid #00e676;
        padding: 10px 14px;
        border-radius: 8px;
        margin-top: 8px;
    }

    .bet-info {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .bet-img {
        width: 42px;
        height: 42px;
        object-fit: contain;
        border-radius: 50%;
        background-color: #2a3245;
        padding: 2px;
    }

    div[data-testid="stMetricValue"] {
        color: #00e676 !important;
        font-weight: bold;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Image Asset Helpers
TEAM_LOGOS = {
    "DEN": "https://a.espncdn.com/i/teamlogos/nfl/500/den.png",
    "GB": "https://a.espncdn.com/i/teamlogos/nfl/500/gb.png",
    "KC": "https://a.espncdn.com/i/teamlogos/nfl/500/kc.png",
    "PHI": "https://a.espncdn.com/i/teamlogos/nfl/500/phi.png",
    "SF": "https://a.espncdn.com/i/teamlogos/nfl/500/sf.png",
    "SEA": "https://a.espncdn.com/i/teamlogos/nfl/500/sea.png",
    "DET": "https://a.espncdn.com/i/teamlogos/nfl/500/det.png",
    "HOU": "https://a.espncdn.com/i/teamlogos/nfl/500/hou.png",
    "BAL": "https://a.espncdn.com/i/teamlogos/nfl/500/bal.png",
    "BUF": "https://a.espncdn.com/i/teamlogos/nfl/500/buf.png",
    "MIA": "https://a.espncdn.com/i/teamlogos/nfl/500/mia.png",
    "CIN": "https://a.espncdn.com/i/teamlogos/nfl/500/cin.png",
}


def get_player_headshot_url(player_id):
    return f"https://a.espncdn.com/i/headshots/nfl/players/full/{player_id}.png"


# Component Builders
def render_team_leg(team_code, team_name, detail):
    logo = TEAM_LOGOS.get(
        team_code, "https://a.espncdn.com/i/teamlogos/nfl/500/nfl.png"
    )
    return f"""
    <div class="bet-row">
        <div class="bet-info">
            <img src="{logo}" class="bet-img"/>
            <div>
                <strong style="color: #ffffff;">{team_name}</strong><br/>
                <span style="color: #a0aec0; font-size: 0.85em;">{detail}</span>
            </div>
        </div>
        <span style="color: #00e676; font-weight: bold;">Leg Active</span>
    </div>
    """


def render_player_leg(player_name, espn_id, detail):
    photo = get_player_headshot_url(espn_id)
    return f"""
    <div class="bet-row">
        <div class="bet-info">
            <img src="{photo}" class="bet-img"/>
            <div>
                <strong style="color: #ffffff;">{player_name}</strong><br/>
                <span style="color: #a0aec0; font-size: 0.85em;">{detail}</span>
            </div>
        </div>
        <span style="color: #00e676; font-weight: bold;">Leg Active</span>
    </div>
    """


# Standings Dataset
standings_2025_data = [
    {"Division": "AFC West", "Team": "Denver Broncos", "W": 14, "L": 3, "PCT": 0.824, "Playoff": "Div Champ"},
    {"Division": "AFC West", "Team": "Los Angeles Chargers", "W": 11, "L": 6, "PCT": 0.647, "Playoff": "Wild Card"},
    {"Division": "AFC West", "Team": "Kansas City Chiefs", "W": 6, "L": 11, "PCT": 0.353, "Playoff": "-"},
    {"Division": "AFC West", "Team": "Las Vegas Raiders", "W": 3, "L": 14, "PCT": 0.176, "Playoff": "-"},
    {"Division": "NFC North", "Team": "Chicago Bears", "W": 11, "L": 6, "PCT": 0.647, "Playoff": "Div Champ"},
    {"Division": "NFC North", "Team": "Green Bay Packers", "W": 9, "L": 7, "PCT": 0.559, "Playoff": "Wild Card"},
    {"Division": "NFC North", "Team": "Minnesota Vikings", "W": 9, "L": 8, "PCT": 0.529, "Playoff": "-"},
    {"Division": "NFC North", "Team": "Detroit Lions", "W": 9, "L": 8, "PCT": 0.529, "Playoff": "-"},
    {"Division": "NFC West", "Team": "Seattle Seahawks", "W": 14, "L": 3, "PCT": 0.824, "Playoff": "Div Champ"},
    {"Division": "NFC West", "Team": "Los Angeles Rams", "W": 12, "L": 5, "PCT": 0.706, "Playoff": "Wild Card"},
    {"Division": "NFC West", "Team": "San Francisco 49ers", "W": 12, "L": 5, "PCT": 0.706, "Playoff": "Wild Card"},
    {"Division": "NFC West", "Team": "Arizona Cardinals", "W": 3, "L": 14, "PCT": 0.176, "Playoff": "-"},
    {"Division": "AFC East", "Team": "New England Patriots", "W": 14, "L": 3, "PCT": 0.824, "Playoff": "Div Champ"},
    {"Division": "AFC East", "Team": "Buffalo Bills", "W": 12, "L": 5, "PCT": 0.706, "Playoff": "Wild Card"},
    {"Division": "AFC East", "Team": "Miami Dolphins", "W": 7, "L": 10, "PCT": 0.412, "Playoff": "-"},
    {"Division": "AFC East", "Team": "New York Jets", "W": 3, "L": 14, "PCT": 0.176, "Playoff": "-"},
]
df_standings = pd.DataFrame(standings_2025_data)

# ==========================================
# 2. APP INTERFACE
# ==========================================
st.title("🏈 NFL Bet Portfolio & Tracker")

tab_parlays, tab_props, tab_full_standings = st.tabs(
    ["Team Parlays & Context", "Player Prop Trackers", "Full Standings Grid"]
)

# --- TAB 1: TEAM BETS SIDE-BY-SIDE WITH DIVISION STANDINGS ---
with tab_parlays:
    st.header("Team Bets & Live Division Context")
    st.caption("Side-by-side view of active team wagers alongside their current divisional race.")

    # PARLAY 1: PLAYOFFS OR BUST
    st.markdown("### 🎯 Parlay 1: Playoffs or Bust (+450)")
    col_bets1, col_stand1 = st.columns([1.1, 0.9])

    with col_bets1:
        st.markdown(
            '<div class="parlay-card">'
            + render_team_leg("DEN", "Denver Broncos", "To Make the Playoffs")
            + render_team_leg("GB", "Green Bay Packers", "To Make the Playoffs")
            + render_team_leg("MIA", "Miami Dolphins", "To Make the Playoffs")
            + "</div>",
            unsafe_allow_html=True,
        )

    with col_stand1:
        st.subheader("Division Context")
        sub_df1 = df_standings[
            df_standings["Division"].isin(["AFC West", "NFC North", "AFC East"])
        ]
        st.dataframe(
            sub_df1,
            hide_index=True,
            use_container_width=True,
            column_config={"PCT": st.column_config.NumberColumn(format="%.3f")},
        )

    st.markdown("---")

    # PARLAY 2: DIVISION WINNERS
    st.markdown("### 🏆 Parlay 2: Division Champions (+1200)")
    col_bets2, col_stand2 = st.columns([1.1, 0.9])

    with col_bets2:
        st.markdown(
            '<div class="parlay-card">'
            + render_team_leg("DET", "Detroit Lions", "Win NFC North")
            + render_team_leg("BUF", "Buffalo Bills", "Win AFC East")
            + render_team_leg("SF", "San Francisco 49ers", "Win NFC West")
            + "</div>",
            unsafe_allow_html=True,
        )

    with col_stand2:
        st.subheader("Division Context")
        sub_df2 = df_standings[
            df_standings["Division"].isin(["NFC North", "AFC East", "NFC West"])
        ]
        st.dataframe(
            sub_df2,
            hide_index=True,
            use_container_width=True,
            column_config={"PCT": st.column_config.NumberColumn(format="%.3f")},
        )

# --- TAB 2: PLAYER PROP TRACKERS WITH HEADSHOTS ---
with tab_props:
    st.header("Player Prop Parlays")

    col_prop1, col_prop2 = st.columns(2)

    with col_prop1:
        st.markdown("### 📈 Parlay 3: Total Yards Over")
        st.markdown(
            '<div class="parlay-card">'
            + render_player_leg("Patrick Mahomes", 3139477, "Over 4,250.5 Passing Yards")
            + render_player_leg("Christian McCaffrey", 3042519, "Over 1,150.5 Rushing Yards")
            + render_player_leg("Tyreek Hill", 3116365, "Over 1,250.5 Receiving Yards")
            + "</div>",
            unsafe_allow_html=True,
        )

        st.markdown("### ⚡ Parlay 5: Floor Multi-Prop")
        st.markdown(
            '<div class="parlay-card">'
            + render_player_leg("Lamar Jackson", 3916387, "50+ Rushing Yards in 10+ Games")
            + render_player_leg("Amon-Ra St. Brown", 4361522, "6+ Receptions in 12+ Games")
            + "</div>",
            unsafe_allow_html=True,
        )

    with col_prop2:
        st.markdown("### 🏈 Parlay 4: TD Machines")
        st.markdown(
            '<div class="parlay-card">'
            + render_player_leg("Derrick Henry", 3043078, "12+ Total Touchdowns")
            + render_player_leg("Travis Kelce", 15847, "8+ Receiving Touchdowns")
            + render_player_leg("Ja'Marr Chase", 4362628, "10+ Receiving Touchdowns")
            + "</div>",
            unsafe_allow_html=True,
        )

        st.markdown("### 🎯 Parlay 6: Longshot Milestones")
        st.markdown(
            '<div class="parlay-card">'
            + render_player_leg("Josh Allen", 3918298, "4,000+ Pass Yds / 35+ Total TDs")
            + render_player_leg("CeeDee Lamb", 4426515, "1,400+ Receiving Yards")
            + "</div>",
            unsafe_allow_html=True,
        )

# --- TAB 3: FULL STANDINGS GRID ---
with tab_full_standings:
    st.header("Overall 2025 Standings")
    st.dataframe(
        df_standings,
        hide_index=True,
        use_container_width=True,
        column_config={"PCT": st.column_config.NumberColumn(format="%.3f")},
    )
    