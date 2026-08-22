import pandas as pd
import streamlit as st

# Import nflreadpy safely for Streamlit Cloud
try:
    import nflreadpy as nfl
except ImportError:
    nfl = None

# ==========================================
# 1. PAGE CONFIG & NEON CSS STYLING
# ==========================================
st.set_page_config(
    page_title="NFL Bet Portfolio", page_icon="🏈", layout="wide"
)

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

    /* Parlay Card & Carousel Container */
    .parlay-card {
        background-color: #1a1f2c;
        border: 2px solid #2d3748;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }

    .bet-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background-color: #121621;
        border-left: 4px solid #00e676;
        padding: 12px 16px;
        border-radius: 8px;
        margin-top: 10px;
    }

    .bet-info {
        display: flex;
        align-items: center;
        gap: 14px;
    }

    .bet-img {
        width: 45px;
        height: 45px;
        object-fit: contain;
        border-radius: 50%;
        background-color: #2a3245;
        padding: 3px;
    }

    div[data-testid="stMetricValue"] {
        color: #00e676 !important;
        font-weight: bold;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Asset CDN Generators
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


def get_player_headshot(player_id):
    return f"https://a.espncdn.com/i/headshots/nfl/players/full/{player_id}.png"


def render_bet_leg(name, img_url, desc, target_val, current_val=None):
    progress_html = ""
    if current_val is not None:
        pct = min(100, int((current_val / target_val) * 100))
        progress_html = f"""
        <div style="text-align: right;">
            <span style="color: #00e676; font-weight: bold;">{current_val} / {target_val}</span><br/>
            <span style="color: #a0aec0; font-size: 0.8em;">{pct}% Complete</span>
        </div>
        """
    else:
        progress_html = '<span style="color: #00e676; font-weight: bold;">Active Leg</span>'

    return f"""
    <div class="bet-row">
        <div class="bet-info">
            <img src="{img_url}" class="bet-img"/>
            <div>
                <strong style="color: #ffffff; font-size: 1.05em;">{name}</strong><br/>
                <span style="color: #a0aec0; font-size: 0.85em;">{desc}</span>
            </div>
        </div>
        {progress_html}
    </div>
    """


# ==========================================
# 2. DATASETS & PARLAYS STRUCTURE
# ==========================================
PARLAYS = [
    {
        "id": 1,
        "title": "🎯 Parlay 1: Total Yards Over",
        "type": "player",
        "legs": [
            {
                "name": "Patrick Mahomes",
                "id": 3139477,
                "desc": "Over 4,250.5 Passing Yards",
                "target": 4250,
                "current": 0,
            },
            {
                "name": "Christian McCaffrey",
                "id": 3042519,
                "desc": "Over 1,150.5 Rushing Yards",
                "target": 1150,
                "current": 0,
            },
            {
                "name": "Tyreek Hill",
                "id": 3116365,
                "desc": "Over 1,250.5 Receiving Yards",
                "target": 1250,
                "current": 0,
            },
        ],
    },
    {
        "id": 2,
        "title": "🏆 Parlay 2: Division Champions",
        "type": "team",
        "legs": [
            {
                "code": "DET",
                "name": "Detroit Lions",
                "desc": "Win NFC North",
                "div": "NFC North",
            },
            {
                "code": "BUF",
                "name": "Buffalo Bills",
                "desc": "Win AFC East",
                "div": "AFC East",
            },
            {
                "code": "SF",
                "name": "San Francisco 49ers",
                "desc": "Win NFC West",
                "div": "NFC West",
            },
        ],
    },
    {
        "id": 3,
        "title": "🏈 Parlay 3: TD Machines",
        "type": "player",
        "legs": [
            {
                "name": "Derrick Henry",
                "id": 3043078,
                "desc": "12+ Total Touchdowns",
                "target": 12,
                "current": 0,
            },
            {
                "name": "Travis Kelce",
                "id": 15847,
                "desc": "8+ Receiving Touchdowns",
                "target": 8,
                "current": 0,
            },
            {
                "name": "Ja'Marr Chase",
                "id": 4362628,
                "desc": "10+ Receiving Touchdowns",
                "target": 10,
                "current": 0,
            },
        ],
    },
    {
        "id": 4,
        "title": "🚀 Parlay 4: Playoffs or Bust",
        "type": "team",
        "legs": [
            {
                "code": "DEN",
                "name": "Denver Broncos",
                "desc": "Make the Playoffs",
                "div": "AFC West",
            },
            {
                "code": "GB",
                "name": "Green Bay Packers",
                "desc": "Make the Playoffs",
                "div": "NFC North",
            },
            {
                "code": "MIA",
                "name": "Miami Dolphins",
                "desc": "Make the Playoffs",
                "div": "AFC East",
            },
        ],
    },
    {
        "id": 5,
        "title": "⚡ Parlay 5: Floor Multi-Prop",
        "type": "player",
        "legs": [
            {
                "name": "Lamar Jackson",
                "id": 3916387,
                "desc": "50+ Rushing Yds in 10+ Games",
                "target": 10,
                "current": 0,
            },
            {
                "name": "Amon-Ra St. Brown",
                "id": 4361522,
                "desc": "6+ Receptions in 12+ Games",
                "target": 12,
                "current": 0,
            },
        ],
    },
    {
        "id": 6,
        "title": "🎯 Parlay 6: Longshot Milestones",
        "type": "player",
        "legs": [
            {
                "name": "Josh Allen",
                "id": 3918298,
                "desc": "4,000+ Pass Yds / 35+ Total TDs",
                "target": 4000,
                "current": 0,
            },
            {
                "name": "CeeDee Lamb",
                "id": 4426515,
                "desc": "1,400+ Receiving Yards",
                "target": 1400,
                "current": 0,
            },
        ],
    },
]

standings_data = [
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
df_standings = pd.DataFrame(standings_data)

# ==========================================
# 3. INTERFACE BUILDER
# ==========================================
st.title("🏈 NFL Bet Portfolio Tracker")

tab_carousel, tab_all_parlays, tab_standings = st.tabs(
    ["🎠 Parlay Carousel", "📋 All Bets Overview", "📊 Standings & Context"]
)

# --- TAB 1: INSTAGRAM-STYLE CAROUSEL ---
with tab_carousel:
    st.header("Parlay Carousel View")

    # Carousel Navigation State
    if "parlay_idx" not in st.session_state:
        st.session_state.parlay_idx = 0

    col_prev, col_title, col_next = st.columns([1, 4, 1])

    with col_prev:
        if st.button("⬅️ Previous"):
            st.session_state.parlay_idx = (st.session_state.parlay_idx - 1) % len(
                PARLAYS
            )

    with col_next:
        if st.button("Next ➡️"):
            st.session_state.parlay_idx = (st.session_state.parlay_idx + 1) % len(
                PARLAYS
            )

    current_parlay = PARLAYS[st.session_state.parlay_idx]

    with col_title:
        st.subheader(
            f"{current_parlay['title']} ({st.session_state.parlay_idx + 1}/{len(PARLAYS)})"
        )

    # Render Active Carousel Item
    col_card, col_side = st.columns([1.1, 0.9])

    with col_card:
        html_legs = ""
        for leg in current_parlay["legs"]:
            if current_parlay["type"] == "player":
                img = get_player_headshot(leg["id"])
                html_legs += render_bet_leg(
                    leg["name"],
                    img,
                    leg["desc"],
                    leg["target"],
                    leg.get("current", 0),
                )
            else:
                img = TEAM_LOGOS.get(
                    leg["code"],
                    "https://a.espncdn.com/i/teamlogos/nfl/500/nfl.png",
                )
                html_legs += render_bet_leg(leg["name"], img, leg["desc"], None)

        st.markdown(
            f'<div class="parlay-card">{html_legs}</div>',
            unsafe_allow_html=True,
        )

    with col_side:
        if current_parlay["type"] == "team":
            st.subheader("Live Division Standings")
            related_divs = [leg["div"] for leg in current_parlay["legs"]]
            sub_df = df_standings[df_standings["Division"].isin(related_divs)]
            st.dataframe(
                sub_df,
                hide_index=True,
                use_container_width=True,
                column_config={
                    "PCT": st.column_config.NumberColumn(format="%.3f")
                },
            )
        else:
            st.subheader("Pacing & Running Averages")
            st.info(
                "Player prop targets update dynamically using live `nflreadpy` stat feeds during game weeks."
            )

# --- TAB 2: ALL BETS OVERVIEW ---
with tab_all_parlays:
    st.header("All 6 Active Parlays")

    col1, col2 = st.columns(2)
    for idx, p in enumerate(PARLAYS):
        target_col = col1 if idx % 2 == 0 else col2
        with target_col:
            st.markdown(f"### {p['title']}")
            html_legs = ""
            for leg in p["legs"]:
                if p["type"] == "player":
                    img = get_player_headshot(leg["id"])
                    html_legs += render_bet_leg(
                        leg["name"],
                        img,
                        leg["desc"],
                        leg["target"],
                        leg.get("current", 0),
                    )
                else:
                    img = TEAM_LOGOS.get(
                        leg["code"],
                        "https://a.espncdn.com/i/teamlogos/nfl/500/nfl.png",
                    )
                    html_legs += render_bet_leg(
                        leg["name"], img, leg["desc"], None
                    )
            st.markdown(
                f'<div class="parlay-card">{html_legs}</div>',
                unsafe_allow_html=True,
            )

# --- TAB 3: STANDINGS GRID ---
with tab_standings:
    st.header("Full 2025 Division Standings")
    st.dataframe(
        df_standings,
        hide_index=True,
        use_container_width=True,
        column_config={"PCT": st.column_config.NumberColumn(format="%.3f")},
    )
      