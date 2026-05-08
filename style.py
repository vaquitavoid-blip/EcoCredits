css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Mono:ital,wght@0,300;0,400;0,500;1,300&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600&display=swap');

:root {
    --bg-base:      #0c0c0e;
    --bg-surface:   #111115;
    --bg-elevated:  #17171d;
    --bg-glass:     rgba(255,255,255,0.03);
    --border:       rgba(255,255,255,0.07);
    --border-glow:  rgba(245,185,60,0.3);
    --gold:         #f5b93c;
    --gold-dim:     #c4922a;
    --gold-subtle:  rgba(245,185,60,0.08);
    --text-primary: #f0ede6;
    --text-secondary: #8a8790;
    --text-muted:   #4a4850;
    --green:        #4ade80;
    --red:          #f87171;
    --blue:         #60a5fa;
    --radius:       12px;
    --radius-lg:    18px;
}

/* ── Reset & Base ── */
* { box-sizing: border-box; }

.stApp {
    background: var(--bg-base);
    color: var(--text-primary);
    font-family: 'DM Sans', sans-serif;
    font-size: 15px;
}

/* Noise texture overlay */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 0;
    opacity: 0.4;
}

/* ── Typography ── */
h1, h2, h3 {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.03em;
    line-height: 1.15;
}

h1 { font-size: 2.2rem; }
h2 { font-size: 1.5rem; }
h3 { font-size: 1.15rem; }

/* Gold accent on h1 last word — via global title rule */
.stTitle, [data-testid="stHeader"] h1 {
    background: linear-gradient(135deg, var(--text-primary) 60%, var(--gold));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--bg-surface) !important;
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"]::after {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 1px; height: 100%;
    background: linear-gradient(180deg, transparent, var(--gold-dim), transparent);
    opacity: 0.4;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label {
    color: var(--text-secondary) !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stSidebar"] .stRadio label {
    color: var(--text-secondary) !important;
    font-size: 0.9rem;
    padding: 6px 0;
    transition: color 0.2s;
}

[data-testid="stSidebar"] .stRadio label:hover {
    color: var(--gold) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: var(--bg-elevated) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.875rem !important;
    padding: 0.55rem 1.25rem !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.01em !important;
}

.stButton > button:hover {
    border-color: var(--gold) !important;
    color: var(--gold) !important;
    background: var(--gold-subtle) !important;
    box-shadow: 0 0 20px rgba(245,185,60,0.1) !important;
    transform: translateY(-1px) !important;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #c4922a, var(--gold)) !important;
    color: #0c0c0e !important;
    border-color: transparent !important;
    font-weight: 600 !important;
}

.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, var(--gold), #f7cf6d) !important;
    color: #0c0c0e !important;
    box-shadow: 0 4px 20px rgba(245,185,60,0.3) !important;
    transform: translateY(-2px) !important;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stTextArea textarea {
    background: var(--bg-elevated) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
    border-radius: var(--radius) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    transition: border-color 0.2s !important;
}

.stTextInput > div > div > input:focus,
.stTextArea textarea:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 3px rgba(245,185,60,0.1) !important;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: var(--bg-elevated);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.2rem 1.4rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s, box-shadow 0.2s;
}

[data-testid="stMetric"]:hover {
    border-color: var(--border-glow);
    box-shadow: 0 0 24px rgba(245,185,60,0.06);
}

[data-testid="stMetric"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
    opacity: 0.5;
}

[data-testid="stMetricLabel"] p {
    color: var(--text-secondary) !important;
    font-size: 0.75rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    font-family: 'DM Mono', monospace !important;
}

[data-testid="stMetricValue"] {
    color: var(--gold) !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 2rem !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 4px;
    gap: 2px;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-secondary) !important;
    border-radius: var(--radius) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.875rem !important;
    padding: 0.5rem 1rem !important;
    transition: all 0.2s !important;
    border: none !important;
}

.stTabs [data-baseweb="tab"]:hover {
    color: var(--text-primary) !important;
    background: var(--bg-glass) !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(245,185,60,0.15), rgba(245,185,60,0.08)) !important;
    color: var(--gold) !important;
    font-weight: 600 !important;
    box-shadow: inset 0 1px 0 rgba(245,185,60,0.3) !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-lg) !important;
    overflow: hidden !important;
    background: var(--bg-elevated) !important;
}

[data-testid="stDataFrame"] table {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.82rem !important;
}

[data-testid="stDataFrame"] th {
    background: var(--bg-surface) !important;
    color: var(--text-secondary) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    border-bottom: 1px solid var(--border) !important;
}

[data-testid="stDataFrame"] td {
    color: var(--text-primary) !important;
    border-bottom: 1px solid var(--border) !important;
}

/* ── Alert boxes ── */
.stSuccess > div {
    background: rgba(74,222,128,0.06) !important;
    border: 1px solid rgba(74,222,128,0.3) !important;
    border-radius: var(--radius) !important;
    color: var(--green) !important;
}

.stWarning > div {
    background: rgba(245,185,60,0.06) !important;
    border: 1px solid rgba(245,185,60,0.3) !important;
    border-radius: var(--radius) !important;
    color: var(--gold) !important;
}

.stError > div {
    background: rgba(248,113,113,0.06) !important;
    border: 1px solid rgba(248,113,113,0.3) !important;
    border-radius: var(--radius) !important;
    color: var(--red) !important;
}

.stInfo > div {
    background: rgba(96,165,250,0.06) !important;
    border: 1px solid rgba(96,165,250,0.3) !important;
    border-radius: var(--radius) !important;
    color: var(--blue) !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: var(--bg-elevated) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text-secondary) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.875rem !important;
    transition: all 0.2s !important;
}

.streamlit-expanderHeader:hover {
    border-color: var(--gold) !important;
    color: var(--gold) !important;
}

.streamlit-expanderContent {
    background: var(--bg-elevated) !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
    border-radius: 0 0 var(--radius) var(--radius) !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: var(--bg-elevated) !important;
    border: 1.5px dashed var(--border) !important;
    border-radius: var(--radius-lg) !important;
    transition: border-color 0.2s !important;
}

[data-testid="stFileUploader"]:hover {
    border-color: var(--gold) !important;
    background: var(--gold-subtle) !important;
}

/* ── Code blocks ── */
.stCode, code, pre {
    background: var(--bg-surface) !important;
    border: 1px solid var(--border) !important;
    color: #c4b89a !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.82rem !important;
    border-radius: var(--radius) !important;
}

/* ── Divider ── */
hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 1.5rem 0 !important;
}

/* ── Caption ── */
.stCaption p {
    color: var(--text-muted) !important;
    font-size: 0.82rem !important;
    font-family: 'DM Mono', monospace !important;
}

/* ── Spinner ── */
.stSpinner > div {
    border-top-color: var(--gold) !important;
}

/* ── Markdown text ── */
p, li {
    color: var(--text-secondary);
    line-height: 1.65;
    font-family: 'DM Sans', sans-serif;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb {
    background: var(--border);
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover { background: var(--gold-dim); }

/* ── Badge helper ── */
.eco-badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 600;
    font-family: 'DM Mono', monospace;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

.badge-gold   { background: rgba(245,185,60,0.12); color: var(--gold); border: 1px solid rgba(245,185,60,0.25); }
.badge-green  { background: rgba(74,222,128,0.1);  color: var(--green); border: 1px solid rgba(74,222,128,0.25); }
.badge-muted  { background: rgba(255,255,255,0.04); color: var(--text-muted); border: 1px solid var(--border); }
.badge-red    { background: rgba(248,113,113,0.1);  color: var(--red); border: 1px solid rgba(248,113,113,0.25); }

/* ── Radio buttons ── */
.stRadio div[role="radio"] label {
    color: var(--text-secondary) !important;
    transition: color 0.15s;
}

.stRadio div[role="radio"][aria-checked="true"] label {
    color: var(--gold) !important;
    font-weight: 600 !important;
}

/* ── Select dropdown ── */
[data-baseweb="select"] div {
    background: var(--bg-elevated) !important;
    border-color: var(--border) !important;
    color: var(--text-primary) !important;
}

/* ── Checkbox ── */
.stCheckbox label { color: var(--text-secondary) !important; }

</style>
"""

# ── Reusable HTML card ────────────────────────────────────────────────────────
def stat_card(label, value, color="#f5b93c", icon=""):
    return f"""
    <div style="
        background: #17171d;
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 16px;
        padding: 1.2rem 1.5rem;
        position: relative;
        overflow: hidden;
    ">
        <div style="
            position: absolute; top: 0; left: 0; right: 0; height: 2px;
            background: linear-gradient(90deg, transparent, {color}, transparent);
        "></div>
        <div style="font-family:'DM Mono',monospace; font-size:0.7rem;
                    letter-spacing:0.1em; text-transform:uppercase;
                    color:#8a8790; margin-bottom:0.5rem;">
            {icon} {label}
        </div>
        <div style="font-family:'Syne',sans-serif; font-size:1.9rem;
                    font-weight:700; color:{color}; line-height:1;">
            {value}
        </div>
    </div>
    """


def section_header(title, subtitle=""):
    sub = f'<div style="font-size:0.82rem;color:#4a4850;font-family:\'DM Mono\',monospace;margin-top:4px;">{subtitle}</div>' if subtitle else ""
    return f"""
    <div style="margin-bottom:1.5rem;">
        <h2 style="font-family:'Syne',sans-serif; font-weight:700;
                   font-size:1.3rem; color:#f0ede6;
                   letter-spacing:-0.02em; margin:0;">{title}</h2>
        {sub}
    </div>
    """