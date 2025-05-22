"""
Streamlit app — HCL Rain‑Reduction Calculator
--------------------------------------------
Calculate the revised par and winning targets for the second innings under
Rule L 8 (l) iv of the Hunters League Playing Conditions, **now with support
for a shortened first innings**.

How to run locally:
    streamlit run rain_reduction_calculator.py
"""

import math
import streamlit as st

st.set_page_config(page_title="HCL Rain‑Reduction Calculator", page_icon="🌧️")

st.title("🌧️ HCL Rain‑Reduction Calculator")

st.markdown(
    """Enter the first‑innings score, the number of overs the first innings was
    *actually* scheduled for after any mid‑innings reduction, and the
    cumulative overs subsequently lost from the second innings. The app applies
    the league rule: each over lopped off the chase deducts two‑thirds of the
    initial required run‑rate from the target, and the result is rounded **up**
    to the next whole run.
    
    **Remember**
      * League maximum reduction *during* the second innings is 20 overs.
      * The chase must always have at least 25 overs available.
    """
)

# ── Inputs ────────────────────────────────────────────────────────────────────

col1, col2, col3 = st.columns(3)

with col1:
    first_innings_score = st.number_input(
        "First‑innings score (runs)", min_value=0, max_value=500, value=180, step=1
    )

with col2:
    scheduled_overs = st.number_input(
        "Overs allocated to each side *after* first‑innings reduction",
        min_value=25,
        max_value=45,
        value=45,
        step=1,
        help="Both teams get the same allocation; league minimum is 25, normal is 45."
    )

with col3:
    overs_lost = st.number_input(
        "Overs lost from the chase",
        min_value=0,
        max_value=20,
        value=0,
        step=1,
        help="Cumulative loss during the second innings. League caps this at 20."
    )

# ── Validation ───────────────────────────────────────────────────────────────

if overs_lost > 20:
    st.error("Overs lost cannot exceed 20 — league maximum.")
    st.stop()

overs_left = scheduled_overs - overs_lost

if overs_left < 25:
    st.error(
        f"Overs left would be {overs_left}, below the 25‑over league minimum. Reduce 'overs lost' or increase 'scheduled overs'."
    )
    st.stop()

# ── Calculation ──────────────────────────────────────────────────────────────

initial_rpo = (first_innings_score + 1) / scheduled_overs  # required rate at start

deduction = overs_lost * 0.66 * initial_rpo

new_par_score_exact = first_innings_score - deduction
new_par_score = math.ceil(new_par_score_exact)

target_to_win = new_par_score + 1

# ── Display ──────────────────────────────────────────────────────────────────

st.subheader("Revised Target")

st.write(f"**Overs available to chasing side:** {overs_left} overs")

colA, colB = st.columns(2)
colA.metric("Par / tie score", f"{new_par_score} runs")
colB.metric("Target to win", f"{target_to_win} runs")

with st.expander("Show calculation", expanded=False):
    st.write(
        f"Initial required run‑rate = (({first_innings_score} + 1) ÷ {scheduled_overs}) = {initial_rpo:.2f} rpo"
    )
    st.write(
        f"Runs deducted = {overs_lost} × 0.66 × {initial_rpo:.2f} = {deduction:.2f}"
    )
    st.write(
        f"Revised par = {first_innings_score} – {deduction:.2f} = {new_par_score_exact:.2f} → round **up** → {new_par_score}"
    )

st.caption(
    "HCL Rule L 8 (l) iv: target is reduced by two‑thirds of the initial RPO for every over lost in the second innings; calculations round up to the nearest whole run."
)
