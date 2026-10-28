
import streamlit as st

st.set_page_config(
    page_title="NxtWave Growth Toolkit",
    page_icon="🚀",
    layout="wide",
)

# Campaign configuration
REGISTRATION_TARGET = 500
CAMPAIGN_BUDGET = 2000
CAMPAIGN_DURATION_DAYS = 7

st.title("🚀 NxtWave Growth Toolkit")
st.caption("Campus Ambassador & Referral Campaign Dashboard")

st.info(
    "Prototype mode: campaign metrics are placeholders until "
    "registration tracking is connected."
)

st.subheader("Campaign Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Registration Target",
        value=REGISTRATION_TARGET,
        help="Target for the seven-day growth challenge.",
    )

with col2:
    st.metric(
        label="Campaign Budget",
        value=f"₹{CAMPAIGN_BUDGET:,}",
        help="Total proposed campaign budget.",
    )

with col3:
    st.metric(
        label="Campaign Duration",
        value=f"{CAMPAIGN_DURATION_DAYS} days",
    )

st.divider()

st.subheader("Growth Strategy")

st.markdown(
    """
    - **Campus ambassadors:** Recruit student representatives to
      share the workshop with relevant final-year students.
    - **Referral tracking:** Attribute registrations to unique
      ambassador links or referral codes.
    - **Daily optimization:** Monitor registrations by campus,
      referral source, and day to identify what is working.
    """
)

st.warning(
    "No registrations have been collected yet. "
    "The dashboard does not claim that the 500-registration "
    "target has been achieved."
)

st.caption("NxtWave Growth Intern Challenge · Working prototype")
