"""
Streamlit app — League Rain‑Reduction Calculator
------------------------------------------------
Calculate the revised par and winning targets for the second innings under
Rule L 8 (l) iv of the HCL Playing Conditions.

How to run locally:
    streamlit run rain_reduction_calculator.py
"""

import math
import streamlit as st

st.set_page_config(page_title="HCL Rain‑Reduction Calculator", page_icon="🌧️")

st.title("🌧️ HCL Rain‑Reduction Calculator")

st.markdown(
    """Enter the first‑innings score and the total **cumulative** overs that will be
    lost from the second innings. The app applies the league rule: each over lost
    knocks two‑thirds of the required run‑rate off the target and the result is
    rounded **up** to the next whole run.
    """
)

# --- Inputs ------------------------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    first_innings_score = st.number_input(
        "First‑innings score (runs)", min_value=0, max_value=500, value=180, step=1
    )

with col2:
    overs_lost = st.number_input(
        "Overs lost from the chase", min_value=0, max_value=20, value=5, step=1,
        help="The league allows a maximum of 20 overs to be deducted; at least 25 overs must remain for the chase."
    )

# Constants
TOTAL_OVERS = 45  # league standard
MAX_OVERS_LOST = 20
MIN_OVERS_LEFT = 25

# --- Validation --------------------------------------------------------------

if overs_lost > MAX_OVERS_LOST:
    st.error("Overs lost cannot exceed 20 — league minimum chase is 25 overs.")
    st.stop()

overs_left = TOTAL_OVERS - overs_lost
if overs_left < MIN_OVERS_LEFT:
    st.error("At least 25 overs must remain for the chase.")
    st.stop()

# --- Calculation -------------------------------------------------------------

initial_rpo = (first_innings_score + 1) / TOTAL_OVERS  # required rate at start

deduction = overs_lost * 0.66 * initial_rpo

new_par_score_exact = first_innings_score - deduction
new_par_score = math.ceil(new_par_score_exact)

target_to_win = new_par_score + 1

# --- Display -----------------------------------------------------------------

st.subheader("Revised Target")

st.write(f"**Overs available to chasing side:** {overs_left} overs")

st.metric("Par / tie score", f"{new_par_score} runs")

st.metric("Target to win", f"{target_to_win} runs")

with st.expander("See the maths", expanded=False):
    st.write(
        f"Initial required run‑rate = (\n(First‑innings score + 1) ÷ {TOTAL_OVERS}\n) = {initial_rpo:.2f} rpo"
    )
    st.write(
        f"Runs deducted = OversLost × 0.66 × Initial RPO\n= {overs_lost} × 0.66 × {initial_rpo:.2f} = {deduction:.2f}"
    )
    st.write(
        f"Revised par =  {first_innings_score} – {deduction:.2f} = {new_par_score_exact:.2f} → round **up** → {new_par_score}"
    )

st.caption("HCL Rule L 8 (l) iv: calculations for revised targets are rounded up to the nearest whole number.")
