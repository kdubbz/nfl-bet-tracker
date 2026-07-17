import streamlit as st
import pandas as pd
import nflreadpy as nfl

# Set page configuration for mobile-first layout
st.set_page_config(page_title="Premium Bet Portfolio", layout="centered")

# --- DATA FETCHING ---
@st.cache_data(ttl=86400)
def load_nfl_data(year):
    try:
        raw_stats = nfl.load_player_stats([year])
        return raw_stats.to_pandas()
    except Exception:
        return pd.DataFrame()

# --- TITLE ---
st.title("🏈 My Premium NFL Bet Portfolio")

# --- SEASON TOGGLE ---
VIEW_MODE = st.radio(
    "Select View Mode:",
    options=["🔬 2025 Research & Baselines", "📊 Live 2026 Tracking Tracker"],
    horizontal=True,
    help="Toggle between deep metric baselines and live 2026 tracking grids."
)

# --- PORTFOLIO DEFINITIONS ---
PARLAYS = [
    {
        "id": "parlay_1",
        "title": "Leg 1: The Triple-Threat Over",
        "wager": "BONUS BET",
        "payout": "$148.94",
        "legs": [
            {"name": "Rome Odunze", "db_name": "R.Odunze", "stat": "receiving_yards", "line": 799.5, "type": "player", "2025_actual": 661.0, 
             "narrative": "Efficient 661-yard rookie profile playing inside a heavy target squeeze. Year 2 WR leaps are mathematically the sharpest in gridiron analytics. With Caleb Williams maturing out of raw rookie mechanics and an elevated snap share floor, clearing 47.1 yards per game is a premium baseline expectation."},
            {"name": "Josh Allen", "db_name": "J.Allen", "stat": "passing_yards", "line": 3549.5, "type": "player", "2025_actual": 3668.0, 
             "narrative": "Cleared this line inside a highly transitionary year for the Bills passing tree in 2025 (3,668 yards). Line setter heavily discounts his historical volume floor; Allen has cleared 4,100 yards in 4 out of the last 6 seasons. Requires just 208.8 passing yards/game inside a highly dynamic, vertical offense."},
            {"name": "Kyren Williams", "db_name": "K.Williams", "stat": "rushing_yards", "line": 999.5, "type": "player", "2025_actual": 1252.0, 
             "narrative": "Engine of Sean McVay's highly structural run-blocking hierarchy, which posted elite rushing success rates. Smashed for 1,252 yards in 2025 at a clean 4.8 YPC. While Blake Corum acts as a luxury spell, the Rams regular run-heavy neutral scripts guarantee high-value usage. A healthy 58.8 yards/game target is ultra-safe."}
        ]
    },
    {
        "id": "parlay_2",
        "title": "Leg 2: Franchise Aerial & Mobile Engine",
        "wager": "BONUS BET",
        "payout": "$39.53",
        "legs": [
            {"name": "Jordan Love", "db_name": "J.Love", "stat": "passing_yards", "line": 3500.0, "type": "player", "2025_actual": 3381.0, 
             "narrative": "Love maintained an elite passing grade in 2025 (88.7 passing grade via PFF, 3rd in NFL). Threw for 3,381 yards despite variable weapon availability. Green Bay's deeply integrated aerial packages run natively through his arm, making 3,500 yards well within his regular efficiency range, especially with full target continuity."},
            {"name": "Drake Maye", "db_name": "D.Maye", "stat": "rushing_touchdowns", "line": 5.0, "type": "player", "2025_actual": 4.0, 
             "narrative": "Boasts a highly elite rushing floor, logging 450 yards and 4 rushing scores in 2025. Alex Van Pelt’s offensive architecture actively utilizes designed heavy QB read-options inside the red zone. With unmatched high-value usage inside the 10-yard line, converting 5 scores on the ground is highly aligned with his athletic deployment."}
        ]
    },
    {
        "id": "parlay_3",
        "title": "Leg 3: Elite High-Volume Touchdown Slate",
        "wager": "BONUS BET",
        "payout": "$141.23",
        "legs": [
            {"name": "Aaron Rodgers", "db_name": "A.Rodgers", "stat": "passing_touchdowns", "line": 21.5, "type": "player", "2025_actual": 24.0, 
             "narrative": "Showed remarkable red-zone efficiency with 24 passing scores in 2025 inside a hard-nosed Pittsburgh landscape. His touchdown percentage floor is historically steady (4.8% in 2025). The target distribution mechanics mean clearing a low threshold of 22 passing scores remains standard business for his operational style."},
            {"name": "George Pickens", "db_name": "G.Pickens", "stat": "receiving_touchdowns", "line": 6.5, "type": "player", "2025_actual": 9.0, 
             "narrative": "Exploded inside the Dallas offense, racking up 1,429 receiving yards and 9 touchdowns in 2025 (ranking 6th among all WRs). Operating out of a highly explosive vertical system, his dynamic contested-catch ability yields premium end-zone targets. Line regression value here is massive."},
            {"name": "Jonathan Taylor", "db_name": "J.Taylor", "stat": "rushing_touchdowns", "line": 11.5, "type": "player", "2025_actual": 18.0, 
             "narrative": "The #1 overall fantasy running back in 2025, completely dominating with a massive 18 rushing touchdowns. Shane Steichen's inside-zone scheme inside the red zone funnels high-percentage carries straight to Taylor. Barring extreme backfield deviations, clearing 12 scores is completely anchored by his usage."}
        ]
    },
    {
        "id": "parlay_4",
        "title": "Leg 4: Heavy Divisional Heavyweights",
        "wager": "$10.00",
        "payout": "$40.19",
        "legs": [
            {"name": "Baltimore Ravens", "type": "division", "division": "AFC North", "target": "1st Place", "2025_result": "Contender", 
             "narrative": "The Ravens field the most multi-dimensional run offense in modern football history. With Todd Monken maximizing dynamic schematics and an elite defensive efficiency anchor, Baltimore retains the physical advantage required to grind out the division crown over high-variance rivals."},
            {"name": "Philadelphia Eagles", "type": "division", "division": "NFC East", "target": "1st Place", "2025_result": "11-6 (Div Winner)", 
             "narrative": "Secured the division at 11-6 in 2025. The Eagles' front office maintains the most premium trenches inside the NFC East. With massive systemic advantages over transitional division rivals, the path to a back-to-back crown is highly backed by positional efficiency mapping."}
        ]
    },
    {
        "id": "parlay_5",
        "title": "Leg 5: Precision Divisional Contenders",
        "wager": "$5.00",
        "payout": "$54.33",
        "legs": [
            {"name": "Green Bay Packers", "type": "division", "division": "NFC North", "target": "1st Place", "2025_result": "9-7-1 (Wildcard)", 
             "narrative": "Matt LaFleur’s creative offensive spacing completely unlocked the second half of their campaign. Green Bay’s deep, ascending collection of young weapon networks represents the modern standard for offensive explosion, making them top favorites to knock off standard division architectures."},
            {"name": "Jacksonville Jaguars", "type": "division", "division": "AFC South", "target": "1st Place", "2025_result": "Contender", 
             "narrative": "The AFC South remains ripe for structural breakout. With high-value draft capital reinforcing defensive spacing and stability inside their operational system, Jacksonville possesses the exact high-value roster blueprint needed to vault ahead and claim the divisional title."}
        ]
    },
    {
        "id": "parlay_6",
        "title": "Leg 6: Mega Playoff Bracket Clean Sweep",
        "wager": "BONUS BET",
        "payout": "$166.35",
        "legs": [
            {"name": "Green Bay Packers", "type": "playoff", "target": "Make Playoffs", "2025_result": "Made Playoffs", "narrative": "Maintained an elite developmental curve under Jordan Love, executing high-value passing matrices. Roster configuration is young, locked into cheap deals, and perfectly primed to retain a steady wildcard baseline at absolute minimum."},
            {"name": "Buffalo Bills", "type": "playoff", "target": "Make Playoffs", "2025_result": "Made Playoffs", "narrative": "As long as Josh Allen is under center, Buffalo’s baseline structural floor guarantees a post-season push. The highly efficient vertical scheme ensures a massive win-floor projection independent of high roster turnover."},
            {"name": "Kansas City Chiefs", "type": "playoff", "target": "Make Playoffs", "2025_result": "Made Playoffs", "narrative": "The standard metric lock of modern football analytics. Andy Reid and Patrick Mahomes' structural playoff blueprint makes calculating anything less than a post-season ticket entirely mathematically invalid."},
            {"name": "Baltimore Ravens", "type": "playoff", "target": "Make Playoffs", "2025_result": "Made Playoffs", "narrative": "Built completely on consistent regular-season destruction through high-efficiency defensive structures and continuous ground dominance. Possess a top-tier consistency floor that minimizes variable volatility."},
            {"name": "Los Angeles Rams", "type": "playoff", "target": "Make Playoffs", "2025_result": "Made Playoffs (12-5)", "narrative": "McVay’s hyper-efficient zone schemes cruised to a strong 12-5 record in 2025. Matthew Stafford's structural processing skill set combined with high-percentage skill weapons locks in a very premium NFC floor."},
            {"name": "Philadelphia Eagles", "type": "playoff", "target": "Make Playoffs", "2025_result": "Made Playoffs (11-6)", "narrative": "An 11-6 foundational output in 2025 underscores a highly premium roster footprint. Built around elite inside line frameworks and premium offensive weapon arrays, securing a post-season berth represents a clear baseline hurdle."}
        ]
    }
]

# --- LOAD DATA PER SELECTION ---
stats_df = load_nfl_data(2025 if "2025" in VIEW_MODE else 2026)
live_active = not stats_df.empty if "2026" in VIEW_MODE else True

# =========================================================
# 🔬 VIEW 1: 2025 RESEARCH & BASELINES
# =========================================================
if "2025" in VIEW_MODE:
    st.header("🔬 Analytical Research & Baseline Metrics")
    st.write("Deep statistical analysis, historical inputs, and structural rationales behind every wager.")
    
    for parlay in PARLAYS:
        with st.container(border=True):
            # Header block with precise bet metrics
            st.subheader(f"⚡ {parlay['title']}")
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f"**Wager:** `{parlay['wager']}`")
            with col_b:
                st.markdown(f"**Est. Payout:** `{parlay['payout']}`")
            st.divider()
            
            # Print details per leg inside the container box
            for leg in parlay['legs']:
                st.markdown(f"#### 🎯 {leg['name']}")
                
                if leg['type'] == 'player':
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.metric(label="2026 Target Line", value=f"{leg['line']:,}")
                    with c2:
                        db_name = leg['db_name'].replace(" ", "")
                        api_stat = 0
                        if not stats_df.empty and 'player_name' in stats_df.columns:
                            player_data = stats_df[stats_df['player_name'] == db_name]
                            if not player_data.empty and leg['stat'] in stats_df.columns:
                                api_stat = player_data[leg['stat']].sum()
                        
                        display_val = api_stat if api_stat > 0 else leg['2025_actual']
                        st.metric(label="2025 Baseline", value=f"{display_val:,.0f}")
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
    if not live_active:
        st.warning("🟡 Live regular season statistics are not active yet. Displaying simulated portfolio tracking.")
        
    for parlay in PARLAYS:
        with st.container(border=True):
            st.subheader(f"⚡ {parlay['title']}")
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f"**Wager:** `{parlay['wager']}`")
            with col_b:
                st.markdown(f"**Est. Payout:** `{parlay['payout']}`")
            st.divider()
            
            # Compute leg data and display progress inside the card
            for leg in parlay['legs']:
                st.markdown(f"##### {leg['name']}")
                
                if leg['type'] == 'player':
                    current_total = 0.0
                    if not stats_df.empty and 'player_name' in stats_df.columns:
                        db_name = leg['db_name'].replace(" ", "")
                        player_data = stats_df[stats_df['player_name'] == db_name]
                        if not player_data.empty and leg['stat'] in stats_df.columns:
                            current_total = player_data[leg['stat']].sum()
                    elif not live_active:
                        # Clean placeholder simulations for display
                        current_total = leg['2025_actual'] * 0.05
                    
                    pct_complete = min(float(current_total / leg['line']), 1.0) if leg['line'] > 0 else 0.0
                    remaining = max(leg['line'] - current_total, 0)
                    
                    c1, c2 = st.columns(2)
                    with c1:
                        st.metric(label="Current 2026 Total", value=f"{current_total:,.1f}")
                    with c2:
                        if remaining > 0:
                            st.metric(label="Yards to Cover", value=f"{remaining:,.1f}")
                        else:
                            st.metric(label="Leg Status", value="🎉 COVERED!")
                    st.progress(pct_complete, text=f"{pct_complete*100:.1f}% of {leg['line']:,} Target completed")
                
                else:
                    # Division / Playoff tracking blocks inside the parlay container
                    c1, c2 = st.columns([2, 1])
                    with c1:
                        st.markdown(f"🎯 Objective: **{leg.get('target', 'Win Division')}**")
                    with c2:
                        st.markdown("Status: `Pending` ⏳")
                st.markdown("<br>", unsafe_allowed_html=True)