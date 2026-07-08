"""Achievements and badges page."""

import streamlit as st

def show_achievements():
    """Display achievements and badges."""
    
    st.markdown("""
    <div style="text-align: center; padding: 20px 0 30px 0;">
        <h1 style="font-size: 36px;">🏅 Achievements</h1>
        <p style="color: #a0aec0;">Your journey of accomplishments</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total XP", f"{st.session_state.xp:,}")
    with col2:
        st.metric("Current Level", st.session_state.level)
    with col3:
        st.metric("Badges Earned", len(st.session_state.achievements))
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # All possible achievements
    all_achievements = [
        # Streak achievements
        {"name": "Getting Started", "icon": "🌱", "desc": "3-day streak", "category": "Streak", "condition": lambda: st.session_state.streak >= 3},
        {"name": "Week Warrior", "icon": "🔥", "desc": "7-day streak", "category": "Streak", "condition": lambda: st.session_state.streak >= 7},
        {"name": "Fortnight Fighter", "icon": "⚡", "desc": "14-day streak", "category": "Streak", "condition": lambda: st.session_state.streak >= 14},
        {"name": "Monthly Master", "icon": "📅", "desc": "30-day streak", "category": "Streak", "condition": lambda: st.session_state.streak >= 30},
        {"name": "Century Scholar", "icon": "💯", "desc": "100-day streak", "category": "Streak", "condition": lambda: st.session_state.streak >= 100},
        # Hour achievements
        {"name": "First Steps", "icon": "👣", "desc": "10 hours studied", "category": "Dedication", "condition": lambda: st.session_state.total_minutes >= 600},
        {"name": "Dedicated Learner", "icon": "📚", "desc": "25 hours studied", "category": "Dedication", "condition": lambda: st.session_state.total_minutes >= 1500},
        {"name": "Half Century", "icon": "🎯", "desc": "50 hours studied", "category": "Dedication", "condition": lambda: st.session_state.total_minutes >= 3000},
        {"name": "Century Club", "icon": "🏆", "desc": "100 hours studied", "category": "Dedication", "condition": lambda: st.session_state.total_minutes >= 6000},
        {"name": "Language Legend", "icon": "👑", "desc": "250 hours studied", "category": "Dedication", "condition": lambda: st.session_state.total_minutes >= 15000},
        # Level achievements
        {"name": "A1 Graduate", "icon": "🎓", "desc": "Complete A1 level", "category": "Progress", "condition": lambda: st.session_state.level_progress["A1"]["completed"]},
        {"name": "A2 Graduate", "icon": "📖", "desc": "Complete A2 level", "category": "Progress", "condition": lambda: st.session_state.level_progress["A2"]["completed"]},
        {"name": "B1 Graduate", "icon": "🚀", "desc": "Complete B1 level", "category": "Progress", "condition": lambda: st.session_state.level_progress["B1"]["completed"]},
        {"name": "B2 Graduate", "icon": "🎖️", "desc": "Complete B2 level", "category": "Progress", "condition": lambda: st.session_state.level_progress["B2"]["completed"]},
        {"name": "C1 Graduate", "icon": "🏅", "desc": "Complete C1 level", "category": "Progress", "condition": lambda: st.session_state.level_progress["C1"]["completed"]},
        {"name": "C2 Meister", "icon": "👑", "desc": "Complete C2 level", "category": "Progress", "condition": lambda: st.session_state.level_progress["C2"]["completed"]},
    ]
    
    earned_names = {a["name"] for a in st.session_state.achievements}
    
    # Display earned
    st.subheader("✅ Earned")
    earned = [a for a in all_achievements if a["name"] in earned_names or a["condition"]()]
    
    if earned:
        cols = st.columns(3)
        for i, ach in enumerate(earned):
            with cols[i % 3]:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(255,215,0,0.15) 0%, rgba(255,107,107,0.15) 100%); border-radius: 16px; padding: 20px; text-align: center; border: 1px solid rgba(255,215,0,0.3); margin-bottom: 15px;">
                    <div style="font-size: 40px; margin-bottom: 10px;">{ach['icon']}</div>
                    <div style="font-weight: 700; color: #FFD700; font-size: 15px;">{ach['name']}</div>
                    <div style="font-size: 12px; color: #a0aec0; margin-top: 5px;">{ach['desc']}</div>
                    <div style="font-size: 11px; color: #6b7280; margin-top: 8px; background: rgba(255,215,0,0.1); display: inline-block; padding: 2px 10px; border-radius: 10px;">{ach['category']}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No achievements yet. Start studying to earn your first badge!")
    
    # Locked achievements
    st.subheader("🔒 Locked")
    locked = [a for a in all_achievements if a["name"] not in earned_names and not a["condition"]()]
    
    cols = st.columns(3)
    for i, ach in enumerate(locked):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.03); border-radius: 16px; padding: 20px; text-align: center; border: 1px solid rgba(255,255,255,0.05); margin-bottom: 15px; opacity: 0.5;">
                <div style="font-size: 40px; margin-bottom: 10px; filter: grayscale(1);">{ach['icon']}</div>
                <div style="font-weight: 700; color: #6b7280; font-size: 15px;">{ach['name']}</div>
                <div style="font-size: 12px; color: #4b5563; margin-top: 5px;">{ach['desc']}</div>
                <div style="font-size: 11px; color: #374151; margin-top: 8px;">{ach['category']}</div>
            </div>
            """, unsafe_allow_html=True)
