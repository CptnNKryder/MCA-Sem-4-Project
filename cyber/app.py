import streamlit as st
import pandas as pd
import time

from data import (
    get_vuln_df, TRAINING_MODULES, QUIZ_QUESTIONS,
    REPORTS, ACTIVITY_FEED
)
from utils import (
    risk_gauge, severity_bar, status_pie,
    cvss_radar, category_bar
)

# ─── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CyberSec Intern Program | Tinymart Global",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Global CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Hide default streamlit chrome */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0a1628;
    border-right: 1px solid rgba(0,212,255,0.15);
}

/* General text */
body, .stMarkdown { color: #e2e8f0; }

/* Metric cards */
[data-testid="stMetricValue"] { color: #00d4ff; font-size: 2rem !important; }
[data-testid="stMetricLabel"] { color: #94a3b8; }

/* Severity / status badges */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}
.critical { background: rgba(255,59,92,0.15);  color:#ff3b5c; border:1px solid rgba(255,59,92,0.3); }
.high     { background: rgba(255,140,0,0.15);  color:#ff8c00; border:1px solid rgba(255,140,0,0.3); }
.medium   { background: rgba(255,200,0,0.15);  color:#ffc800; border:1px solid rgba(255,200,0,0.3); }
.low      { background: rgba(0,255,136,0.15);  color:#00ff88; border:1px solid rgba(0,255,136,0.3); }
.open     { background: rgba(255,59,92,0.10);  color:#ff3b5c; border:1px solid rgba(255,59,92,0.25);}
.progress { background: rgba(255,140,0,0.10);  color:#ff8c00; border:1px solid rgba(255,140,0,0.25);}
.resolved { background: rgba(0,255,136,0.10);  color:#00ff88; border:1px solid rgba(0,255,136,0.25);}

/* Buttons */
.stButton > button {
    background: #00d4ff;
    color: #050c1a;
    border: none;
    font-weight: 700;
    border-radius: 8px;
}
.stButton > button:hover {
    background: #00b8d9;
    color: #050c1a;
}

/* Expander */
[data-testid="stExpander"] {
    background: #0d1f3c;
    border: 1px solid rgba(0,212,255,0.15);
    border-radius: 10px;
}

/* Quiz options */
div[data-baseweb="radio"] label {
    color: #e2e8f0 !important;
}

/* Data frame */
[data-testid="stDataFrame"] { border-radius: 10px; }

/* Divider */
hr { border-color: rgba(0,212,255,0.15); }
</style>
""", unsafe_allow_html=True)


# ─── Session state ───────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = {}


# ─── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔒 CyberSec Portal")
    st.caption("Tinymart Global Pvt. Ltd., Noida")
    st.divider()

    pages = {
        "Dashboard":   "📊",
        "Assessment":  "🔍",
        "Training":    "📚",
        "Reports":     "📄",
    }
    for name, icon in pages.items():
        if st.button(f"{icon}  {name}", key=f"nav_{name}", use_container_width=True):
            st.session_state.page = name

    st.divider()
    st.markdown("**👤 Nishchay Kumar**")
    st.caption("Security Intern · Enrolled 28/02/2026")


page = st.session_state.page


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 1 — DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
if page == "Dashboard":
    st.title("📊 Security Dashboard")
    st.caption("Enhancing Cybersecurity Measures in a Tech Intern Program — Tinymart Global Private Limited, Noida")
    st.divider()

    df = get_vuln_df()

    # KPI row
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Vulnerabilities", len(df))
    c2.metric("🔴 Critical", len(df[df["Severity"] == "Critical"]))
    c3.metric("🟠 High",     len(df[df["Severity"] == "High"]))
    c4.metric("🟡 Medium",   len(df[df["Severity"] == "Medium"]))
    c5.metric("✅ Resolved", len(df[df["Status"] == "Resolved"]))

    st.divider()

    # Charts row 1
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(risk_gauge(df), use_container_width=True)
    with col2:
        st.plotly_chart(severity_bar(df), use_container_width=True)

    # Charts row 2
    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(cvss_radar(df), use_container_width=True)
    with col4:
        st.plotly_chart(status_pie(df), use_container_width=True)

    st.divider()
    st.subheader("📡 Live Activity Feed")
    activity_df = pd.DataFrame(ACTIVITY_FEED)
    st.dataframe(activity_df, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 2 — SECURITY ASSESSMENT
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Assessment":
    st.title("🔍 Security Assessment")
    st.caption("Identify and track vulnerabilities within the Tech Intern Program infrastructure")
    st.divider()

    df = get_vuln_df()

    # Summary KPIs
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Critical", len(df[df["Severity"] == "Critical"]))
    c2.metric("High",     len(df[df["Severity"] == "High"]))
    c3.metric("Medium",   len(df[df["Severity"] == "Medium"]))
    c4.metric("Open",     len(df[df["Status"] == "Open"]))
    st.divider()

    # Run Scan
    col_btn, col_status = st.columns([1, 3])
    with col_btn:
        run_scan = st.button("▶ Run Security Scan", use_container_width=True)
    with col_status:
        if run_scan:
            with st.spinner("Scanning intern program portal..."):
                time.sleep(2)
            st.success(f"✅ Scan complete! {len(df)} vulnerabilities found. Risk Score: 62/100")

    st.divider()

    # Filters
    st.subheader("Vulnerability Register")
    col1, col2, col3 = st.columns(3)
    with col1:
        sev_filter = st.multiselect("Severity", df["Severity"].unique(), default=list(df["Severity"].unique()))
    with col2:
        stat_filter = st.multiselect("Status", df["Status"].unique(), default=list(df["Status"].unique()))
    with col3:
        cat_filter = st.multiselect("Category", df["Category"].unique(), default=list(df["Category"].unique()))

    filtered = df[
        df["Severity"].isin(sev_filter) &
        df["Status"].isin(stat_filter) &
        df["Category"].isin(cat_filter)
    ]

    st.caption(f"Showing {len(filtered)} of {len(df)} vulnerabilities")
    st.divider()

    # Vulnerability cards
    SEV_BADGE  = {"Critical": "critical", "High": "high", "Medium": "medium", "Low": "low"}
    STAT_BADGE = {"Open": "open", "In Progress": "progress", "Resolved": "resolved"}

    for _, row in filtered.iterrows():
        sev_cls  = SEV_BADGE.get(row["Severity"], "low")
        stat_cls = STAT_BADGE.get(row["Status"], "open")
        with st.expander(f"{row['ID']}  ·  {row['Name']}  (CVSS {row['CVSS Score']})"):
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.markdown(f"<span class='badge {sev_cls}'>{row['Severity']}</span>&nbsp;"
                            f"<span class='badge {stat_cls}'>{row['Status']}</span>&nbsp;"
                            f"<span class='badge medium'>{row['Category']}</span>",
                            unsafe_allow_html=True)
            with col2:
                st.metric("CVSS Score", row["CVSS Score"])
            with col3:
                st.metric("Discovered", row["Discovered"])

            st.markdown(f"**Description:** {row['Description']}")
            st.info(f"💡 **Recommendation:** {row['Recommendation']}")

    st.divider()
    st.subheader("📊 Visual Breakdown")
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(category_bar(filtered), use_container_width=True)
    with col2:
        st.plotly_chart(status_pie(filtered), use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 3 — TRAINING MODULES
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Training":
    st.title("📚 Training Modules")
    st.caption("Cybersecurity awareness and best practices for intern program participants")
    st.divider()

    completed = sum(1 for m in TRAINING_MODULES if m["completed"])
    scores    = [m["score"] for m in TRAINING_MODULES if m["score"]]
    avg_score = round(sum(scores) / len(scores), 1) if scores else 0

    c1, c2, c3 = st.columns(3)
    c1.metric("Modules Completed", f"{completed}/{len(TRAINING_MODULES)}")
    c2.metric("Average Score",     f"{avg_score}%")
    c3.metric("Status", "In Progress" if completed < len(TRAINING_MODULES) else "Complete")

    st.divider()

    LEVEL_EMOJI = {"Beginner": "🟢", "Intermediate": "🟡", "Advanced": "🔴"}

    for mod in TRAINING_MODULES:
        emoji   = LEVEL_EMOJI.get(mod["level"], "⚪")
        check   = "✅" if mod["completed"] else "⏳"
        score_s = f"  |  Score: **{mod['score']}%**" if mod["score"] else ""
        header  = f"{check} {mod['title']} ({mod['level']}) — {mod['duration']}{score_s}"

        with st.expander(header):
            st.markdown(f"**{mod['description']}**")
            st.markdown("**Topics covered:**")
            cols = st.columns(2)
            for i, topic in enumerate(mod["topics"]):
                cols[i % 2].markdown(f"- {topic}")

            # Quiz available for modules 1 and 2
            if mod["id"] in QUIZ_QUESTIONS:
                st.divider()
                quiz_key = f"quiz_{mod['id']}"
                submitted_key = f"submitted_{mod['id']}"

                if not st.session_state.quiz_submitted.get(mod["id"], False):
                    st.markdown(f"### 📝 {QUIZ_QUESTIONS[mod['id']]['title']}")
                    quiz = QUIZ_QUESTIONS[mod["id"]]
                    answers = {}

                    for qi, q in enumerate(quiz["questions"]):
                        st.markdown(f"**Q{qi+1}. {q['q']}**")
                        choice = st.radio(
                            label=f"q_{mod['id']}_{qi}",
                            options=q["options"],
                            label_visibility="collapsed",
                            key=f"radio_{mod['id']}_{qi}"
                        )
                        answers[qi] = q["options"].index(choice)

                    if st.button(f"Submit Quiz — Module {mod['id']}", key=f"submit_{mod['id']}"):
                        correct = sum(
                            1 for qi, q in enumerate(quiz["questions"])
                            if answers[qi] == q["answer"]
                        )
                        pct = round(correct / len(quiz["questions"]) * 100)
                        st.session_state.quiz_submitted[mod["id"]] = {"score": pct, "correct": correct, "total": len(quiz["questions"])}
                        st.rerun()

                else:
                    result = st.session_state.quiz_submitted[mod["id"]]
                    if result["score"] >= 70:
                        st.success(f"🎉 Passed! Score: **{result['score']}%** ({result['correct']}/{result['total']} correct)")
                    else:
                        st.error(f"❌ Not passed. Score: **{result['score']}%** ({result['correct']}/{result['total']} correct). Minimum passing score is 70%.")

                    if st.button(f"Retake Quiz — Module {mod['id']}", key=f"retake_{mod['id']}"):
                        del st.session_state.quiz_submitted[mod["id"]]
                        st.rerun()
            else:
                st.info("📌 Quiz coming soon for this module.")


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 4 — REPORTS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Reports":
    st.title("📄 Security Reports")
    st.caption("Assessment reports, progress tracking, and recommendations documentation")
    st.divider()

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Reports",  len(REPORTS))
    c2.metric("Final Reports",  sum(1 for r in REPORTS if r["status"] == "Final"))
    c3.metric("Open Findings",  sum(r["critical"] + r["high"] for r in REPORTS))

    st.divider()

    # Generate new report button
    if st.button("➕ Generate New Report"):
        with st.spinner("Generating report..."):
            time.sleep(1.5)
        st.success("✅ New draft report generated successfully!")

    st.divider()
    st.subheader("All Reports")

    for report in REPORTS:
        total = report["critical"] + report["high"] + report["medium"] + report["low"]
        status_cls = "resolved" if report["status"] == "Final" else "progress"
        with st.expander(f"📋 {report['title']}  ·  {report['date']}"):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(
                    f"<span class='badge {status_cls}'>{report['status']}</span>&nbsp;"
                    f"<span class='badge medium'>{report['type']}</span>",
                    unsafe_allow_html=True
                )
                st.markdown(f"**Author:** {report['author']}  |  **Date:** {report['date']}  |  **Total Findings:** {total}")
                st.markdown(f"**Summary:** {report['summary']}")
            with col2:
                st.metric("Critical", report["critical"])
                st.metric("High",     report["high"])

            st.divider()
            st.markdown("**🔑 Key Recommendations:**")
            for i, rec in enumerate(report["recommendations"], 1):
                st.markdown(f"{i}. {rec}")

            # Findings breakdown chart
            import plotly.graph_objects as go
            fig = go.Figure(go.Bar(
                x=["Critical", "High", "Medium", "Low"],
                y=[report["critical"], report["high"], report["medium"], report["low"]],
                marker_color=["#ff3b5c", "#ff8c00", "#ffc800", "#00ff88"],
                text=[report["critical"], report["high"], report["medium"], report["low"]],
                textposition="outside",
                textfont=dict(color="#e2e8f0"),
            ))
            fig.update_layout(
                title="Findings Breakdown",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#94a3b8"),
                height=220,
                margin=dict(t=40, b=10, l=10, r=10),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)"),
            )
            st.plotly_chart(fig, use_container_width=True)