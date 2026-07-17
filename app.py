import streamlit as st
import pandas as pd
import nflreadpy as nfl

# Set page configuration for mobile-first layout
st.set_page_config(page_title="NFL Bet Portfolio", layout="centered")

# --- CUSTOM CSS FOR MODERN BORDERS ---
# This injects a high-end glowing border style to make your parlay container pop
st.html("""
<style>
.st-key-parlay-card {
    border: 2px solid #31333F !important;
    border-radius: 12px !important;
    padding: 20px !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
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

# --- STAT LABEL HELPER ---
# Converts raw API stat names into clean, readable display titles
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
        "title": "The Triple-Threat Over",
        "wager": "BONUS BET",
        "payout": "$148.94",
        "legs": [
            {"name": "Rome Odunze", "db_name": "R.Odunze", "stat": "receiving_yards", "line": 799.5, "type": "player", "2025_actual": 661.0, 
             "narrative": "Requires clearing **799.5 receiving yards** (averaging 47.1 yards/game over a 17-game season). After a highly efficient 661-yard rookie campaign playing inside a heavy target squeeze, Year 2 wide receiver leaps are mathematically the sharpest in gridiron analytics. With Caleb Williams maturing and an elevated snap share floor, clearing this target is a premium baseline expectation."},
            {"name": "Josh Allen", "db_name": "J.Allen", "stat": "passing_yards", "line": 3549.5, "type": "player", "2025_actual": 3668.0, 
             "narrative": "Requires clearing **3,549.5 passing yards** (averaging 208.8 yards/game). Allen cleared this line in 2025 with 3,668 yards despite a highly transitional Bills passing tree. This line heavily discounts his historical volume floor, as Allen has cleared 4,100 yards in four of his last six seasons."},
            {"name": "Kyren Williams", "db_name": "K.Williams", "stat": "rushing_yards", "line": 999.5, "type": "player", "2025_actual": 1252.0, 
             "narrative": "Requires clearing **999.5 rushing yards** (averaging 58.8 yards/game). Williams is the engine of Sean McVay's highly structural run-blocking hierarchy, smashing for 1,252 yards in 2025 at a clean 4.8 YPC. While Blake Corum acts as a luxury spell, high-value usage in neutral scripts makes this target ultra-safe."}
        ]
    },
    {
        "id": 1,
        "title": "Franchise Aerial & Mobile Engine",
        "wager": "BONUS BET",
        "payout": "$39.53",
        "legs": [
            {"name": "Jordan Love", "db_name": "J.Love", "stat": "passing_yards", "line": 3500.0, "type": "player", "2025_actual": 3381.0, 
             "narrative": "Requires clearing **3,500.0 passing yards** (averaging 205.9 yards/game). Love maintained an elite passing grade in 2025, throwing for 3,381 yards despite variable weapon availability. With full target continuity in Green Bay's deeply integrated aerial packages, 3,500 yards is well within his efficiency baseline."},
            {"name": "Drake Maye", "db_name": "D.Maye", "stat": "rushing_touchdowns", "line": 5.0, "type": "player", "2025_actual": 4.0, 
             "narrative": "Requires reaching **5 rushing touchdowns** (needs 5 to push, 6 to win). Maye logged 4 rushing scores in 2025 alongside 450 rushing yards. Alex Van Pelt’s offensive architecture actively utilizes designed heavy QB read-options inside the red zone, guaranteeing Maye the high-value touches inside the 10-yard line required to clear this mark."}
        ]
    },
    {
        "id": 2,
        "title": "Elite High-Volume Touchdown Slate",
        "wager": "BONUS BET",
        "payout": "$141.23",
        "legs": [
            {"name": "Aaron Rodgers", "db_name": "A.Rodgers", "stat": "passing_touchdowns", "line": 21.5, "type": "player", "2025_actual": 24.0, 
             "narrative": "Requires clearing **21.5 passing touchdowns** (needs 22 scores, averaging 1.3 per game). Rodgers showed remarkable red-zone efficiency with 24 passing scores in 2025. His touchdown percentage floor is historically steady (4.8% in 2025), making 22 passing scores a standard business expectation for his operational style."},
            {"name": "George Pickens", "db_name": "G.Pickens", "stat": "receiving_touchdowns", "line": 6.5, "type": "player", "2025_actual": 9.0, 
             "narrative": "Requires clearing **6.5 receiving touchdowns** (needs 7 scores). Operating in an explosive offense, Pickens racked up 1,429 receiving yards and 9 touchdowns in 2025. His dynamic contested-catch ability yields premium end-zone looks, making this regression-based line massive value."},
            {"name": "Jonathan Taylor", "db_name": "J.Taylor", "stat": "rushing_touchdowns", "line": 11.5, "type": "player", "2025_actual": 18.0, 
             "narrative": "Requires clearing **11.5 rushing touchdowns** (needs 12 scores). Taylor completely dominated as the league's top-tier fantasy back with a massive 18 rushing touchdowns in 2025. Shane Steichen's inside-zone scheme funnels high-percentage carries straight to Taylor inside the red zone, making 12 scores highly anchored by his usage."}
        ]
    },
    {
        "id": 3,
        "title": "Heavy Divisional Heavyweights",
        "wager": "$10.00",
        "payout": "$40.19",
        "legs": [
            {"name": "Baltimore Ravens", "type": "division", "division": "AFC North", "target": "1st Place", "2025_result": "8-9 Regular Season Record", 
             "narrative": "The Ravens field the most multi-dimensional run offense in modern football history. To surpass their 2025 record of **8-9** and win the division, Todd Monken must maximize dynamic schematics and leverage Baltimore's elite defensive efficiency to grind out AFC North wins over high-variance rivals."},
            {"name": "Philadelphia Eagles", "type": "division", "division": "NFC East", "target": "1st Place", "2025_result": "11-6 Regular Season Record", 
             "narrative": "The Eagles took the NFC East crown with an **11-6** record in 2025. Philadelphia's front office maintains the most premium trenches in the division. With massive systemic advantages over transitional division rivals (Cowboys: 7-9-1, Commanders: 5-12, Giants: 4-13), the path to a back-to-back crown is highly secure."}
        ]
    },
    {
        "id": 4,
        "title": "Precision Divisional Contenders",
        "wager": "$5.00",
        "payout": "$54.33",
        "legs": [
            {"name": "Green Bay Packers", "type": "division", "division": "NFC North", "target": "1st Place", "2025_result": "9-7-1 Regular Season Record", 
             "narrative": "Matt LaFleur’s creative offensive spacing completely unlocked the second half of the campaign, helping Green Bay secure a **9-7-1** wildcard finish in 2025. The Packers’ ascending collection of young playmakers represents the modern standard for offensive explosion, making them top favorites to knock off divisional rivals like the Bears (11-6), Lions (9-8), and Vikings (9-8)."},
            {"name": "Jacksonville Jaguars", "type": "division", "division": "AFC South", "target": "1st Place", "2025_result": "13-4 Regular Season Record", 
             "narrative": "Jacksonville dominated the AFC South in 2025 with an elite **13-4** record. With high-value draft capital reinforcing their defensive spacing and absolute stability inside their operational system, they possess the exact roster blueprint needed to keep the Texans (12-5), Colts (8-9), and Titans (3-14) at bay."}
        ]
    },
    {
        "id": 5,
        "title": "Mega Playoff Bracket Clean Sweep",
        "wager": "BONUS BET",
        "payout": "$166.35",
        "legs": [
            {"name": "Green Bay Packers", "type": "playoff", "target": "Make Playoffs", "2025_result": "9-7-1 Regular Season Record", 
             "narrative": "The Packers executed an elite developmental curve under Jordan Love to grab a wildcard spot in 2025 at **9-7-1**. This young, cheap, and highly talented roster is perfectly primed to retain a steady wildcard baseline at absolute minimum."},
            {"name": "Buffalo Bills", "type": "playoff", "target": "Make Playoffs", "2025_result": "12-5 Regular Season Record", 
             "narrative": "Buffalo cruised to a **12-5** record in 2025. As long as Josh Allen is under center, Buffalo’s baseline structural floor guarantees a deep post-season push. The highly efficient vertical scheme ensures a massive win-floor projection independent of roster turnover."},
            {"name": "Kansas City Chiefs", "type": "playoff", "target": "Make Playoffs", "2025_result": "6-11 Regular Season Record", 
             "narrative": "The standard metric lock of modern football analytics. Despite a transitional **6-11** rebuilding regular season in 2025, Andy Reid and Patrick Mahomes' structural playoff blueprint makes calculating anything less than a post-season ticket entirely mathematically invalid."},
            {"name": "Baltimore Ravens", "type": "playoff", "target": "Make Playoffs", "2025_result": "8-9 Regular Season Record", 
             "narrative": "Following an **8-9** run in 2025, the Ravens are built entirely on consistent regular-season defensive structures and continuous ground dominance. They possess a top-tier consistency floor that minimizes variable volatility and secures wildcard contention."},
            {"name": "Los Angeles Rams", "type": "playoff", "target": "Make Playoffs", "2025_result": "12-5 Regular Season Record", 
             "narrative": "McVay’s hyper-efficient zone schemes cruised to a strong **12-5** record in 2025. Matthew Stafford's structural processing skill set combined with high-percentage skill weapons locks in a very premium NFC playoff floor."},
            {"name": "Philadelphia Eagles", "type": "playoff", "target": "Make Playoffs", "2025_result": "11-6 Regular Season Record", 
             "narrative": "An **11-6** foundational output in 2025 underscores a highly premium roster footprint. Built around elite inside line frameworks and premium offensive weapon arrays, securing a consecutive post-season berth represents a clear baseline hurdle."}
        ]
    }
]

# --- INSTAGRAM-STYLE CAROUSEL STATE ---
if "parlay_index" not in st.session_state:
    st.session_state.parlay_index = 0

def prev_slide():
    if st.session_state.parlay_index > 0:
        st.session_state.parlay_index -= 1

def next_slide():
    if st.session_state.parlay_index < len(PARLAYS) - 1:
        st.session_state.parlay_index += 1

# Extract currently selected parlay based on scroll state
idx = st.session_state.parlay_index
current_parlay = PARLAYS[idx]

# Load API stats dataframe
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
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"**Target Objective:** `{leg.get('target', leg.get('division'))}`")
                with c2:
                    st.markdown(f"**2025 Structural Context:** `{leg['2025_result']}`")
            
            st.markdown(leg['narrative'])
            st.markdown("---")

# =========================================================
# 📊 VIEW 2: 2026 LIVE TRACK
# =========================================================
else:
    st.header("📊 Active 2026 Parlay Progress Tracker")
    st.info("ℹ️ Note: Live statistics will refresh automatically throughout the course of the season once games begin.")
    
    with st.container(border=True, key="parlay-card"):
        st.subheader(f"⚡ {current_parlay['title']}")
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"**Wager:** `{current_parlay['wager']}`")
        with col_b:
            st.markdown(f"**Est. Payout:** `{current_parlay['payout']}`")
        st.divider()
        
        for leg in current_parlay['legs']:
            st.markdown(f"##### {leg['name']}")
            
            if leg['type'] == 'player':
                current_total = 0.0
                if not stats_df.empty and 'player_name' in stats_df.columns:
                    db_name = leg['db_name'].replace(" ", "")
                    player_data = stats_df[stats_df['player_name'] == db_name]
                    if not player_data.empty and leg['stat'] in stats_df.columns:
                        current_total = player_data[leg['stat']].sum()
                
                pct_complete = min(float(current_total / leg['line']), 1.0) if leg['line'] > 0 else 0.0
                stat_name = get_stat_label(leg['stat'])
                
                # Single metrics row displaying only Current Progress vs Goal with precise context
                c1, c2 = st.columns(2)
                with c1:
                    st.metric(label=f"Current {stat_name}", value=f"{current_total:,.1f}")
                with c2:
                    st.metric(label=f"Goal {stat_name}", value=f"{leg['line']:,}")
                    
                st.progress(pct_complete, text=f"{pct_complete*100:.1f}% of {stat_name} Completed")
            
            else:
                c1, c2 = st.columns([2, 1])
                with c1:
                    st.markdown(f"🎯 Objective: **{leg.get('target', 'Win Division')}**")
                with c2:
                    st.markdown("Status: `Pending` ⏳")
            st.markdown(leg['narrative'])
            st.markdown("<br>", unsafe_allow_html=True)

# --- DYNAMIC BOTTOM NAVIGATION ---
st.write("---")
# Build column space depending on if buttons should be hidden
if idx == 0:
    # First parlay: Hide "Previous" by using an empty spacer column
    col_prev, col_indicator, col_next = st.columns([1, 2, 1])
    with col_indicator:
        st.markdown(f"<h4 style='text-align: center; margin-top: 5px;'>Parlay {idx + 1} of {len(PARLAYS)}</h4>", unsafe_allow_html=True)
    with col_next:
        st.button("Next ▶", on_click=next_slide, use_container_width=True)
elif idx == len(PARLAYS) - 1:
    # Last parlay: Hide "Next" by using an empty spacer column
    col_prev, col_indicator, col_next = st.columns([1, 2, 1])
    with col_prev:
        st.button("◀ Previous", on_click=prev_slide, use_container_width=True)
    with col_indicator:
        st.markdown(f"<h4 style='text-align: center; margin-top: 5px;'>Parlay {idx + 1} of {len(PARLAYS)}</h4>", unsafe_allow_html=True)
else:
    # Middle parlays: Render both buttons
    col_prev, col_indicator, col_next = st.columns([1, 2, 1])
    with col_prev:
        st.button("◀ Previous", on_click=prev_slide, use_container_width=True)
    with col_indicator:
        st.markdown(f"<h4 style='text-align: center; margin-top: 5px;'>Parlay {idx + 1} of {len(PARLAYS)}</h4>", unsafe_allow_html=True)
    with col_next:
        st.button("Next ▶", on_click=next_slide, use_container_width=True)
st.write("---")