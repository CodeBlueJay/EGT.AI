# chatbot_core.py

from rapidfuzz import fuzz, process
from collections import defaultdict, Counter
import random
import re
import random

INSULT_KEYWORDS = [
    "fuck", "idiot", "dumb", "shut up", "trash", "useless",
    "noob", "loser", "retard"
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
    "That really hurt my feelings",
    "https://media.discordapp.net/attachments/1112003889928093859/1404606365103821004/attachment.gif?ex=69e16f9d&is=69e01e1d&hm=ed84365e8a9a4b017536ae408d54ccf6a2b5755889cf1e2b9f7ceada822d8d55&=&width=560&height=450"
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
    "What is this guy yapping about",
    "https://media.discordapp.net/attachments/1250239994610716743/1265155388010135662/speed.gif?ex=69e10685&is=69dfb505&hm=fde704b7519a750983dc5a7e6b44a126f762414254d4e8d360f8e907f128af5d&=&width=416&height=747",
]

SLANG_QUESTIONS = [
    "bro",
    "wsg",
    "wyd",
    "what you doing",
    "are we deadass",
    "deadass",
    "fr",
    "huh",
    "hello?",
    "yo"
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
    "https://media.discordapp.net/attachments/1112003889928093859/1404606365103821004/attachment.gif?ex=69e16f9d&is=69e01e1d&hm=ed84365e8a9a4b017536ae408d54ccf6a2b5755889cf1e2b9f7ceada822d8d55&=&width=560&height=450"
]

YES_NO_RESPONSES = [
    "yea",
    "nga no",
    "absolutely not",
    "https://media.discordapp.net/attachments/1112003889928093859/1404606365103821004/attachment.gif?ex=69e16f9d&is=69e01e1d&hm=ed84365e8a9a4b017536ae408d54ccf6a2b5755889cf1e2b9f7ceada822d8d55&=&width=560&height=450"
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

    # punctuation question
    if text.endswith("?"):
        return True

    # starter words
    if words[0] in QUESTION_STARTERS:
        return True

    # slang-based questions
    for phrase in SLANG_QUESTIONS:
        if phrase in text:
            return True

    return False


def handle_question(text):
    words = text.split()

    # slang responses
    if any(x in text for x in ["wsg", "wyd", "bro"]):
        return random.choice([
            "Not much",
            "Idk just existing",
            "Chillin"
        ])

    # yes/no logic
    if words and words[0] in ["is", "are", "do", "does", "did", "can", "could", "should", "would", "will", "am"]:
        return random.choice(YES_NO_RESPONSES)

    return random.choice(QUESTION_RESPONSES)

# =========================
# 🔹 Trigger → Responses
# =========================
TRIGGERS = {
    "greeting": {
        "patterns": ["hello", "hi", "hey", "yo"],
        "responses": [
            "What do you want",
            "Hello I am Eric toy",
            "?",
            "hello",
            "the goat is here",
            "https://media.discordapp.net/attachments/1250239994610716743/1265155388010135662/speed.gif?ex=69e10685&is=69dfb505&hm=fde704b7519a750983dc5a7e6b44a126f762414254d4e8d360f8e907f128af5d&=&width=416&height=747"
        ]
    },
    "npc": {
        "patterns": ["npc"],
        "responses": [
            "What!11!!",
            "I am NOT an npc",
            "https://media.discordapp.net/attachments/1112003889928093859/1404606365103821004/attachment.gif?ex=69e16f9d&is=69e01e1d&hm=ed84365e8a9a4b017536ae408d54ccf6a2b5755889cf1e2b9f7ceada822d8d55&=&width=560&height=450"
        ]
    },
    "bye": {
        "patterns": ["bye", "goodbye", "see ya", "later"],
        "responses": [
            "bye",
            "https://media.discordapp.net/attachments/1250239994610716743/1265155388010135662/speed.gif?ex=69e10685&is=69dfb505&hm=fde704b7519a750983dc5a7e6b44a126f762414254d4e8d360f8e907f128af5d&=&width=416&height=747"
        ]
    },
    "laugh": {
        "patterns": ["lmao", "lol", "lmfao"],
        "responses": [
            "That isn't funny",
            "What's so funny",
            "This is no laughing matter"
        ]
    },
    "gif": {
        "patterns": ["gif"],
        "responses": [
            "https://media.discordapp.net/attachments/1112003889928093859/1404606365103821004/attachment.gif?ex=69e16f9d&is=69e01e1d&hm=ed84365e8a9a4b017536ae408d54ccf6a2b5755889cf1e2b9f7ceada822d8d55&=&width=560&height=450",
            "https://media.discordapp.net/attachments/1250239994610716743/1265155388010135662/speed.gif?ex=69e10685&is=69dfb505&hm=fde704b7519a750983dc5a7e6b44a126f762414254d4e8d360f8e907f128af5d&=&width=416&height=747"
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
        if cleaned == pattern or fuzz.ratio(cleaned, pattern) > 95:
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

    # Final fallback
    return random.choice(DEFAULT_RESPONSES)
