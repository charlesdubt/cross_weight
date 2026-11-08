import streamlit as st

st.set_page_config(
    page_title="Kart Cross Weight",
    page_icon="🏎️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------- Mobile-friendly styling ----------
st.markdown(
    """
    <style>
      /* Bigger touch targets and readable type on phones */
      html { font-size: 18px; }
      .block-container { padding-top: 1.2rem; padding-bottom: 3rem; max-width: 480px; }
      div[data-testid="stNumberInput"] input {
          font-size: 1.4rem !important;
          height: 3.2rem !important;
          text-align: center;
      }
      div[data-testid="stNumberInput"] button {
          height: 3.2rem !important;
          width: 2.6rem !important;
      }
      .big-result {
          font-size: 2.6rem;
          font-weight: 800;
          line-height: 1.1;
          text-align: center;
      }
      .result-label {
          font-size: 0.95rem;
          color: #888;
          text-align: center;
          text-transform: uppercase;
          letter-spacing: 0.08em;
      }
      .delta-ok   { color: #2ecc71; }
      .delta-bad  { color: #e74c3c; }
      .divider { border-top: 1px solid #444; margin: 1.2rem 0; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🏎️ Kart Cross Weight")

# ---------- Inputs ----------
unit = st.radio("Unit", ["lb", "kg"], horizontal=True)

c1, c2 = st.columns(2)
lf = c1.number_input(f"Front Left ({unit})", min_value=0.0, value=55.0, step=0.5, key="lf")
rf = c2.number_input(f"Front Right ({unit})", min_value=0.0, value=45.0, step=0.5, key="rf")
lr = c1.number_input(f"Rear Left ({unit})", min_value=0.0, value=57.0, step=0.5, key="lr")
rr = c2.number_input(f"Rear Right ({unit})", min_value=0.0, value=43.0, step=0.5, key="rr")

turn_dir = st.radio(
    "Cross weight pairs",
    ["LF + RR (right-hand track)", "RF + LR (left-hand track)"],
    horizontal=True,
)
target_cross = st.number_input("Target cross weight (%)", min_value=0.0, max_value=100.0, value=50.0, step=0.1)

# ---------- Calculations ----------
total = lf + rf + lr + rr

if total > 0:
    cross = (lf + rr) if "LF + RR" in turn_dir else (rf + lr)
    cross_pct = cross / total * 100.0

    front_pct = (lf + rf) / total * 100.0
    rear_pct = 100.0 - front_pct
    left_pct = (lf + lr) / total * 100.0
    right_pct = 100.0 - left_pct

    delta = cross_pct - target_cross

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ---- Cross weight (hero number) ----
    st.markdown('<p class="result-label">Cross Weight</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="big-result">{cross_pct:.1f}%</p>', unsafe_allow_html=True)
    delta_cls = "delta-ok" if abs(delta) <= 0.5 else "delta-bad"
    st.markdown(
        f'<p class="result-label {delta_cls}">{delta:+.1f}% vs target {target_cross:.1f}%</p>',
        unsafe_allow_html=True,
    )

    # ---- Ballast hint ----
    # Moving W from one corner to the diagonal-opposite pair changes cross by 2W/total*100.
    # Adding W to one corner of the active pair changes cross by W/total*100.
    if abs(delta) > 0.05:
        add_corner = "Front Left or Rear Right" if "LF + RR" in turn_dir else "Front Right or Rear Left"
        remove_corner = "Front Right or Rear Left" if "LF + RR" in turn_dir else "Front Left or Rear Right"
        add_w = abs(delta) / 100.0 * total
        move_w = add_w / 2.0
        direction = "Add" if delta < 0 else "Remove"
        st.info(
            f"**{direction} ~{add_w:.1f} {unit}** at **{add_corner}** "
            f"(or {direction.lower()} ~{move_w:.1f} {unit} from **{remove_corner}**). "
            f"Ballast moved between diagonal corners counts double."
        )

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ---- Bias breakdown ----
    st.subheader("Weight Bias")
    r1c1, r1c2 = st.columns(2)
    r1c1.metric("Front", f"{front_pct:.1f}%", f"{lf + rf:.1f} {unit}")
    r1c2.metric("Rear", f"{rear_pct:.1f}%", f"{lr + rr:.1f} {unit}")
    r2c1, r2c2 = st.columns(2)
    r2c1.metric("Left", f"{left_pct:.1f}%", f"{lf + lr:.1f} {unit}")
    r2c2.metric("Right", f"{right_pct:.1f}%", f"{rf + rr:.1f} {unit}")

    st.metric(f"Total weight", f"{total:.1f} {unit}")

    st.caption(
        "Tip: cross weight above 50% tightens the kart on corner entry for right-hand tracks; "
        "below 50% frees it up. Adjust in small steps and re-scale."
    )
else:
    st.warning("Enter all four corner weights to see results.")
