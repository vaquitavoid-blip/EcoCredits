import re
import os
import shutil
import requests
import pytesseract

from bs4 import BeautifulSoup

from PIL import (
    Image,
    ImageFilter,
    ImageEnhance
)

# ─────────────────────────────────────────────
# TESSERACT — works on Windows AND Streamlit Cloud
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
# IMAGE PREPROCESSING
# ─────────────────────────────────────────────

def preprocess_image(image):

    image = image.convert("L")

    image = ImageEnhance.Contrast(image).enhance(3)

    image = image.filter(ImageFilter.SHARPEN)

    image = image.resize(
        (
            image.width * 2,
            image.height * 2
        )
    )

    return image


# ─────────────────────────────────────────────
# OCR
# ─────────────────────────────────────────────

def extract_text(image_path):

    image = Image.open(image_path)

    processed = preprocess_image(image)

    configs = [
        "--psm 6",
        "--psm 4",
        "--psm 11",
        "--psm 3",
        "--psm 12"
    ]

    texts = []

    for cfg in configs:

        try:

            txt = pytesseract.image_to_string(
                processed,
                config=cfg
            )

            texts.append(txt)

        except:
            pass

    combined = "\n".join(texts)

    return combined


# ─────────────────────────────────────────────
# SUBJECTS
# ─────────────────────────────────────────────

SUBJECT_ALIASES = {

    "Combined Science": [
        "combined science",
        "science"
    ],

    "Add Maths": [
        "additional mathematics",
        "additional maths",
        "add maths",
        "add math"
    ],

    "Extended Maths": [
        "extended mathematics",
        "mathematics",
        "maths",
        "math"
    ],

    "FLE": [
        "first language english",
        "english first language",
        "fle"
    ],

    "ESL": [
        "english second language",
        "esl"
    ],

    "ICT": [
        "ict",
        "computer science",
        "computing"
    ],

    "Economics": [
        "economics",
        "econ"
    ],

    "Business Studies": [
        "business studies",
        "business"
    ],

    "Accounting": [
        "accounting",
        "accounts"
    ],

    "DT": [
        "design technology",
        "design and technology",
        "dt"
    ],

    "Art and Design": [
        "art and design",
        "art",
        "design"
    ]
}

ALL_SUBJECTS = list(SUBJECT_ALIASES.keys())


# ─────────────────────────────────────────────
# GRADE DETECTION
# ─────────────────────────────────────────────

def detect_grades(text):

    detected = {}

    clean = text.lower()

    for subject, aliases in SUBJECT_ALIASES.items():

        found = False

        for alias in aliases:

            patterns = [

                rf"{re.escape(alias)}[\s\S]{{0,30}}?(a\*|a|b|c|d)",

                rf"{re.escape(alias)}[\s\S]{{0,20}}?grade[\s:]+(a\*|a|b|c|d)"
            ]

            for pattern in patterns:

                match = re.search(
                    pattern,
                    clean,
                    re.IGNORECASE
                )

                if match:

                    grade = match.group(1).upper()

                    detected[subject] = grade

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

    scores = {
        "Creative Arts": 0,
        "Technology":    0,
        "Science":       0,
        "Finance":       0,
        "Mathematics":   0,
        "Sports":        0
    }

    mapping = {

        "Creative Arts": [
            "essay", "writing", "poetry",
            "debate", "literature", "story", "art"
        ],

        "Technology": [
            "coding", "python", "hackathon", "robotics"
        ],

        "Science": [
            "science", "research"
        ],

        "Finance": [
            "economics", "business", "finance", "accounting"
        ],

        "Mathematics": [
            "math", "mathematics", "olympiad"
        ],

        "Sports": [
            "football", "cricket", "basketball", "athletics"
        ]
    }

    for category, words in mapping.items():
        for w in words:
            if w in t:
                scores[category] += 1

    best = max(scores, key=scores.get)

    if scores[best] == 0:
        return "Other"

    return best


# ─────────────────────────────────────────────
# LEVEL KEYWORDS
# ─────────────────────────────────────────────

LEVEL_KEYWORDS = {

    "International": [
        "international", "global", "worldwide",
        "world championship", "olympic", "commonwealth",
        "cambridge international", "unicef", "unesco",
        "across countries", "multinational"
    ],

    "National": [
        "national", "all india", "nationwide",
        "national finals", "national level",
        "national competition", "federal", "country-wide"
    ],

    "State": [
        "state", "statewide", "state level",
        "state championship", "state finals",
        "provincial", "state competition"
    ],

    "District": [
        "district", "district level", "zonal",
        "zone level", "district finals", "regional",
        "inter-school", "interschool", "inter school",
        "district competition", "district winner",
        "area competition"
    ],

    "School": [
        "school", "intra-school", "house level",
        "within school", "school competition", "school level"
    ]
}


# ─────────────────────────────────────────────
# TEACHER ASSIGNMENT
# ─────────────────────────────────────────────

def assign_teacher(category):

    mapping = {
        "Science":       "science_teacher",
        "Technology":    "cs_teacher",
        "Mathematics":   "maths_teacher",
        "Finance":       "business_teacher",
        "Creative Arts": "english_teacher",
        "Sports":        "class_teacher",
        "Other":         "class_teacher"
    }

    return mapping.get(category, "class_teacher")


# ─────────────────────────────────────────────
# SEARCH HELPERS
# ─────────────────────────────────────────────

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9"
}


def fetch_search(url, query):

    try:

        r = requests.get(
            url,
            params={"q": query, "num": 8},
            headers=HEADERS,
            timeout=10
        )

        soup = BeautifulSoup(r.text, "html.parser")

        return soup.get_text(" ").lower()

    except:
        return ""


# ─────────────────────────────────────────────
# ACHIEVEMENT ANALYSIS
# ─────────────────────────────────────────────

def analyze_achievement_google(title):

    log = []
    title_lower = title.lower().strip()

    # ── Step 1: Check award name itself for level words ───────────────────
    # Most reliable signal — if "regional" is IN the award name, it IS regional
    direct_level = None

    if any(k in title_lower for k in [
        "international", "global", "world"
    ]):
        direct_level = "International"

    elif any(k in title_lower for k in [
        "national", "nationwide", "all india"
    ]):
        direct_level = "National"

    elif any(k in title_lower for k in [
        "state level", "state championship", "state competition"
    ]):
        direct_level = "State"

    elif any(k in title_lower for k in [
        "regional", "district", "zonal", "inter-school",
        "interschool", "inter school", "zone"
    ]):
        direct_level = "District"

    elif any(k in title_lower for k in [
        "school", "intra-school", "house"
    ]):
        direct_level = "School"

    if direct_level:
        log.append(f"✅ Level detected directly from award name: **{direct_level}**")
        log.append("⚡ Skipping web search — title is self-explanatory.")
        return {
            "urls_found": [],
            "level": direct_level,
            "confidence": "High",
            "is_irrational": False,
            "log": log
        }

    # ── Step 2: Web search ────────────────────────────────────────────────
    log.append("🔍 Award name has no direct level indicator — searching web...")

    queries = [
        title,
        f"{title} competition",
        f"{title} award",
        f"{title} certificate",
    ]

    combined = ""

    for q in queries:
        log.append(f"🔍 Searching: **{q}**")
        google = fetch_search("https://www.google.com/search", q)
        bing   = fetch_search("https://www.bing.com/search", q)
        combined += google + bing

    combined = combined.lower()

    # ── Step 3: Proximity scoring ─────────────────────────────────────────
    # Only count level keywords if they appear NEAR the title in results.
    # This stops "international" on a random part of the page
    # from inflating the score.

    WINDOW = 300  # characters either side of title mention

    title_positions = [
        m.start()
        for m in re.finditer(re.escape(title_lower), combined)
    ]

    log.append(
        f"📍 Title found at **{len(title_positions)}** position(s) in search results"
    )

    level_scores = {lv: 0 for lv in LEVEL_KEYWORDS}

    if title_positions:
        # Score only in windows around each title mention
        for pos in title_positions:
            nearby = combined[
                max(0, pos - WINDOW): pos + WINDOW
            ]
            for lv, kws in LEVEL_KEYWORDS.items():
                for kw in kws:
                    if kw in nearby:
                        level_scores[lv] += 1
    else:
        # Title not found literally in results —
        # fall back to full text with lower weight
        log.append("⚠️ Title not found literally in results — using full text fallback.")
        for lv, kws in LEVEL_KEYWORDS.items():
            level_scores[lv] = sum(kw in combined for kw in kws)

    log.append(f"📊 Proximity level scores: {level_scores}")

    best_level = max(level_scores, key=level_scores.get)
    best_score = level_scores[best_level]

    # ── Step 4: Confidence decision ───────────────────────────────────────
    is_irrational = len(combined.strip()) < 300

    if is_irrational:
        level      = "School"
        confidence = "Low"
        log.append("❌ No search results found — cannot verify. Sending to teacher.")

    elif best_score >= 2:
        level      = best_level
        confidence = "High"
        log.append(f"✅ Strong proximity match → **{level}** (High confidence)")

    elif best_score == 1:
        level      = best_level
        confidence = "Medium"
        log.append(f"🟡 Weak proximity match → **{level}** (Medium confidence)")

    else:
        # Found something on Google but no level context at all
        # Safer to send to teacher than guess wrong
        level      = "School"
        confidence = "Low"
        log.append(
            "⚠️ Award found on web but level is unclear — sending to teacher to be safe."
        )

    return {
        "urls_found": [],
        "level": level,
        "confidence": confidence,
        "is_irrational": is_irrational,
        "log": log
    }


# ─────────────────────────────────────────────
# AUTO APPROVAL
# ─────────────────────────────────────────────

def should_auto_approve(
    confidence,
    is_irrational=False
):

    if is_irrational:
        return False

    return confidence in ["High", "Medium"]