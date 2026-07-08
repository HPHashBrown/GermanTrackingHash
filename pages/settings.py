"""Settings page."""

import streamlit as st

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
