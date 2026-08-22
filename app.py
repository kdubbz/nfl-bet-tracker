# Check if current leg is a Touchdown metric
is_td_leg = "touchdown" in leg['stat'] or leg['stat'].endswith("_tds")

# Calculations
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
        # Custom display for TD legs only
        st.metric(
            label="TDs Remaining", 
            value=f"{units_remaining:,.1f}", 
            delta=f"{games_remaining} games left"
        )
    else:
        # Default display for yardage legs
        st.metric(
            label="Needed / Game", 
            value=f"{needed_per_game:.1f}", 
            delta=f"{games_remaining} games left"
        )

# Progress Bar display
progress_label = f"{pct_complete*100:.1f}% Completed ({units_remaining:,.1f} {stat_name.lower()} remaining)"
st.progress(pct_complete, text=progress_label)