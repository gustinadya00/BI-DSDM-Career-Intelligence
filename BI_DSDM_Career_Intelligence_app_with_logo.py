
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# BI DSDM Career Intelligence — Confidential Prototype
# ============================================================

st.set_page_config(
    page_title="BI DSDM Career Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Theme / CSS
# -----------------------------
st.markdown("""
<style>
    :root {
        --bi-blue: #0B4F9C;
        --bi-blue-dark: #07366B;
        --bi-blue-light: #EAF3FF;
        --bi-red: #D71920;
        --ink: #17324D;
        --muted: #6B7C93;
        --line: #DCE5EF;
        --surface: #FFFFFF;
        --bg: #F5F8FC;
    }

    .stApp { background: var(--bg); }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #07366B 0%, #0B4F9C 100%);
        border-right: 0;
    }
    [data-testid="stSidebar"] * { color: white !important; }

    .brand {
        padding: 10px 4px 18px 4px;
        border-bottom: 1px solid rgba(255,255,255,.20);
        margin-bottom: 18px;
    }
    .brand-mark {
        display:inline-flex;
        width:42px;height:42px;
        border-radius:12px;
        align-items:center;justify-content:center;
        background:white;
        color:#0B4F9C;
        font-weight:900;font-size:20px;
        margin-right:10px;
        vertical-align:middle;
    }
    .brand-title { font-weight:800; font-size:15px; vertical-align:middle; }
    .brand-sub { font-size:11px; opacity:.72; margin-left:54px; margin-top:-5px; }

    .confidential {
        background: rgba(215,25,32,.95);
        color:white !important;
        padding:7px 11px;
        border-radius:999px;
        font-size:11px;
        font-weight:800;
        letter-spacing:.5px;
        display:inline-block;
        margin-bottom:12px;
    }

    .page-kicker {
        color: var(--bi-blue);
        font-size:12px;
        font-weight:800;
        letter-spacing:1.3px;
        text-transform:uppercase;
        margin-bottom:3px;
    }
    .page-title {
        color: var(--ink);
        font-size:32px;
        line-height:1.15;
        font-weight:850;
        margin:0 0 6px 0;
    }
    .page-desc { color:var(--muted); font-size:14px; margin-bottom:18px; }

    .card {
        background:var(--surface);
        border:1px solid var(--line);
        border-radius:16px;
        padding:18px;
        box-shadow:0 5px 18px rgba(24,54,86,.05);
        height:100%;
    }
    .card-title { font-weight:800; color:var(--ink); font-size:15px; margin-bottom:3px; }
    .card-sub { color:var(--muted); font-size:12px; margin-bottom:12px; }

    .metric {
        background:white;
        border:1px solid var(--line);
        border-radius:15px;
        padding:17px 18px;
        box-shadow:0 4px 16px rgba(24,54,86,.04);
    }
    .metric-label { color:var(--muted); font-size:12px; font-weight:700; }
    .metric-value { color:var(--ink); font-size:27px; font-weight:850; margin-top:2px; }
    .metric-delta { color:#1A7F37; font-size:11px; font-weight:750; }

    .status {
        display:inline-block;
        padding:5px 9px;
        border-radius:999px;
        font-size:11px;
        font-weight:800;
    }
    .status-green { background:#E9F7EF;color:#16703A; }
    .status-blue { background:#EAF3FF;color:#0B4F9C; }
    .status-yellow { background:#FFF5D9;color:#8A6200; }
    .status-red { background:#FDEBEC;color:#A9141A; }

    .notice {
        border-left:4px solid var(--bi-red);
        background:#FFF6F6;
        border-radius:10px;
        padding:12px 15px;
        color:#6D2024;
        font-size:12px;
        margin-bottom:18px;
    }

    .footer {
        color:#8492A6;
        font-size:10px;
        text-align:center;
        padding:25px 0 5px 0;
    }

    div[data-testid="stDataFrame"] { border-radius:12px; overflow:hidden; }
    .stButton button { border-radius:9px; font-weight:700; }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Dummy data
# -----------------------------
np.random.seed(7)

names = [
    "Alya Prameswari", "Bima Adinata", "Citra Maheswari", "Dimas Nugraha",
    "Eka Putri", "Fajar Wicaksono", "Gita Larasati", "Hendra Saputra",
    "Intan Permata", "Jovan Ramadhan", "Kirana Dewi", "Luthfi Akbar",
    "Maya Anggraini", "Nadia Kurnia", "Oka Pratama", "Putri Anindya",
    "Raka Wijaya", "Salsa Maharani", "Tegar Haryanto", "Vina Oktaviani"
]
units = [
    "DKEM", "DKSP", "DSPK", "DSDM", "DKMP", "DLP", "DSSK", "DPPK",
    "DKPP", "DKEM", "DSDM", "DSPK", "DKMP", "DLP", "DKEM", "DSDM",
    "DSSK", "DKPP", "DKEM", "DSDM"
]
roles = [
    "Economist", "Policy Analyst", "Payment Specialist", "HR Specialist",
    "Financial Analyst", "Research Analyst", "Data Analyst", "Legal Analyst"
]
levels = ["Associate", "Specialist", "Senior Specialist", "Manager"]
potential = np.random.randint(58, 97, len(names))
performance = np.random.randint(62, 99, len(names))
readiness = np.random.randint(48, 96, len(names))

employees = pd.DataFrame({
    "Employee ID": [f"BI-{1001+i}" for i in range(len(names))],
    "Employee": names,
    "Unit": units,
    "Current Role": np.random.choice(roles, len(names)),
    "Level": np.random.choice(levels, len(names)),
    "Performance": performance,
    "Potential": potential,
    "Readiness": readiness,
    "Tenure (yrs)": np.round(np.random.uniform(1.2, 15.5, len(names)), 1),
})

employees["Talent Segment"] = np.select(
    [
        (employees["Performance"] >= 80) & (employees["Potential"] >= 80),
        (employees["Performance"] >= 80) & (employees["Potential"] < 80),
        (employees["Performance"] < 80) & (employees["Potential"] >= 80),
    ],
    ["High Potential / High Performance", "High Performer", "High Potential"],
    default="Core Talent"
)

jobs = pd.DataFrame({
    "Target Role": [
        "Senior Economist", "Monetary Policy Analyst", "Digital Payment Strategist",
        "People Analytics Lead", "Financial Stability Specialist", "Research Lead",
        "Data & AI Specialist", "Strategic Policy Advisor"
    ],
    "Domain": [
        "Macroeconomics", "Monetary Policy", "Digital Payment", "Human Capital",
        "Financial Stability", "Research", "Data & Technology", "Strategy"
    ],
    "Critical Skills": [
        "Macro modelling, policy analysis", "Policy transmission, forecasting",
        "Payment systems, digital economy", "People analytics, talent strategy",
        "Risk analytics, financial system", "Research design, writing",
        "Python, analytics, AI", "Strategy, stakeholder management"
    ]
})

# -----------------------------
# Helpers
# -----------------------------
def header(kicker, title, desc):
    st.markdown(f'<div class="page-kicker">{kicker}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-desc">{desc}</div>', unsafe_allow_html=True)

def metric(label, value, delta):
    st.markdown(f"""
    <div class="metric">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-delta">{delta}</div>
    </div>
    """, unsafe_allow_html=True)

def status(text, kind="blue"):
    return f'<span class="status status-{kind}">{text}</span>'

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    # Logo file must be in the same folder as app.py
    # Example:
    # BI-DSDM-Career-Intelligence/
    # ├── app.py
    # └── logo.png
    st.image("logo.png", use_container_width=True)

    st.markdown("""
    <div style="
        font-size: 11px;
        color: rgba(255,255,255,.75);
        text-align: center;
        margin-top: -8px;
        margin-bottom: 18px;
    ">
        Strategic Human Capital Platform
    </div>

    <div class="confidential">
        ● CONFIDENTIAL — DSDM ONLY
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "NAVIGATION",
        [
            "Executive Dashboard",
            "Employee Intelligence",
            "Career Mapping",
            "Talent Pool",
            "Job Fit Intelligence",
            "Career Recommendation",
            "Analytics",
            "Settings",
        ],
        label_visibility="visible",
    )

    st.markdown("---")
    st.caption("ACCESS LEVEL")
    st.markdown("**DSDM / Authorized User**")
    st.caption("Prototype • Dummy Data")
    st.markdown("---")
    st.caption("Last data refresh")
    st.markdown("**14 September 2026 • 08:00 WIB**")

# -----------------------------
# Executive Dashboard
# -----------------------------
if page == "Executive Dashboard":
    header("DSDM • STRATEGIC OVERVIEW", "Executive Dashboard",
           "Enterprise-level view of workforce capability, talent readiness, and career pipeline.")

    st.markdown('<div class="notice"><b>CONFIDENTIAL:</b> This dashboard is an internal DSDM prototype. All displayed records are dummy data and must not be interpreted as actual employee information.</div>', unsafe_allow_html=True)

    cols = st.columns(4)
    with cols[0]: metric("Employees in Scope", "2,486", "+4.2% vs. prior cycle")
    with cols[1]: metric("Talent Pool", "312", "+18 identified this cycle")
    with cols[2]: metric("Ready Now", "87", "+9.6% vs. prior cycle")
    with cols[3]: metric("Avg. Job Fit", "82.4%", "+3.1 pp vs. prior cycle")

    st.write("")
    c1, c2 = st.columns([1.35, 1])

    with c1:
        st.markdown('<div class="card"><div class="card-title">Talent Distribution</div><div class="card-sub">Illustrative distribution across strategic talent segments</div>', unsafe_allow_html=True)
        seg = employees["Talent Segment"].value_counts().reset_index()
        seg.columns = ["Segment", "Count"]
        fig = px.bar(seg, x="Count", y="Segment", orientation="h")
        fig.update_layout(height=330, margin=dict(l=0,r=10,t=10,b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="card"><div class="card-title">Career Readiness</div><div class="card-sub">Illustrative readiness profile</div>', unsafe_allow_html=True)
        buckets = pd.cut(employees["Readiness"], bins=[0,59,74,89,100], labels=["Watch","Develop","Ready","Ready Now"])
        rd = buckets.value_counts().reindex(["Watch","Develop","Ready","Ready Now"]).fillna(0).reset_index()
        rd.columns = ["Readiness", "Count"]
        fig2 = px.pie(rd, names="Readiness", values="Count", hole=.62)
        fig2.update_layout(height=330, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor="rgba(0,0,0,0)", showlegend=True)
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    st.markdown('<div class="card"><div class="card-title">Priority Talent Signals</div><div class="card-sub">Illustrative signals requiring DSDM attention</div>', unsafe_allow_html=True)
    signal_df = pd.DataFrame({
        "Signal": ["Ready-now successors", "Critical role coverage", "Skill gap concentration", "Mobility candidates"],
        "Volume": [87, 42, 126, 73],
        "Priority": ["High", "High", "Medium", "Medium"],
        "Trend": ["↑ 9.6%", "↑ 4.1%", "↓ 2.8%", "↑ 7.3%"]
    })
    st.dataframe(signal_df, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Employee Intelligence
# -----------------------------
elif page == "Employee Intelligence":
    header("DSDM • EMPLOYEE INTELLIGENCE", "Employee Intelligence",
           "Search and inspect a consolidated, confidential employee intelligence profile.")

    left, right = st.columns([1, 2.2])
    with left:
        selected = st.selectbox("Select employee", employees["Employee"].tolist())
    person = employees[employees["Employee"] == selected].iloc[0]

    with right:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">{person["Employee"]}</div>
            <div class="card-sub">{person["Employee ID"]} • {person["Unit"]} • {person["Current Role"]}</div>
            {status(person["Talent Segment"], "blue")}
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    cols = st.columns(4)
    with cols[0]: metric("Performance", f'{person["Performance"]}/100', "Latest cycle")
    with cols[1]: metric("Potential", f'{person["Potential"]}/100', "Assessment score")
    with cols[2]: metric("Readiness", f'{person["Readiness"]}/100', "Career readiness")
    with cols[3]: metric("Tenure", f'{person["Tenure (yrs)"]} yrs', "Illustrative")

    st.write("")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="card"><div class="card-title">Capability Profile</div><div class="card-sub">Illustrative competency scores</div>', unsafe_allow_html=True)
        capability = pd.DataFrame({
            "Capability": ["Strategic Thinking", "Domain Expertise", "Leadership", "Collaboration", "Digital Fluency", "Communication"],
            "Score": np.clip(np.array([person["Performance"], person["Potential"], 76, 84, 71, 88]) + np.random.randint(-5,6,6), 50, 100)
        })
        fig = px.bar(capability, x="Score", y="Capability", orientation="h", range_x=[0,100])
        fig.update_layout(height=330, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card"><div class="card-title">Development Signals</div><div class="card-sub">Illustrative intelligence generated from profile inputs</div>', unsafe_allow_html=True)
        signals = [
            ("Strength", "Strategic thinking & stakeholder communication", "green"),
            ("Strength", "Cross-functional collaboration", "green"),
            ("Development", "Advanced data analytics", "yellow"),
            ("Opportunity", "Leadership exposure in strategic initiatives", "blue"),
        ]
        for a,b,k in signals:
            st.markdown(f'<div style="padding:10px 0;border-bottom:1px solid #E7EDF4"><b>{status(a,k)}</b>&nbsp;&nbsp;{b}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Career Mapping
# -----------------------------
elif page == "Career Mapping":
    header("DSDM • CAREER ARCHITECTURE", "Career Mapping",
           "Visualize employee positioning against performance, potential, and career readiness.")

    st.markdown('<div class="card"><div class="card-title">9-Box Talent Map</div><div class="card-sub">Illustrative placement of employees based on performance and potential</div>', unsafe_allow_html=True)
    fig = px.scatter(
        employees, x="Performance", y="Potential",
        size="Readiness", hover_name="Employee",
        color="Talent Segment",
        range_x=[50,100], range_y=[50,100]
    )
    fig.add_hline(y=80, line_dash="dash")
    fig.add_vline(x=80, line_dash="dash")
    fig.update_layout(height=560, margin=dict(l=10,r=10,t=10,b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    st.markdown('<div class="card"><div class="card-title">Career Pathway Examples</div><div class="card-sub">Prototype-only pathways for demonstration</div>', unsafe_allow_html=True)
    pathway = pd.DataFrame({
        "Current Role": ["Policy Analyst", "Research Analyst", "HR Specialist", "Data Analyst"],
        "Next Role": ["Senior Policy Analyst", "Research Lead", "People Analytics Lead", "Data & AI Specialist"],
        "Readiness": ["Ready Now", "Ready", "Develop", "Ready"],
        "Key Gap": ["Leadership exposure", "Advanced modelling", "Analytics", "Central banking domain"]
    })
    st.dataframe(pathway, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Talent Pool
# -----------------------------
elif page == "Talent Pool":
    header("DSDM • TALENT PORTFOLIO", "Talent Pool",
           "Curated talent segments for strategic workforce planning and succession discussions.")

    segment_filter = st.multiselect(
        "Talent segment",
        sorted(employees["Talent Segment"].unique()),
        default=sorted(employees["Talent Segment"].unique())
    )
    pool = employees[employees["Talent Segment"].isin(segment_filter)].copy()

    cols = st.columns(3)
    with cols[0]: metric("Selected Pool", len(pool), "Illustrative")
    with cols[1]: metric("Avg. Potential", f'{pool["Potential"].mean():.1f}', "Score / 100")
    with cols[2]: metric("Avg. Readiness", f'{pool["Readiness"].mean():.1f}', "Score / 100")

    st.write("")
    st.markdown('<div class="card"><div class="card-title">Talent Pool Register</div><div class="card-sub">Dummy records for prototype demonstration</div>', unsafe_allow_html=True)
    display = pool[["Employee ID","Employee","Unit","Current Role","Level","Performance","Potential","Readiness","Talent Segment"]]
    st.dataframe(display, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Job Fit Intelligence
# -----------------------------
elif page == "Job Fit Intelligence":
    header("DSDM • ROLE INTELLIGENCE", "Job Fit Intelligence",
           "Compare employee capability profiles with target-role requirements.")

    employee_name = st.selectbox("Employee", employees["Employee"].tolist(), key="fit_emp")
    role = st.selectbox("Target role", jobs["Target Role"].tolist())
    p = employees[employees["Employee"] == employee_name].iloc[0]

    role_idx = jobs.index[jobs["Target Role"] == role][0]
    base = int(np.clip((p["Performance"] + p["Potential"]) / 2, 55, 96))
    fit_score = int(np.clip(base + [4,-2,2,6,0,3,5,-1][role_idx], 55, 98))

    cols = st.columns(4)
    with cols[0]: metric("Overall Job Fit", f"{fit_score}%", "Illustrative model")
    with cols[1]: metric("Domain Fit", f"{np.clip(fit_score+2,0,100)}%", "Role alignment")
    with cols[2]: metric("Skill Fit", f"{np.clip(fit_score-5,0,100)}%", "Capability match")
    with cols[3]: metric("Readiness", f'{p["Readiness"]}%', "Current profile")

    st.write("")
    c1,c2 = st.columns([1.2,1])
    with c1:
        st.markdown('<div class="card"><div class="card-title">Fit Dimension Analysis</div><div class="card-sub">Illustrative matching dimensions</div>', unsafe_allow_html=True)
        dims = pd.DataFrame({
            "Dimension": ["Technical / Domain", "Behavioral", "Strategic", "Leadership", "Digital"],
            "Employee": [fit_score+2, fit_score-4, fit_score+5, fit_score-8, fit_score-2],
            "Required": [85, 80, 82, 78, 80]
        })
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Employee", x=dims["Dimension"], y=dims["Employee"]))
        fig.add_trace(go.Bar(name="Required", x=dims["Dimension"], y=dims["Required"]))
        fig.update_layout(barmode="group", height=360, margin=dict(l=0,r=0,t=10,b=0), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        job = jobs.iloc[role_idx]
        st.markdown(f"""
        <div class="card">
            <div class="card-title">{job["Target Role"]}</div>
            <div class="card-sub">{job["Domain"]}</div>
            <p><b>Critical skills</b></p>
            <p style="color:#6B7C93;font-size:13px">{job["Critical Skills"]}</p>
            <hr>
            <p><b>Fit interpretation</b></p>
            <p style="font-size:13px">The profile indicates a <b>{'strong' if fit_score >= 80 else 'moderate'} alignment</b> with the illustrative role requirements.</p>
        </div>
        """, unsafe_allow_html=True)

# -----------------------------
# Career Recommendation
# -----------------------------
elif page == "Career Recommendation":
    header("DSDM • DECISION SUPPORT", "Career Recommendation",
           "Illustrative recommendation engine to support—not replace—DSDM career decisions.")

    emp = st.selectbox("Select employee", employees["Employee"].tolist(), key="rec_emp")
    p = employees[employees["Employee"] == emp].iloc[0]

    recs = pd.DataFrame({
        "Recommended Path": [
            "Senior Specialist — Strategic Policy",
            "Cross-Functional Assignment",
            "Advanced Analytics Development"
        ],
        "Confidence": [
            int(np.clip(p["Potential"] + 1, 60, 96)),
            int(np.clip(p["Performance"] - 3, 55, 94)),
            int(np.clip(p["Readiness"] + 2, 55, 95))
        ],
        "Rationale": [
            "High potential and sustained performance suggest suitability for broader strategic responsibilities.",
            "Cross-unit exposure could strengthen enterprise perspective and leadership readiness.",
            "Closing analytics capability gaps can expand future role options."
        ]
    })

    st.markdown('<div class="notice"><b>Decision-support disclaimer:</b> Recommendations shown here are generated from dummy data and illustrative rules. They are not automated personnel decisions and require authorized human review.</div>', unsafe_allow_html=True)

    for _, r in recs.iterrows():
        st.markdown(f"""
        <div class="card" style="margin-bottom:12px">
            <div style="display:flex;justify-content:space-between;gap:15px">
                <div>
                    <div class="card-title">{r["Recommended Path"]}</div>
                    <div class="card-sub">{r["Rationale"]}</div>
                </div>
                <div style="min-width:105px;text-align:right">
                    <div style="font-size:25px;font-weight:850;color:#0B4F9C">{r["Confidence"]}%</div>
                    <div style="font-size:10px;color:#6B7C93">confidence</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# -----------------------------
# Analytics
# -----------------------------
elif page == "Analytics":
    header("DSDM • WORKFORCE ANALYTICS", "Analytics",
           "Explore illustrative trends and relationships across workforce capability indicators.")

    trend = pd.DataFrame({
        "Cycle": ["S1 2025","S2 2025","S1 2026","S2 2026"],
        "Avg Job Fit": [76.2, 78.9, 80.1, 82.4],
        "Readiness": [67.4, 71.2, 74.8, 78.1],
        "Internal Mobility": [12.8, 14.1, 15.7, 17.3]
    })

    c1,c2 = st.columns(2)
    with c1:
        st.markdown('<div class="card"><div class="card-title">Capability Trend</div><div class="card-sub">Illustrative historical trend</div>', unsafe_allow_html=True)
        fig = px.line(trend, x="Cycle", y=["Avg Job Fit","Readiness"], markers=True)
        fig.update_layout(height=340, margin=dict(l=0,r=0,t=10,b=0), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card"><div class="card-title">Unit Readiness</div><div class="card-sub">Illustrative comparison</div>', unsafe_allow_html=True)
        unit = employees.groupby("Unit", as_index=False)["Readiness"].mean().sort_values("Readiness", ascending=False)
        fig = px.bar(unit, x="Unit", y="Readiness", range_y=[0,100])
        fig.update_layout(height=340, margin=dict(l=0,r=0,t=10,b=0), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    st.markdown('<div class="card"><div class="card-title">Key Analytical Insights</div><div class="card-sub">Illustrative observations from dummy data</div>', unsafe_allow_html=True)
    insights = [
        "Readiness has improved across recent cycles, indicating a larger pool of employees suitable for accelerated development.",
        "High-potential employees with moderate performance form a priority development segment.",
        "Digital and analytics capabilities represent an opportunity area for future role mobility.",
    ]
    for i, x in enumerate(insights, 1):
        st.markdown(f"**{i}.** {x}")
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Settings
# -----------------------------
else:
    header("DSDM • SYSTEM CONFIGURATION", "Settings",
           "Prototype configuration and access-control concepts.")

    st.markdown('<div class="card"><div class="card-title">Access & Confidentiality</div><div class="card-sub">Conceptual controls for a production implementation</div>', unsafe_allow_html=True)
    st.toggle("Confidential mode", value=True, disabled=True)
    st.toggle("DSDM-only access", value=True, disabled=True)
    st.toggle("Audit logging", value=False, disabled=True)
    st.info("Production implementation should connect these controls to an approved identity and access-management mechanism. This prototype intentionally uses no external authentication service.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    c1,c2 = st.columns(2)
    with c1:
        st.markdown('<div class="card"><div class="card-title">Model Configuration</div><div class="card-sub">Illustrative parameters</div>', unsafe_allow_html=True)
        st.slider("Performance threshold", 50, 100, 80)
        st.slider("Potential threshold", 50, 100, 80)
        st.slider("Readiness threshold", 50, 100, 80)
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card"><div class="card-title">Prototype Information</div><div class="card-sub">Environment details</div>', unsafe_allow_html=True)
        st.write("**Application:** BI DSDM Career Intelligence")
        st.write("**Environment:** Prototype / Demo")
        st.write("**Data source:** Dummy data")
        st.write("**External API:** None")
        st.write("**Database:** None")
        st.write("**Primary user:** DSDM / Authorized User")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    BI DSDM Career Intelligence • CONFIDENTIAL • Prototype using dummy data only
</div>
""", unsafe_allow_html=True)
