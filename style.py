css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;500;600&family=Orbitron:wght@400;500;600;700;800;900&display=swap');

:root {
    --void:          #000000;
    --deep:          #050a05;
    --surface:       #0a140a;
    --elevated:      #0f1e0f;
    --emerald:       #10b981;
    --emerald-bright:#34d399;
    --emerald-dim:   #059669;
    --emerald-glow:  rgba(16,185,129,0.15);
    --emerald-subtle:rgba(16,185,129,0.06);
    --gold:          #f59e0b;
    --gold-bright:   #fbbf24;
    --gold-dim:      #d97706;
    --gold-glow:     rgba(245,158,11,0.15);
    --gold-subtle:   rgba(245,158,11,0.06);
    --green:         #22c55e;
    --red:           #ef4444;
    --blue:          #3b82f6;
    --text-primary:  #f0fdf4;
    --text-secondary:#6b9e7e;
    --text-muted:    #1a3a1a;
    --border:        rgba(16,185,129,0.1);
    --border-bright: rgba(16,185,129,0.3);
    --border-gold:   rgba(245,158,11,0.3);
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
        linear-gradient(rgba(16,185,129,0.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(16,185,129,0.025) 1px, transparent 1px);
    background-size: 48px 48px;
    pointer-events: none;
    z-index: 0;
    animation: gridPulse 10s ease-in-out infinite;
}
@keyframes gridPulse {
    0%,100% { opacity:0.3; }
    50%     { opacity:0.8; }
}

/* Spotlight */
.stApp::after {
    content: '';
    position: fixed;
    top: -25%; left: 50%;
    transform: translateX(-50%);
    width: 60vw; height: 50vh;
    background: radial-gradient(ellipse, rgba(16,185,129,0.04) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
    animation: spotPulse 8s ease-in-out infinite;
}
@keyframes spotPulse {
    0%,100% { opacity:0.4; }
    50%     { opacity:1; }
}

/* Typography */
h1 {
    font-family: 'Orbitron', monospace !important;
    font-weight: 800 !important;
    font-size: 1.7rem !important;
    letter-spacing: 0.06em !important;
    background: linear-gradient(135deg, var(--emerald-bright), var(--gold)) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    line-height: 1.2 !important;
}
h2 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1.1rem !important;
    color: var(--text-primary) !important;
}
h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 500 !important;
    color: var(--text-secondary) !important;
}
p, li { color: var(--text-secondary) !important; line-height: 1.65 !important; }

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
    background: linear-gradient(180deg, transparent, var(--emerald), transparent);
    opacity: 0.3;
    animation: scanLine 5s ease-in-out infinite;
}
@keyframes scanLine { 0%,100%{opacity:0.1;} 50%{opacity:0.4;} }

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label {
    color: var(--text-secondary) !important;
    font-family: 'Space Grotesk', sans-serif !important;
}
[data-testid="stSidebar"] .stRadio label {
    color: var(--text-secondary) !important;
    font-size: 0.85rem !important;
    padding: 5px 0 !important;
    transition: color 0.2s !important;
}
[data-testid="stSidebar"] .stRadio div[role="radio"][aria-checked="true"] label {
    color: var(--emerald-bright) !important;
    text-shadow: 0 0 10px rgba(52,211,153,0.5) !important;
    font-weight: 600 !important;
}

/* Buttons — NO overlap, full width stacking */
.stButton > button {
    background: transparent !important;
    color: var(--emerald-bright) !important;
    border: 1px solid var(--border-bright) !important;
    border-radius: var(--r) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.73rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    padding: 0.55rem 1rem !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
    display: block !important;
    margin-bottom: 6px !important;
}
.stButton > button:hover {
    border-color: var(--emerald-bright) !important;
    background: var(--emerald-subtle) !important;
    box-shadow: 0 0 15px var(--emerald-glow) !important;
    transform: translateY(-1px) !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, rgba(16,185,129,0.2), rgba(5,150,105,0.1)) !important;
    border-color: var(--emerald-bright) !important;
    color: var(--emerald-bright) !important;
    box-shadow: 0 0 16px var(--emerald-glow) !important;
    font-weight: 600 !important;
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, rgba(16,185,129,0.3), rgba(5,150,105,0.2)) !important;
    box-shadow: 0 0 28px rgba(16,185,129,0.3) !important;
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
    caret-color: var(--emerald-bright) !important;
}
.stTextInput > div > div > input:focus,
.stTextArea textarea:focus {
    border-color: var(--emerald-bright) !important;
    box-shadow: 0 0 0 1px var(--emerald-bright), 0 0 16px var(--emerald-glow) !important;
    background: var(--elevated) !important;
}

/* Selectbox */
[data-baseweb="select"] > div {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r) !important;
    color: var(--text-primary) !important;
    font-family: 'Space Grotesk', sans-serif !important;
}
[data-baseweb="select"] > div:hover { border-color: var(--border-bright) !important; }
[data-baseweb="menu"] {
    background: var(--elevated) !important;
    border: 1px solid var(--border-bright) !important;
    border-radius: var(--r) !important;
}

/* Metrics — gold accent */
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
    border-color: var(--border-gold) !important;
    box-shadow: 0 0 24px var(--gold-glow) !important;
}
[data-testid="stMetric"]::before {
    content: '' !important;
    position: absolute !important;
    top: 0; left: 0; right: 0 !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, var(--gold), transparent) !important;
    animation: shimmer 4s ease-in-out infinite !important;
}
@keyframes shimmer {
    0%,100%{ opacity:0.3; transform:scaleX(0.5); }
    50%    { opacity:1;   transform:scaleX(1); }
}
[data-testid="stMetricLabel"] p {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.62rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: var(--text-secondary) !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Orbitron', monospace !important;
    font-weight: 700 !important;
    font-size: 1.6rem !important;
    color: var(--gold-bright) !important;
    text-shadow: 0 0 12px rgba(251,191,36,0.4) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: var(--deep) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r-lg) !important;
    padding: 4px !important;
    gap: 2px !important;
    flex-wrap: wrap !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-secondary) !important;
    border-radius: var(--r) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.68rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    padding: 0.45rem 0.8rem !important;
    transition: all 0.2s !important;
    border: none !important;
    white-space: nowrap !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: var(--emerald-bright) !important;
    background: var(--emerald-subtle) !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(16,185,129,0.15), rgba(16,185,129,0.06)) !important;
    color: var(--emerald-bright) !important;
    font-weight: 600 !important;
    box-shadow: inset 0 1px 0 rgba(16,185,129,0.3) !important;
    text-shadow: 0 0 10px rgba(52,211,153,0.5) !important;
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
    color: var(--emerald-bright) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.1em !important;
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
    background: var(--emerald-subtle) !important;
}

/* Alerts */
.stSuccess > div {
    background: rgba(34,197,94,0.04) !important;
    border: 1px solid rgba(34,197,94,0.25) !important;
    border-left: 3px solid var(--green) !important;
    border-radius: var(--r) !important;
    color: var(--green) !important;
}
.stWarning > div {
    background: rgba(245,158,11,0.04) !important;
    border: 1px solid rgba(245,158,11,0.25) !important;
    border-left: 3px solid var(--gold) !important;
    border-radius: var(--r) !important;
    color: var(--gold) !important;
}
.stError > div {
    background: rgba(239,68,68,0.04) !important;
    border: 1px solid rgba(239,68,68,0.25) !important;
    border-left: 3px solid var(--red) !important;
    border-radius: var(--r) !important;
    color: var(--red) !important;
}
.stInfo > div {
    background: rgba(16,185,129,0.04) !important;
    border: 1px solid var(--border-bright) !important;
    border-left: 3px solid var(--emerald-bright) !important;
    border-radius: var(--r) !important;
    color: var(--emerald-bright) !important;
}

/* Expander */
.streamlit-expanderHeader {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r) !important;
    color: var(--text-secondary) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.75rem !important;
    transition: all 0.2s !important;
}
.streamlit-expanderHeader:hover {
    border-color: var(--border-bright) !important;
    color: var(--emerald-bright) !important;
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
    border-color: var(--emerald-bright) !important;
    background: var(--emerald-subtle) !important;
    box-shadow: 0 0 24px var(--emerald-glow) !important;
}

/* Code */
.stCode, code, pre {
    background: var(--deep) !important;
    border: 1px solid var(--border) !important;
    color: var(--emerald-bright) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.78rem !important;
    border-radius: var(--r) !important;
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
    border-top-color: var(--emerald-bright) !important;
    filter: drop-shadow(0 0 6px var(--emerald-bright)) !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--void); }
::-webkit-scrollbar-thumb { background: var(--border-bright); border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: var(--emerald); }

/* Radio */
.stRadio div[role="radio"] label { color: var(--text-secondary) !important; }
.stRadio div[role="radio"][aria-checked="true"] label {
    color: var(--emerald-bright) !important;
    font-weight: 600 !important;
}

/* Markdown */
.stMarkdown p { color: var(--text-secondary) !important; font-size: 0.88rem !important; }
.stMarkdown strong { color: var(--text-primary) !important; font-weight: 600 !important; }

/* Progress */
.stProgress > div > div {
    background: linear-gradient(90deg, var(--emerald-dim), var(--emerald-bright)) !important;
    box-shadow: 0 0 8px var(--emerald-glow) !important;
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


def page_title(title):
    return f"""
    <div style="margin-bottom:1.5rem;">
        <h1 style="font-family:Orbitron,monospace;font-size:1.6rem;font-weight:800;
                   background:linear-gradient(135deg,#34d399,#f59e0b);
                   -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                   background-clip:text;letter-spacing:0.05em;margin:0;">
            {title}
        </h1>
    </div>"""


def stat_card(label, value, color="#f59e0b", icon="◈"):
    return f"""
    <div style="background:linear-gradient(135deg,#0a140a,#0f1e0f);
                border:1px solid rgba(16,185,129,0.12);border-radius:14px;
                padding:1.2rem 1.4rem;position:relative;overflow:hidden;margin-bottom:8px;">
        <div style="position:absolute;top:0;left:0;right:0;height:1px;
                    background:linear-gradient(90deg,transparent,{color},transparent);opacity:0.6;"></div>
        <div style="font-family:JetBrains Mono,monospace;font-size:0.6rem;
                    letter-spacing:0.15em;text-transform:uppercase;color:#6b9e7e;margin-bottom:8px;">
            {icon} {label}
        </div>
        <div style="font-family:Orbitron,monospace;font-size:1.6rem;
                    font-weight:700;color:{color};text-shadow:0 0 12px {color}66;line-height:1;">
            {value}
        </div>
    </div>"""