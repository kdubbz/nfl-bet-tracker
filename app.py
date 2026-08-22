import pandas as pd
import streamlit as st

# ==========================================
# 1. PAGE CONFIG & CUSTOM ACCENT STYLING
# ==========================================
st.set_page_config(
    page_title="NFL Bet Portfolio", page_icon="🏈", layout="wide"
)

# Custom CSS for UI polish and dark-mode accent highlights
st.markdown(
    """
    <style>
    /* Global Background and Accent Glows */
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    
    /* Header Accent Bar */
    h1, h2, h3 {
        color: #00e676 !important;
        font-family: 'Trebuchet MS', sans-serif;
    }

    /* Custom Bet Cards */
    .bet-card {
        background-color: #1a1f2c;
        border: 1px solid #2d3748;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    .bet-card-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 8px;
    }
    
    .bet-card-img {
        width: 45px;
        height: 45px;
        object-fit: contain;
        border-radius: 50%;
        background-color: #2a3245;
        padding: 3px;
    }

    /* Custom Metric Accent Cards */
    div[data-testid="stMetricValue"] {
        color: #00e676 !important;
        font-weight: bold;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Dynamic asset URL functions
# ESPN's public static endpoints provide crisp PNGs for team logos and player headshots
TEAM_LOGOS = {
    "DEN": "https://a.espncdn.com/i/teamlogos/nfl/500/den.png",
    "GB": "https://a.espncdn.com/i/teamlogos/nfl/500/gb.png",
    "KC": "https://a.espncdn.com/i/teamlogos/nfl/500/kc.png",
    "PHI": "https://a.espncdn.com/i/teamlogos/nfl/500/phi.png",
    "SF": "https://a.espncdn.com/i/teamlogos/nfl/500/sf.png",
    "SEA": "https://a.espncdn.com/i/teamlogos/nfl/500/sea.png",
}


def get_player_headshot_url(player_id):
    return f"https://a.espncdn.com/i/headshots/nfl/players/full/{player_id}.png"


# Helper Functions to Render Styled Bet Cards
def render_team_bet(team_code, team_name, bet_desc, odds, wager):
    logo_url = TEAM_LOGOS.get(
        team_code, "https://a.espncdn.com/i/teamlogos/nfl/500/nfl.png"
    )
    st.markdown(
        f"""
    <div class="bet-card">
        <div class="bet-card-header">
            <img src="{logo_url}" class="bet-card-img"/>
            <div>
                <strong style="font-size: 1.1em; color: #ffffff;">{team_name}</strong><br/>
                <span style="color: #a0aec0; font-size: 0.9em;">{bet_desc}</span>
            </div>
        </div>
        <div style="display: flex; justify-content: space-between; margin-top: 5px; font-size: 0.95em;">
            <span>Odds: <strong>{odds}</strong></span>
            <span>Wager: <strong style="color: #00e676;">${wager}</strong></span>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )


def render_player_bet(player_name, espn_id, prop_desc, odds, wager):
    photo_url = get_player_headshot_url(espn_id)
    st.markdown(
        f"""
    <div class="bet-card">
        <div class="bet-card-header">
            <img src="{photo_url}" class="bet-card-img"/>
            <div>
                <strong style="font-size: 1.1em; color: #ffffff;">{player_name}</strong><br/>
                <span style="color: #a0aec0; font-size: 0.9em;">{prop_desc}</span>
            </div>
        </div>
        <div style="display: flex; justify-content: space-between; margin-top: 5px; font-size: 0.95em;">
            <span>Odds: <strong>{odds}</strong></span>
            <span>Wager: <strong style="color: #00e676;">${wager}</strong></span>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )


# ==========================================
# 2. MAIN APP & TABS
# ==========================================
st.title("🏈 NFL Bet Portfolio Dashboard")

tab_portfolio, tab_2025 = st.tabs(["Active Portfolio", "2025 Standings"])

# --- TAB 1: ACTIVE PORTFOLIO WITH LOGOS & HEADSHOTS ---
with tab_portfolio:
    st.header("Active Wagers & Prop Builder")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Team Bets")
        render_team_bet("DEN", "Denver Broncos", "Moneyline vs. KC", "-120", 50)
        render_team_bet(
            "GB", "Green Bay Packers", "Spread -3.5 vs. CHI", "-110", 100
        )

    with col2:
        st.subheader("Player Props")
        # Example using Patrick Mahomes (ESPN ID: 3139477)
        render_player_bet(
            "Patrick Mahomes", 3139477, "Over 265.5 Passing Yards", "-115", 75
        )
        # Example using Christian McCaffrey (ESPN ID: 3042519)
        render_player_bet(
            "Christian McCaffrey",
            3042519,
            "Anytime Touchdown Scorer",
            "-140",
            80,
        )

# --- TAB 2: 2025 STANDINGS TAB ---
with tab_2025:
    st.header("2025 Regular Season Standings")

    standings_2025_data = [
        # AFC East
        {
            "Conference": "AFC",
            "Division": "AFC East",
            "Team": "New England Patriots",
            "W": 14,
            "L": 3,
            "T": 0,
            "PCT": 0.824,
            "Playoff": "Division Champion (1)",
        },
        {
            "Conference": "AFC",
            "Division": "AFC East",
            "Team": "Buffalo Bills",
            "W": 12,
            "L": 5,
            "T": 0,
            "PCT": 0.706,
            "Playoff": "Wild Card",
        },
        {
            "Conference": "AFC",
            "Division": "AFC East",
            "Team": "Miami Dolphins",
            "W": 7,
            "L": 10,
            "T": 0,
            "PCT": 0.412,
            "Playoff": "-",
        },
        {
            "Conference": "AFC",
            "Division": "AFC East",
            "Team": "New York Jets",
            "W": 3,
            "L": 14,
            "T": 0,
            "PCT": 0.176,
            "Playoff": "-",
        },
        # AFC North
        {
            "Conference": "AFC",
            "Division": "AFC North",
            "Team": "Pittsburgh Steelers",
            "W": 10,
            "L": 7,
            "T": 0,
            "PCT": 0.588,
            "Playoff": "Division Champion",
        },
        {
            "Conference": "AFC",
            "Division": "AFC North",
            "Team": "Baltimore Ravens",
            "W": 8,
            "L": 9,
            "T": 0,
            "PCT": 0.471,
            "Playoff": "-",
        },
        {
            "Conference": "AFC",
            "Division": "AFC North",
            "Team": "Cincinnati Bengals",
            "W": 6,
            "L": 11,
            "T": 0,
            "PCT": 0.353,
            "Playoff": "-",
        },
        {
            "Conference": "AFC",
            "Division": "AFC North",
            "Team": "Cleveland Browns",
            "W": 5,
            "L": 12,
            "T": 0,
            "PCT": 0.294,
            "Playoff": "-",
        },
        # AFC South
        {
            "Conference": "AFC",
            "Division": "AFC South",
            "Team": "Jacksonville Jaguars",
            "W": 13,
            "L": 4,
            "T": 0,
            "PCT": 0.765,
            "Playoff": "Division Champion",
        },
        {
            "Conference": "AFC",
            "Division": "AFC South",
            "Team": "Houston Texans",
            "W": 12,
            "L": 5,
            "T": 0,
            "PCT": 0.706,
            "Playoff": "Wild Card",
        },
        {
            "Conference": "AFC",
            "Division": "AFC South",
            "Team": "Indianapolis Colts",
            "W": 8,
            "L": 9,
            "T": 0,
            "PCT": 0.471,
            "Playoff": "-",
        },
        {
            "Conference": "AFC",
            "Division": "AFC South",
            "Team": "Tennessee Titans",
            "W": 3,
            "L": 14,
            "T": 0,
            "PCT": 0.176,
            "Playoff": "-",
        },
        # AFC West
        {
            "Conference": "AFC",
            "Division": "AFC West",
            "Team": "Denver Broncos",
            "W": 14,
            "L": 3,
            "T": 0,
            "PCT": 0.824,
            "Playoff": "Division Champion",
        },
        {
            "Conference": "AFC",
            "Division": "AFC West",
            "Team": "Los Angeles Chargers",
            "W": 11,
            "L": 6,
            "T": 0,
            "PCT": 0.647,
            "Playoff": "Wild Card",
        },
        {
            "Conference": "AFC",
            "Division": "AFC West",
            "Team": "Kansas City Chiefs",
            "W": 6,
            "L": 11,
            "T": 0,
            "PCT": 0.353,
            "Playoff": "-",
        },
        {
            "Conference": "AFC",
            "Division": "AFC West",
            "Team": "Las Vegas Raiders",
            "W": 3,
            "L": 14,
            "T": 0,
            "PCT": 0.176,
            "Playoff": "-",
        },
        # NFC East
        {
            "Conference": "NFC",
            "Division": "NFC East",
            "Team": "Philadelphia Eagles",
            "W": 11,
            "L": 6,
            "T": 0,
            "PCT": 0.647,
            "Playoff": "Division Champion",
        },
        {
            "Conference": "NFC",
            "Division": "NFC East",
            "Team": "Dallas Cowboys",
            "W": 7,
            "L": 9,
            "T": 1,
            "PCT": 0.441,
            "Playoff": "-",
        },
        {
            "Conference": "NFC",
            "Division": "NFC East",
            "Team": "Washington Commanders",
            "W": 5,
            "L": 12,
            "T": 0,
            "PCT": 0.294,
            "Playoff": "-",
        },
        {
            "Conference": "NFC",
            "Division": "NFC East",
            "Team": "New York Giants",
            "W": 4,
            "L": 13,
            "T": 0,
            "PCT": 0.235,
            "Playoff": "-",
        },
        # NFC North
        {
            "Conference": "NFC",
            "Division": "NFC North",
            "Team": "Chicago Bears",
            "W": 11,
            "L": 6,
            "T": 0,
            "PCT": 0.647,
            "Playoff": "Division Champion",
        },
        {
            "Conference": "NFC",
            "Division": "NFC North",
            "Team": "Green Bay Packers",
            "W": 9,
            "L": 7,
            "T": 1,
            "PCT": 0.559,
            "Playoff": "Wild Card",
        },
        {
            "Conference": "NFC",
            "Division": "NFC North",
            "Team": "Minnesota Vikings",
            "W": 9,
            "L": 8,
            "T": 0,
            "PCT": 0.529,
            "Playoff": "-",
        },
        {
            "Conference": "NFC",
            "Division": "NFC North",
            "Team": "Detroit Lions",
            "W": 9,
            "L": 8,
            "T": 0,
            "PCT": 0.529,
            "Playoff": "-",
        },
        # NFC South
        {
            "Conference": "NFC",
            "Division": "NFC South",
            "Team": "Carolina Panthers",
            "W": 8,
            "L": 9,
            "T": 0,
            "PCT": 0.471,
            "Playoff": "Division Champion",
        },
        {
            "Conference": "NFC",
            "Division": "NFC South",
            "Team": "Tampa Bay Buccaneers",
            "W": 8,
            "L": 9,
            "T": 0,
            "PCT": 0.471,
            "Playoff": "-",
        },
        {
            "Conference": "NFC",
            "Division": "NFC South",
            "Team": "Atlanta Falcons",
            "W": 8,
            "L": 9,
            "T": 0,
            "PCT": 0.471,
            "Playoff": "-",
        },
        {
            "Conference": "NFC",
            "Division": "NFC South",
            "Team": "New Orleans Saints",
            "W": 6,
            "L": 11,
            "T": 0,
            "PCT": 0.353,
            "Playoff": "-",
        },
        # NFC West
        {
            "Conference": "NFC",
            "Division": "NFC West",
            "Team": "Seattle Seahawks",
            "W": 14,
            "L": 3,
            "T": 0,
            "PCT": 0.824,
            "Playoff": "Division Champion (Super Bowl Champion)",
        },
        {
            "Conference": "NFC",
            "Division": "NFC West",
            "Team": "Los Angeles Rams",
            "W": 12,
            "L": 5,
            "T": 0,
            "PCT": 0.706,
            "Playoff": "Wild Card",
        },
        {
            "Conference": "NFC",
            "Division": "NFC West",
            "Team": "San Francisco 49ers",
            "W": 12,
            "L": 5,
            "T": 0,
            "PCT": 0.706,
            "Playoff": "Wild Card",
        },
        {
            "Conference": "NFC",
            "Division": "NFC West",
            "Team": "Arizona Cardinals",
            "W": 3,
            "L": 14,
            "T": 0,
            "PCT": 0.176,
            "Playoff": "-",
        },
    ]

    df_2025 = pd.DataFrame(standings_2025_data)

    conf_choice = st.radio(
        "Select View:",
        ["By Division", "AFC Overall", "NFC Overall"],
        horizontal=True,
    )

    if conf_choice == "By Division":
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("AFC Standings")
            for div in ["AFC East", "AFC North", "AFC South", "AFC West"]:
                st.write(f"**{div}**")
                sub_df = df_2025[df_2025["Division"] == div][
                    ["Team", "W", "L", "T", "PCT", "Playoff"]
                ]
                st.dataframe(
                    sub_df,
                    hide_index=True,
                    use_container_width=True,
                    column_config={"PCT": st.column_config.NumberColumn(format="%.3f")},
                )

        with col2:
            st.subheader("NFC Standings")
            for div in ["NFC East", "NFC North", "NFC South", "NFC West"]:
                st.write(f"**{div}**")
                sub_df = df_2025[df_2025["Division"] == div][
                    ["Team", "W", "L", "T", "PCT", "Playoff"]
                ]
                st.dataframe(
                    sub_df,
                    hide_index=True,
                    use_container_width=True,
                    column_config={"PCT": st.column_config.NumberColumn(format="%.3f")},
                )
                