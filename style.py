css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;500;600&family=Orbitron:wght@400;500;600;700;800;900&display=swap');

:root {
    --void:          #020408;
    --deep:          #060d14;
    --surface:       #0a1628;
    --elevated:      #0f2040;
    --cyan:          #00d4ff;
    --cyan-dim:      #0099cc;
    --cyan-glow:     rgba(0,212,255,0.15);
    --cyan-subtle:   rgba(0,212,255,0.06);
    --gold:          #ffd700;
    --green:         #00ff88;
    --red:           #ff4466;
    --amber:         #ffaa00;
    --text-primary:  #e8f4f8;
    --text-secondary:#5a8fa8;
    --text-muted:    #1e3a4a;
    --border:        rgba(0,212,255,0.08);
    --border-bright: rgba(0,212,255,0.25);
    --r:    8px;
    --r-lg: 14px;
    --r-xl: 20px;
}

*, *::before, *::after { box-sizing: border-box; }

.stApp {
    background: var(--void);
    color: var(--text-primary);
    font-family: 'Space Grotesk', sans-serif;
    font-size: 14px;
}

/* Animated grid */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(0,212,255,0.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,212,255,0.025) 1px, transparent 1px);
    background-size: 44px 44px;
    pointer-events: none;
    z-index: 0;
    animation: gridPulse 8s ease-in-out infinite;
}
@keyframes gridPulse {
    0%,100% { opacity:0.4; }
    50%     { opacity:0.9; }
}

/* Spotlight */
.stApp::after {
    content: '';
    position: fixed;
    top: -20%; left: 50%;
    transform: translateX(-50%);
    width: 70vw; height: 50vh;
    background: radial-gradient(ellipse, rgba(0,212,255,0.035) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
    animation: spotPulse 7s ease-in-out infinite;
}
@keyframes spotPulse {
    0%,100% { opacity:0.5; }
    50%     { opacity:1; }
}

/* Typography */
h1 {
    font-family: 'Orbitron', monospace !important;
    font-weight: 700 !important;
    font-size: 1.75rem !important;
    letter-spacing: 0.06em !important;
    color: var(--cyan) !important;
    text-shadow: 0 0 20px rgba(0,212,255,0.5), 0 0 60px rgba(0,212,255,0.15) !important;
    line-height: 1.2 !important;
}
h2 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1.1rem !important;
    color: var(--text-primary) !important;
    letter-spacing: 0.02em !important;
}
h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 500 !important;
    color: var(--text-secondary) !important;
}
p, li, span, label {
    font-family: 'Space Grotesk', sans-serif !important;
    color: var(--text-secondary) !important;
    line-height: 1.65 !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: var(--deep) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"]::after {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 1px; height: 100%;
    background: linear-gradient(180deg, transparent, var(--cyan), transparent);
    opacity: 0.25;
    animation: scanLine 5s linear infinite;
}
@keyframes scanLine {
    0%,100% { opacity:0.1; }
    50%     { opacity:0.4; }
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label {
    color: var(--text-secondary) !important;
    font-family: 'Space Grotesk', sans-serif !important;
}
[data-testid="stSidebar"] .stRadio label {
    color: var(--text-secondary) !important;
    font-size: 0.83rem !important;
    letter-spacing: 0.03em !important;
    padding: 5px 0 !important;
    transition: color 0.2s, text-shadow 0.2s !important;
}
[data-testid="stSidebar"] .stRadio div[role="radio"][aria-checked="true"] label {
    color: var(--cyan) !important;
    text-shadow: 0 0 10px rgba(0,212,255,0.6) !important;
    font-weight: 600 !important;
}

/* Buttons */
.stButton > button {
    background: transparent !important;
    color: var(--cyan) !important;
    border: 1px solid var(--border-bright) !important;
    border-radius: var(--r) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.75rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    padding: 0.55rem 1.3rem !important;
    transition: all 0.25s ease !important;
}
.stButton > button:hover {
    border-color: var(--cyan) !important;
    box-shadow: 0 0 15px var(--cyan-glow), inset 0 0 12px var(--cyan-subtle) !important;
    transform: translateY(-1px) !important;
    text-shadow: 0 0 8px rgba(0,212,255,0.8) !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, rgba(0,212,255,0.15), rgba(0,153,204,0.08)) !important;
    border-color: var(--cyan) !important;
    box-shadow: 0 0 18px var(--cyan-glow) !important;
    font-weight: 600 !important;
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, rgba(0,212,255,0.25), rgba(0,153,204,0.15)) !important;
    box-shadow: 0 0 30px rgba(0,212,255,0.3), 0 0 60px rgba(0,212,255,0.1) !important;
    transform: translateY(-2px) !important;
}

/* Inputs */
.stTextInput > div > div > input,
.stTextArea textarea {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
    border-radius: var(--r) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.85rem !important;
    transition: all 0.2s !important;
    caret-color: var(--cyan) !important;
}
.stTextInput > div > div > input:focus,
.stTextArea textarea:focus {
    border-color: var(--cyan) !important;
    box-shadow: 0 0 0 1px var(--cyan), 0 0 18px var(--cyan-glow) !important;
    background: var(--elevated) !important;
}

/* Selectbox */
[data-baseweb="select"] > div {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r) !important;
    color: var(--text-primary) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    transition: border-color 0.2s !important;
}
[data-baseweb="select"] > div:hover {
    border-color: var(--border-bright) !important;
}
[data-baseweb="menu"] {
    background: var(--elevated) !important;
    border: 1px solid var(--border-bright) !important;
    border-radius: var(--r) !important;
}

/* Metrics */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, var(--surface), var(--elevated)) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r-lg) !important;
    padding: 1.2rem 1.4rem !important;
    position: relative !important;
    overflow: hidden !important;
    transition: border-color 0.3s, box-shadow 0.3s !important;
}
[data-testid="stMetric"]:hover {
    border-color: var(--border-bright) !important;
    box-shadow: 0 0 28px var(--cyan-glow) !important;
}
[data-testid="stMetric"]::before {
    content: '' !important;
    position: absolute !important;
    top: 0; left: 0; right: 0 !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, var(--cyan), transparent) !important;
    animation: shimmer 3s ease-in-out infinite !important;
}
@keyframes shimmer {
    0%,100% { opacity:0.3; transform:scaleX(0.6); }
    50%     { opacity:1;   transform:scaleX(1); }
}
[data-testid="stMetricLabel"] p {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.62rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    color: var(--text-secondary) !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Orbitron', monospace !important;
    font-weight: 700 !important;
    font-size: 1.65rem !important;
    color: var(--cyan) !important;
    text-shadow: 0 0 14px rgba(0,212,255,0.4) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: var(--deep) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r-lg) !important;
    padding: 4px !important;
    gap: 2px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-secondary) !important;
    border-radius: var(--r) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.7rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    padding: 0.5rem 1rem !important;
    transition: all 0.2s !important;
    border: none !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: var(--cyan) !important;
    background: var(--cyan-subtle) !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(0,212,255,0.12), rgba(0,212,255,0.05)) !important;
    color: var(--cyan) !important;
    font-weight: 600 !important;
    box-shadow: inset 0 1px 0 rgba(0,212,255,0.3), 0 0 12px rgba(0,212,255,0.08) !important;
    text-shadow: 0 0 10px rgba(0,212,255,0.6) !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: var(--r-lg) !important;
    overflow: hidden !important;
    background: var(--surface) !important;
}
[data-testid="stDataFrame"] th {
    background: var(--deep) !important;
    color: var(--cyan) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    border-bottom: 1px solid var(--border-bright) !important;
    padding: 10px 12px !important;
}
[data-testid="stDataFrame"] td {
    color: var(--text-primary) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.8rem !important;
    border-bottom: 1px solid var(--border) !important;
    padding: 8px 12px !important;
}
[data-testid="stDataFrame"] tr:hover td {
    background: var(--cyan-subtle) !important;
}

/* Alerts */
.stSuccess > div {
    background: rgba(0,255,136,0.04) !important;
    border: 1px solid rgba(0,255,136,0.2) !important;
    border-left: 3px solid var(--green) !important;
    border-radius: var(--r) !important;
    color: var(--green) !important;
}
.stWarning > div {
    background: rgba(255,170,0,0.04) !important;
    border: 1px solid rgba(255,170,0,0.2) !important;
    border-left: 3px solid var(--amber) !important;
    border-radius: var(--r) !important;
    color: var(--amber) !important;
}
.stError > div {
    background: rgba(255,68,102,0.04) !important;
    border: 1px solid rgba(255,68,102,0.2) !important;
    border-left: 3px solid var(--red) !important;
    border-radius: var(--r) !important;
    color: var(--red) !important;
}
.stInfo > div {
    background: rgba(0,212,255,0.04) !important;
    border: 1px solid var(--border-bright) !important;
    border-left: 3px solid var(--cyan) !important;
    border-radius: var(--r) !important;
    color: var(--cyan) !important;
}

/* Expander */
.streamlit-expanderHeader {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r) !important;
    color: var(--text-secondary) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.06em !important;
    transition: all 0.2s !important;
}
.streamlit-expanderHeader:hover {
    border-color: var(--border-bright) !important;
    color: var(--cyan) !important;
    box-shadow: 0 0 12px var(--cyan-glow) !important;
}
.streamlit-expanderContent {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
    border-radius: 0 0 var(--r) var(--r) !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: var(--surface) !important;
    border: 1.5px dashed var(--border-bright) !important;
    border-radius: var(--r-xl) !important;
    transition: all 0.3s !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--cyan) !important;
    background: var(--cyan-subtle) !important;
    box-shadow: 0 0 30px var(--cyan-glow) !important;
}

/* Code */
.stCode, code, pre {
    background: var(--deep) !important;
    border: 1px solid var(--border) !important;
    color: var(--cyan) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.78rem !important;
    border-radius: var(--r) !important;
    line-height: 1.6 !important;
}

/* Divider */
hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, var(--border-bright), transparent) !important;
    margin: 1.5rem 0 !important;
}

/* Caption */
.stCaption p {
    color: var(--text-secondary) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.08em !important;
}

/* Spinner */
.stSpinner > div {
    border-top-color: var(--cyan) !important;
    filter: drop-shadow(0 0 6px var(--cyan)) !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--void); }
::-webkit-scrollbar-thumb { background: var(--border-bright); border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: var(--cyan-dim); }

/* Radio */
.stRadio div[role="radio"] label {
    color: var(--text-secondary) !important;
    transition: color 0.15s !important;
}
.stRadio div[role="radio"][aria-checked="true"] label {
    color: var(--cyan) !important;
    font-weight: 600 !important;
    text-shadow: 0 0 10px rgba(0,212,255,0.5) !important;
}

/* Markdown */
.stMarkdown p { color: var(--text-secondary) !important; font-size: 0.88rem !important; }
.stMarkdown strong { color: var(--text-primary) !important; font-weight: 600 !important; }

/* Progress */
.stProgress > div > div {
    background: linear-gradient(90deg, var(--cyan-dim), var(--cyan)) !important;
    box-shadow: 0 0 8px var(--cyan-glow) !important;
}
.stProgress > div { background: var(--surface) !important; }

/* Hide Streamlit chrome */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }
.stDeployButton { display: none; }

/* Main container */
.main .block-container {
    padding-top: 2rem !important;
    padding-bottom: 3rem !important;
    max-width: 1200px !important;
}
</style>
"""

# ── Reusable components ───────────────────────────────────────────────────────

def page_header(title, subtitle=""):
    sub = f'<div style="font-family:JetBrains Mono,monospace;font-size:0.68rem;letter-spacing:0.1em;text-transform:uppercase;color:#5a8fa8;margin-top:8px;">{subtitle}</div>' if subtitle else ""
    return f"""
    <div style="margin-bottom:2rem;padding-bottom:1.5rem;border-bottom:1px solid rgba(0,212,255,0.1);">
        <div style="font-family:JetBrains Mono,monospace;font-size:0.58rem;letter-spacing:0.2em;text-transform:uppercase;color:#1e3a4a;margin-bottom:8px;">◈ ECOCREDITS / MODULE</div>
        <h1 style="font-family:Orbitron,monospace;font-size:1.6rem;font-weight:700;color:#00d4ff;letter-spacing:0.05em;text-shadow:0 0 20px rgba(0,212,255,0.5);margin:0;">{title}</h1>
        {sub}
    </div>"""


def stat_card(label, value, color="#00d4ff", icon="◈"):
    return f"""
    <div style="background:linear-gradient(135deg,#0a1628,#0f2040);border:1px solid rgba(0,212,255,0.1);border-radius:14px;padding:1.2rem 1.4rem;position:relative;overflow:hidden;">
        <div style="position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,{color},transparent);opacity:0.5;"></div>
        <div style="font-family:JetBrains Mono,monospace;font-size:0.6rem;letter-spacing:0.15em;text-transform:uppercase;color:#5a8fa8;margin-bottom:10px;">{icon} {label}</div>
        <div style="font-family:Orbitron,monospace;font-size:1.65rem;font-weight:700;color:{color};text-shadow:0 0 14px {color}66;line-height:1;">{value}</div>
    </div>"""