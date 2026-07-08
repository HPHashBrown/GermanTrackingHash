"""
DeutschMeister - Premium German Learning Tracker
Single-file self-contained Streamlit app
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import random
import json

st.set_page_config(page_title="DeutschMeister 🇩🇪", page_icon="🇩🇪", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%); }
.main .block-container { padding-top: 1rem; padding-bottom: 2rem; max-width: 1200px; }
h1 { background: linear-gradient(90deg, #FFD700, #FF6B6B, #FFD700); -webkit-background-clip: text !important; -webkit-text-fill-color: transparent !important; font-weight: 800 !important; }
h2, h3, h4 { color: #e2e8f0 !important; }
p, label, .stMarkdown { color: #a0aec0 !important; }
.glass-card { background: rgba(255,255,255,0.05); border-radius: 16px; padding: 20px; border: 1px solid rgba(255,255,255,0.1); }
.stat-card { background: linear-gradient(135deg, rgba(102,126,234,0.2) 0%, rgba(118,75,162,0.2) 100%); border-radius: 16px; padding: 20px; text-align: center; border: 1px solid rgba(255,255,255,0.1); }
.stButton > button { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important; color: white !important; border: none !important; border-radius: 12px !important; font-weight: 600 !important; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%) !important; }
.stTextInput > div > div > input, .stNumberInput > div > div > input, .stSelectbox > div > div > div, .stTextArea > div > div > textarea { background: rgba(255,255,255,0.05) !important; border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 12px !important; color: white !important; }
.stProgress > div > div { background: linear-gradient(90deg, #667eea, #764ba2) !important; border-radius: 10px; }
.stTabs [data-baseweb="tab"] { background: rgba(255,255,255,0.05) !important; border-radius: 10px 10px 0 0 !important; color: #a0aec0 !important; border: none !important; }
.stTabs [aria-selected="true"] { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important; color: white !important; }
#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

def init_state():
    defaults = {
        "current_page": "Dashboard",
        "user_profile": {"name": "Learner", "current_level": "B1", "target_level": "C1", "daily_goal_minutes": 30, "weekly_goal_hours": 5, "joined_date": date.today().isoformat()},
        "xp": 0, "level": 1, "streak": 0, "longest_streak": 0, "last_study_date": None,
        "achievements": [], "study_sessions": [], "total_minutes": 0,
        "today_minutes": 0, "weekly_minutes": 0, "monthly_minutes": 0,
        "vocabulary": [],
        "skill_minutes": {"Grammar": 0, "Vocabulary": 0, "Listening": 0, "Reading": 0, "Speaking": 0, "Writing": 0},
        "level_progress": {"A1": {"completed": True, "hours": 80, "required": 80}, "A2": {"completed": True, "hours": 120, "required": 120}, "B1": {"completed": False, "hours": 45, "required": 180}, "B2": {"completed": False, "hours": 0, "required": 240}, "C1": {"completed": False, "hours": 0, "required": 300}, "C2": {"completed": False, "hours": 0, "required": 400}},
        "daily_missions": [], "missions_completed_today": [], "last_mission_reset": date.today().isoformat(),
        "word_of_the_day": None, "last_word_reset": date.today().isoformat(),
        "daily_quote": None, "last_quote_reset": date.today().isoformat(),
        "flashcard_index": 0, "flashcard_flipped": False,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val
    if not st.session_state.daily_missions or st.session_state.last_mission_reset != date.today().isoformat():
        st.session_state.daily_missions = generate_missions()
        st.session_state.missions_completed_today = []
        st.session_state.last_mission_reset = date.today().isoformat()
        st.session_state.today_minutes = 0
    if not st.session_state.word_of_the_day or st.session_state.last_word_reset != date.today().isoformat():
        st.session_state.word_of_the_day = get_word()
        st.session_state.last_word_reset = date.today().isoformat()
    if not st.session_state.daily_quote or st.session_state.last_quote_reset != date.today().isoformat():
        st.session_state.daily_quote = get_quote()
        st.session_state.last_quote_reset = date.today().isoformat()

def generate_missions():
    pool = [
        {"id": "grammar_30", "title": "Study 30 minutes of grammar", "icon": "📖", "target": 30, "unit": "min", "skill": "Grammar", "xp": 50},
        {"id": "vocab_10", "title": "Learn 10 new vocabulary words", "icon": "📝", "target": 10, "unit": "words", "skill": "Vocabulary", "xp": 40},
        {"id": "listening_1", "title": "Complete a listening exercise", "icon": "🎧", "target": 1, "unit": "exercise", "skill": "Listening", "xp": 30},
        {"id": "reading_15", "title": "Read for 15 minutes", "icon": "📚", "target": 15, "unit": "min", "skill": "Reading", "xp": 35},
        {"id": "speaking_10", "title": "Practice speaking for 10 minutes", "icon": "🗣️", "target": 10, "unit": "min", "skill": "Speaking", "xp": 45},
        {"id": "writing_1", "title": "Write a short paragraph", "icon": "✍️", "target": 1, "unit": "paragraph", "skill": "Writing", "xp": 40},
        {"id": "streak_maintain", "title": "Maintain your study streak", "icon": "🔥", "target": 1, "unit": "day", "skill": "General", "xp": 25},
        {"id": "review_20", "title": "Review flashcards for 20 minutes", "icon": "🃏", "target": 20, "unit": "min", "skill": "Vocabulary", "xp": 35},
    ]
    return random.sample(pool, min(3, len(pool)))

def get_word():
    words = [
        {"word": "die Geduld", "translation": "patience", "example": "Geduld ist die Mutter der Weisheit.", "example_en": "Patience is the mother of wisdom."},
        {"word": "das Abenteuer", "translation": "adventure", "example": "Das Leben ist entweder ein Abenteuer oder nichts.", "example_en": "Life is either a daring adventure or nothing."},
        {"word": "die Freundschaft", "translation": "friendship", "example": "Echte Freundschaft ist eine langsame Pflanze.", "example_en": "True friendship is a plant of slow growth."},
        {"word": "das Wissen", "translation": "knowledge", "example": "Wissen ist Macht.", "example_en": "Knowledge is power."},
        {"word": "die Hoffnung", "translation": "hope", "example": "Hoffnung ist der Regenbogen über dem herabstürzenden Strom des Lebens.", "example_en": "Hope is the rainbow over the cascading stream of life."},
        {"word": "die Entschlossenheit", "translation": "determination", "example": "Entschlossenheit ist der Schlüssel zum Erfolg.", "example_en": "Determination is the key to success."},
        {"word": "die Neugier", "translation": "curiosity", "example": "Neugier ist der Funke hinter jedem großen Entdeckung.", "example_en": "Curiosity is the spark behind every great discovery."},
        {"word": "die Ausdauer", "translation": "perseverance", "example": "Ausdauer ist der Weg zum Ziel.", "example_en": "Perseverance is the path to the goal."},
        {"word": "die Leidenschaft", "translation": "passion", "example": "Leidenschaft ist der Antrieb aller großen Taten.", "example_en": "Passion is the driving force behind all great deeds."},
        {"word": "die Kreativität", "translation": "creativity", "example": "Kreativität ist Intelligenz, die Spaß hat.", "example_en": "Creativity is intelligence having fun."},
    ]
    return random.choice(words)

def get_quote():
    quotes = [
        {"text": "Sprich Deutsch, lebe mehr.", "author": "German Proverb", "en": "Speak German, live more."},
        {"text": "Übung macht den Meister.", "author": "German Proverb", "en": "Practice makes perfect."},
        {"text": "Aller Anfang ist schwer.", "author": "German Proverb", "en": "All beginnings are difficult."},
        {"text": "Ohne Fleiß kein Preis.", "author": "German Proverb", "en": "No pain, no gain."},
        {"text": "Der Weg ist das Ziel.", "author": "Konfuzius", "en": "The journey is the destination."},
        {"text": "Wer nicht wagt, der nicht gewinnt.", "author": "German Proverb", "en": "Nothing ventured, nothing gained."},
        {"text": "Kleine Schritte führen auch ans Ziel.", "author": "Unknown", "en": "Small steps also lead to the goal."},
        {"text": "Jeder Tag ist eine neue Chance.", "author": "Unknown", "en": "Every day is a new chance."},
    ]
    return random.choice(quotes)

def add_xp(amount):
    st.session_state.xp += amount
    new_level = 1
    xp_needed = 100
    total_xp = st.session_state.xp
    while total_xp >= xp_needed:
        total_xp -= xp_needed
        new_level += 1
        xp_needed = int(xp_needed * 1.2)
    if new_level > st.session_state.level:
        st.session_state.level = new_level
        st.balloons()
        st.success(f"🎉 Level Up! You reached Level {new_level}!")

def get_xp_next():
    level = st.session_state.level
    xp_needed = 100
    total = 0
    for i in range(1, level):
        total += xp_needed
        xp_needed = int(xp_needed * 1.2)
    return total + xp_needed

def update_streak():
    today = date.today().isoformat()
    if st.session_state.last_study_date != today:
        if st.session_state.last_study_date:
            last = datetime.strptime(st.session_state.last_study_date, "%Y-%m-%d").date()
            diff = (date.today() - last).days
            if diff == 1:
                st.session_state.streak += 1
            elif diff > 1:
                st.session_state.streak = 1
        else:
            st.session_state.streak = 1
        st.session_state.last_study_date = today
        if st.session_state.streak > st.session_state.longest_streak:
            st.session_state.longest_streak = st.session_state.streak

def check_achievements():
    total_hours = st.session_state.total_minutes // 60
    streak = st.session_state.streak
    earned = {a["name"] for a in st.session_state.achievements}
    checks = [
        (streak >= 3, "Getting Started", "🌱", "3-day streak", 30),
        (streak >= 7, "Week Warrior", "🔥", "7-day streak", 70),
        (streak >= 14, "Fortnight Fighter", "⚡", "14-day streak", 140),
        (streak >= 30, "Monthly Master", "📅", "30-day streak", 300),
        (streak >= 100, "Century Scholar", "💯", "100-day streak", 1000),
        (total_hours >= 10, "First Steps", "👣", "10 hours studied", 100),
        (total_hours >= 25, "Dedicated Learner", "📚", "25 hours studied", 250),
        (total_hours >= 50, "Half Century", "🎯", "50 hours studied", 500),
        (total_hours >= 100, "Century Club", "🏆", "100 hours studied", 1000),
        (total_hours >= 250, "Language Legend", "👑", "250 hours studied", 2500),
        (st.session_state.level_progress["A1"]["completed"], "A1 Graduate", "🎓", "Completed A1", 100),
        (st.session_state.level_progress["A2"]["completed"], "A2 Graduate", "📖", "Completed A2", 200),
        (st.session_state.level_progress["B1"]["completed"], "B1 Graduate", "🚀", "Completed B1", 500),
    ]
    for condition, name, icon, desc, xp in checks:
        if condition and name not in earned:
            st.session_state.achievements.append({"name": name, "icon": icon, "description": desc, "date": date.today().isoformat(), "xp": xp})
            add_xp(xp)
            st.balloons()


def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 10px 0 20px 0;">
            <div style="font-size: 48px; margin-bottom: 5px;">🇩🇪</div>
            <h2 style="margin: 0; background: linear-gradient(90deg, #FFD700, #FF6B6B); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 22px;">DeutschMeister</h2>
            <p style="color: #6b7280; font-size: 11px; margin-top: 5px;">Master German, One Day at a Time</p>
        </div>
        """, unsafe_allow_html=True)
        st.divider()
        profile = st.session_state.user_profile
        xp = st.session_state.xp
        level = st.session_state.level
        xp_next = get_xp_next()
        xp_progress = min(xp / xp_next, 1.0) if xp_next > 0 else 0
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.05); border-radius: 16px; padding: 16px; margin-bottom: 20px; border: 1px solid rgba(255,255,255,0.1);">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
                <div style="width: 45px; height: 45px; background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 20px;">👤</div>
                <div>
                    <div style="font-weight: 700; color: white; font-size: 15px;">{profile['name']}</div>
                    <div style="font-size: 11px; color: #a0aec0;">Level {level} • {profile['current_level']}</div>
                </div>
            </div>
            <div style="background: rgba(255,255,255,0.1); border-radius: 10px; height: 8px; overflow: hidden;">
                <div style="width: {xp_progress*100}%; height: 100%; background: linear-gradient(90deg, #FFD700, #FF6B6B); border-radius: 10px;"></div>
            </div>
            <div style="display: flex; justify-content: space-between; margin-top: 6px;">
                <span style="font-size: 10px; color: #a0aec0;">⭐ {xp:,} XP</span>
                <span style="font-size: 10px; color: #a0aec0;">{xp_next:,} needed</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-top: 10px; padding-top: 10px; border-top: 1px solid rgba(255,255,255,0.1);">
                <div style="text-align: center;"><div style="font-size: 16px;">🔥</div><div style="font-size: 13px; font-weight: 700; color: #FFD700;">{st.session_state.streak}</div><div style="font-size: 9px; color: #6b7280;">Streak</div></div>
                <div style="text-align: center;"><div style="font-size: 16px;">⏱️</div><div style="font-size: 13px; font-weight: 700; color: #3b82f6;">{st.session_state.total_minutes//60}h</div><div style="font-size: 9px; color: #6b7280;">Total</div></div>
                <div style="text-align: center;"><div style="font-size: 16px;">🏆</div><div style="font-size: 13px; font-weight: 700; color: #10b981;">{len(st.session_state.achievements)}</div><div style="font-size: 9px; color: #6b7280;">Badges</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<p style='color: #6b7280; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px;'>Navigation</p>", unsafe_allow_html=True)
        nav_items = [("Dashboard", "📊"), ("Study Session", "📝"), ("Roadmap", "🗺️"), ("Study Plan", "📅"), ("Vocabulary", "📚"), ("Resources", "🔗"), ("Achievements", "🏅"), ("Analytics", "📈"), ("Settings", "⚙️")]
        for page_name, icon in nav_items:
            is_active = st.session_state.current_page == page_name
            if st.button(f"{icon} {page_name}", key=f"nav_{page_name}", use_container_width=True, type="primary" if is_active else "secondary"):
                st.session_state.current_page = page_name
                st.rerun()
        st.divider()
        quote = st.session_state.daily_quote
        st.markdown(f"""
        <div style="background: rgba(102,126,234,0.1); border-left: 3px solid #667eea; border-radius: 0 8px 8px 0; padding: 12px; margin-top: 10px;">
            <p style="font-style: italic; color: #e2e8f0; font-size: 12px; margin: 0;">"{quote['text']}"</p>
            <p style="color: #6b7280; font-size: 10px; margin: 5px 0 0 0;">— {quote['author']}</p>
        </div>
        """, unsafe_allow_html=True)


def page_dashboard():
    st.markdown("""
    <div style="text-align: center; padding: 10px 0 25px 0;">
        <h1 style="font-size: 38px; margin-bottom: 5px;">🇩🇪 Willkommen zurück!</h1>
        <p style="color: #a0aec0; font-size: 16px;">Your German learning journey continues</p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, rgba(255,107,107,0.25) 0%, rgba(238,90,36,0.25) 100%);">
            <div style="font-size: 32px; margin-bottom: 5px;">🔥</div>
            <div style="font-size: 28px; font-weight: 700; color: #FF6B6B;">{st.session_state.streak}</div>
            <div style="font-size: 13px; color: #a0aec0;">Day Streak</div>
            <div style="font-size: 10px; color: #6b7280; margin-top: 5px;">Best: {st.session_state.longest_streak}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, rgba(255,215,0,0.15) 0%, rgba(255,107,107,0.15) 100%);">
            <div style="font-size: 32px; margin-bottom: 5px;">⭐</div>
            <div style="font-size: 28px; font-weight: 700; color: #FFD700;">{st.session_state.xp:,}</div>
            <div style="font-size: 13px; color: #a0aec0;">XP Points</div>
            <div style="font-size: 10px; color: #6b7280; margin-top: 5px;">Level {st.session_state.level}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        total_hours = st.session_state.total_minutes // 60
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, rgba(59,130,246,0.25) 0%, rgba(37,99,235,0.25) 100%);">
            <div style="font-size: 32px; margin-bottom: 5px;">📚</div>
            <div style="font-size: 28px; font-weight: 700; color: #3b82f6;">{total_hours}h</div>
            <div style="font-size: 13px; color: #a0aec0;">Total Study Time</div>
            <div style="font-size: 10px; color: #6b7280; margin-top: 5px;">{st.session_state.total_minutes % 60}m today</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        current = st.session_state.user_profile["current_level"]
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, rgba(16,185,129,0.25) 0%, rgba(5,150,105,0.25) 100%);">
            <div style="font-size: 32px; margin-bottom: 5px;">🎯</div>
            <div style="font-size: 28px; font-weight: 700; color: #10b981;">{current}</div>
            <div style="font-size: 13px; color: #a0aec0;">Current Level</div>
            <div style="font-size: 10px; color: #6b7280; margin-top: 5px;">Target: {st.session_state.user_profile["target_level"]}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    left_col, right_col = st.columns([2, 1])
    with left_col:
        st.markdown("""
        <div class="glass-card" style="margin-bottom: 20px;">
            <h3 style="margin: 0 0 15px 0; display: flex; align-items: center; gap: 10px;">
                <span>🎯</span> Today's Missions
            </h3>
        """, unsafe_allow_html=True)
        missions = st.session_state.daily_missions
        completed = st.session_state.missions_completed_today
        for mission in missions:
            is_done = mission["id"] in completed
            opacity = "0.4" if is_done else "1"
            strike = "text-decoration: line-through;" if is_done else ""
            check = "✅" if is_done else "⬜"
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.05); border-radius: 12px; padding: 12px 14px; margin-bottom: 8px; display: flex; align-items: center; gap: 12px; opacity: {opacity}; border: 1px solid rgba(255,255,255,0.05);">
                <span style="font-size: 22px;">{mission['icon']}</span>
                <div style="flex: 1;">
                    <div style="font-weight: 600; color: white; font-size: 13px; {strike}">{mission['title']}</div>
                    <div style="font-size: 11px; color: #6b7280;">+{mission['xp']} XP • {mission['skill']}</div>
                </div>
                <span style="font-size: 18px;">{check}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="glass-card">
            <h3 style="margin: 0 0 15px 0; display: flex; align-items: center; gap: 10px;">
                <span>📊</span> Skill Progress
            </h3>
        """, unsafe_allow_html=True)
        skills = st.session_state.skill_minutes
        total_skill = sum(skills.values()) or 1
        skill_colors = {"Grammar": "#FF6B6B", "Vocabulary": "#FFD700", "Listening": "#3b82f6", "Reading": "#10b981", "Speaking": "#8b5cf6", "Writing": "#f97316"}
        for skill, minutes in skills.items():
            pct = (minutes / total_skill) * 100 if total_skill > 0 else 0
            color = skill_colors.get(skill, "#667eea")
            hours = minutes // 60
            mins = minutes % 60
            st.markdown(f"""
            <div style="margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                    <span style="font-size: 12px; color: #e2e8f0;">{skill}</span>
                    <span style="font-size: 11px; color: #6b7280;">{hours}h {mins}m</span>
                </div>
                <div style="background: rgba(255,255,255,0.08); border-radius: 10px; height: 8px; overflow: hidden;">
                    <div style="width: {pct}%; height: 100%; background: {color}; border-radius: 10px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with right_col:
        word = st.session_state.word_of_the_day
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(102,126,234,0.15) 0%, rgba(118,75,162,0.15) 100%); border-radius: 20px; padding: 20px; border: 1px solid rgba(102,126,234,0.2); margin-bottom: 20px;">
            <h3 style="margin: 0 0 12px 0; font-size: 14px; color: #a0aec0;">💡 Word of the Day</h3>
            <div style="text-align: center; padding: 10px 0;">
                <div style="font-size: 24px; font-weight: 700; color: white; margin-bottom: 5px;">{word['word']}</div>
                <div style="font-size: 14px; color: #a0aec0; margin-bottom: 8px;">{word['translation']}</div>
                <div style="background: rgba(255,255,255,0.05); border-radius: 10px; padding: 10px; margin-top: 8px;">
                    <p style="font-style: italic; color: #e2e8f0; font-size: 12px; margin: 0;">"{word['example']}"</p>
                    <p style="color: #6b7280; font-size: 10px; margin: 4px 0 0 0;">{word['example_en']}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="glass-card" style="margin-bottom: 20px;">
            <h3 style="margin: 0 0 12px 0; font-size: 14px; color: #a0aec0;">⚡ Quick Actions</h3>
        """, unsafe_allow_html=True)
        if st.button("📝 Log Study Session", use_container_width=True, type="primary"):
            st.session_state.current_page = "Study Session"
            st.rerun()
        if st.button("🃏 Practice Flashcards", use_container_width=True):
            st.session_state.current_page = "Vocabulary"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="glass-card">
            <h3 style="margin: 0 0 12px 0; font-size: 14px; color: #a0aec0;">📅 Weekly Progress</h3>
        """, unsafe_allow_html=True)
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        today_idx = date.today().weekday()
        for i, day in enumerate(days):
            if i < today_idx:
                fill = random.choice([20, 45, 60, 30, 0, 15, 50])
                color = "#10b981" if fill > 0 else "#374151"
            elif i == today_idx:
                fill = st.session_state.today_minutes
                color = "#3b82f6"
            else:
                fill = 0
                color = "#374151"
            pct = min(fill / 60 * 100, 100)
            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                <span style="font-size: 11px; color: #6b7280; width: 30px;">{day}</span>
                <div style="flex: 1; background: rgba(255,255,255,0.05); border-radius: 6px; height: 16px; overflow: hidden;">
                    <div style="width: {pct}%; height: 100%; background: {color}; border-radius: 6px;"></div>
                </div>
                <span style="font-size: 10px; color: #6b7280; width: 25px; text-align: right;">{fill}m</span>
            </div>
            """, unsafe_allow_html=True)
        weekly_goal = st.session_state.user_profile["weekly_goal_hours"] * 60
        weekly_progress = st.session_state.weekly_minutes
        weekly_pct = min((weekly_progress / weekly_goal) * 100, 100)
        st.markdown(f"""
            <div style="margin-top: 12px; padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.1);">
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                    <span style="font-size: 11px; color: #a0aec0;">Weekly Goal</span>
                    <span style="font-size: 11px; color: #a0aec0;">{weekly_progress//60}h {weekly_progress%60}m / {weekly_goal//60}h</span>
                </div>
                <div style="background: rgba(255,255,255,0.05); border-radius: 10px; height: 8px; overflow: hidden;">
                    <div style="width: {weekly_pct}%; height: 100%; background: linear-gradient(90deg, #FFD700, #FF6B6B); border-radius: 10px;"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="glass-card">
        <h3 style="margin: 0 0 15px 0;">📋 Recent Activity</h3>
    """, unsafe_allow_html=True)
    sessions = st.session_state.study_sessions
    if sessions:
        recent = sessions[-5:][::-1]
        for session in recent:
            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 12px; padding: 10px; background: rgba(255,255,255,0.03); border-radius: 10px; margin-bottom: 6px; border: 1px solid rgba(255,255,255,0.05);">
                <div style="width: 36px; height: 36px; background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 16px;">📖</div>
                <div style="flex: 1;">
                    <div style="font-weight: 600; color: white; font-size: 13px;">{session.get('skill', 'Study')} • {session.get('level', 'B1')}</div>
                    <div style="font-size: 11px; color: #6b7280;">{session.get('focus', 'General study')} • {session.get('date', 'Today')}</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-weight: 700; color: #FFD700; font-size: 14px;">+{session.get('minutes', 0)}m</div>
                    <div style="font-size: 10px; color: #6b7280;">+{session.get('xp', 0)} XP</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No study sessions yet. Start your first session today! 🚀")
    st.markdown("</div>", unsafe_allow_html=True)


def page_study_session():
    st.markdown("""
    <div style="text-align: center; padding: 10px 0 25px 0;">
        <h1 style="font-size: 32px;">📝 Log Your Study Session</h1>
        <p style="color: #a0aec0;">Every minute counts on your journey to fluency</p>
    </div>
    """, unsafe_allow_html=True)
    with st.form("study_session_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            level = st.selectbox("📊 CEFR Level", ["A1", "A2", "B1", "B2", "C1", "C2"],
                                index=["A1", "A2", "B1", "B2", "C1", "C2"].index(st.session_state.user_profile["current_level"]))
            skill = st.selectbox("🎯 Skill Focus", ["Grammar", "Vocabulary", "Listening", "Reading", "Speaking", "Writing"])
            minutes = st.number_input("⏱️ Minutes Studied", min_value=1, max_value=300, value=30, step=5)
        with col2:
            focus = st.text_input("📝 What did you focus on?", placeholder="e.g., Modal verbs, Subjunctive...")
            difficulty = st.select_slider("📈 Difficulty", options=["Easy", "Medium", "Hard", "Challenge"], value="Medium")
            satisfaction = st.slider("😊 Satisfaction (1-10)", min_value=1, max_value=10, value=7)
        notes = st.text_area("🗒️ Session Notes", placeholder="What did you learn? Any challenges?", height=80)
        base_xp = minutes
        diff_mult = {"Easy": 1.0, "Medium": 1.2, "Hard": 1.5, "Challenge": 2.0}
        xp_gain = int(base_xp * diff_mult[difficulty])
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(255,215,0,0.1) 0%, rgba(255,107,107,0.1) 100%); border-radius: 12px; padding: 12px; text-align: center; margin: 15px 0; border: 1px solid rgba(255,215,0,0.2);">
            <span style="font-size: 13px; color: #a0aec0;">You will earn approximately </span>
            <span style="font-size: 18px; font-weight: 700; color: #FFD700;">⭐ {xp_gain} XP</span>
        </div>
        """, unsafe_allow_html=True)
        submitted = st.form_submit_button("🚀 Log Session & Earn XP", use_container_width=True, type="primary")
        if submitted:
            session = {
                "date": date.today().isoformat(), "datetime": datetime.now().isoformat(),
                "level": level, "skill": skill, "minutes": minutes,
                "focus": focus or "General study", "difficulty": difficulty,
                "satisfaction": satisfaction, "notes": notes, "xp": xp_gain
            }
            st.session_state.study_sessions.append(session)
            st.session_state.total_minutes += minutes
            st.session_state.today_minutes += minutes
            st.session_state.weekly_minutes += minutes
            st.session_state.monthly_minutes += minutes
            st.session_state.skill_minutes[skill] += minutes
            if level in st.session_state.level_progress:
                st.session_state.level_progress[level]["hours"] += minutes / 60
                if st.session_state.level_progress[level]["hours"] >= st.session_state.level_progress[level]["required"]:
                    st.session_state.level_progress[level]["completed"] = True
            update_streak()
            add_xp(xp_gain)
            check_achievements()
            for mission in st.session_state.daily_missions:
                if mission["id"] not in st.session_state.missions_completed_today:
                    if (mission["skill"] == skill or mission["skill"] == "General"):
                        if mission["unit"] == "min" and minutes >= mission["target"]:
                            st.session_state.missions_completed_today.append(mission["id"])
                            add_xp(mission["xp"])
            st.success(f"✅ Session logged! +{xp_gain} XP earned!")
            st.balloons()
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""<div class="glass-card"><h3 style="margin: 0 0 15px 0;">📋 Session History</h3>""", unsafe_allow_html=True)
    sessions = st.session_state.study_sessions
    if sessions:
        df = pd.DataFrame(sessions)
        if not df.empty:
            display_cols = ["date", "level", "skill", "minutes", "focus", "difficulty", "xp"]
            available_cols = [c for c in display_cols if c in df.columns]
            df_display = df[available_cols].copy()
            df_display.columns = [c.title() for c in available_cols]
            st.dataframe(df_display, use_container_width=True, hide_index=True)
    else:
        st.info("No sessions logged yet. Start studying! 📚")
    st.markdown("</div>", unsafe_allow_html=True)


def page_roadmap():
    st.markdown("""
    <div style="text-align: center; padding: 10px 0 25px 0;">
        <h1 style="font-size: 32px;">🗺️ Your Learning Roadmap</h1>
        <p style="color: #a0aec0;">From beginner to mastery — A1 to C2</p>
    </div>
    """, unsafe_allow_html=True)
    levels = {
        "A1": {"name": "Beginner", "hours": 80, "grammar": "Present tense, articles, word order, pronouns", "vocab": "650 words", "listening": "Simple phrases slowly", "reading": "Familiar names, simple sentences", "speaking": "Introduce yourself, basic Q&A", "writing": "Postcards, forms", "exam": "Goethe-Zertifikat A1", "plan": "5-7 hrs/week ~3 months"},
        "A2": {"name": "Elementary", "hours": 120, "grammar": "Past tense, dative, modal verbs, comparatives", "vocab": "1,300 words", "listening": "Personal/family topics", "reading": "Short simple texts", "speaking": "Describe daily life", "writing": "Notes, messages, letters", "exam": "Goethe-Zertifikat A2", "plan": "5-7 hrs/week ~4 months"},
        "B1": {"name": "Intermediate", "hours": 180, "grammar": "Subjunctive II, relative clauses, passive", "vocab": "2,400 words", "listening": "Clear standard speech", "reading": "Everyday/job texts", "speaking": "Most situations, experiences", "writing": "Connected text, letters", "exam": "Goethe-Zertifikat B1", "plan": "7-10 hrs/week ~5 months"},
        "B2": {"name": "Upper Intermediate", "hours": 240, "grammar": "Advanced subjunctive, nominalizations", "vocab": "3,500+ words", "listening": "Extended speech, TV, films", "reading": "Articles, literary prose", "speaking": "Fluency, discussions", "writing": "Detailed text, essays", "exam": "Goethe-Zertifikat B2", "plan": "8-12 hrs/week ~6 months"},
        "C1": {"name": "Advanced", "hours": 300, "grammar": "Refined usage, academic register", "vocab": "5,000+ words", "listening": "Unstructured extended speech", "reading": "Long complex texts", "speaking": "Flexible social/professional", "writing": "Well-structured detailed text", "exam": "Goethe-Zertifikat C1", "plan": "10-15 hrs/week ~7 months"},
        "C2": {"name": "Mastery", "hours": 400, "grammar": "Near-native command, idioms", "vocab": "8,000+ words", "listening": "Any spoken language", "reading": "All written forms", "speaking": "Spontaneous precision", "writing": "Flowing appropriate style", "exam": "Goethe-Zertifikat C2", "plan": "10+ hrs/week ongoing"},
    }
    progress = st.session_state.level_progress
    cols = st.columns(6)
    for i, (col, lvl) in enumerate(zip(cols, ["A1", "A2", "B1", "B2", "C1", "C2"])):
        with col:
            p = progress[lvl]
            if p["completed"]:
                color, status, glow = "#10b981", "✓", "box-shadow: 0 0 15px rgba(16,185,129,0.4);"
            elif p["hours"] > 0:
                color, status, glow = "#3b82f6", f"{int(p['hours'])}h", "box-shadow: 0 0 15px rgba(59,130,246,0.4); border: 2px solid #FFD700;"
            else:
                color, status, glow = "#6b7280", "🔒", ""
            pct = min((p["hours"] / p["required"]) * 100, 100)
            st.markdown(f"""
            <div style="text-align: center;">
                <div style="width: 55px; height: 55px; background: {color}; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 18px; color: white; margin: 0 auto; {glow}">
                    {lvl}
                </div>
                <div style="font-size: 10px; margin-top: 6px; color: {'#10b981' if p['completed'] else '#3b82f6' if p['hours'] > 0 else '#6b7280'};">
                    {status}
                </div>
                <div style="background: rgba(255,255,255,0.06); border-radius: 4px; height: 5px; margin-top: 6px; overflow: hidden;">
                    <div style="width: {pct}%; height: 100%; background: {color}; border-radius: 4px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    for lvl, info in levels.items():
        p = progress[lvl]
        pct = min((p["hours"] / p["required"]) * 100, 100)
        with st.expander(f"{'✅' if p['completed'] else '🎯' if p['hours'] > 0 else '🔒'} {lvl}: {info['name']} ({p['hours']:.0f}/{info['hours']} hrs)"):
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f"""
                <div class="glass-card">
                    <p><span style="color: #FFD700;">📖 Grammar:</span> <span style="color: #a0aec0;">{info['grammar']}</span></p>
                    <p><span style="color: #FFD700;">📝 Vocabulary:</span> <span style="color: #a0aec0;">{info['vocab']}</span></p>
                    <p><span style="color: #FFD700;">🎧 Listening:</span> <span style="color: #a0aec0;">{info['listening']}</span></p>
                    <p><span style="color: #FFD700;">📚 Reading:</span> <span style="color: #a0aec0;">{info['reading']}</span></p>
                    <p><span style="color: #FFD700;">🗣️ Speaking:</span> <span style="color: #a0aec0;">{info['speaking']}</span></p>
                    <p><span style="color: #FFD700;">✍️ Writing:</span> <span style="color: #a0aec0;">{info['writing']}</span></p>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="glass-card" style="text-align: center;">
                    <div style="font-size: 40px; margin-bottom: 10px;">{'🏆' if p['completed'] else '📈' if p['hours'] > 0 else '🔐'}</div>
                    <div style="font-size: 28px; font-weight: 700; color: {'#10b981' if p['completed'] else '#3b82f6'};">{pct:.0f}%</div>
                    <div style="font-size: 12px; color: #6b7280; margin-top: 10px;">Exam</div>
                    <div style="font-size: 13px; color: #e2e8f0;">{info['exam']}</div>
                    <div style="font-size: 12px; color: #6b7280; margin-top: 10px;">Plan</div>
                    <div style="font-size: 13px; color: #e2e8f0;">{info['plan']}</div>
                </div>
                """, unsafe_allow_html=True)


def page_study_plan():
    st.markdown("""
    <div style="text-align: center; padding: 10px 0 25px 0;">
        <h1 style="font-size: 32px;">📅 Your Study Plan</h1>
        <p style="color: #a0aec0;">AI-powered recommendations for balanced learning</p>
    </div>
    """, unsafe_allow_html=True)
    skills = st.session_state.skill_minutes
    total = sum(skills.values()) or 1
    weakest = min(skills, key=skills.get)
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(102,126,234,0.12) 0%, rgba(118,75,162,0.12) 100%); border-radius: 20px; padding: 20px; border: 1px solid rgba(102,126,234,0.2); margin-bottom: 20px;">
        <h3 style="margin: 0 0 12px 0;">🎯 Today's Recommended Focus</h3>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div style="text-align: center; padding: 15px; background: rgba(255,255,255,0.05); border-radius: 12px;">
            <div style="font-size: 32px; margin-bottom: 8px;">📖</div>
            <div style="font-weight: 700; color: white;">{weakest}</div>
            <div style="font-size: 11px; color: #FF6B6B; margin-top: 5px;">Priority Skill</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="text-align: center; padding: 15px; background: rgba(255,255,255,0.05); border-radius: 12px;">
            <div style="font-size: 32px; margin-bottom: 8px;">⏱️</div>
            <div style="font-weight: 700; color: white;">{st.session_state.user_profile['daily_goal_minutes']} min</div>
            <div style="font-size: 11px; color: #10b981; margin-top: 5px;">{st.session_state.today_minutes}/{st.session_state.user_profile['daily_goal_minutes']} done</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        current = st.session_state.user_profile["current_level"]
        next_lvl = {"A1": "A2", "A2": "B1", "B1": "B2", "B2": "C1", "C1": "C2", "C2": "Mastery"}[current]
        st.markdown(f"""
        <div style="text-align: center; padding: 15px; background: rgba(255,255,255,0.05); border-radius: 12px;">
            <div style="font-size: 32px; margin-bottom: 8px;">🚀</div>
            <div style="font-weight: 700; color: white;">{next_lvl}</div>
            <div style="font-size: 11px; color: #3b82f6; margin-top: 5px;">Next Milestone</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("""<div class="glass-card" style="margin-bottom: 20px;"><h3 style="margin: 0 0 15px 0;">📆 Suggested Weekly Schedule</h3>""", unsafe_allow_html=True)
    schedule = {
        "Monday": [("Grammar", "30 min", "#FF6B6B"), ("Vocabulary", "20 min", "#FFD700")],
        "Tuesday": [("Listening", "30 min", "#3b82f6"), ("Reading", "20 min", "#10b981")],
        "Wednesday": [("Grammar", "25 min", "#FF6B6B"), ("Speaking", "25 min", "#8b5cf6")],
        "Thursday": [("Vocabulary", "30 min", "#FFD700"), ("Writing", "20 min", "#f97316")],
        "Friday": [("Listening", "25 min", "#3b82f6"), ("Reading", "25 min", "#10b981")],
        "Saturday": [("Speaking", "30 min", "#8b5cf6"), ("Review", "20 min", "#667eea")],
        "Sunday": [("Free Practice", "40 min", "#10b981"), ("Culture", "20 min", "#ec4899")]
    }
    for day, activities in schedule.items():
        is_today = day == date.today().strftime("%A")
        border = "1px solid rgba(102,126,234,0.4)" if is_today else "1px solid rgba(255,255,255,0.05)"
        bg = "rgba(102,126,234,0.08)" if is_today else "rgba(255,255,255,0.03)"
        st.markdown(f"""
        <div style="background: {bg}; border-radius: 10px; padding: 10px 12px; margin-bottom: 8px; border: {border};">
            <div style="font-weight: 600; color: {'#667eea' if is_today else 'white'}; margin-bottom: 6px; font-size: 13px;">
                {'● ' if is_today else ''}{day}{' (Today)' if is_today else ''}
            </div>
            <div style="display: flex; gap: 8px; flex-wrap: wrap;">
        """, unsafe_allow_html=True)
        for skill, duration, color in activities:
            st.markdown(f"""
            <span style="background: {color}18; color: {color}; padding: 3px 10px; border-radius: 15px; font-size: 11px; border: 1px solid {color}30;">
                {skill} • {duration}
            </span>
            """, unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("""<div class="glass-card"><h3 style="margin: 0 0 15px 0;">⚖️ Skill Balance</h3>""", unsafe_allow_html=True)
    for skill, minutes in skills.items():
        avg = total / 6
        ratio = minutes / avg if avg > 0 else 0
        color = "#10b981" if 0.7 <= ratio <= 1.5 else "#FF6B6B" if ratio < 0.5 else "#3b82f6"
        st.markdown(f"""
        <div style="margin-bottom: 10px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 3px;">
                <span style="font-size: 12px; color: #e2e8f0;">{skill}</span>
                <span style="font-size: 11px; color: {color};">{minutes}m ({ratio:.1f}x avg)</span>
            </div>
            <div style="background: rgba(255,255,255,0.05); border-radius: 6px; height: 6px; overflow: hidden;">
                <div style="width: {min(ratio * 16.67, 100)}%; height: 100%; background: {color}; border-radius: 6px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def page_vocabulary():
    st.markdown("""
    <div style="text-align: center; padding: 10px 0 25px 0;">
        <h1 style="font-size: 32px;">📚 Vocabulary</h1>
        <p style="color: #a0aec0;">Build and practice your German vocabulary</p>
    </div>
    """, unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["📝 My Words", "🃏 Flashcards", "➕ Add Word"])
    with tab1:
        vocab = st.session_state.vocabulary
        if vocab:
            st.write(f"**{len(vocab)}** words saved")
            for word in vocab:
                with st.expander(f"{word['german']} — {word['translation']}"):
                    st.write(f"**Example:** {word.get('example', 'No example')}")
                    st.write(f"**Category:** {word.get('category', 'General')}")
        else:
            st.info("No words saved yet. Add your first word or use flashcards!")
    with tab2:
        flash_words = [
            {"german": "das Haus", "translation": "house", "example": "Das Haus ist groß."},
            {"german": "die Zeit", "translation": "time", "example": "Die Zeit vergeht schnell."},
            {"german": "der Mensch", "translation": "human/person", "example": "Der Mensch ist frei."},
            {"german": "die Arbeit", "translation": "work", "example": "Die Arbeit macht Spaß."},
            {"german": "das Leben", "translation": "life", "example": "Das Leben ist schön."},
        ] + st.session_state.vocabulary
        if flash_words:
            idx = st.session_state.flashcard_index % len(flash_words)
            word = flash_words[idx]
            if st.session_state.flashcard_flipped:
                card = f"""
                <div style="background: linear-gradient(135deg, rgba(102,126,234,0.15) 0%, rgba(118,75,162,0.15) 100%); border-radius: 20px; padding: 50px 30px; text-align: center; border: 2px solid rgba(102,126,234,0.3); min-height: 200px; display: flex; flex-direction: column; justify-content: center;">
                    <div style="font-size: 12px; color: #667eea; margin-bottom: 10px;">TRANSLATION</div>
                    <div style="font-size: 28px; font-weight: 700; color: white; margin-bottom: 10px;">{word['translation']}</div>
                    <div style="font-size: 14px; color: #a0aec0; font-style: italic;">"{word.get('example', '')}"</div>
                </div>
                """
            else:
                card = f"""
                <div style="background: linear-gradient(135deg, rgba(255,215,0,0.08) 0%, rgba(255,107,107,0.08) 100%); border-radius: 20px; padding: 50px 30px; text-align: center; border: 2px solid rgba(255,215,0,0.2); min-height: 200px; display: flex; flex-direction: column; justify-content: center;">
                    <div style="font-size: 12px; color: #FFD700; margin-bottom: 10px;">GERMAN</div>
                    <div style="font-size: 36px; font-weight: 700; color: white; margin-bottom: 10px;">{word['german']}</div>
                    <div style="font-size: 12px; color: #6b7280;">Click to reveal</div>
                </div>
                """
            st.markdown(card, unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("🔄 Flip", use_container_width=True):
                    st.session_state.flashcard_flipped = not st.session_state.flashcard_flipped
                    st.rerun()
            with c2:
                if st.button("✅ Know it", use_container_width=True):
                    st.session_state.flashcard_index += 1
                    st.session_state.flashcard_flipped = False
                    add_xp(10)
                    st.rerun()
            with c3:
                if st.button("❌ Again", use_container_width=True):
                    st.session_state.flashcard_index += 1
                    st.session_state.flashcard_flipped = False
                    st.rerun()
    with tab3:
        with st.form("add_word"):
            german = st.text_input("German Word")
            translation = st.text_input("Translation")
            example = st.text_input("Example Sentence (optional)")
            category = st.selectbox("Category", ["Noun", "Verb", "Adjective", "Phrase", "Other"])
            if st.form_submit_button("➕ Add to Collection"):
                if german and translation:
                    st.session_state.vocabulary.append({
                        "german": german, "translation": translation,
                        "example": example, "category": category,
                        "date_added": str(date.today())
                    })
                    st.success(f"Added '{german}' to your collection!")
                    add_xp(5)


def page_resources():
    st.markdown("""
    <div style="text-align: center; padding: 10px 0 25px 0;">
        <h1 style="font-size: 32px;">🔗 Free German Resources</h1>
        <p style="color: #a0aec0;">Curated collection of the best free learning materials</p>
    </div>
    """, unsafe_allow_html=True)
    resources = {
        "🎓 Official Courses": [
            {"name": "Deutsche Welle (DW Learn German)", "url": "https://www.dw.com/en/learn-german/s-2469", "desc": "Comprehensive free courses from A1 to C1 with videos, audio, and interactive exercises. The gold standard for self-study.", "level": "All levels"},
            {"name": "Goethe-Institut Free Resources", "url": "https://www.goethe.de/en/spr/ueb.html", "desc": "High-quality exercises, apps, videos, and games from Germany's official cultural institute.", "level": "All levels"},
            {"name": "Nico's Weg", "url": "https://www.dw.com/en/nicos-weg/c-40451752", "desc": "DW's award-winning interactive course following Nico's journey. Excellent for beginners.", "level": "A1-B1"},
            {"name": "deutsch.info", "url": "https://deutsch.info/", "desc": "Multilingual platform with courses, grammar, media library, and practical info about Germany/Austria.", "level": "A1-B2"},
        ],
        "📺 YouTube Channels": [
            {"name": "Easy German", "url": "https://www.youtube.com/@EasyGerman", "desc": "Street interviews with subtitles. Perfect for real-world listening practice and cultural immersion.", "level": "A2-C1"},
            {"name": "Learn German with Anja", "url": "https://www.youtube.com/@LearnGermanwithAnja", "desc": "Engaging lessons with clear explanations. Great for grammar and vocabulary building.", "level": "A1-B2"},
            {"name": "Natürlich German", "url": "https://www.youtube.com/@NatuerlichGerman", "desc": "Authentic content for intermediate learners focusing on natural speech patterns.", "level": "B1-C2"},
            {"name": "German Stories", "url": "https://www.youtube.com/@GermanStories", "desc": "Slow, clear stories in German with explanations. Excellent for listening comprehension.", "level": "A2-B1"},
        ],
        "🎧 Podcasts & Audio": [
            {"name": "Coffee Break German", "url": "https://coffeebreaklanguages.com/coffeebreakgerman/", "desc": "Structured podcast lessons from beginner to advanced. Very accessible and well-paced.", "level": "A1-B2"},
            {"name": "Slow German", "url": "https://slowgerman.com/", "desc": "Annik Rubens reads interesting topics slowly and clearly. Great for intermediate listening.", "level": "B1-B2"},
            {"name": "DW Deutsch lernen Podcasts", "url": "https://www.dw.com/en/learn-german/german-courses/podcasts/s-9601", "desc": "Various podcast series for different levels with transcripts.", "level": "All levels"},
        ],
        "📱 Apps & Tools": [
            {"name": "Anki", "url": "https://apps.ankiweb.net/", "desc": "Powerful spaced repetition flashcard app. Essential for vocabulary retention.", "level": "All levels"},
            {"name": "Clozemaster", "url": "https://www.clozemaster.com/", "desc": "Learn vocabulary in context through fill-in-the-blank exercises. Gamified and effective.", "level": "A1-C2"},
            {"name": "Language Reactor", "url": "https://www.languagereactor.com/", "desc": "Browser extension for Netflix/YouTube with dual subtitles and vocabulary tools.", "level": "A2-C2"},
            {"name": "LingQ", "url": "https://www.lingq.com/", "desc": "Read and listen to content while tracking known words. Extensive German library.", "level": "A2-C2"},
        ],
        "📰 News & Reading": [
            {"name": "Tagesschau in Einfacher Sprache", "url": "https://www.tagesschau.de/einfach", "desc": "German news simplified for learners. Current events in accessible language.", "level": "A2-B1"},
            {"name": "Deutsche Welle Nachrichten", "url": "https://www.dw.com/de/deutsch-lernen/nachrichten/s-8030", "desc": "News specifically written for German learners with vocabulary help.", "level": "B1-C1"},
            {"name": "Nachrichtenleicht", "url": "https://www.nachrichtenleicht.de/", "desc": "Weekly news in simple German with audio. Perfect for B1 learners.", "level": "B1"},
        ],
        "📝 Grammar & Practice": [
            {"name": "Deutsches Institut (Free Grammar)", "url": "https://www.deutschesinstitut.it/eng/", "desc": "Completely free grammar courses with downloadable PDFs and MP3s.", "level": "All levels"},
            {"name": "German.net", "url": "https://german.net/", "desc": "Free grammar exercises organized by topic with clear explanations.", "level": "A1-B2"},
            {"name": "Lingolia Deutsch", "url": "https://deutsch.lingolia.com/", "desc": "Clear grammar explanations with exercises. Well-organized by topic.", "level": "A1-C1"},
        ],
    }
    tabs = st.tabs(list(resources.keys()))
    for tab, (category, items) in zip(tabs, resources.items()):
        with tab:
            for item in items:
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.03); border-radius: 16px; padding: 18px; margin-bottom: 12px; border: 1px solid rgba(255,255,255,0.06);">
                    <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 6px;">
                        <a href="{item['url']}" target="_blank" style="font-size: 15px; font-weight: 600; color: #667eea; text-decoration: none;">{item['name']}</a>
                        <span style="background: rgba(102,126,234,0.15); color: #667eea; padding: 2px 10px; border-radius: 10px; font-size: 10px;">{item['level']}</span>
                    </div>
                    <p style="color: #a0aec0; font-size: 12px; margin: 0; line-height: 1.5;">{item['desc']}</p>
                </div>
                """, unsafe_allow_html=True)


def page_achievements():
    st.markdown("""
    <div style="text-align: center; padding: 10px 0 25px 0;">
        <h1 style="font-size: 32px;">🏅 Achievements</h1>
        <p style="color: #a0aec0;">Your journey of accomplishments</p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total XP", f"{st.session_state.xp:,}")
    with col2:
        st.metric("Current Level", st.session_state.level)
    with col3:
        st.metric("Badges Earned", len(st.session_state.achievements))
    st.markdown("<br>", unsafe_allow_html=True)
    all_achievements = [
        {"name": "Getting Started", "icon": "🌱", "desc": "3-day streak", "category": "Streak", "condition": lambda: st.session_state.streak >= 3},
        {"name": "Week Warrior", "icon": "🔥", "desc": "7-day streak", "category": "Streak", "condition": lambda: st.session_state.streak >= 7},
        {"name": "Fortnight Fighter", "icon": "⚡", "desc": "14-day streak", "category": "Streak", "condition": lambda: st.session_state.streak >= 14},
        {"name": "Monthly Master", "icon": "📅", "desc": "30-day streak", "category": "Streak", "condition": lambda: st.session_state.streak >= 30},
        {"name": "Century Scholar", "icon": "💯", "desc": "100-day streak", "category": "Streak", "condition": lambda: st.session_state.streak >= 100},
        {"name": "First Steps", "icon": "👣", "desc": "10 hours studied", "category": "Dedication", "condition": lambda: st.session_state.total_minutes >= 600},
        {"name": "Dedicated Learner", "icon": "📚", "desc": "25 hours studied", "category": "Dedication", "condition": lambda: st.session_state.total_minutes >= 1500},
        {"name": "Half Century", "icon": "🎯", "desc": "50 hours studied", "category": "Dedication", "condition": lambda: st.session_state.total_minutes >= 3000},
        {"name": "Century Club", "icon": "🏆", "desc": "100 hours studied", "category": "Dedication", "condition": lambda: st.session_state.total_minutes >= 6000},
        {"name": "Language Legend", "icon": "👑", "desc": "250 hours studied", "category": "Dedication", "condition": lambda: st.session_state.total_minutes >= 15000},
        {"name": "A1 Graduate", "icon": "🎓", "desc": "Completed A1", "category": "Progress", "condition": lambda: st.session_state.level_progress["A1"]["completed"]},
        {"name": "A2 Graduate", "icon": "📖", "desc": "Completed A2", "category": "Progress", "condition": lambda: st.session_state.level_progress["A2"]["completed"]},
        {"name": "B1 Graduate", "icon": "🚀", "desc": "Completed B1", "category": "Progress", "condition": lambda: st.session_state.level_progress["B1"]["completed"]},
        {"name": "B2 Graduate", "icon": "🎖️", "desc": "Completed B2", "category": "Progress", "condition": lambda: st.session_state.level_progress["B2"]["completed"]},
        {"name": "C1 Graduate", "icon": "🏅", "desc": "Completed C1", "category": "Progress", "condition": lambda: st.session_state.level_progress["C1"]["completed"]},
        {"name": "C2 Meister", "icon": "👑", "desc": "Completed C2", "category": "Progress", "condition": lambda: st.session_state.level_progress["C2"]["completed"]},
    ]
    earned_names = {a["name"] for a in st.session_state.achievements}
    st.subheader("✅ Earned")
    earned = [a for a in all_achievements if a["name"] in earned_names or a["condition"]()]
    if earned:
        cols = st.columns(3)
        for i, ach in enumerate(earned):
            with cols[i % 3]:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(255,215,0,0.12) 0%, rgba(255,107,107,0.12) 100%); border-radius: 16px; padding: 18px; text-align: center; border: 1px solid rgba(255,215,0,0.2); margin-bottom: 12px;">
                    <div style="font-size: 36px; margin-bottom: 8px;">{ach['icon']}</div>
                    <div style="font-weight: 700; color: #FFD700; font-size: 14px;">{ach['name']}</div>
                    <div style="font-size: 11px; color: #a0aec0; margin-top: 4px;">{ach['desc']}</div>
                    <div style="font-size: 10px; color: #6b7280; margin-top: 6px; background: rgba(255,215,0,0.08); display: inline-block; padding: 2px 8px; border-radius: 8px;">{ach['category']}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No achievements yet. Start studying to earn your first badge!")
    st.subheader("🔒 Locked")
    locked = [a for a in all_achievements if a["name"] not in earned_names and not a["condition"]()]
    cols = st.columns(3)
    for i, ach in enumerate(locked):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.02); border-radius: 16px; padding: 18px; text-align: center; border: 1px solid rgba(255,255,255,0.04); margin-bottom: 12px; opacity: 0.5;">
                <div style="font-size: 36px; margin-bottom: 8px; filter: grayscale(1);">{ach['icon']}</div>
                <div style="font-weight: 700; color: #6b7280; font-size: 14px;">{ach['name']}</div>
                <div style="font-size: 11px; color: #4b5563; margin-top: 4px;">{ach['desc']}</div>
                <div style="font-size: 10px; color: #374151; margin-top: 6px;">{ach['category']}</div>
            </div>
            """, unsafe_allow_html=True)


def page_analytics():
    st.markdown("""
    <div style="text-align: center; padding: 10px 0 25px 0;">
        <h1 style="font-size: 32px;">📈 Analytics</h1>
        <p style="color: #a0aec0;">Deep insights into your learning patterns</p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Sessions", len(st.session_state.study_sessions))
    with col2:
        avg = sum(s["minutes"] for s in st.session_state.study_sessions) / len(st.session_state.study_sessions) if st.session_state.study_sessions else 0
        st.metric("Avg Session", f"{avg:.0f} min")
    with col3:
        st.metric("This Week", f"{st.session_state.weekly_minutes} min")
    with col4:
        st.metric("This Month", f"{st.session_state.monthly_minutes} min")
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("🎯 Time Distribution by Skill")
    skills = st.session_state.skill_minutes
    if sum(skills.values()) > 0:
        try:
            import plotly.express as px
            fig = px.pie(values=list(skills.values()), names=list(skills.keys()),
                        color_discrete_sequence=["#FF6B6B", "#FFD700", "#3b82f6", "#10b981", "#8b5cf6", "#f97316"], hole=0.4)
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0",
                            showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=-0.2))
            st.plotly_chart(fig, use_container_width=True)
        except:
            st.bar_chart(skills)
    else:
        st.info("Start logging sessions to see your skill distribution!")
    st.subheader("🔥 Study Heatmap (Last 28 Days)")
    days = []
    today = date.today()
    for i in range(27, -1, -1):
        d = today - timedelta(days=i)
        day_sessions = [s for s in st.session_state.study_sessions if s.get("date") == d.isoformat()]
        minutes = sum(s["minutes"] for s in day_sessions)
        days.append({"date": d, "minutes": minutes})
    weeks = [days[i:i+7] for i in range(0, len(days), 7)]
    for week in weeks:
        cols = st.columns(7)
        for col, day in zip(cols, week):
            intensity = min(day["minutes"] / 60, 1)
            if day["minutes"] == 0:
                color = "#1f2937"
            elif intensity < 0.3:
                color = "#065f46"
            elif intensity < 0.6:
                color = "#059669"
            elif intensity < 0.9:
                color = "#10b981"
            else:
                color = "#34d399"
            with col:
                st.markdown(f"""
                <div style="aspect-ratio: 1; background: {color}; border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 9px; color: {'white' if day['minutes'] > 0 else '#374151'};">
                    {day['date'].strftime('%d')}
                </div>
                <div style="text-align: center; font-size: 8px; color: #6b7280; margin-top: 2px;">{day['minutes']}m</div>
                """, unsafe_allow_html=True)


def page_settings():
    st.markdown("""
    <div style="text-align: center; padding: 10px 0 25px 0;">
        <h1 style="font-size: 32px;">⚙️ Settings</h1>
        <p style="color: #a0aec0;">Customize your learning experience</p>
    </div>
    """, unsafe_allow_html=True)
    with st.form("settings"):
        name = st.text_input("Your Name", value=st.session_state.user_profile["name"])
        current = st.selectbox("Current Level", ["A1", "A2", "B1", "B2", "C1", "C2"],
                                index=["A1", "A2", "B1", "B2", "C1", "C2"].index(st.session_state.user_profile["current_level"]))
        target = st.selectbox("Target Level", ["A1", "A2", "B1", "B2", "C1", "C2"],
                             index=["A1", "A2", "B1", "B2", "C1", "C2"].index(st.session_state.user_profile["target_level"]))
        daily = st.number_input("Daily Goal (minutes)", min_value=5, max_value=240, value=st.session_state.user_profile["daily_goal_minutes"])
        weekly = st.number_input("Weekly Goal (hours)", min_value=1, max_value=40, value=st.session_state.user_profile["weekly_goal_hours"])
        if st.form_submit_button("💾 Save Settings"):
            st.session_state.user_profile.update({"name": name, "current_level": current, "target_level": target, "daily_goal_minutes": daily, "weekly_goal_hours": weekly})
            st.success("Settings saved!")
    st.subheader("💾 Data Management")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📤 Export Data"):
            data = {"profile": st.session_state.user_profile, "sessions": st.session_state.study_sessions,
                   "vocabulary": st.session_state.vocabulary, "xp": st.session_state.xp,
                   "level": st.session_state.level, "streak": st.session_state.streak}
            st.download_button("Download JSON", json.dumps(data, indent=2), "deutschmeister_data.json", "application/json")
    with col2:
        if st.button("🗑️ Reset All Progress"):
            st.warning("This will delete ALL your progress. Are you sure?")
            if st.button("Yes, reset everything", type="primary"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.success("All progress reset!")
                st.rerun()


def main():
    init_state()
    render_sidebar()
    page = st.session_state.current_page
    if page == "Dashboard":
        page_dashboard()
    elif page == "Study Session":
        page_study_session()
    elif page == "Roadmap":
        page_roadmap()
    elif page == "Study Plan":
        page_study_plan()
    elif page == "Vocabulary":
        page_vocabulary()
    elif page == "Resources":
        page_resources()
    elif page == "Achievements":
        page_achievements()
    elif page == "Analytics":
        page_analytics()
    elif page == "Settings":
        page_settings()
    else:
        page_dashboard()


if __name__ == "__main__":
    main()
