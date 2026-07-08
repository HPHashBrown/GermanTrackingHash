"""Personalized study plan page."""

import streamlit as st
from datetime import date, timedelta

def show_study_plan():
    """Display personalized study plan."""
    
    st.markdown("""
    <div style="text-align: center; padding: 20px 0 30px 0;">
        <h1 style="font-size: 36px;">📅 Your Study Plan</h1>
        <p style="color: #a0aec0;">AI-powered recommendations for balanced learning</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate recommendations based on history
    skills = st.session_state.skill_minutes
    total = sum(skills.values()) or 1
    
    # Find weakest skill
    weakest = min(skills, key=skills.get)
    strongest = max(skills, key=skills.get)
    
    # Today's recommendation
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(102,126,234,0.15) 0%, rgba(118,75,162,0.15) 100%); border-radius: 20px; padding: 25px; border: 1px solid rgba(102,126,234,0.3); margin-bottom: 25px;">
        <h3 style="margin: 0 0 15px 0;">🎯 Today's Recommended Focus</h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; background: rgba(255,255,255,0.05); border-radius: 12px;">
            <div style="font-size: 36px; margin-bottom: 10px;">📖</div>
            <div style="font-weight: 700; color: white;">{weakest}</div>
            <div style="font-size: 12px; color: #6b7280; margin-top: 5px;">Priority Skill</div>
            <div style="font-size: 11px; color: #FF6B6B; margin-top: 5px;">Needs attention</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; background: rgba(255,255,255,0.05); border-radius: 12px;">
            <div style="font-size: 36px; margin-bottom: 10px;">⏱️</div>
            <div style="font-weight: 700; color: white;">{st.session_state.user_profile['daily_goal_minutes']} min</div>
            <div style="font-size: 12px; color: #6b7280; margin-top: 5px;">Daily Goal</div>
            <div style="font-size: 11px; color: #10b981; margin-top: 5px;">{st.session_state.today_minutes}/{st.session_state.user_profile['daily_goal_minutes']} done</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        current = st.session_state.user_profile["current_level"]
        next_level = {"A1": "A2", "A2": "B1", "B1": "B2", "B2": "C1", "C1": "C2", "C2": "Mastery"}[current]
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; background: rgba(255,255,255,0.05); border-radius: 12px;">
            <div style="font-size: 36px; margin-bottom: 10px;">🚀</div>
            <div style="font-weight: 700; color: white;">{next_level}</div>
            <div style="font-size: 12px; color: #6b7280; margin-top: 5px;">Next Milestone</div>
            <div style="font-size: 11px; color: #3b82f6; margin-top: 5px;">Keep going!</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Weekly schedule
    st.markdown("""
    <div style="background: rgba(255,255,255,0.03); border-radius: 20px; padding: 25px; border: 1px solid rgba(255,255,255,0.08); margin-bottom: 25px;">
        <h3 style="margin: 0 0 20px 0;">📆 Suggested Weekly Schedule</h3>
    """, unsafe_allow_html=True)
    
    schedule = {
        "Monday": [("Grammar", "30 min", "#FF6B6B"), ("Vocabulary", "20 min", "#FFD700")],
        "Tuesday": [("Listening", "30 min", "#3b82f6"), ("Reading", "20 min", "#10b981")],
        "Wednesday": [("Grammar", "25 min", "#FF6B6B"), ("Speaking", "25 min", "#8b5cf6")],
        "Thursday": [("Vocabulary", "30 min", "#FFD700"), ("Writing", "20 min", "#f97316")],
        "Friday": [("Listening", "25 min", "#3b82f6"), ("Reading", "25 min", "#10b981")],
        "Saturday": [("Speaking", "30 min", "#8b5cf6"), ("Review", "20 min", "#667eea")],
        "Sunday": [("Free Practice", "40 min", "#10b981"), ("Cultural Content", "20 min", "#ec4899")]
    }
    
    for day, activities in schedule.items():
        is_today = day == date.today().strftime("%A")
        bg = "rgba(102,126,234,0.1)" if is_today else "rgba(255,255,255,0.03)"
        border = "1px solid rgba(102,126,234,0.3)" if is_today else "1px solid rgba(255,255,255,0.05)"
        
        st.markdown(f"""
        <div style="background: {bg}; border-radius: 12px; padding: 14px 16px; margin-bottom: 10px; border: {border};">
            <div style="font-weight: 600; color: {'#667eea' if is_today else 'white'}; margin-bottom: 8px; font-size: 14px;">
                {'● ' if is_today else ''}{day}{' (Today)' if is_today else ''}
            </div>
            <div style="display: flex; gap: 10px; flex-wrap: wrap;">
        """, unsafe_allow_html=True)
        
        for skill, duration, color in activities:
            st.markdown(f"""
            <span style="background: {color}20; color: {color}; padding: 4px 12px; border-radius: 20px; font-size: 12px; border: 1px solid {color}40;">
                {skill} • {duration}
            </span>
            """, unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Skill balance radar
    st.markdown("""
    <div style="background: rgba(255,255,255,0.03); border-radius: 20px; padding: 25px; border: 1px solid rgba(255,255,255,0.08);">
        <h3 style="margin: 0 0 20px 0;">⚖️ Skill Balance</h3>
    """, unsafe_allow_html=True)
    
    # Simple bar chart representation
    for skill, minutes in skills.items():
        avg = total / 6
        ratio = minutes / avg if avg > 0 else 0
        color = "#10b981" if 0.8 <= ratio <= 1.5 else "#FF6B6B" if ratio < 0.5 else "#3b82f6"
        
        st.markdown(f"""
        <div style="margin-bottom: 12px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                <span style="font-size: 13px; color: #e2e8f0;">{skill}</span>
                <span style="font-size: 12px; color: {color};">{minutes}m ({ratio:.1f}x avg)</span>
            </div>
            <div style="background: rgba(255,255,255,0.05); border-radius: 8px; height: 8px; overflow: hidden;">
                <div style="width: {min(ratio * 16.67, 100)}%; height: 100%; background: {color}; border-radius: 8px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
