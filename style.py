css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;500;600&family=Orbitron:wght@400;500;600;700;800;900&display=swap');

/* ═══════════════════════════════════════════════════
   DESIGN TOKENS
═══════════════════════════════════════════════════ */
:root {
    --void:         #020408;
    --deep:         #060d14;
    --surface:      #0a1628;
    --elevated:     #0f2040;
    --glass:        rgba(15,32,64,0.6);
    --glass-light:  rgba(255,255,255,0.02);

    --cyan:         #00d4ff;
    --cyan-dim:     #0099cc;
    --cyan-glow:    rgba(0,212,255,0.15);
    --cyan-subtle:  rgba(0,212,255,0.06);

    --gold:         #ffd700;
    --gold-dim:     #cc9900;
    --gold-glow:    rgba(255,215,0,0.12);

    --green:        #00ff88;
    --green-dim:    rgba(0,255,136,0.15);
    --red:          #ff4466;
    --red-dim:      rgba(255,68,102,0.12);
    --amber:        #ffaa00;
    --purple:       #8b5cf6;

    --text-primary:   #e8f4f8;
    --text-secondary: #5a8fa8;
    --text-muted:     #1e3a4a;
    --text-dim:       #0d2030;

    --border:       rgba(0,212,255,0.08);
    --border-bright:rgba(0,212,255,0.25);
    --border-glow:  rgba(0,212,255,0.4);

    --r:    8px;
    --r-lg: 14px;
    --r-xl: 20px;
}

/* ═══════════════════════════════════════════════════
   RESET
═══════════════════════════════════════════════════ */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

/* ═══════════════════════════════════════════════════
   BASE — animated grid background
═══════════════════════════════════════════════════ */
.stApp {
    background: var(--void);
    color: var(--text-primary);
    font-family: 'Space Grotesk', sans-serif;
    font-size: 14px;
    min-height: 100vh;
}

/* Animated grid overlay */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(0,212,255,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,212,255,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
    animation: gridPulse 8s ease-in-out infinite;
}

@keyframes gridPulse {
    0%, 100% { opacity: 0.4; }
    50%       { opacity: 0.8; }
}

/* Radial gradient spotlight */
.stApp::after {
    content: '';
    position: fixed;
    top: -30%;
    left: 50%;
    transform: translateX(-50%);
    width: 80vw;
    height: 60vh;
    background: radial-gradient(ellipse, rgba(0,212,255,0.04) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
    animation: spotPulse 6s ease-in-out infinite;
}

@keyframes spotPulse {
    0%, 100% { opacity: 0.5; transform: translateX(-50%) scale(1); }
    50%       { opacity: 1;   transform: translateX(-50%) scale(1.1); }
}

/* ═══════════════════════════════════════════════════
   TYPOGRAPHY
═══════════════════════════════════════════════════ */
h1 {
    font-family: 'Orbitron', monospace !important;
    font-weight: 700 !important;
    font-size: 1.8rem !important;
    letter-spacing: 0.05em !important;
    color: var(--cyan) !important;
    text-shadow:
        0 0 20px rgba(0,212,255,0.5),
        0 0 60px rgba(0,212,255,0.2) !important;
    line-height: 1.2 !important;
}

h2 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1.15rem !important;
    color: var(--text-primary) !important;
    letter-spacing: 0.02em !important;
}

h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 500 !important;
    font-size: 1rem !important;
    color: var(--text-secondary) !important;
}

p, li, span, label {
    font-family: 'Space Grotesk', sans-serif !important;
    color: var(--text-secondary) !important;
    line-height: 1.6 !important;
}

/* ═══════════════════════════════════════════════════
   SIDEBAR — dark panel with cyan accent line
═══════════════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: var(--deep) !important;
    border-right: 1px solid var(--border) !important;
    position: relative;
}

[data-testid="stSidebar"]::after {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 1px; height: 100%;
    background: linear-gradient(
        180deg,
        transparent 0%,
        var(--cyan) 30%,
        var(--cyan-dim) 70%,
        transparent 100%
    );
    opacity: 0.3;
    animation: scanLine 4s linear infinite;
}

@keyframes scanLine {
    0%   { opacity: 0.1; }
    50%  { opacity: 0.5; }
    100% { opacity: 0.1; }
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div {
    font-family: 'Space Grotesk', sans-serif !important;
    color: var(--text-secondary) !important;
}

[data-testid="stSidebar"] .stRadio label {
    color: var(--text-secondary) !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.03em !important;
    padding: 6px 0 !important;
    transition: color 0.2s, text-shadow 0.2s !important;
}

[data-testid="stSidebar"] .stRadio div[role="radio"][aria-checked="true"] label {
    color: var(--cyan) !important;
    text-shadow: 0 0 12px rgba(0,212,255,0.6) !important;
    font-weight: 600 !important;
}

/* ═══════════════════════════════════════════════════
   BUTTONS
═══════════════════════════════════════════════════ */
.stButton > button {
    background: transparent !important;
    color: var(--cyan) !important;
    border: 1px solid var(--border-bright) !important;
    border-radius: var(--r) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    padding: 0.6rem 1.4rem !important;
    transition: all 0.25s ease !important;
    position: relative !important;
    overflow: hidden !important;
}

.stButton > button::before {
    content: '';
    position: absolute;
    inset: 0;
    background: var(--cyan-subtle);
    opacity: 0;
    transition: opacity 0.2s;
}

.stButton > button:hover {
    border-color: var(--cyan) !important;
    box-shadow:
        0 0 15px var(--cyan-glow),
        inset 0 0 15px var(--cyan-subtle) !important;
    transform: translateY(-1px) !important;
    text-shadow: 0 0 8px rgba(0,212,255,0.8) !important;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(
        135deg,
        rgba(0,212,255,0.15),
        rgba(0,153,204,0.1)
    ) !important;
    border-color: var(--cyan) !important;
    color: var(--cyan) !important;
    box-shadow: 0 0 20px var(--cyan-glow) !important;
    font-weight: 600 !important;
}

.stButton > button[kind="primary"]:hover {
    background: linear-gradient(
        135deg,
        rgba(0,212,255,0.25),
        rgba(0,153,204,0.2)
    ) !important;
    box-shadow:
        0 0 30px rgba(0,212,255,0.3),
        0 0 60px rgba(0,212,255,0.1),
        inset 0 0 20px rgba(0,212,255,0.1) !important;
    transform: translateY(-2px) !important;
}

/* ═══════════════════════════════════════════════════
   INPUTS
═══════════════════════════════════════════════════ */
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
    box-shadow:
        0 0 0 1px var(--cyan),
        0 0 20px var(--cyan-glow) !important;
    background: var(--elevated) !important;
}

.stTextInput > div > div > input::placeholder {
    color: var(--text-muted) !important;
}

/* ═══════════════════════════════════════════════════
   SELECTBOX
═══════════════════════════════════════════════════ */
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

/* ═══════════════════════════════════════════════════
   METRICS — holographic cards
═══════════════════════════════════════════════════ */
[data-testid="stMetric"] {
    background: linear-gradient(
        135deg,
        var(--surface) 0%,
        var(--elevated) 100%
    ) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r-lg) !important;
    padding: 1.2rem 1.4rem !important;
    position: relative !important;
    overflow: hidden !important;
    transition: border-color 0.3s, box-shadow 0.3s !important;
}

[data-testid="stMetric"]:hover {
    border-color: var(--border-bright) !important;
    box-shadow: 0 0 30px var(--cyan-glow) !important;
}

/* Top glow line */
[data-testid="stMetric"]::before {
    content: '' !important;
    position: absolute !important;
    top: 0; left: 0; right: 0 !important;
    height: 1px !important;
    background: linear-gradient(
        90deg,
        transparent,
        var(--cyan),
        transparent
    ) !important;
    animation: shimmer 3s ease-in-out infinite !important;
}

@keyframes shimmer {
    0%   { opacity: 0.3; transform: scaleX(0.5); }
    50%  { opacity: 1;   transform: scaleX(1); }
    100% { opacity: 0.3; transform: scaleX(0.5); }
}

/* Corner decoration */
[data-testid="stMetric"]::after {
    content: '' !important;
    position: absolute !important;
    bottom: 0; right: 0 !important;
    width: 30px; height: 30px !important;
    border-bottom: 1px solid var(--border-bright) !important;
    border-right: 1px solid var(--border-bright) !important;
    border-radius: 0 0 var(--r-lg) 0 !important;
    opacity: 0.4 !important;
}

[data-testid="stMetricLabel"] p {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.65rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: var(--text-secondary) !important;
}

[data-testid="stMetricValue"] {
    font-family: 'Orbitron', monospace !important;
    font-weight: 700 !important;
    font-size: 1.7rem !important;
    color: var(--cyan) !important;
    text-shadow: 0 0 15px rgba(0,212,255,0.4) !important;
}

/* ═══════════════════════════════════════════════════
   TABS
═══════════════════════════════════════════════════ */
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
    font-size: 0.72rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.08em !important;
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
    background: linear-gradient(
        135deg,
        rgba(0,212,255,0.12),
        rgba(0,212,255,0.06)
    ) !important;
    color: var(--cyan) !important;
    font-weight: 600 !important;
    box-shadow:
        inset 0 1px 0 rgba(0,212,255,0.3),
        0 0 15px rgba(0,212,255,0.1) !important;
    text-shadow: 0 0 10px rgba(0,212,255,0.6) !important;
}

/* ═══════════════════════════════════════════════════
   DATAFRAME — terminal style
═══════════════════════════════════════════════════ */
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
    font-weight: 600 !important;
    font-size: 0.68rem !important;
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
    background: var(--cyan-subtle) !important;
    color: var(--cyan) !important;
}

/* ═══════════════════════════════════════════════════
   ALERTS
═══════════════════════════════════════════════════ */
.stSuccess > div {
    background: rgba(0,255,136,0.04) !important;
    border: 1px solid rgba(0,255,136,0.25) !important;
    border-left: 3px solid var(--green) !important;
    border-radius: var(--r) !important;
    color: var(--green) !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

.stWarning > div {
    background: rgba(255,170,0,0.04) !important;
    border: 1px solid rgba(255,170,0,0.25) !important;
    border-left: 3px solid var(--amber) !important;
    border-radius: var(--r) !important;
    color: var(--amber) !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

.stError > div {
    background: rgba(255,68,102,0.04) !important;
    border: 1px solid rgba(255,68,102,0.25) !important;
    border-left: 3px solid var(--red) !important;
    border-radius: var(--r) !important;
    color: var(--red) !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

.stInfo > div {
    background: rgba(0,212,255,0.04) !important;
    border: 1px solid var(--border-bright) !important;
    border-left: 3px solid var(--cyan) !important;
    border-radius: var(--r) !important;
    color: var(--cyan) !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

/* ═══════════════════════════════════════════════════
   EXPANDER
═══════════════════════════════════════════════════ */
.streamlit-expanderHeader {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r) !important;
    color: var(--text-secondary) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.05em !important;
    transition: all 0.2s !important;
}

.streamlit-expanderHeader:hover {
    border-color: var(--border-bright) !important;
    color: var(--cyan) !important;
    box-shadow: 0 0 15px var(--cyan-glow) !important;
}

.streamlit-expanderContent {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
    border-radius: 0 0 var(--r) var(--r) !important;
}

/* ═══════════════════════════════════════════════════
   FILE UPLOADER
═══════════════════════════════════════════════════ */
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

/* ═══════════════════════════════════════════════════
   CODE BLOCKS
═══════════════════════════════════════════════════ */
.stCode, code, pre {
    background: var(--deep) !important;
    border: 1px solid var(--border) !important;
    color: var(--cyan) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.78rem !important;
    border-radius: var(--r) !important;
    line-height: 1.6 !important;
}

/* ═══════════════════════════════════════════════════
   DIVIDER
═══════════════════════════════════════════════════ */
hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(
        90deg,
        transparent,
        var(--border-bright),
        transparent
    ) !important;
    margin: 1.5rem 0 !important;
}

/* ═══════════════════════════════════════════════════
   CAPTION
═══════════════════════════════════════════════════ */
.stCaption p {
    color: var(--text-secondary) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.08em !important;
}

/* ═══════════════════════════════════════════════════
   SPINNER
═══════════════════════════════════════════════════ */
.stSpinner > div {
    border-top-color: var(--cyan) !important;
    filter: drop-shadow(0 0 6px var(--cyan)) !important;
}

/* ═══════════════════════════════════════════════════
   SCROLLBAR
═══════════════════════════════════════════════════ */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--void); }
::-webkit-scrollbar-thumb {
    background: var(--border-bright);
    border-radius: 2px;
}
::-webkit-scrollbar-thumb:hover { background: var(--cyan-dim); }

/* ═══════════════════════════════════════════════════
   RADIO
═══════════════════════════════════════════════════ */
.stRadio div[role="radio"] label {
    color: var(--text-secondary) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    transition: color 0.15s !important;
}

.stRadio div[role="radio"][aria-checked="true"] label {
    color: var(--cyan) !important;
    font-weight: 600 !important;
    text-shadow: 0 0 10px rgba(0,212,255,0.5) !important;
}

/* ═══════════════════════════════════════════════════
   CHECKBOX
═══════════════════════════════════════════════════ */
.stCheckbox label {
    color: var(--text-secondary) !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

/* ═══════════════════════════════════════════════════
   MARKDOWN GENERAL
═══════════════════════════════════════════════════ */
.stMarkdown p {
    color: var(--text-secondary) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.88rem !important;
}

/* Bold in markdown */
.stMarkdown strong {
    color: var(--text-primary) !important;
    font-weight: 600 !important;
}

/* ═══════════════════════════════════════════════════
   LOGIN PAGE SPECIAL
═══════════════════════════════════════════════════ */
.login-container {
    background: linear-gradient(135deg, var(--surface), var(--elevated));
    border: 1px solid var(--border-bright);
    border-radius: var(--r-xl);
    padding: 2.5rem;
    box-shadow: 0 0 60px var(--cyan-glow), inset 0 1px 0 rgba(0,212,255,0.1);
    position: relative;
    overflow: hidden;
}

/* ═══════════════════════════════════════════════════
   UTILITY CLASSES
═══════════════════════════════════════════════════ */

/* Glowing status badges */
.badge-online {
    display: inline-block;
    width: 6px; height: 6px;
    background: var(--green);
    border-radius: 50%;
    box-shadow: 0 0 8px var(--green);
    animation: blink 2s ease-in-out infinite;
    margin-right: 6px;
}

@keyframes blink {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.3; }
}

/* Terminal-style label */
.sys-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--text-secondary);
    margin-bottom: 4px;
}

/* Cyan text glow */
.glow-text {
    color: var(--cyan);
    text-shadow: 0 0 15px rgba(0,212,255,0.7);
    font-family: 'Orbitron', monospace;
}

/* Data card */
.data-card {
    background: linear-gradient(135deg, var(--surface), var(--elevated));
    border: 1px solid var(--border);
    border-radius: var(--r-lg);
    padding: 1.2rem 1.5rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s, box-shadow 0.3s;
}

.data-card:hover {
    border-color: var(--border-bright);
    box-shadow: 0 0 25px var(--cyan-glow);
}

.data-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--cyan), transparent);
    opacity: 0.4;
}

/* ═══════════════════════════════════════════════════
   SECTION DIVIDERS
═══════════════════════════════════════════════════ */
.section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--text-secondary);
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 1.5rem 0 1rem;
}

.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, var(--border-bright), transparent);
}

/* ═══════════════════════════════════════════════════
   HIDE STREAMLIT CHROME
═══════════════════════════════════════════════════ */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }
.stDeployButton { display: none; }

/* ═══════════════════════════════════════════════════
   MAIN CONTENT AREA
═══════════════════════════════════════════════════ */
.main .block-container {
    padding-top: 2rem !important;
    padding-bottom: 3rem !important;
    max-width: 1200px !important;
}

/* ═══════════════════════════════════════════════════
   PROGRESS / LOADING BARS
═══════════════════════════════════════════════════ */
.stProgress > div > div {
    background: linear-gradient(90deg, var(--cyan-dim), var(--cyan)) !important;
    box-shadow: 0 0 10px var(--cyan-glow) !important;
    border-radius: 2px !important;
}

.stProgress > div {
    background: var(--surface) !important;
    border-radius: 2px !important;
}

</style>
"""


# ═══════════════════════════════════════════════════
# REUSABLE HTML COMPONENTS
# ═══════════════════════════════════════════════════

def page_header(title, subtitle="", icon=""):
    sub_html = f"""
    <div style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;
                letter-spacing:0.12em;text-transform:uppercase;
                color:#5a8fa8;margin-top:8px;">
        {subtitle}
    </div>""" if subtitle else ""

    return f"""
    <div style="margin-bottom:2rem;padding-bottom:1.5rem;
                border-bottom:1px solid rgba(0,212,255,0.1);">
        <div style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;
                    letter-spacing:0.2em;text-transform:uppercase;
                    color:#1e3a4a;margin-bottom:8px;">
            ◈ SYSTEM / MODULE
        </div>
        <h1 style="font-family:'Orbitron',monospace !important;
                   font-size:1.6rem !important;font-weight:700 !important;
                   color:#00d4ff !important;letter-spacing:0.05em !important;
                   text-shadow:0 0 20px rgba(0,212,255,0.5),0 0 60px rgba(0,212,255,0.2) !important;
                   margin:0 !important;">
            {icon} {title}
        </h1>
        {sub_html}
    </div>
    """


def stat_card(label, value, color="#00d4ff", icon="◈", sublabel=""):
    sub = f'<div style="font-size:0.65rem;color:#1e3a4a;font-family:\'JetBrains Mono\',monospace;margin-top:4px;">{sublabel}</div>' if sublabel else ""
    return f"""
    <div style="
        background:linear-gradient(135deg,#0a1628,#0f2040);
        border:1px solid rgba(0,212,255,0.1);
        border-radius:14px;
        padding:1.2rem 1.4rem;
        position:relative;
        overflow:hidden;
        transition:border-color 0.3s,box-shadow 0.3s;
    ">
        <div style="position:absolute;top:0;left:0;right:0;height:1px;
                    background:linear-gradient(90deg,transparent,{color},transparent);
                    opacity:0.5;"></div>
        <div style="position:absolute;bottom:0;right:0;width:20px;height:20px;
                    border-bottom:1px solid rgba(0,212,255,0.2);
                    border-right:1px solid rgba(0,212,255,0.2);
                    border-radius:0 0 14px 0;"></div>
        <div style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;
                    letter-spacing:0.15em;text-transform:uppercase;
                    color:#5a8fa8;margin-bottom:10px;">
            {icon} {label}
        </div>
        <div style="font-family:'Orbitron',monospace;font-size:1.7rem;
                    font-weight:700;color:{color};
                    text-shadow:0 0 15px {color}66;line-height:1;">
            {value}
        </div>
        {sub}
    </div>
    """


def info_row(label, value, color="#5a8fa8"):
    return f"""
    <div style="display:flex;align-items:center;justify-content:space-between;
                padding:8px 0;border-bottom:1px solid rgba(0,212,255,0.05);">
        <span style="font-family:'JetBrains Mono',monospace;font-size:0.72rem;
                     letter-spacing:0.06em;text-transform:uppercase;color:#1e3a4a;">
            {label}
        </span>
        <span style="font-family:'JetBrains Mono',monospace;font-size:0.8rem;
                     color:{color};font-weight:600;">
            {value}
        </span>
    </div>
    """