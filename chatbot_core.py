# chatbot_core.py

from rapidfuzz import fuzz, process
from collections import defaultdict, Counter
import random
import re
import random

INSULT_KEYWORDS = [
    "fuck", "idiot", "dumb", "shut up", "trash", "useless",
    "noob", "loser", "retard", "hate you", "suck"
]

INSULT_RESPONSES = [
    "Wrong",
    "Bro",
    "Take that back rn",
    "Shut up stinky",
    "ig bro",
    "O snap",
    "Yo I'm sorry",
    "Forgive me",
    "It was js a joke",
    "Not that deep",
    "Mb mb",
    "Stupid idiot",
    "Apologise immediately",
    "That really hurt my feelings"
]

MAX_INPUT_CHARS = 100

LONG_INPUT_RESPONSES = [
    "Please dumb it down for me",
    "Dumb it down for me please",
    "That's too many words",
    "I'm not reading allat",
    "Wow"
]
DEFAULT_RESPONSES = [
    "Wow",
    "Awesome",
    "Bro ig",
    "Bro what",
    "what",
    "bro",
]

QUESTION_STARTERS = [
    "what", "why", "how", "when", "where", "who",
    "is", "are", "do", "does", "did", "can", "could",
    "should", "would", "will", "am"
]

QUESTION_RESPONSES = [
    "what",
    "bro ig",
    "bro obv",
]

YES_NO_RESPONSES = [
    "yea",
    "nga no",
    "absolutely not",
]

def detect_insult(text):
    text = text.lower()

    # direct keyword match
    for word in INSULT_KEYWORDS:
        if word in text:
            return True

    # fuzzy match (handles typos like "stooopid")
    for word in INSULT_KEYWORDS:
        if fuzz.partial_ratio(text, word) > 85:
            return True

    return False

def is_question(text):
    words = text.split()
    
    if not words:
        return False

    # Ends with ?
    if text.endswith("?"):
        return True

    # Starts like a question
    if words[0] in QUESTION_STARTERS:
        return True

    return False


def handle_question(text):
    words = text.split()

    # Yes/No style question
    if words[0] in ["is", "are", "do", "does", "did", "can", "could", "should", "would", "will", "am"]:
        return random.choice(YES_NO_RESPONSES)

    # Open-ended question
    return random.choice(QUESTION_RESPONSES)
# =========================
# 🔹 Trigger → Responses
# =========================
TRIGGERS = {
    "greeting": {
        "patterns": ["hello", "hi", "hey", "yo", "what's up"],
        "responses": [
            "What do you want",
            "Hello I am Eric toy",
            "?",
            "hello",
            "the goat is here"
        ]
    },
    "bye": {
        "patterns": ["bye", "goodbye", "see ya", "later"],
        "responses": [
            "bye",
        ]
    },
    "laugh": {
        "patterns": ["lmao", "lol", "lmfao"],
        "responses": [
            "That isn’t funny",
            "What’s so funny",
            "This is no laughing matter"
        ]
    },
    "npc": {
        "patterns": ["npc"],
        "responses": [
            "What!11!!",
            "I am NOT an npc"
        ]
    }
}

# Flatten patterns for fuzzy search
ALL_PATTERNS = []
PATTERN_TO_INTENT = {}

for intent, data in TRIGGERS.items():
    for pattern in data["patterns"]:
        ALL_PATTERNS.append(pattern)
        PATTERN_TO_INTENT[pattern] = intent

# =========================
# 🔹 Memory (per session)
# =========================
user_memory = defaultdict(list)
word_frequency = Counter()

# =========================
# 🔹 Text Cleaning
# =========================
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return text.strip()

# =========================
# 🔹 Intent Detection
# =========================
def detect_intent(user_input):
    cleaned = clean_text(user_input)

    # Exact match first
    for pattern in ALL_PATTERNS:
        if pattern in cleaned:
            return PATTERN_TO_INTENT[pattern], 100

    # Fuzzy match
    match, score, _ = process.extractOne(
        cleaned,
        ALL_PATTERNS,
        scorer=fuzz.partial_ratio
    )

    if score >= 70:  # threshold
        return PATTERN_TO_INTENT[match], score

    return None, score

# =========================
# 🔹 Generate Response
# =========================
def get_response(user_input, user_id="default"):
    cleaned = clean_text(user_input)

    # 🚨 INPUT TOO LONG CHECK (you already have this maybe)
    if len(cleaned) > MAX_INPUT_CHARS:
        return random.choice(LONG_INPUT_RESPONSES)

    # 🚨 INSULT DETECTION
    if detect_insult(cleaned):
        # random tone response
        return random.choice(INSULT_RESPONSES)

    # Store memory
    user_memory[user_id].append(cleaned)
    word_frequency.update(cleaned.split())

    intent, score = detect_intent(cleaned)

    # If intent found
    if intent:
        response = random.choice(TRIGGERS[intent]["responses"])
        
        return response

    # =========================
    # 🔹 Pattern-based fallback
    # =========================
    
    # Question detection
    if is_question(cleaned):
      return handle_question(cleaned)

    # Keyword-based mini logic
    if "name" in cleaned:
        return "I'm eric toy"

    if "help" in cleaned:
        return "Oh snap"

    # =========================
    # 🔹 Smart fallback
    # =========================
    most_common = word_frequency.most_common(3)

    if most_common:
        words = ", ".join([w for w, _ in most_common])
        return f"what is this guy yapping about"

    # Final fallback
    return random.choice(DEFAULT_RESPONSES)