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
    # Windows local
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )
else:
    # Linux / Streamlit Cloud
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
        "Technology": 0,
        "Science": 0,
        "Finance": 0,
        "Mathematics": 0,
        "Sports": 0
    }

    mapping = {

        "Creative Arts": [
            "essay",
            "writing",
            "poetry",
            "debate",
            "literature",
            "story",
            "art"
        ],

        "Technology": [
            "coding",
            "python",
            "hackathon",
            "robotics"
        ],

        "Science": [
            "science",
            "research"
        ],

        "Finance": [
            "economics",
            "business",
            "finance",
            "accounting"
        ],

        "Mathematics": [
            "math",
            "mathematics",
            "olympiad"
        ],

        "Sports": [
            "football",
            "cricket",
            "basketball",
            "athletics"
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
# LEVEL DETECTION
# ─────────────────────────────────────────────

def detect_level(text):

    t = text.lower()

    if any(k in t for k in [
        "international",
        "global",
        "world",
        "cambridge international"
    ]):
        return "International"

    if any(k in t for k in [
        "national",
        "all india",
        "nationwide"
    ]):
        return "National"

    if any(k in t for k in [
        "state level",
        "state competition",
        "state"
    ]):
        return "State"

    if any(k in t for k in [
        "district",
        "regional",
        "zonal",
        "inter school"
    ]):
        return "District"

    return "School"


# ─────────────────────────────────────────────
# TEACHER ASSIGNMENT
# ─────────────────────────────────────────────

def assign_teacher(category):

    mapping = {

        "Science": "science_teacher",
        "Technology": "cs_teacher",
        "Mathematics": "maths_teacher",
        "Finance": "business_teacher",
        "Creative Arts": "english_teacher",
        "Sports": "class_teacher",
        "Other": "class_teacher"
    }

    return mapping.get(
        category,
        "class_teacher"
    )


# ─────────────────────────────────────────────
# SEARCH
# ─────────────────────────────────────────────

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}


def fetch_search(url, query):

    try:

        r = requests.get(
            url,
            params={"q": query},
            headers=HEADERS,
            timeout=10
        )

        soup = BeautifulSoup(
            r.text,
            "html.parser"
        )

        return soup.get_text(" ").lower()

    except:
        return ""


# ─────────────────────────────────────────────
# ACHIEVEMENT ANALYSIS
# ─────────────────────────────────────────────

def analyze_achievement_google(title):

    log = []

    queries = [

        title,

        f"{title} competition",

        f"{title} award",

        f"{title} certificate",

        f"{title} results",

        f"{title} international"
    ]

    combined = ""

    for q in queries:

        log.append(f"🔍 Searching: **{q}**")

        google = fetch_search(
            "https://www.google.com/search",
            q
        )

        bing = fetch_search(
            "https://www.bing.com/search",
            q
        )

        combined += google + bing

    combined = combined.lower()

    level = detect_level(combined)

    evidence_words = [

        "official",
        "competition",
        "award",
        "certificate",
        "winner",
        "results",
        "international",
        "national",
        "students",
        "essay",
        "school"
    ]

    score = 0

    for word in evidence_words:

        if word in combined:
            score += 1

    if score >= 6:

        confidence = "High"

    elif score >= 3:

        confidence = "Medium"

    else:

        confidence = "Low"

    is_irrational = False

    if len(combined.strip()) < 300:

        is_irrational = True

        confidence = "Low"

    log.append(f"📊 Evidence Score: **{score}/11**")

    log.append(f"🌍 Detected Level: **{level}**")

    log.append(f"✅ Confidence: **{confidence}**")

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

    return confidence in [
        "High",
        "Medium"
    ]