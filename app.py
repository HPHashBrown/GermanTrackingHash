
import streamlit as st
import json
import os
import random
import datetime
from datetime import date, timedelta

# ============================================================
# CONFIGURATION
# ============================================================
LANGUAGE = "Deutsch"
LANGUAGE_CODE = "de-DE"
ENGLISH_NAME = "German"
USER_LEVEL = "Beginner"

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================
def init_session_state():
    defaults = {
        "chat_history": [],
        "current_scenario": "Free Chat",
        "vocab_decks": {},
        "learned_words": set(),
        "current_deck": None,
        "current_card_index": 0,
        "card_flipped": False,
        "streak": 0,
        "last_practice_date": None,
        "daily_practiced": False,
        "alphabet_progress": {},
        "api_key": "",
        "translate_input": "",
        "translate_result": None,
        "custom_topic": "",
        "custom_deck_loading": False,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

    # Load saved progress from file
    if os.path.exists("progress.json"):
        try:
            with open("progress.json", "r") as f:
                saved = json.load(f)
            for key in ["streak", "last_practice_date", "learned_words", "alphabet_progress", "vocab_decks"]:
                if key in saved:
                    if key == "learned_words":
                        st.session_state[key] = set(saved[key])
                    else:
                        st.session_state[key] = saved[key]
        except:
            pass

def save_progress():
    data = {
        "streak": st.session_state.streak,
        "last_practice_date": st.session_state.last_practice_date,
        "learned_words": list(st.session_state.learned_words),
        "alphabet_progress": st.session_state.alphabet_progress,
        "vocab_decks": st.session_state.vocab_decks,
    }
    with open("progress.json", "w") as f:
        json.dump(data, f)

def update_streak():
    today = date.today().isoformat()
    last = st.session_state.last_practice_date
    if last is None:
        st.session_state.streak = 1
    elif last == today:
        pass
    elif last == (date.today() - timedelta(days=1)).isoformat():
        st.session_state.streak += 1
    else:
        st.session_state.streak = 1
    st.session_state.last_practice_date = today
    st.session_state.daily_practiced = True
    save_progress()

# ============================================================
# DATA: GERMAN ALPHABET
# ============================================================
GERMAN_ALPHABET = [
    ("A", "ah", "Apfel", "apple", "ˈapfəl"),
    ("Ä", "eh", "Äpfel", "apples", "ˈɛːpfəl"),
    ("B", "beh", "Banane", "banana", "baˈnaːnə"),
    ("C", "tseh", "Computer", "computer", "kɔmˈpyːtɐ"),
    ("D", "deh", "Dach", "roof", "dax"),
    ("E", "eh", "Elefant", "elephant", "eleˈfant"),
    ("F", "eff", "Fisch", "fish", "fɪʃ"),
    ("G", "geh", "Garten", "garden", "ˈɡaʁtən"),
    ("H", "hah", "Haus", "house", "haʊ̯s"),
    ("I", "ee", "Insel", "island", "ˈɪnzl̩"),
    ("J", "yot", "Jahr", "year", "jaːɐ̯"),
    ("K", "kah", "Katze", "cat", "ˈkatsə"),
    ("L", "ell", "Lampe", "lamp", "ˈlampə"),
    ("M", "emm", "Maus", "mouse", "maʊ̯s"),
    ("N", "enn", "Nase", "nose", "ˈnaːzə"),
    ("O", "oh", "Orange", "orange", "oˈʁaːʒə"),
    ("Ö", "öh", "Öl", "oil", "øːl"),
    ("P", "peh", "Pferd", "horse", "pfɛʁt"),
    ("Q", "kuh", "Qualität", "quality", "kvaliˈtɛːt"),
    ("R", "err", "Regen", "rain", "ˈʁeːɡən"),
    ("S", "ess", "Sonne", "sun", "ˈzɔnə"),
    ("ß", "ess-tsett", "Straße", "street", "ˈʃtʁaːsə"),
    ("T", "teh", "Tisch", "table", "tɪʃ"),
    ("U", "oo", "Uhr", "clock", "uːɐ̯"),
    ("Ü", "üh", "über", "over", "ˈyːbɐ"),
    ("V", "fau", "Vogel", "bird", "ˈfoːɡəl"),
    ("W", "veh", "Wasser", "water", "ˈvasɐ"),
    ("X", "iks", "Xylophon", "xylophone", "ksyloˈfoːn"),
    ("Y", "ypsilon", "Yoga", "yoga", "ˈjoːɡa"),
    ("Z", "tsett", "Zebra", "zebra", "ˈtseːbʁa"),
]

# ============================================================
# DATA: PRESET VOCAB DECKS
# ============================================================
PRESET_DECKS = {
    "Greetings": [
        ("Hallo", "Hello", "haˈloː"),
        ("Guten Morgen", "Good morning", "ˈɡuːtən ˈmɔʁɡən"),
        ("Guten Tag", "Good day", "ˈɡuːtən taːk"),
        ("Guten Abend", "Good evening", "ˈɡuːtən ˈaːbənt"),
        ("Gute Nacht", "Good night", "ˈɡuːtə naxt"),
        ("Auf Wiedersehen", "Goodbye", "aʊ̯f ˈviːdɐzeːən"),
        ("Tschüss", "Bye", "tʃʏs"),
        ("Wie geht's?", "How are you?", "viː ɡeːts"),
        ("Mir geht's gut", "I'm doing well", "miːɐ̯ ɡeːts ɡuːt"),
        ("Danke", "Thank you", "ˈdaŋkə"),
        ("Bitte", "Please / You're welcome", "ˈbɪtə"),
        ("Entschuldigung", "Excuse me", "ɛntˈʃʊldɪɡʊŋ"),
    ],
    "Food": [
        ("Brot", "Bread", "bʁoːt"),
        ("Wasser", "Water", "ˈvasɐ"),
        ("Kaffee", "Coffee", "kaˈfeː"),
        ("Tee", "Tea", "teː"),
        ("Milch", "Milk", "mɪlç"),
        ("Ei", "Egg", "aɪ̯"),
        ("Käse", "Cheese", "ˈkɛːzə"),
        ("Fleisch", "Meat", "flaɪ̯ʃ"),
        ("Fisch", "Fish", "fɪʃ"),
        ("Apfel", "Apple", "ˈapfəl"),
        ("Banane", "Banana", "baˈnaːnə"),
        ("Kuchen", "Cake", "ˈkuːxən"),
    ],
    "Travel": [
        ("Flughafen", "Airport", "ˈfluːkˌhafən"),
        ("Bahnhof", "Train station", "ˈbaːnhoːf"),
        ("Hotel", "Hotel", "hoˈtɛl"),
        ("Zug", "Train", "tsuːk"),
        ("Bus", "Bus", "bʊs"),
        ("Taxi", "Taxi", "ˈtaksi"),
        ("Pass", "Passport", "pas"),
        ("Ticket", "Ticket", "ˈtɪkɪt"),
        ("Koffer", "Suitcase", "ˈkɔfɐ"),
        ("Karte", "Map / Ticket", "ˈkaʁtə"),
        ("Stadt", "City", "ʃtat"),
        ("Straße", "Street", "ˈʃtʁaːsə"),
    ],
    "Numbers": [
        ("eins", "one", "aɪ̯ns"),
        ("zwei", "two", "tsvaɪ̯"),
        ("drei", "three", "dʁaɪ̯"),
        ("vier", "four", "fiːɐ̯"),
        ("fünf", "five", "fʏnf"),
        ("sechs", "six", "zɛks"),
        ("sieben", "seven", "ˈziːbən"),
        ("acht", "eight", "axt"),
        ("neun", "nine", "nɔʏ̯n"),
        ("zehn", "ten", "tseːn"),
        ("elf", "eleven", "ɛlf"),
        ("zwölf", "twelve", "tsvœlf"),
    ],
}

# ============================================================
# SIMULATED CLAUDE API (since we don't have actual API key)
# ============================================================
def simulate_claude_chat(user_msg, scenario, level, history):
    """Simulate Claude API responses for German tutoring"""
    scenario_prompts = {
        "Order Coffee": "You are a barista in a German café. Respond naturally in German.",
        "Meet Someone": "You just met someone new in Germany. Respond naturally in German.",
        "At the Airport": "You work at a German airport information desk. Respond naturally in German.",
        "Free Chat": "You are a friendly German language tutor. Respond in German.",
    }

    # Simple response generation based on scenario
    responses = {
        "Order Coffee": [
            ("Guten Morgen! Was darf es sein? Möchten Sie einen Cappuccino oder einen Espresso?", 
             "Good morning! What can I get you? Would you like a cappuccino or an espresso?",
             "ˈɡuːtən ˈmɔʁɡən! vas ˈdaʁf ɛs zaɪ̯n? ˈmœçtən ziː ˈaɪ̯nən kapuˈtʃiːnoː oːdɐ ˈaɪ̯nən ɛsˈprɛsoː?"),
            ("Sehr gerne! Mit Milch und Zucker?", 
             "With pleasure! With milk and sugar?",
             "zeːɐ̯ ˈɡɛʁnə! mɪt mɪlç ʊnt ˈtsʊkɐ?"),
            ("Das macht 3,50 Euro. Bitte schön, Ihr Kaffee!", 
             "That will be 3.50 euros. Here you go, your coffee!",
             "das maxt ˈdʁaɪ̯ ˈkɔma ˈfʏnf ˈɔʏ̯ʁoː. ˈbɪtə ʃøːn, iːɐ̯ kaˈfeː!"),
        ],
        "Meet Someone": [
            ("Hallo! Ich heiße Anna. Wie heißt du?", 
             "Hello! My name is Anna. What's your name?",
             "haˈloː! ɪç ˈhaɪ̯sə ˈana. viː ˈhaɪ̯st duː?"),
            ("Schön, dich kennenzulernen! Woher kommst du?", 
             "Nice to meet you! Where are you from?",
             "ʃøːn, dɪç ˈkɛnənˌtsuːlɛʁnən! voˈheːɐ̯ kɔmst duː?"),
            ("Ich komme aus Berlin. Und du?", 
             "I come from Berlin. And you?",
             "ɪç ˈkɔmə aʊ̯s bɛʁˈliːn. ʊnt duː?"),
        ],
        "At the Airport": [
            ("Guten Tag! Wohin möchten Sie fliegen?", 
             "Good day! Where would you like to fly to?",
             "ˈɡuːtən taːk! voˈhɪn ˈmœçtən ziː ˈfliːɡən?"),
            ("Ihr Flug geht um 14 Uhr von Gate B12.", 
             "Your flight departs at 2 PM from gate B12.",
             "iːɐ̯ fluːk ɡeːt ʊm ˈfiːɐ̯ˈtsɛn ˈuːɐ̯ fɔn ɡeːt ˈbeː ˈtsvœlf."),
            ("Bitte gehen Sie zur Sicherheitskontrolle.", 
             "Please go to the security check.",
             "ˈbɪtə ˈɡeːən ziː tsuːɐ̯ zɪçɐˈhaɪ̯tsˌkɔntʁoːlə."),
        ],
        "Free Chat": [
            ("Das Wetter ist heute sehr schön, nicht wahr?", 
             "The weather is very nice today, isn't it?",
             "das ˈvɛtɐ ɪst ˈhɔʏ̯tə zeːɐ̯ ʃøːn, nɪçt vaːɐ̯?"),
            ("Hast du schon Pläne für das Wochenende?", 
             "Do you already have plans for the weekend?",
             "hast duː ʃoːn ˈplɛːnə fyːɐ̯ das ˈvɔxənˌɛndə?"),
            ("Ich lerne gerade Deutsch. Es ist eine schöne Sprache!", 
             "I'm currently learning German. It's a beautiful language!",
             "ɪç ˈlɛʁnə ɡəˈʁaːdə dɔʏ̯tʃ. ɛs ɪst ˈaɪ̯nə ˈʃøːnə ˈʃpʁaːxə!"),
            ("Wie findest du das deutsche Essen?", 
             "How do you like German food?",
             "viː ˈfɪnst duː das ˈdɔʏ̯tʃə ˈɛsən?"),
            ("Berlin ist eine faszinierende Stadt!", 
             "Berlin is a fascinating city!",
             "bɛʁˈliːn ɪst ˈaɪ̯nə fasɪniˈʁeːndə ʃtat!"),
        ],
    }

    # Pick response based on conversation length
    idx = len(history) % len(responses.get(scenario, responses["Free Chat"]))
    resp = responses.get(scenario, responses["Free Chat"])[idx]

    # Simple correction logic
    corrections = []
    if user_msg:
        # Check for common beginner mistakes
        if "ich bin" in user_msg.lower() and "gut" in user_msg.lower():
            corrections.append({
                "mistake": "Ich bin gut",
                "correction": "Mir geht's gut",
                "explanation": "In German, we say 'Mir geht's gut' (It's going well for me), not 'Ich bin gut' (I am good/virtuous)."
            })
        if "ich heiße" in user_msg.lower() and not user_msg.endswith("."):
            corrections.append({
                "mistake": "Missing punctuation",
                "correction": user_msg + ".",
                "explanation": "Sentences in German end with a period."
            })
        if "der" in user_msg.lower() and random.random() > 0.7:
            corrections.append({
                "mistake": "Article usage",
                "correction": "Check der/die/das",
                "explanation": "German has three genders: der (masculine), die (feminine), das (neuter). 'der Mann' (the man), 'die Frau' (the woman), 'das Kind' (the child)."
            })

    return {
        "german": resp[0],
        "english": resp[1],
        "pronunciation": resp[2],
        "corrections": corrections,
    }

def simulate_claude_vocab(topic):
    """Generate a 10-card vocab deck for any topic"""
    topic_lower = topic.lower()

    # Predefined topics
    topics_data = {
        "weather": [
            ("Sonne", "sun", "ˈzɔnə"),
            ("Regen", "rain", "ˈʁeːɡən"),
            ("Wolke", "cloud", "ˈvɔlkə"),
            ("Schnee", "snow", "ʃneː"),
            ("Wind", "wind", "vɪnt"),
            ("warm", "warm", "vaʁm"),
            ("kalt", "cold", "kalt"),
            ("heiß", "hot", "haɪ̯s"),
            ("Nebel", "fog", "ˈneːbəl"),
            ("Gewitter", "thunderstorm", "ɡəˈvɪtɐ"),
        ],
        "family": [
            ("Mutter", "mother", "ˈmʊtɐ"),
            ("Vater", "father", "ˈfaːtɐ"),
            ("Schwester", "sister", "ˈʃvɛstɐ"),
            ("Bruder", "brother", "ˈbʁuːdɐ"),
            ("Großmutter", "grandmother", "ˈɡʁoːsˌmʊtɐ"),
            ("Großvater", "grandfather", "ˈɡʁoːsˌfaːtɐ"),
            ("Tante", "aunt", "ˈtantə"),
            ("Onkel", "uncle", "ˈɔŋkəl"),
            ("Cousin", "cousin", "kuˈzɛ̃ː"),
            ("Familie", "family", "faˈmiːliə"),
        ],
        "colors": [
            ("rot", "red", "ʁoːt"),
            ("blau", "blue", "blaʊ̯"),
            ("grün", "green", "ɡʁyːn"),
            ("gelb", "yellow", "ɡɛlp"),
            ("schwarz", "black", "ʃvaʁts"),
            ("weiß", "white", "vaɪ̯s"),
            ("grau", "gray", "ɡʁaʊ̯"),
            ("braun", "brown", "bʁaʊ̯n"),
            ("orange", "orange", "oˈʁaːʒə"),
            ("rosa", "pink", "ˈʁoːza"),
        ],
    }

    if topic_lower in topics_data:
        return topics_data[topic_lower]

    # Generic generation
    generic = [
        (f"{topic.capitalize()}wort 1", f"{topic} word 1", "ˈvɔʁt"),
        (f"{topic.capitalize()}wort 2", f"{topic} word 2", "ˈvɔʁt"),
        (f"{topic.capitalize()}wort 3", f"{topic} word 3", "ˈvɔʁt"),
        (f"{topic.capitalize()}wort 4", f"{topic} word 4", "ˈvɔʁt"),
        (f"{topic.capitalize()}wort 5", f"{topic} word 5", "ˈvɔʁt"),
        (f"{topic.capitalize()}wort 6", f"{topic} word 6", "ˈvɔʁt"),
        (f"{topic.capitalize()}wort 7", f"{topic} word 7", "ˈvɔʁt"),
        (f"{topic.capitalize()}wort 8", f"{topic} word 8", "ˈvɔʁt"),
        (f"{topic.capitalize()}wort 9", f"{topic} word 9", "ˈvɔʁt"),
        (f"{topic.capitalize()}wort 10", f"{topic} word 10", "ˈvɔʁt"),
    ]
    return generic

def simulate_claude_translate(text, direction):
    """Simulate translation with grammar breakdown"""
    # Simple dictionary-based translation
    en_to_de = {
        "hello": ("Hallo", "haˈloː"),
        "good morning": ("Guten Morgen", "ˈɡuːtən ˈmɔʁɡən"),
        "thank you": ("Danke", "ˈdaŋkə"),
        "how are you": ("Wie geht es dir?", "viː ɡeːt ɛs diːɐ̯"),
        "i love you": ("Ich liebe dich", "ɪç ˈliːbə dɪç"),
        "where is the bathroom": ("Wo ist die Toilette?", "voː ɪst diː toaˈlɛtə"),
        "the cat is on the table": ("Die Katze ist auf dem Tisch.", "diː ˈkatsə ɪst aʊ̯f deːm tɪʃ"),
        "i am learning german": ("Ich lerne Deutsch.", "ɪç ˈlɛʁnə dɔʏ̯tʃ"),
        "can you help me": ("Kannst du mir helfen?", "kanst duː miːɐ̯ ˈhɛlfən"),
        "how much does this cost": ("Wie viel kostet das?", "viː fiːl ˈkɔstət das"),
    }

    de_to_en = {
        "hallo": ("Hello", "haˈloː"),
        "guten morgen": ("Good morning", "ˈɡuːtən ˈmɔʁɡən"),
        "danke": ("Thank you", "ˈdaŋkə"),
        "wie geht es dir": ("How are you?", "viː ɡeːt ɛs diːɐ̯"),
        "ich liebe dich": ("I love you", "ɪç ˈliːbə dɪç"),
        "auf wiedersehen": ("Goodbye", "aʊ̯f ˈviːdɐzeːən"),
        "tschüss": ("Bye", "tʃʏs"),
        "bitte": ("Please / You're welcome", "ˈbɪtə"),
        "entschuldigung": ("Excuse me", "ɛntˈʃʊldɪɡʊŋ"),
        "ich verstehe nicht": ("I don't understand", "ɪç fɛɐ̯ˈʃteːə nɪçt"),
    }

    text_lower = text.lower().strip().rstrip(".?!")

    if direction == "en_to_de":
        if text_lower in en_to_de:
            trans, pron = en_to_de[text_lower]
        else:
            trans = f"[Übersetzung von '{text}']"
            pron = "[Aussprache]"
    else:
        if text_lower in de_to_en:
            trans, pron = de_to_en[text_lower]
        else:
            trans = f"[Translation of '{text}']"
            pron = "[Pronunciation]"

    # Word-by-word breakdown
    words = text.split()
    breakdown = []

    grammar_notes = []
    if direction == "en_to_de":
        if "the" in words:
            grammar_notes.append({
                "word": "the",
                "note": "German has three articles: der (masc.), die (fem.), das (neuter). The article changes based on case (nominative, accusative, dative, genitive)."
            })
        if any(w in words for w in ["am", "is", "are"]):
            grammar_notes.append({
                "word": "to be",
                "note": "German 'sein': ich bin, du bist, er/sie/es ist, wir sind, ihr seid, sie sind."
            })
        if "you" in words:
            grammar_notes.append({
                "word": "you",
                "note": "German has two 'you' forms: 'du' (informal, singular) and 'Sie' (formal/plural)."
            })
    else:
        if any(w.lower() in ["der", "die", "das"] for w in words):
            grammar_notes.append({
                "word": "der/die/das",
                "note": "These are definite articles. 'der' = masculine, 'die' = feminine, 'das' = neuter. Every German noun has a gender that must be memorized."
            })
        if "ich" in text_lower:
            grammar_notes.append({
                "word": "ich",
                "note": "First person singular pronoun. German verbs conjugate based on the subject."
            })

    return {
        "original": text,
        "translated": trans,
        "pronunciation": pron,
        "direction": direction,
        "breakdown": breakdown,
        "grammar_notes": grammar_notes,
    }

# ============================================================
# STYLING
# ============================================================
st.set_page_config(
    page_title=f"LinguaLearn — {LANGUAGE}",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

.block-container {
    padding-top: 1rem !important;
    padding-bottom: 1rem !important;
    max-width: 900px !important;
}

/* Header */
.app-header {
    background: linear-gradient(135deg, #FF6B35 0%, #F7931E 50%, #FFD23F 100%);
    border-radius: 20px;
    padding: 24px 32px;
    margin-bottom: 20px;
    color: white;
    box-shadow: 0 8px 32px rgba(255, 107, 53, 0.3);
}
.app-header h1 {
    font-size: 2.2rem;
    font-weight: 900;
    margin: 0;
    letter-spacing: -1px;
}
.app-header p {
    margin: 4px 0 0 0;
    opacity: 0.95;
    font-weight: 500;
}

/* Stats bar */
.stats-bar {
    display: flex;
    gap: 16px;
    margin-bottom: 20px;
}
.stat-card {
    background: white;
    border-radius: 16px;
    padding: 16px 20px;
    flex: 1;
    text-align: center;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    border: 2px solid #f0f0f0;
}
.stat-number {
    font-size: 1.8rem;
    font-weight: 800;
    color: #FF6B35;
    line-height: 1;
}
.stat-label {
    font-size: 0.75rem;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600;
    margin-top: 4px;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: #f8f9fa;
    border-radius: 16px;
    padding: 6px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 12px !important;
    padding: 10px 20px !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    border: none !important;
    color: #666 !important;
}
.stTabs [aria-selected="true"] {
    background: #FF6B35 !important;
    color: white !important;
    box-shadow: 0 4px 16px rgba(255,107,53,0.3) !important;
}

/* Buttons */
.stButton > button {
    border-radius: 12px !important;
    font-weight: 700 !important;
    padding: 10px 24px !important;
    border: none !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.15) !important;
}

/* Cards */
.chat-bubble-user {
    background: linear-gradient(135deg, #FF6B35, #F7931E);
    color: white;
    padding: 14px 18px;
    border-radius: 18px 18px 4px 18px;
    margin: 8px 0;
    max-width: 80%;
    margin-left: auto;
    font-weight: 500;
}
.chat-bubble-tutor {
    background: #f0f4f8;
    color: #1a1a2e;
    padding: 14px 18px;
    border-radius: 18px 18px 18px 4px;
    margin: 8px 0;
    max-width: 80%;
    border-left: 4px solid #FF6B35;
}
.correction-box {
    background: #fff3cd;
    border: 2px solid #ffc107;
    border-radius: 12px;
    padding: 12px 16px;
    margin: 8px 0;
}
.correction-box .mistake {
    color: #dc3545;
    text-decoration: line-through;
    font-weight: 600;
}
.correction-box .fix {
    color: #198754;
    font-weight: 700;
}

/* Alphabet grid */
.letter-card {
    background: white;
    border: 2px solid #e9ecef;
    border-radius: 16px;
    padding: 16px 8px;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s;
}
.letter-card:hover {
    border-color: #FF6B35;
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(255,107,53,0.15);
}
.letter-big {
    font-size: 2.2rem;
    font-weight: 900;
    color: #FF6B35;
    line-height: 1;
}
.letter-sound {
    font-size: 0.75rem;
    color: #888;
    margin-top: 4px;
}

/* Flashcard */
.flashcard-container {
    perspective: 1000px;
    width: 100%;
    max-width: 500px;
    margin: 0 auto;
}
.flashcard {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 24px;
    padding: 48px 32px;
    text-align: center;
    color: white;
    min-height: 280px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    box-shadow: 0 12px 40px rgba(102, 126, 234, 0.3);
    cursor: pointer;
    transition: transform 0.3s;
}
.flashcard:hover {
    transform: scale(1.02);
}
.flashcard-word {
    font-size: 2.5rem;
    font-weight: 800;
    margin-bottom: 8px;
}
.flashcard-pron {
    font-size: 1rem;
    opacity: 0.8;
    font-style: italic;
}
.flashcard-back {
    background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%) !important;
    box-shadow: 0 12px 40px rgba(17, 153, 142, 0.3) !important;
}

/* Deck selector */
.deck-btn {
    background: white;
    border: 2px solid #e9ecef;
    border-radius: 14px;
    padding: 14px 20px;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s;
    font-weight: 700;
}
.deck-btn:hover, .deck-btn.active {
    border-color: #FF6B35;
    background: #fff5f0;
    color: #FF6B35;
}

/* Translate */
.translate-box {
    background: white;
    border-radius: 20px;
    padding: 24px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    border: 2px solid #f0f0f0;
}
.translate-result {
    background: linear-gradient(135deg, #f8f9fa, #e9ecef);
    border-radius: 16px;
    padding: 20px;
    margin-top: 16px;
}
.grammar-note {
    background: #e7f3ff;
    border-left: 4px solid #0066cc;
    border-radius: 8px;
    padding: 12px 16px;
    margin: 8px 0;
}

/* TTS button */
.tts-btn {
    background: #FF6B35 !important;
    color: white !important;
    border-radius: 50% !important;
    width: 40px !important;
    height: 40px !important;
    padding: 0 !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 1.1rem !important;
}

/* Microphone */
.mic-btn {
    background: linear-gradient(135deg, #FF6B35, #F7931E) !important;
    color: white !important;
    border-radius: 50% !important;
    width: 56px !important;
    height: 56px !important;
    padding: 0 !important;
    font-size: 1.4rem !important;
    box-shadow: 0 4px 16px rgba(255,107,53,0.4) !important;
}
.mic-btn:hover {
    transform: scale(1.1) !important;
}
.mic-recording {
    animation: pulse 1.5s infinite;
}
@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(255,107,53,0.7); }
    70% { box-shadow: 0 0 0 20px rgba(255,107,53,0); }
    100% { box-shadow: 0 0 0 0 rgba(255,107,53,0); }
}

/* Scenario pills */
.scenario-pill {
    display: inline-block;
    padding: 8px 18px;
    border-radius: 100px;
    font-weight: 700;
    font-size: 0.85rem;
    cursor: pointer;
    transition: all 0.2s;
    margin: 4px;
    border: 2px solid #e9ecef;
    background: white;
    color: #666;
}
.scenario-pill:hover, .scenario-pill.active {
    background: #FF6B35;
    color: white;
    border-color: #FF6B35;
    box-shadow: 0 4px 12px rgba(255,107,53,0.3);
}

/* Progress */
.progress-ring {
    width: 60px;
    height: 60px;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 6px;
}
::-webkit-scrollbar-track {
    background: #f1f1f1;
}
::-webkit-scrollbar-thumb {
    background: #FF6B35;
    border-radius: 3px;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# TTS / SPEECH RECOGNITION HELPERS (JavaScript injection)
# ============================================================
def tts_button(text, lang="de-DE", label="🔊"):
    """Inject a TTS button using Web Speech API"""
    btn_id = f"tts_{hash(text) % 100000}"
    js = f"""
    <button id="{btn_id}" style="background:#FF6B35;color:white;border:none;border-radius:50%;width:36px;height:36px;cursor:pointer;font-size:1rem;display:inline-flex;align-items:center;justify-content:center;margin-left:8px;" onclick="speakText(this)" data-text="{text.replace(chr(34), '&quot;')}" data-lang="{lang}">{label}</button>
    <script>
    function speakText(btn) {{
        const text = btn.getAttribute('data-text');
        const lang = btn.getAttribute('data-lang');
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = lang;
        utterance.rate = 0.9;
        utterance.pitch = 1.0;
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(utterance);
    }}
    </script>
    """
    return js

def speech_recognition_input(key="speech_input"):
    """Inject speech recognition input"""
    js = """
    <div style="display:flex;align-items:center;gap:10px;margin:10px 0;">
        <input type="text" id="speech_result" placeholder="🎤 Click mic to speak in German..." 
            style="flex:1;padding:12px 16px;border:2px solid #e9ecef;border-radius:12px;font-size:1rem;outline:none;"
            onfocus="this.style.borderColor='#FF6B35'" onblur="this.style.borderColor='#e9ecef'">
        <button id="mic_btn" onclick="toggleMic()" 
            style="background:linear-gradient(135deg,#FF6B35,#F7931E);color:white;border:none;border-radius:50%;width:50px;height:50px;cursor:pointer;font-size:1.3rem;box-shadow:0 4px 16px rgba(255,107,53,0.4);">
            🎤
        </button>
    </div>
    <script>
    let recognition = null;
    let isRecording = false;
    function toggleMic() {
        const btn = document.getElementById('mic_btn');
        const input = document.getElementById('speech_result');
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            alert('Speech recognition not supported in this browser. Try Chrome!');
            return;
        }
        if (!recognition) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognition = new SpeechRecognition();
            recognition.lang = 'de-DE';
            recognition.continuous = false;
            recognition.interimResults = true;
            recognition.onresult = function(event) {
                let final = '';
                for (let i = event.resultIndex; i < event.results.length; i++) {
                    if (event.results[i].isFinal) {
                        final += event.results[i][0].transcript;
                    }
                }
                if (final) input.value = final;
            };
            recognition.onend = function() {
                isRecording = false;
                btn.style.background = 'linear-gradient(135deg,#FF6B35,#F7931E)';
                btn.innerHTML = '🎤';
                // Auto-submit to Streamlit
                const event = new Event('input', { bubbles: true });
                input.dispatchEvent(event);
            };
            recognition.onerror = function() {
                isRecording = false;
                btn.style.background = 'linear-gradient(135deg,#FF6B35,#F7931E)';
                btn.innerHTML = '🎤';
            };
        }
        if (isRecording) {
            recognition.stop();
            isRecording = false;
            btn.style.background = 'linear-gradient(135deg,#FF6B35,#F7931E)';
            btn.innerHTML = '🎤';
        } else {
            recognition.start();
            isRecording = true;
            btn.style.background = '#dc3545';
            btn.innerHTML = '⏹️';
            input.value = '';
            input.placeholder = 'Listening...';
        }
    }
    // Bridge to Streamlit
    const observer = new MutationObserver(() => {
        const input = document.getElementById('speech_result');
        if (input && !input._streamlitBound) {
            input._streamlitBound = true;
            input.addEventListener('change', () => {
                window.parent.postMessage({type: 'streamlit:setComponentValue', value: input.value}, '*');
            });
        }
    });
    observer.observe(document.body, { childList: true, subtree: true });
    </script>
    """
    return js

# ============================================================
# MAIN APP
# ============================================================
init_session_state()

# Header
st.markdown(f"""
<div class="app-header">
    <h1>🌍 LinguaLearn</h1>
    <p>Master {LANGUAGE} · {USER_LEVEL} Level · Learn. Speak. Connect.</p>
</div>
""", unsafe_allow_html=True)

# Stats bar
learned_count = len(st.session_state.learned_words)
streak = st.session_state.streak
st.markdown(f"""
<div class="stats-bar">
    <div class="stat-card">
        <div class="stat-number">{streak}</div>
        <div class="stat-label">🔥 Day Streak</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">{learned_count}</div>
        <div class="stat-label">📚 Words Learned</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">{len(PRESET_DECKS) + len(st.session_state.vocab_decks)}</div>
        <div class="stat-label">🗂️ Decks</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">{USER_LEVEL[:3]}</div>
        <div class="stat-label">📊 Level</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# TABS
# ============================================================
tabs = st.tabs(["💬 CHAT", "🔤 ALPHABET", "🗂️ VOCAB", "🔄 TRANSLATE"])

# ===================== TAB 1: CHAT =====================
with tabs[0]:
    st.markdown("<h2 style='margin-bottom:4px;'>💬 German Tutor</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#888;margin-bottom:16px;'>Practice speaking German with your AI tutor. Pick a scenario below!</p>", unsafe_allow_html=True)

    # Scenario selector
    scenarios = ["Free Chat", "Order Coffee", "Meet Someone", "At the Airport"]
    cols = st.columns(len(scenarios))
    for i, sc in enumerate(scenarios):
        is_active = st.session_state.current_scenario == sc
        btn_style = "background:#FF6B35;color:white;border-color:#FF6B35;" if is_active else ""
        if cols[i].button(sc, key=f"sc_{sc}", use_container_width=True):
            st.session_state.current_scenario = sc
            st.session_state.chat_history = []
            st.rerun()

    st.markdown(f"<p style='color:#FF6B35;font-weight:700;margin:12px 0;'>📍 Current: {st.session_state.current_scenario}</p>", unsafe_allow_html=True)

    # Chat history display
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f"""
                <div style="display:flex;justify-content:flex-end;">
                    <div class="chat-bubble-user">{msg["text"]}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                tts_html = tts_button(msg["german"], LANGUAGE_CODE)
                corrections_html = ""
                if msg.get("corrections"):
                    for c in msg["corrections"]:
                        corrections_html += f"""
                        <div class="correction-box">
                            <span class="mistake">✗ {c['mistake']}</span> → 
                            <span class="fix">✓ {c['correction']}</span><br>
                            <small style="color:#666;">💡 {c['explanation']}</small>
                        </div>
                        """
                st.markdown(f"""
                <div style="display:flex;justify-content:flex-start;">
                    <div class="chat-bubble-tutor">
                        <div style="font-size:1.15rem;font-weight:700;margin-bottom:4px;">{msg["german"]}</div>
                        <div style="font-size:0.9rem;color:#666;margin-bottom:4px;">🔊 {msg["pronunciation"]}</div>
                        <div style="font-size:0.85rem;color:#888;font-style:italic;">"{msg["english"]}"</div>
                        {tts_html}
                    </div>
                </div>
                {corrections_html}
                """, unsafe_allow_html=True)

    # Input area
    st.markdown("---")

    # Text input
    col1, col2 = st.columns([6, 1])
    with col1:
        user_input = st.text_input("Type in German or English...", key="chat_input", label_visibility="collapsed", placeholder="Type your message here...")
    with col2:
        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
        send_clicked = st.button("➤ Send", key="send_btn", use_container_width=True)

    # Speech recognition
    st.markdown(speech_recognition_input(), unsafe_allow_html=True)

    # Handle send
    if send_clicked and user_input.strip():
        update_streak()
        st.session_state.chat_history.append({"role": "user", "text": user_input.strip()})

        # Get tutor response
        resp = simulate_claude_chat(
            user_input.strip(),
            st.session_state.current_scenario,
            USER_LEVEL,
            st.session_state.chat_history
        )
        st.session_state.chat_history.append({
            "role": "tutor",
            "german": resp["german"],
            "english": resp["english"],
            "pronunciation": resp["pronunciation"],
            "corrections": resp["corrections"],
        })
        save_progress()
        st.rerun()

# ===================== TAB 2: ALPHABET =====================
with tabs[1]:
    st.markdown("<h2 style='margin-bottom:4px;'>🔤 German Alphabet</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#888;margin-bottom:16px;'>Tap any letter to hear its sound and see an example word.</p>", unsafe_allow_html=True)

    # Display alphabet in a grid
    cols_per_row = 6
    for i in range(0, len(GERMAN_ALPHABET), cols_per_row):
        row_letters = GERMAN_ALPHABET[i:i+cols_per_row]
        cols = st.columns(cols_per_row)
        for j, (letter, sound, word, meaning, pron) in enumerate(row_letters):
            with cols[j]:
                tts = tts_button(letter, LANGUAGE_CODE, "🔊")
                is_learned = letter in st.session_state.alphabet_progress
                border_color = "#28a745" if is_learned else "#e9ecef"
                st.markdown(f"""
                <div class="letter-card" style="border-color:{border_color};" onclick="document.getElementById('letter_detail_{letter}').scrollIntoView({{behavior:'smooth'}})">
                    <div class="letter-big">{letter}</div>
                    <div class="letter-sound">/{sound}/</div>
                    {tts}
                </div>
                """, unsafe_allow_html=True)

    # Letter detail section
    st.markdown("---")
    st.markdown("<h3>📖 Letter Details</h3>", unsafe_allow_html=True)

    selected_letter = st.selectbox("Select a letter to explore:", [l[0] for l in GERMAN_ALPHABET])

    for letter, sound, word, meaning, pron in GERMAN_ALPHABET:
        if letter == selected_letter:
            tts_letter = tts_button(letter, LANGUAGE_CODE, "🔊 Letter")
            tts_word = tts_button(word, LANGUAGE_CODE, "🔊 Word")
            st.markdown(f"""
            <div id="letter_detail_{letter}" style="background:white;border-radius:20px;padding:28px;box-shadow:0 4px20px rgba(0,0,0,0.06);border:2px solid #f0f0f0;">
                <div style="display:flex;align-items:center;gap:16px;margin-bottom:16px;">
                    <div style="font-size:4rem;font-weight:900;color:#FF6B35;line-height:1;">{letter}</div>
                    <div>
                        <div style="font-size:1.3rem;font-weight:700;">Sound: /{sound}/</div>
                        <div style="color:#888;">IPA: [{pron}]</div>
                    </div>
                    {tts_letter}
                </div>
                <div style="background:#f8f9fa;border-radius:12px;padding:16px;">
                    <div style="font-size:1.1rem;font-weight:700;margin-bottom:4px;">Example: {word}</div>
                    <div style="color:#666;margin-bottom:8px;">"{meaning}" · 🔊 {pron}</div>
                    {tts_word}
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"✓ Mark {letter} as learned", key=f"learn_letter_{letter}"):
                st.session_state.alphabet_progress[letter] = True
                update_streak()
                save_progress()
                st.success(f"🎉 {letter} marked as learned!")
                st.rerun()
            break

# ===================== TAB 3: VOCAB =====================
with tabs[2]:
    st.markdown("<h2 style='margin-bottom:4px;'>🗂️ Vocabulary Flashcards</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#888;margin-bottom:16px;'>Flip cards, hear pronunciations, and build your vocabulary!</p>", unsafe_allow_html=True)

    # Deck selection
    st.markdown("<h4>📚 Choose a Deck</h4>", unsafe_allow_html=True)

    all_decks = {**PRESET_DECKS, **st.session_state.vocab_decks}
    deck_names = list(all_decks.keys())

    deck_cols = st.columns(min(len(deck_names) + 1, 5))
    for i, name in enumerate(deck_names):
        is_active = st.session_state.current_deck == name
        btn_type = "primary" if is_active else "secondary"
        if deck_cols[i].button(f"📂 {name}", key=f"deck_{name}", type=btn_type, use_container_width=True):
            st.session_state.current_deck = name
            st.session_state.current_card_index = 0
            st.session_state.card_flipped = False
            st.rerun()

    # Custom deck generator
    st.markdown("---")
    st.markdown("<h4>✨ Generate Custom Deck</h4>", unsafe_allow_html=True)
    custom_topic = st.text_input("Enter any topic (e.g., 'sports', 'emotions', 'office')...", key="custom_topic_input")
    if st.button("🚀 Generate 10-Card Deck", type="primary"):
        if custom_topic.strip():
            with st.spinner("Generating your custom deck..."):
                deck = simulate_claude_vocab(custom_topic.strip())
                st.session_state.vocab_decks[custom_topic.strip().capitalize()] = deck
                st.session_state.current_deck = custom_topic.strip().capitalize()
                st.session_state.current_card_index = 0
                st.session_state.card_flipped = False
                save_progress()
            st.success(f"✅ Generated '{custom_topic.strip().capitalize()}' deck with 10 cards!")
            st.rerun()

    # Flashcard display
    if st.session_state.current_deck and st.session_state.current_deck in all_decks:
        deck = all_decks[st.session_state.current_deck]
        idx = st.session_state.current_card_index
        total = len(deck)

        st.markdown(f"<p style='text-align:center;color:#888;'>Card {idx + 1} of {total}</p>", unsafe_allow_html=True)

        # Progress bar
        progress = (idx + 1) / total
        st.progress(progress)

        # Card
        card = deck[idx]
        german, english, pron = card

        is_flipped = st.session_state.card_flipped

        if is_flipped:
            card_html = f"""
            <div class="flashcard-container">
                <div class="flashcard flashcard-back" onclick="window.location.reload()">
                    <div class="flashcard-word">{english}</div>
                    <div class="flashcard-pron">English</div>
                </div>
            </div>
            """
        else:
            tts = tts_button(german, LANGUAGE_CODE, "🔊")
            card_html = f"""
            <div class="flashcard-container">
                <div class="flashcard" onclick="window.location.reload()">
                    <div class="flashcard-word">{german}</div>
                    <div class="flashcard-pron">{pron}</div>
                    {tts}
                </div>
            </div>
            """

        st.markdown(card_html, unsafe_allow_html=True)

        # Card controls
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("🔄 Flip", use_container_width=True, key="flip_btn"):
                st.session_state.card_flipped = not st.session_state.card_flipped
                st.rerun()

        with col2:
            if st.button("🔊 Hear", use_container_width=True, key="hear_btn"):
                st.markdown(f"""
                <script>
                const u = new SpeechSynthesisUtterance("{german}");
                u.lang = 'de-DE';
                u.rate = 0.9;
                window.speechSynthesis.speak(u);
                </script>
                """, unsafe_allow_html=True)

        with col3:
            if st.button("✅ Learned", use_container_width=True, key="learned_btn"):
                st.session_state.learned_words.add(german)
                update_streak()
                save_progress()
                st.success(f"🎉 '{german}' marked as learned!")
                if idx < total - 1:
                    st.session_state.current_card_index += 1
                    st.session_state.card_flipped = False
                st.rerun()

        with col4:
            if st.button("⏭️ Next", use_container_width=True, key="next_btn"):
                if idx < total - 1:
                    st.session_state.current_card_index += 1
                    st.session_state.card_flipped = False
                else:
                    st.session_state.current_card_index = 0
                    st.session_state.card_flipped = False
                    st.balloons()
                st.rerun()

        # Navigation
        nav_cols = st.columns(3)
        with nav_cols[0]:
            if st.button("⏮️ Previous", use_container_width=True, disabled=idx==0):
                st.session_state.current_card_index = max(0, idx - 1)
                st.session_state.card_flipped = False
                st.rerun()
        with nav_cols[1]:
            if st.button("🔀 Shuffle", use_container_width=True):
                random.shuffle(deck)
                all_decks[st.session_state.current_deck] = deck
                st.session_state.current_card_index = 0
                st.session_state.card_flipped = False
                st.rerun()
        with nav_cols[2]:
            if st.button("🔄 Restart", use_container_width=True):
                st.session_state.current_card_index = 0
                st.session_state.card_flipped = False
                st.rerun()
    else:
        st.info("👆 Select a deck above to start learning!")

# ===================== TAB 4: TRANSLATE =====================
with tabs[3]:
    st.markdown("<h2 style='margin-bottom:4px;'>🔄 Translator</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#888;margin-bottom:16px;'>Translate between English and German with pronunciation and grammar notes.</p>", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col1:
        translate_input = st.text_area("Enter text to translate...", height=100, key="translate_input_area", placeholder="Type English or German here...")
    with col2:
        st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
        direction = st.radio("Direction:", ["English → German", "German → English"], key="trans_dir")

    if st.button("🚀 Translate", type="primary", use_container_width=True):
        if translate_input.strip():
            dir_code = "en_to_de" if direction == "English → German" else "de_to_en"
            result = simulate_claude_translate(translate_input.strip(), dir_code)
            st.session_state.translate_result = result
            update_streak()
            save_progress()
            st.rerun()

    # Display result
    if st.session_state.translate_result:
        res = st.session_state.translate_result
        tts_orig = tts_button(res["original"], "de-DE" if res["direction"] == "de_to_en" else "en-US", "🔊")
        tts_trans = tts_button(res["translated"], "de-DE" if res["direction"] == "en_to_de" else "en-US", "🔊")

        st.markdown(f"""
        <div class="translate-result">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
                <div>
                    <div style="font-size:0.75rem;color:#888;text-transform:uppercase;letter-spacing:1px;font-weight:700;">Original</div>
                    <div style="font-size:1.2rem;font-weight:700;">{res["original"]}</div>
                </div>
                {tts_orig}
            </div>
            <div style="border-top:2px dashed #ddd;margin:12px 0;"></div>
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
                <div>
                    <div style="font-size:0.75rem;color:#888;text-transform:uppercase;letter-spacing:1px;font-weight:700;">Translation</div>
                    <div style="font-size:1.4rem;font-weight:800;color:#FF6B35;">{res["translated"]}</div>
                    <div style="font-size:0.9rem;color:#666;font-style:italic;">🔊 {res["pronunciation"]}</div>
                </div>
                {tts_trans}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Grammar notes
        if res.get("grammar_notes"):
            st.markdown("<h4 style='margin-top:20px;'>📚 Grammar Breakdown</h4>", unsafe_allow_html=True)
            for note in res["grammar_notes"]:
                st.markdown(f"""
                <div class="grammar-note">
                    <strong style="color:#0066cc;">{note['word']}</strong><br>
                    <span style="color:#444;">{note['note']}</span>
                </div>
                """, unsafe_allow_html=True)

        # Word-by-word
        st.markdown("<h4 style='margin-top:16px;'>🔍 Word-by-Word</h4>", unsafe_allow_html=True)
        words = res["original"].split()
        for w in words:
            clean = w.strip(".,!?;:")
            st.markdown(f"""
            <span style="display:inline-block;background:#f0f4f8;border-radius:8px;padding:6px 12px;margin:4px;font-weight:600;">
                {clean}
            </span>
            """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align:center;color:#aaa;font-size:0.8rem;'>🌍 LinguaLearn · Built with ❤️ for language learners · Progress auto-saved</p>", unsafe_allow_html=True)
