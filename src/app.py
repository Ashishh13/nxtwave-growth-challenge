
import os

import streamlit as st

from src.ambassadors import register_ambassador
from src.analytics import get_campaign_analytics
from src.db import get_campaign_settings
from src.registrations import register_student


st.set_page_config(
    page_title="NxtWave Growth Toolkit",
    page_icon="🚀",
    layout="wide",
)

st.title("🚀 NxtWave Growth Toolkit")
st.caption("Campus Ambassador & Referral Campaign Dashboard")


# ---------------- CAMPAIGN SETTINGS ----------------

try:
    settings = get_campaign_settings()
except Exception as exc:
    st.error(
        f"Could not load campaign settings: "
        f"{type(exc).__name__}: {exc}"
    )
    st.stop()


st.header("Campaign Overview")

overview = st.columns(3)
overview[0].metric(
    "Registration Target",
    settings["registration_target"],
)
overview[1].metric(
    "Campaign Budget",
    f'₹{settings["budget_inr"]:,}',
)
overview[2].metric(
    "Campaign Duration",
    f'{settings["duration_days"]} days',
)

st.divider()


# ---------------- AMBASSADOR REGISTRATION ----------------

st.header("🎓 Campus Ambassador Registration")
st.write(
    "Register to receive a unique referral code "
    "for the workshop campaign."
)

with st.form("ambassador_registration_form"):
    ambassador_name = st.text_input(
        "Full name",
        key="ambassador_name",
    )
    ambassador_email = st.text_input(
        "Email address",
        key="ambassador_email",
    )
    ambassador_college = st.text_input(
        "College",
        key="ambassador_college",
    )

    ambassador_submitted = st.form_submit_button(
        "Register as Ambassador",
        use_container_width=True,
    )

if ambassador_submitted:
    try:
        ambassador = register_ambassador(
            full_name=ambassador_name,
            email=ambassador_email,
            college=ambassador_college,
        )

        st.success("Ambassador registered successfully!")
        st.write("Your unique referral code:")
        st.code(ambassador["referral_code"])
        st.caption(
            "Save this code to track registrations "
            "generated through your outreach."
        )

    except ValueError as exc:
        st.warning(str(exc))

    except Exception as exc:
        details = str(exc)

        for secret_name in ("SUPABASE_KEY", "SUPABASE_URL"):
            secret = os.getenv(secret_name, "")
            if secret:
                details = details.replace(secret, "[REDACTED]")

        st.error(
            f"Ambassador registration failed: "
            f"{type(exc).__name__}: {details}"
        )
        print(
            f"Ambassador registration error: "
            f"{type(exc).__name__}: {details}",
            flush=True,
        )

st.divider()


# ---------------- STUDENT WORKSHOP REGISTRATION ----------------

st.header("🤖 Workshop Registration")
st.subheader("Build Your First AI Project in 60 Minutes")

st.write(
    "Free online workshop for final-year engineering students. "
    "Register below to be counted toward the campaign target."
)

with st.form("student_registration_form"):
    student_name = st.text_input(
        "Student full name",
        key="student_name",
    )
    student_email = st.text_input(
        "Student email",
        key="student_email",
    )
    student_college = st.text_input(
        "Engineering college",
        key="student_college",
    )

    final_year = st.checkbox(
        "I am a final-year engineering student",
        key="student_final_year",
    )

    referral_code = st.text_input(
        "Ambassador referral code (optional)",
        placeholder="Example: ASHISH-7ZLKK6",
        key="student_referral_code",
    )

    student_submitted = st.form_submit_button(
        "Register for Free Workshop",
        use_container_width=True,
        type="primary",
    )

if student_submitted:
    try:
        register_student(
            full_name=student_name,
            email=student_email,
            college=student_college,
            is_final_year=final_year,
            referral_code=referral_code,
        )

        st.success(
            "Workshop registration successful! "
            "Your registration has been recorded."
        )

    except ValueError as exc:
        st.warning(str(exc))

    except Exception as exc:
        details = str(exc)

        for secret_name in ("SUPABASE_KEY", "SUPABASE_URL"):
            secret = os.getenv(secret_name, "")
            if secret:
                details = details.replace(secret, "[REDACTED]")

        st.error(
            f"Student registration failed: "
            f"{type(exc).__name__}: {details}"
        )
        print(
            f"Student registration error: "
            f"{type(exc).__name__}: {details}",
            flush=True,
        )

st.divider()


# ---------------- LIVE GROWTH DASHBOARD ----------------

st.header("📈 Live Growth Dashboard")
st.caption(
    "Live aggregate metrics from Supabase. "
    "Student names and email addresses are not shown here."
)

if st.button("🔄 Refresh analytics"):
    st.rerun()

try:
    analytics = get_campaign_analytics()

    total = int(analytics.get("total_registrations", 0))
    target = int(settings["registration_target"])
    remaining = max(target - total, 0)
    progress = min(total / target, 1.0) if target > 0 else 0.0

    metric_cols = st.columns(3)

    metric_cols[0].metric(
        "Registrations",
        total,
    )
    metric_cols[1].metric(
        "Still Needed",
        remaining,
    )
    metric_cols[2].metric(
        "Target Progress",
        f"{progress:.1%}",
    )

    st.progress(
        progress,
        text=f"{total} of {target} registrations",
    )

    if total >= target:
        st.success("Registration target reached!")
    else:
        st.info(
            f"{remaining} more registrations needed "
            "to reach the campaign goal."
        )

    # Daily registration chart
    st.subheader("📅 Daily Registrations")

    daily = analytics.get("daily_registrations", [])

    if daily:
        daily_sorted = sorted(
            daily,
            key=lambda item: item["date"],
        )

        st.bar_chart(
            data={
                "Date": [
                    item["date"] for item in daily_sorted
                ],
                "Registrations": [
                    int(item["count"]) for item in daily_sorted
                ],
            },
            x="Date",
            y="Registrations",
        )
    else:
        st.info("No registrations recorded yet.")

    left, right = st.columns(2)

    # Registrations by source
    with left:
        st.subheader("📊 Registrations by Source")

        sources = analytics.get("by_source", [])

        if sources:
            sources_sorted = sorted(
                sources,
                key=lambda item: item["count"],
                reverse=True,
            )

            st.bar_chart(
                data={
                    "Source": [
                        item["source"] for item in sources_sorted
                    ],
                    "Registrations": [
                        int(item["count"]) for item in sources_sorted
                    ],
                },
                x="Source",
                y="Registrations",
            )
        else:
            st.info(
                "Source data will appear after the first registration."
            )

    # Ambassador leaderboard
    with right:
        st.subheader("🏆 Ambassador Leaderboard")

        ambassadors = analytics.get("by_ambassador", [])

        if ambassadors:
            leaderboard = sorted(
                ambassadors,
                key=lambda item: item["registrations"],
                reverse=True,
            )

            leaderboard_rows = [
                {
                    "Ambassador": item["name"],
                    "College": item["college"],
                    "Referral Code": item["referral_code"],
                    "Registrations": int(item["registrations"]),
                }
                for item in leaderboard
            ]

            st.dataframe(
                leaderboard_rows,
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No ambassadors registered yet.")

except Exception as exc:
    details = str(exc)

    for secret_name in ("SUPABASE_KEY", "SUPABASE_URL"):
        secret = os.getenv(secret_name, "")
        if secret:
            details = details.replace(secret, "[REDACTED]")

    st.error(
        f"Could not load campaign analytics: "
        f"{type(exc).__name__}: {details}"
    )
    print(
        f"Campaign analytics error: "
        f"{type(exc).__name__}: {details}",
        flush=True,
    )


# ---------------- GROWTH STRATEGY ----------------

st.divider()
st.header("🎯 Growth Strategy")

st.markdown(
    """
    - **Campus ambassadors:** Recruit student representatives to reach relevant final-year engineering students.
    - **Referral tracking:** Attribute registrations to unique ambassador codes.
    - **Daily optimization:** Compare campus and referral performance to decide where to focus outreach.
    """
)

st.caption(
    "NxtWave Growth Intern Challenge · Working prototype · "
    "The registration target is a goal, not an achieved result."
)
