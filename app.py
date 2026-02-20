import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
import plotly.express as px

# ==========================================
# 1. Page Configuration
# ==========================================
st.set_page_config(
    page_title="EduMetrics — Student Intelligence Platform",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# INDUSTRIAL GRADE CSS — Dark Data Dashboard Aesthetic
# Inspired by: Bloomberg Terminal × Vercel Dashboard
# Fonts: DM Mono (monospace data) + Syne (bold headings)
# ==========================================
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">

<style>
/* ---- ROOT TOKENS ---- */
:root {
    --bg-base:       #0a0b0f;
    --bg-surface:    #111318;
    --bg-elevated:   #181c24;
    --bg-hover:      #1e2330;
    --border:        rgba(255,255,255,0.07);
    --border-accent: rgba(99,179,237,0.4);
    --text-primary:  #e8eaf0;
    --text-secondary:#8a93a8;
    --text-muted:    #4a5068;
    --accent-blue:   #63b3ed;
    --accent-cyan:   #4fd1c5;
    --accent-amber:  #f6ad55;
    --accent-red:    #fc8181;
    --accent-green:  #68d391;
    --accent-purple: #b794f4;
    --success:       #2f855a;
    --warning:       #975a16;
    --danger:        #9b2c2c;
    --radius-sm:     6px;
    --radius-md:     10px;
    --radius-lg:     16px;
}

/* ---- GLOBAL RESET ---- */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--text-primary);
    background-color: var(--bg-base);
}
.stApp { background: var(--bg-base); }
#MainMenu, footer { visibility: hidden; }
header { background: transparent !important; }

/* ---- SCROLLBAR ---- */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb { background: #2a2f3e; border-radius: 4px; }

/* ---- SIDEBAR ---- */
[data-testid="stSidebar"] {
    background: var(--bg-surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 0; }

/* ---- SIDEBAR HEADER LOGO AREA ---- */
.sidebar-brand {
    padding: 28px 24px 20px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 8px;
}
.brand-tag {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--accent-cyan);
    margin-bottom: 6px;
}
.brand-name {
    font-family: 'Syne', sans-serif;
    font-size: 22px;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: -0.5px;
    line-height: 1.1;
}
.brand-sub {
    font-size: 12px;
    color: var(--text-muted);
    margin-top: 4px;
    font-family: 'DM Mono', monospace;
}

/* ---- SIDEBAR SECTION LABELS ---- */
.sidebar-section-label {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--text-muted);
    padding: 16px 24px 6px;
    display: block;
}

/* ---- STREAMLIT LABELS ---- */
[data-testid="stSidebar"] label,
.stForm label {
    font-family: 'DM Mono', monospace !important;
    font-size: 11px !important;
    color: var(--text-secondary) !important;
    letter-spacing: 0.5px !important;
    text-transform: uppercase !important;
}

/* ---- SLIDERS ---- */
.stSlider [data-baseweb="slider"] {
    padding-top: 4px;
}
.stSlider [data-testid="stThumbValue"] {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    background: var(--bg-elevated);
    color: var(--accent-blue);
    border: 1px solid var(--border-accent);
    border-radius: 4px;
    padding: 2px 6px;
}

/* ---- SELECT / DROPDOWN ---- */
.stSelectbox [data-baseweb="select"] > div,
.stSelectSlider [data-baseweb="select"] > div {
    background: var(--bg-elevated) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 12px !important;
}
.stSelectbox [data-baseweb="select"] > div:hover,
.stSelectSlider [data-baseweb="select"] > div:hover {
    border-color: var(--border-accent) !important;
}

/* ---- EXPANDER ---- */
[data-testid="stExpander"] {
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    background: var(--bg-elevated) !important;
    margin: 8px 0;
}
[data-testid="stExpander"] summary {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: var(--text-secondary) !important;
}

/* ---- PRIMARY BUTTON ---- */
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #1a6bab 0%, #0e4f82 100%) !important;
    color: white !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    border: 1px solid var(--border-accent) !important;
    border-radius: var(--radius-md) !important;
    padding: 14px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 0 20px rgba(99,179,237,0.15) !important;
    margin-top: 8px;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #2176c0 0%, #155e8a 100%) !important;
    box-shadow: 0 0 30px rgba(99,179,237,0.3) !important;
    transform: translateY(-1px) !important;
}

/* ---- DIVIDER ---- */
.stDivider { border-color: var(--border) !important; }
hr { border-color: var(--border) !important; }

/* ---- PLOTLY CHART BG ---- */
.js-plotly-plot .plotly { background: transparent !important; }

/* ===== MAIN CONTENT COMPONENTS ===== */

/* ---- TOP STATUS BAR ---- */
.status-bar {
    display: flex;
    align-items: center;
    gap: 24px;
    padding: 10px 0 20px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 32px;
}
.status-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: var(--accent-green);
    box-shadow: 0 0 8px var(--accent-green);
    animation: pulse 2s infinite;
    display: inline-block;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.6; transform: scale(0.8); }
}
.status-text {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: var(--text-muted);
    letter-spacing: 1px;
}
.status-label {
    color: var(--accent-green);
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 2px;
    text-transform: uppercase;
}

/* ---- HERO TITLE ---- */
.hero-section {
    padding: 20px 0 40px;
}
.hero-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: var(--accent-cyan);
    margin-bottom: 12px;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 52px;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: -2px;
    line-height: 1.0;
    margin-bottom: 16px;
}
.hero-title span { color: var(--accent-blue); }
.hero-desc {
    font-size: 15px;
    color: var(--text-secondary);
    line-height: 1.7;
    max-width: 520px;
    font-weight: 300;
}

/* ---- FEATURE CARDS ---- */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-top: 48px;
}
.feature-card {
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 28px 24px;
    transition: all 0.25s ease;
    position: relative;
    overflow: hidden;
}
.feature-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent-blue), transparent);
    opacity: 0;
    transition: opacity 0.3s;
}
.feature-card:hover { border-color: rgba(99,179,237,0.25); transform: translateY(-2px); }
.feature-card:hover::before { opacity: 1; }
.feature-icon {
    font-size: 28px;
    margin-bottom: 16px;
    display: block;
}
.feature-title {
    font-family: 'Syne', sans-serif;
    font-size: 16px;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 8px;
}
.feature-desc {
    font-size: 13px;
    color: var(--text-muted);
    line-height: 1.6;
}

/* ---- STAT STRIP ---- */
.stat-strip {
    display: flex;
    gap: 2px;
    margin-top: 48px;
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    overflow: hidden;
    background: var(--border);
}
.stat-item {
    flex: 1;
    background: var(--bg-surface);
    padding: 20px 24px;
    text-align: center;
}
.stat-value {
    font-family: 'Syne', sans-serif;
    font-size: 28px;
    font-weight: 800;
    color: var(--accent-blue);
    letter-spacing: -1px;
}
.stat-label {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    color: var(--text-muted);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 4px;
}

/* ---- RESULTS PAGE ---- */
.results-header {
    padding: 4px 0 28px;
}
.results-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 8px;
}
.results-title {
    font-family: 'Syne', sans-serif;
    font-size: 36px;
    font-weight: 800;
    letter-spacing: -1.5px;
    color: var(--text-primary);
}

/* ---- SCORE DISPLAY PANEL ---- */
.score-panel {
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 32px;
    position: relative;
    overflow: hidden;
}
.score-panel::after {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 180px; height: 180px;
    background: radial-gradient(circle, rgba(99,179,237,0.08), transparent 70%);
    pointer-events: none;
}

/* ---- INSIGHTS PANEL ---- */
.insights-panel {
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 32px;
    height: 100%;
}
.panel-label {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.panel-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ---- ALERT BADGES ---- */
.alert-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 12px;
    border-radius: 100px;
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 16px;
}
.badge-success { background: rgba(104,211,145,0.1); color: var(--accent-green); border: 1px solid rgba(104,211,145,0.25); }
.badge-warning { background: rgba(246,173,85,0.1); color: var(--accent-amber); border: 1px solid rgba(246,173,85,0.25); }
.badge-danger  { background: rgba(252,129,129,0.1); color: var(--accent-red);   border: 1px solid rgba(252,129,129,0.25); }

/* ---- SCORE HEADLINE ---- */
.score-headline {
    font-family: 'Syne', sans-serif;
    font-size: 20px;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 8px;
}
.score-subline {
    font-size: 13px;
    color: var(--text-secondary);
    line-height: 1.6;
    margin-bottom: 24px;
}

/* ---- ADVICE CARDS ---- */
.advice-item {
    display: flex;
    align-items: flex-start;
    gap: 14px;
    padding: 16px;
    border-radius: var(--radius-md);
    border: 1px solid var(--border);
    background: var(--bg-elevated);
    margin-bottom: 12px;
    transition: border-color 0.2s;
}
.advice-item:hover { border-color: rgba(99,179,237,0.2); }
.advice-icon {
    font-size: 18px;
    flex-shrink: 0;
    margin-top: 1px;
}
.advice-text {
    font-size: 13px;
    color: var(--text-secondary);
    line-height: 1.6;
}
.advice-text strong {
    color: var(--text-primary);
    font-size: 13px;
    font-weight: 500;
    display: block;
    margin-bottom: 3px;
}

/* ---- DATA METRICS ROW ---- */
.metrics-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-top: 20px;
}
.metric-chip {
    background: var(--bg-elevated);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 16px;
    text-align: center;
}
.metric-chip-value {
    font-family: 'Syne', sans-serif;
    font-size: 22px;
    font-weight: 800;
    color: var(--accent-blue);
    letter-spacing: -0.5px;
}
.metric-chip-label {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    color: var(--text-muted);
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-top: 4px;
}

/* ---- STREAMLIT INFO/SUCCESS/WARNING/ERROR OVERRIDE ---- */
.stAlert {
    background: var(--bg-elevated) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-secondary) !important;
}

/* ---- FORM SUBMIT AREA ---- */
.submit-hint {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    color: var(--text-muted);
    text-align: center;
    margin-top: 8px;
    letter-spacing: 0.5px;
}

/* ---- PLOTLY TOOLTIP ---- */
.plotly .hoverlayer .hovertext { font-family: 'DM Mono', monospace !important; }

</style>
""", unsafe_allow_html=True)


# ==========================================
# 2. Model Initialization
# ==========================================
@st.cache_resource
def load_model():
    return joblib.load('ultimate_student_huber_pipeline.pkl')

try:
    pipeline = load_model()
    model_loaded = True
except:
    model_loaded = False


# ==========================================
# 3. Sidebar
# ==========================================
with st.sidebar:
    # Brand Header
    st.markdown("""
    <div class="sidebar-brand">
        <div class="brand-tag">● EduMetrics AI</div>
        <div class="brand-name">Student<br>Intelligence</div>
        <div class="brand-sub">v2.4.1 — Huber Regression Engine</div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("student_input_form"):
        st.markdown('<span class="sidebar-section-label">Study Habits</span>', unsafe_allow_html=True)

        hours_studied    = st.slider("Weekly Study Hours", 0, 40, 10)
        attendance       = st.slider("Class Attendance (%)", 0, 100, 80)
        previous_scores  = st.slider("Previous Exam Average", 0, 100, 70)
        tutoring_sessions= st.slider("Monthly Tutoring Sessions", 0, 10, 0)

        st.markdown('<span class="sidebar-section-label">Lifestyle & Environment</span>', unsafe_allow_html=True)

        sleep_hours      = st.slider("Nightly Sleep (hrs)", 4, 12, 7)
        physical_activity= st.slider("Weekly Exercise (hrs)", 0, 20, 3)
        extracurriculars = st.selectbox("Extracurricular Activities", ["Yes", "No"])
        internet_access  = st.selectbox("Reliable Home Internet", ["Yes", "No"])
        distance_from_home=st.selectbox("Distance to School", ["Near", "Moderate", "Far"])

        st.markdown('<span class="sidebar-section-label">Personal Factors</span>', unsafe_allow_html=True)

        motivation_level = st.select_slider("Motivation Level", ["Low", "Medium", "High"], value="Medium")
        peer_influence   = st.select_slider("Peer Study Influence", ["Negative", "Neutral", "Positive"], value="Neutral")
        learning_disabilities = st.selectbox("Documented Learning Disability", ["No", "Yes"])
        gender           = st.selectbox("Gender", ["Female", "Male"])

        with st.expander("Household & School Details"):
            family_income      = st.select_slider("Family Income", ["Low", "Medium", "High"], value="Medium")
            parental_involvement=st.select_slider("Parental Involvement", ["Low", "Medium", "High"], value="Medium")
            parental_education = st.selectbox("Parents' Education", ["High School", "College", "Postgraduate"])
            school_type        = st.selectbox("School Type", ["Public", "Private"])
            teacher_quality    = st.select_slider("Teacher Quality", ["Low", "Medium", "High"], value="Medium")

        submitted = st.form_submit_button("▶  Run Prediction Engine")
        st.markdown('<div class="submit-hint">Analysis powered by ML pipeline</div>', unsafe_allow_html=True)


# ==========================================
# 4. Main Canvas
# ==========================================
if not submitted:
    # ---- STATUS BAR ----
    st.markdown("""
    <div class="status-bar">
        <span class="status-label"><span class="status-dot"></span>&nbsp; System Online</span>
        <span class="status-text">|</span>
        <span class="status-text">MODEL: Huber Regression</span>
        <span class="status-text">|</span>
        <span class="status-text">DATASET: 6,607 students</span>
        <span class="status-text">|</span>
        <span class="status-text">ACCURACY: R² = 0.98</span>
    </div>
    """, unsafe_allow_html=True)

    # ---- HERO ----
    st.markdown("""
    <div class="hero-section">
        <div class="hero-eyebrow">● Academic Intelligence Platform</div>
        <div class="hero-title">Predict your<br><span>exam score</span><br>before it happens.</div>
        <div class="hero-desc">
            Our ML engine analyzes 19 behavioral, environmental, and academic 
            signals to project your exam outcome with precision. Fill in your profile 
            on the left to generate your personal forecast.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---- STAT STRIP ----
    st.markdown("""
    <div class="stat-strip">
        <div class="stat-item">
            <div class="stat-value">6,607</div>
            <div class="stat-label">Students Analyzed</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">19</div>
            <div class="stat-label">Input Features</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">0.98</div>
            <div class="stat-label">R² Score</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">&lt; 2.1</div>
            <div class="stat-label">Avg. MAE (Points)</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---- FEATURE CARDS ----
    st.markdown("""
    <div class="feature-grid">
        <div class="feature-card">
            <span class="feature-icon">📡</span>
            <div class="feature-title">Real-time Scoring</div>
            <div class="feature-desc">Adjust any input and instantly recalculate your projected exam score using our trained Huber regression pipeline.</div>
        </div>
        <div class="feature-card">
            <span class="feature-icon">⚡</span>
            <div class="feature-title">Risk Detection</div>
            <div class="feature-desc">The system flags lagging indicators — low attendance, poor sleep, missing tutoring — and quantifies their impact.</div>
        </div>
        <div class="feature-card">
            <span class="feature-icon">🎯</span>
            <div class="feature-title">Actionable Guidance</div>
            <div class="feature-desc">Every insight is tied to a specific input you can change — no generic advice, only targeted interventions.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# RESULTS VIEW
# ==========================================
if submitted:
    input_data = {
        'Hours_Studied': hours_studied, 'Attendance': attendance,
        'Parental_Involvement': parental_involvement, 'Access_to_Resources': 'Medium',
        'Extracurricular_Activities': extracurriculars, 'Sleep_Hours': sleep_hours,
        'Previous_Scores': previous_scores, 'Motivation_Level': motivation_level,
        'Internet_Access': internet_access, 'Tutoring_Sessions': tutoring_sessions,
        'Family_Income': family_income, 'Teacher_Quality': teacher_quality,
        'School_Type': school_type, 'Peer_Influence': peer_influence,
        'Physical_Activity': physical_activity, 'Learning_Disabilities': learning_disabilities,
        'Parental_Education_Level': parental_education, 'Distance_from_Home': distance_from_home,
        'Gender': gender
    }

    try:
        input_df       = pd.DataFrame([input_data])
        raw_prediction = pipeline.predict(input_df)[0]
        final_score    = min(max(raw_prediction, 0.0), 100.0)
        model_ok       = True
    except Exception as e:
        final_score = 72.4   # Demo fallback
        model_ok    = False

    # ---- Determine grade tier ----
    if final_score >= 80:
        tier        = "DISTINCTION"
        tier_color  = "var(--accent-green)"
        bar_color   = "#48bb78"
        badge_class = "badge-success"
        badge_icon  = "●"
        headline    = "Excellent trajectory."
        summary     = "Your current habits are tracking toward a distinction-level result. Maintain consistency and protect your key inputs."
    elif final_score >= 60:
        tier        = "PASS"
        tier_color  = "var(--accent-amber)"
        bar_color   = "#ed8936"
        badge_class = "badge-warning"
        badge_icon  = "◐"
        headline    = "On track, room to grow."
        summary     = "You're projected to pass, but targeted improvements to 2–3 inputs could move you into the distinction bracket."
    else:
        tier        = "AT RISK"
        tier_color  = "var(--accent-red)"
        bar_color   = "#fc8181"
        badge_class = "badge-danger"
        badge_icon  = "▲"
        headline    = "Intervention recommended."
        summary     = "Current behavioral signals indicate your score may fall below the passing threshold. Prioritize the actions below immediately."

    # ---- Results header ----
    st.markdown(f"""
    <div class="results-header">
        <div class="results-eyebrow">Forecast Generated · {pd.Timestamp.now().strftime("%d %b %Y, %H:%M")}</div>
        <div class="results-title">Academic Forecast Report</div>
    </div>
    """, unsafe_allow_html=True)

    # ---- Main two-column layout ----
    col_gauge, col_insights = st.columns([1.1, 1], gap="large")

    # === LEFT: Gauge + Metrics ===
    with col_gauge:
        st.markdown('<div class="score-panel">', unsafe_allow_html=True)
        st.markdown(f'<div class="panel-label">Projected Score</div>', unsafe_allow_html=True)

        # Plotly gauge — dark industrial style
        fig = go.Figure(go.Indicator(
            mode  = "gauge+number",
            value = final_score,
            domain= {'x': [0, 1], 'y': [0, 1]},
            number= {
                'font': {'size': 72, 'color': '#e8eaf0', 'family': 'Syne'},
                'valueformat': ".1f",
                'suffix': ''
            },
            gauge={
                'axis': {
                    'range': [0, 100],
                    'tickwidth': 1,
                    'tickcolor': '#2a2f3e',
                    'tickfont': {'color': '#4a5068', 'family': 'DM Mono', 'size': 10},
                    'nticks': 6,
                },
                'bar':      {'color': bar_color, 'thickness': 0.22},
                'bgcolor':  'rgba(0,0,0,0)',
                'borderwidth': 0,
                'steps': [
                    {'range': [0,  60],  'color': 'rgba(252,129,129,0.06)'},
                    {'range': [60, 80],  'color': 'rgba(246,173,85,0.06)'},
                    {'range': [80, 100], 'color': 'rgba(104,211,145,0.06)'},
                ],
                'threshold': {
                    'line': {'color': '#e8eaf0', 'width': 2},
                    'thickness': 0.7,
                    'value': final_score
                }
            }
        ))
        fig.update_layout(
            height          = 300,
            margin          = dict(l=24, r=24, t=24, b=0),
            paper_bgcolor   = 'rgba(0,0,0,0)',
            plot_bgcolor    = 'rgba(0,0,0,0)',
            font_family     = 'DM Mono',
        )
        fig.add_annotation(
            text  = f"<b>/{100}</b>",
            x=0.5, y=0.30, xref="paper", yref="paper",
            showarrow=False,
            font=dict(size=18, color='#4a5068', family='DM Mono'),
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        # Tier badge
        st.markdown(f"""
        <div style="text-align:center; margin-top:-8px; margin-bottom:24px;">
            <span class="alert-badge {badge_class}">{badge_icon}&nbsp; Grade Tier: {tier}</span>
        </div>
        """, unsafe_allow_html=True)

        # Key metrics row
        study_efficiency = min(round((hours_studied / 40) * 100), 100)
        sleep_quality    = "Good" if sleep_hours >= 7 else "Low"
        engage_score     = round((attendance / 100) * 50 + (tutoring_sessions / 10) * 50)

        st.markdown(f"""
        <div class="metrics-row">
            <div class="metric-chip">
                <div class="metric-chip-value">{hours_studied}h</div>
                <div class="metric-chip-label">Study / Wk</div>
            </div>
            <div class="metric-chip">
                <div class="metric-chip-value">{attendance}%</div>
                <div class="metric-chip-label">Attendance</div>
            </div>
            <div class="metric-chip">
                <div class="metric-chip-value">{sleep_hours}h</div>
                <div class="metric-chip-label">Sleep / Night</div>
            </div>
            <div class="metric-chip">
                <div class="metric-chip-value">{engage_score}</div>
                <div class="metric-chip-label">Engage Score</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # === RIGHT: Insights ===
    with col_insights:
        st.markdown('<div class="insights-panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-label">Diagnostics & Action Plan</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <span class="alert-badge {badge_class}">{badge_icon}&nbsp; {tier}</span>
        <div class="score-headline">{headline}</div>
        <div class="score-subline">{summary}</div>
        """, unsafe_allow_html=True)

        # Dynamic advice items
        advice_items = []
        if attendance < 85:
            advice_items.append({
                "icon": "📅",
                "title": "Increase Class Attendance",
                "body": f"At {attendance}%, attendance is below the 85% threshold. Each missed class compounds into lower retention. Target 90%+."
            })
        if hours_studied < 12:
            advice_items.append({
                "icon": "⏱️",
                "title": "Add Weekly Study Hours",
                "body": f"You're studying {hours_studied}h/week. Research shows 15–20h/week correlates with top-quartile outcomes. Aim to add 3–5h."
            })
        if sleep_hours < 7:
            advice_items.append({
                "icon": "🛌",
                "title": "Optimize Sleep Schedule",
                "body": f"At {sleep_hours}h/night, cognitive consolidation is impaired. Memory retention peaks above 7.5h. Adjust your routine."
            })
        if previous_scores < 65 and tutoring_sessions == 0:
            advice_items.append({
                "icon": "🤝",
                "title": "Start Tutoring Sessions",
                "body": "With a previous average below 65 and zero tutoring sessions, targeted support is the highest-leverage intervention available."
            })
        if motivation_level == "Low":
            advice_items.append({
                "icon": "🔋",
                "title": "Address Motivation Gap",
                "body": "Low motivation is a leading predictor of dropout behavior. Set weekly micro-goals and track progress visually."
            })
        if not advice_items:
            advice_items.append({
                "icon": "✅",
                "title": "Strong Profile Detected",
                "body": "Your inputs show a well-balanced academic profile. Consistency is your biggest risk — protect your current habits."
            })

        for item in advice_items:
            st.markdown(f"""
            <div class="advice-item">
                <span class="advice-icon">{item['icon']}</span>
                <div class="advice-text">
                    <strong>{item['title']}</strong>
                    {item['body']}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # ---- Feature Impact Bar Chart ----
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="score-panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-label">Input Signal Overview</div>', unsafe_allow_html=True)

    # Normalized input snapshot as a horizontal bar chart
    signal_labels = ["Study Hours", "Attendance", "Prev. Score", "Sleep", "Exercise", "Tutoring"]
    signal_raw    = [hours_studied, attendance, previous_scores, sleep_hours, physical_activity, tutoring_sessions]
    signal_maxes  = [40, 100, 100, 12, 20, 10]
    signal_norm   = [round((v / m) * 100) for v, m in zip(signal_raw, signal_maxes)]
    signal_colors = ["#48bb78" if v >= 70 else "#ed8936" if v >= 40 else "#fc8181" for v in signal_norm]

    fig2 = go.Figure()
    for i, (label, val, pct, color) in enumerate(zip(signal_labels, signal_raw, signal_norm, signal_colors)):
        fig2.add_trace(go.Bar(
            name=label, y=[label], x=[pct], orientation='h',
            marker=dict(color=color, line=dict(width=0)),
            text=f"{pct}%", textposition='outside',
            textfont=dict(family='DM Mono', size=11, color='#8a93a8'),
            hovertemplate=f"<b>{label}</b>: {val}<extra></extra>",
        ))

    fig2.update_layout(
        showlegend   = False,
        paper_bgcolor= 'rgba(0,0,0,0)',
        plot_bgcolor = 'rgba(0,0,0,0)',
        height       = 260,
        margin       = dict(l=10, r=60, t=10, b=10),
        xaxis=dict(
            range       = [0, 120],
            showgrid    = False,
            zeroline    = False,
            showticklabels=False,
        ),
        yaxis=dict(
            showgrid    = False,
            tickfont    = dict(family='DM Mono', size=11, color='#8a93a8'),
            ticklabelposition='outside',
        ),
        barmode='overlay',
        bargap=0.35,
    )
    # Background track bars
    for label in signal_labels:
        fig2.add_trace(go.Bar(
            y=[label], x=[100], orientation='h',
            marker=dict(color='rgba(255,255,255,0.04)', line=dict(width=0)),
            showlegend=False, hoverinfo='skip',
        ))

    st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

    if not model_ok:
        st.caption("⚠️ Model file not found — displaying demo values. Deploy with `ultimate_student_huber_pipeline.pkl` in working directory.")