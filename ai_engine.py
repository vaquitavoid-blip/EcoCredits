import re
import os
import shutil
import hashlib
import requests
import pytesseract

from bs4 import BeautifulSoup
from PIL import Image, ImageFilter, ImageEnhance, ImageOps

# ─────────────────────────────────────────────
# TESSERACT PATH
# ─────────────────────────────────────────────

if os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )
else:
    cloud_path = shutil.which("tesseract")
    if cloud_path:
        pytesseract.pytesseract.tesseract_cmd = cloud_path

# ─────────────────────────────────────────────
# IMAGE HASH
# ─────────────────────────────────────────────

def get_image_hash(image_path):
    with open(image_path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

# ─────────────────────────────────────────────
# IMAGE PREPROCESSING — 5 variants
# ─────────────────────────────────────────────

def preprocess_variants(image):
    variants = []
    gray = image.convert("L")

    # V1: high contrast + sharpen
    v1 = ImageEnhance.Contrast(gray).enhance(3.0)
    v1 = v1.filter(ImageFilter.SHARPEN)
    v1 = v1.resize((v1.width * 2, v1.height * 2), Image.LANCZOS)
    variants.append(v1)

    # V2: histogram equalize
    v2 = ImageOps.equalize(gray)
    v2 = v2.resize((v2.width * 2, v2.height * 2), Image.LANCZOS)
    variants.append(v2)

    # V3: medium contrast
    v3 = ImageEnhance.Contrast(gray).enhance(1.8)
    v3 = ImageEnhance.Sharpness(v3).enhance(2.0)
    v3 = v3.resize((v3.width * 2, v3.height * 2), Image.LANCZOS)
    variants.append(v3)

    # V4: raw upscale only
    v4 = gray.resize((gray.width * 2, gray.height * 2), Image.LANCZOS)
    variants.append(v4)

    # V5: inverted (dark background certs)
    v5 = ImageOps.invert(gray)
    v5 = ImageEnhance.Contrast(v5).enhance(2.5)
    v5 = v5.resize((v5.width * 2, v5.height * 2), Image.LANCZOS)
    variants.append(v5)

    return variants

# ─────────────────────────────────────────────
# OCR — 5 variants × 6 PSM modes
# ─────────────────────────────────────────────

PSM_CONFIGS = [
    "--psm 6",
    "--psm 4",
    "--psm 3",
    "--psm 11",
    "--psm 12",
    "--psm 1",
]


def extract_text(image_path):
    image    = Image.open(image_path)
    variants = preprocess_variants(image)

    seen_lines    = set()
    combined_lines = []

    for variant in variants:
        for cfg in PSM_CONFIGS:
            try:
                txt = pytesseract.image_to_string(variant, config=cfg)
                for line in txt.split("\n"):
                    line = line.strip()
                    if line and line.lower() not in seen_lines:
                        seen_lines.add(line.lower())
                        combined_lines.append(line)
            except Exception:
                pass

    return "\n".join(combined_lines)

# ─────────────────────────────────────────────
# TITLE EXTRACTION
# ─────────────────────────────────────────────

def extract_best_title(text):
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    if not lines:
        return ""

    title_keywords = [
        "certificate", "award", "competition", "olympiad",
        "achievement", "recognition", "excellence", "merit",
        "winner", "champion", "participation", "prize",
        "first place", "second place", "third place",
        "gold", "silver", "bronze", "distinction", "level",
    ]

    keyword_hits = []
    for line in lines:
        score = sum(kw in line.lower() for kw in title_keywords)
        if score > 0:
            keyword_hits.append((score, len(line), line))

    if keyword_hits:
        keyword_hits.sort(reverse=True)
        return keyword_hits[0][2]

    caps_lines = [l for l in lines if l.isupper() and len(l) > 8]
    if caps_lines:
        return max(caps_lines, key=len)

    return max(lines[:15], key=len)

# ─────────────────────────────────────────────
# SUBJECT ALIASES
# ─────────────────────────────────────────────

SUBJECT_ALIASES = {
    "Combined Science": ["combined science", "science (combined)", "sciences"],
    "Add Maths":        ["additional mathematics", "additional maths", "add maths", "add math"],
    "Extended Maths":   ["extended mathematics", "mathematics", "maths", "math"],
    "FLE":              ["first language english", "english first language", "fle"],
    "ESL":              ["english second language", "esl"],
    "Physics":          ["physics"],
    "Chemistry":        ["chemistry"],
    "Biology":          ["biology"],
    "ICT":              ["ict", "computer science", "computing", "information technology"],
    "Economics":        ["economics", "econ"],
    "Business Studies": ["business studies", "business"],
    "Accounting":       ["accounting", "accounts"],
    "DT":               ["design technology", "design and technology", "dt"],
    "Art and Design":   ["art and design", "art & design", "art"],
    "History":          ["history"],
    "Geography":        ["geography", "geog"],
    "Sociology":        ["sociology"],
    "Literature":       ["literature in english", "english literature", "literature"],
    "Psychology":       ["psychology"],
}

ALL_SUBJECTS = list(SUBJECT_ALIASES.keys())

# ─────────────────────────────────────────────
# GRADE DETECTION
# ─────────────────────────────────────────────

def detect_grades(text):
    detected = {}
    clean    = text.lower()

    for subject, aliases in SUBJECT_ALIASES.items():
        found = False
        for alias in aliases:
            patterns = [
                rf"{re.escape(alias)}[\s\S]{{0,30}}?\b(a\*|a|b|c|d)\b",
                rf"{re.escape(alias)}[\s\S]{{0,20}}?grade[\s:]+(a\*|a|b|c|d)",
                rf"{re.escape(alias)}[\s\S]{{0,60}}?(\d{{2,3}})\s*(?:/\s*100|%)",
            ]
            for pattern in patterns:
                match = re.search(pattern, clean, re.IGNORECASE)
                if match:
                    raw = match.group(1).strip().upper()
                    if raw.isdigit():
                        pct = int(raw)
                        if pct >= 90:   raw = "A*"
                        elif pct >= 80: raw = "A"
                        elif pct >= 70: raw = "B"
                        elif pct >= 60: raw = "C"
                        else:           raw = "D"
                    if raw in ("A*", "A", "B", "C", "D"):
                        detected[subject] = raw
                        found = True
                        break
            if found:
                break

    return detected

# ─────────────────────────────────────────────
# CATEGORY DETECTION
# ─────────────────────────────────────────────

def detect_category(text):
    t = text.lower()
    mapping = {
        "Creative Arts": ["essay","writing","poetry","debate","literature","story","art","drama","music"],
        "Technology":    ["coding","python","hackathon","robotics","programming","software","app","tech"],
        "Science":       ["science","research","biology","chemistry","physics","lab","experiment"],
        "Finance":       ["economics","business","finance","accounting","commerce","stock","banking"],
        "Mathematics":   ["math","mathematics","olympiad","statistics","calculus","algebra"],
        "Sports":        ["football","cricket","basketball","athletics","swimming","tennis","sports","game"],
    }
    scores = {cat: sum(w in t for w in words) for cat, words in mapping.items()}
    best   = max(scores, key=scores.get)
    return best if scores[best] > 0 else "Other"

# ─────────────────────────────────────────────
# TEACHER ASSIGNMENT
# ─────────────────────────────────────────────

def assign_teacher(category):
    mapping = {
        "Science":       "science_teacher",
        "Technology":    "cs_teacher",
        "Mathematics":   "maths_teacher",
        "Finance":       "business_teacher",
        "Creative Arts": "arts_teacher",
        "Sports":        "class_teacher",
        "Other":         "class_teacher",
    }
    return mapping.get(category, "class_teacher")

# ─────────────────────────────────────────────
# LEVEL KEYWORDS
# ─────────────────────────────────────────────

LEVEL_KEYWORDS = {
    "International": [
        "international","global","worldwide","world championship",
        "olympic","commonwealth","cambridge international",
        "unicef","unesco","multinational","across countries",
    ],
    "National": [
        "national","all india","nationwide","national finals",
        "national level","national competition","federal","country-wide",
    ],
    "State": [
        "state","statewide","state level","state championship",
        "state finals","provincial","state competition",
    ],
    "District": [
        "district","district level","zonal","zone level",
        "district finals","regional","inter-school","interschool",
        "inter school","district competition","area competition",
    ],
    "School": [
        "school","intra-school","house level",
        "within school","school competition","school level",
    ],
}

# ─────────────────────────────────────────────
# MULTI-PLATFORM SEARCH
# ─────────────────────────────────────────────

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def fetch_search(base_url, query, timeout=10):
    try:
        r = requests.get(
            base_url,
            params={"q": query},
            headers=HEADERS,
            timeout=timeout
        )
        soup = BeautifulSoup(r.text, "html.parser")
        return soup.get_text(" ", strip=True).lower()
    except Exception:
        return ""


def multi_search(query):
    """Search Google + Bing + DuckDuckGo and return combined text + log."""
    platforms = [
        ("https://www.google.com/search",     "Google"),
        ("https://www.bing.com/search",       "Bing"),
        ("https://html.duckduckgo.com/html/", "DuckDuckGo"),
    ]
    combined = ""
    log      = []
    for url, name in platforms:
        text = fetch_search(url, query)
        if text:
            combined += " " + text
            log.append(f"  ✅ {name}: results found")
        else:
            log.append(f"  ⚠️ {name}: no results")
    return combined, log

# ─────────────────────────────────────────────
# ACHIEVEMENT ANALYSIS
# ─────────────────────────────────────────────

def analyze_achievement_google(title):
    log         = []
    title_lower = title.lower().strip()

    # Step 1 — direct level from title
    direct_level = None
    if any(k in title_lower for k in ["international","global","world"]):
        direct_level = "International"
    elif any(k in title_lower for k in ["national","nationwide","all india"]):
        direct_level = "National"
    elif any(k in title_lower for k in ["state level","state championship","state competition"]):
        direct_level = "State"
    elif any(k in title_lower for k in [
        "regional","district","zonal","inter-school",
        "interschool","inter school","zone"
    ]):
        direct_level = "District"
    elif any(k in title_lower for k in ["school","intra-school","house"]):
        direct_level = "School"

    if direct_level:
        log.append(f"⚡ Level found directly in title: **{direct_level}**")
        log.append("Web search skipped — title is self-explanatory.")
        return {
            "urls_found": [], "level": direct_level,
            "confidence": "High", "is_irrational": False, "log": log
        }

    # Step 2 — multi-platform search
    log.append("🔍 No direct level in title — searching web...")
    queries = [
        title,
        f"{title} award competition",
        f"{title} certificate recognition",
        f'"{title}"',
    ]

    combined = ""
    for q in queries:
        log.append(f"\n🔍 **{q}**")
        text, plog = multi_search(q)
        combined  += " " + text
        for pl in plog:
            log.append(pl)

    combined = combined.lower()

    # Step 3 — proximity scoring
    WINDOW          = 400
    title_positions = [m.start() for m in re.finditer(re.escape(title_lower), combined)]
    log.append(f"\n📍 Title found at **{len(title_positions)}** position(s) in results")

    level_scores = {lv: 0 for lv in LEVEL_KEYWORDS}

    if title_positions:
        for pos in title_positions:
            nearby = combined[max(0, pos - WINDOW): pos + WINDOW]
            for lv, kws in LEVEL_KEYWORDS.items():
                for kw in kws:
                    if kw in nearby:
                        level_scores[lv] += 1
    else:
        log.append("⚠️ Title not literal in results — using full-text fallback")
        for lv, kws in LEVEL_KEYWORDS.items():
            level_scores[lv] = sum(kw in combined for kw in kws)

    log.append(f"📊 Scores: {level_scores}")

    best_level   = max(level_scores, key=level_scores.get)
    best_score   = level_scores[best_level]
    is_irrational = len(combined.strip()) < 300

    if is_irrational:
        level, confidence = "School", "Low"
        log.append("❌ No results on any platform — sending to teacher.")
    elif best_score >= 2:
        level, confidence = best_level, "High"
        log.append(f"✅ Strong match → **{level}** (High)")
    elif best_score == 1:
        level, confidence = best_level, "Medium"
        log.append(f"🟡 Weak match → **{level}** (Medium)")
    else:
        level, confidence = "School", "Low"
        log.append("⚠️ Level unclear — sending to teacher.")

    return {
        "urls_found": [], "level": level,
        "confidence": confidence, "is_irrational": is_irrational, "log": log
    }


def should_auto_approve(confidence, is_irrational=False):
    if is_irrational:
        return False
    return confidence in ["High", "Medium"]