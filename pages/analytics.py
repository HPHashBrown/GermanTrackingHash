"""Analytics page."""

import streamlit as st
import pandas as pd
from datetime import date, timedelta

def show_analytics():
    """Display detailed analytics."""
    
    st.markdown("""
    <div style="text-align: center; padding: 20px 0 30px 0;">
        <h1 style="font-size: 36px;">📈 Analytics</h1>
        <p style="color: #a0aec0;">Deep insights into your learning patterns</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Summary metrics
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
    
    # Skill distribution
    st.subheader("🎯 Time Distribution by Skill")
    skills = st.session_state.skill_minutes
    if sum(skills.values()) > 0:
        import plotly.express as px
        fig = px.pie(
            values=list(skills.values()),
            names=list(skills.keys()),
            color_discrete_sequence=["#FF6B6B", "#FFD700", "#3b82f6", "#10b981", "#8b5cf6", "#f97316"],
            hole=0.4
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e2e8f0",
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2)
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Start logging sessions to see your skill distribution!")
    
    # Study heatmap (simplified)
    st.subheader("🔥 Study Heatmap")
    
    # Generate last 28 days
    days = []
    today = date.today()
    for i in range(27, -1, -1):
        d = today - timedelta(days=i)
        # Mock data or real
        day_sessions = [s for s in st.session_state.study_sessions if s.get("date") == d.isoformat()]
        minutes = sum(s["minutes"] for s in day_sessions)
        days.append({"date": d, "minutes": minutes})
    
    # Display as simple grid
    weeks = [days[i:i+7] for i in range(0, len(days), 7)]
    
    for week in weeks:
        cols = st.columns(7)
        for col, day in zip(cols, week):
            intensity = min(day["minutes"] / 60, 1)  # Normalize to 60 min
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
                <div style="aspect-ratio: 1; background: {color}; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 10px; color: {'white' if day['minutes'] > 0 else '#374151'};">
                    {day['date'].strftime('%d')}
                </div>
                <div style="text-align: center; font-size: 9px; color: #6b7280; margin-top: 2px;">{day['minutes']}m</div>
                """, unsafe_allow_html=True)

def show_settings():
    """Display settings page."""
    st.markdown("""
    <div style="text-align: center; padding: 20px 0 30px 0;">
        <h1 style="font-size: 36px;">⚙️ Settings</h1>
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
            st.session_state.user_profile.update({
                "name": name,
                "current_level": current,
                "target_level": target,
                "daily_goal_minutes": daily,
                "weekly_goal_hours": weekly
            })
            st.success("Settings saved!")
    
    # Data management
    st.subheader("💾 Data Management")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📤 Export Data"):
            import json
            data = {
                "profile": st.session_state.user_profile,
                "sessions": st.session_state.study_sessions,
                "vocabulary": st.session_state.vocabulary,
                "xp": st.session_state.xp,
                "level": st.session_state.level,
                "streak": st.session_state.streak
            }
            st.download_button("Download JSON", json.dumps(data, indent=2), "deutschmeister_data.json", "application/json")
    with col2:
        if st.button("🗑️ Reset All Progress"):
            if st.checkbox("I understand this cannot be undone"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.success("All progress reset!")
                st.rerun()
