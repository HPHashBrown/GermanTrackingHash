"""Learning roadmap page for DeutschMeister."""

import streamlit as st

def show_roadmap():
    """Display the CEFR learning roadmap."""
    
    st.markdown("""
    <div style="text-align: center; padding: 20px 0 30px 0;">
        <h1 style="font-size: 36px;">🗺️ Your Learning Roadmap</h1>
        <p style="color: #a0aec0;">From beginner to mastery — A1 → C2</p>
    </div>
    """, unsafe_allow_html=True)
    
    levels = {
        "A1": {
            "name": "Beginner",
            "hours": 80,
            "grammar": "Present tense, articles, basic word order, personal pronouns",
            "vocab": "650 words — everyday objects, numbers, colors, family",
            "listening": "Understand simple phrases when spoken slowly",
            "reading": "Read familiar names, words, very simple sentences",
            "speaking": "Introduce yourself, ask/answer simple questions",
            "writing": "Write a short postcard, fill in forms with personal details",
            "exam": "Goethe-Zertifikat A1, Start Deutsch 1",
            "weekly_plan": "5-7 hours/week for ~3 months"
        },
        "A2": {
            "name": "Elementary",
            "hours": 120,
            "grammar": "Past tense (Perfekt), dative case, modal verbs, comparatives",
            "vocab": "1,300 words — shopping, work, environment, daily routines",
            "listening": "Understand phrases related to personal/family life",
            "reading": "Read short simple texts, find specific information",
            "speaking": "Describe daily life, immediate needs, surroundings",
            "writing": "Write short notes, messages, simple personal letters",
            "exam": "Goethe-Zertifikat A2, Start Deutsch 2",
            "weekly_plan": "5-7 hours/week for ~4 months"
        },
        "B1": {
            "name": "Intermediate",
            "hours": 180,
            "grammar": "Subjunctive II, relative clauses, passive voice, complex sentences",
            "vocab": "2,400 words — school, work, leisure, travel, opinions",
            "listening": "Understand main points of clear standard speech",
            "reading": "Understand texts with everyday/job-related language",
            "speaking": "Deal with most situations, describe experiences, dreams",
            "writing": "Write connected text on familiar topics, personal letters",
            "exam": "Goethe-Zertifikat B1, TestDaF (partial)",
            "weekly_plan": "7-10 hours/week for ~5 months"
        },
        "B2": {
            "name": "Upper Intermediate",
            "hours": 240,
            "grammar": "Advanced subjunctive, nominalizations, complex syntax",
            "vocab": "3,500+ words — abstract topics, technical discussions",
            "listening": "Understand extended speech, TV, films",
            "reading": "Read articles on contemporary problems, literary prose",
            "speaking": "Interact with fluency, take active part in discussions",
            "writing": "Write clear detailed text on various subjects, essays",
            "exam": "Goethe-Zertifikat B2, TestDaF",
            "weekly_plan": "8-12 hours/week for ~6 months"
        },
        "C1": {
            "name": "Advanced",
            "hours": 300,
            "grammar": "Refined usage, stylistic nuances, academic register",
            "vocab": "5,000+ words — specialized, professional, academic",
            "listening": "Understand extended speech even when not structured",
            "reading": "Understand long complex texts, appreciate distinctions of style",
            "speaking": "Express fluently, use language flexibly for social/professional",
            "writing": "Write clear well-structured detailed text, complex letters",
            "exam": "Goethe-Zertifikat C1, TestDaF, DSH",
            "weekly_plan": "10-15 hours/week for ~7 months"
        },
        "C2": {
            "name": "Mastery",
            "hours": 400,
            "grammar": "Near-native command, all nuances, idiomatic expressions",
            "vocab": "8,000+ words — complete mastery of vocabulary",
            "listening": "Understand any kind of spoken language effortlessly",
            "reading": "Read with ease virtually all forms of written language",
            "speaking": "Express spontaneously with precision, differentiate finer shades",
            "writing": "Write clear smoothly flowing text in appropriate style",
            "exam": "Goethe-Zertifikat C2: GDS",
            "weekly_plan": "10+ hours/week ongoing"
        }
    }
    
    # Visual roadmap
    progress = st.session_state.level_progress
    
    st.markdown("""
    <div style="display: flex; align-items: center; justify-content: space-between; padding: 30px 0; position: relative;">
    """, unsafe_allow_html=True)
    
    # Roadmap nodes
    cols = st.columns(6)
    level_names = ["A1", "A2", "B1", "B2", "C1", "C2"]
    
    for i, (col, lvl) in enumerate(zip(cols, level_names)):
        with col:
            p = progress[lvl]
            if p["completed"]:
                color = "#10b981"
                status = "✓"
                glow = "box-shadow: 0 0 20px rgba(16,185,129,0.5);"
            elif p["hours"] > 0:
                color = "#3b82f6"
                status = f"{int(p['hours'])}h"
                glow = "box-shadow: 0 0 25px rgba(59,130,246,0.6); border: 3px solid #FFD700;"
            else:
                color = "#6b7280"
                status = "🔒"
                glow = ""
            
            pct = min((p["hours"] / p["required"]) * 100, 100)
            
            st.markdown(f"""
            <div style="text-align: center;">
                <div style="width: 60px; height: 60px; background: {color}; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 20px; color: white; margin: 0 auto; {glow}">
                    {lvl}
                </div>
                <div style="font-size: 11px; margin-top: 8px; color: {'#10b981' if p['completed'] else '#3b82f6' if p['hours'] > 0 else '#6b7280'};">
                    {status}
                </div>
                <div style="background: rgba(255,255,255,0.08); border-radius: 6px; height: 6px; margin-top: 8px; overflow: hidden;">
                    <div style="width: {pct}%; height: 100%; background: {color}; border-radius: 6px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Detailed level cards
    st.markdown("<br>", unsafe_allow_html=True)
    
    for lvl, info in levels.items():
        p = progress[lvl]
        pct = min((p["hours"] / p["required"]) * 100, 100)
        
        with st.expander(f"{'✅' if p['completed'] else '🎯' if p['hours'] > 0 else '🔒'} {lvl}: {info['name']} ({p['hours']:.0f}/{info['hours']} hours)"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.03); border-radius: 12px; padding: 20px;">
                    <div style="margin-bottom: 15px;">
                        <span style="color: #FFD700; font-weight: 600;">📖 Grammar:</span>
                        <span style="color: #a0aec0;"> {info['grammar']}</span>
                    </div>
                    <div style="margin-bottom: 15px;">
                        <span style="color: #FFD700; font-weight: 600;">📝 Vocabulary:</span>
                        <span style="color: #a0aec0;"> {info['vocab']}</span>
                    </div>
                    <div style="margin-bottom: 15px;">
                        <span style="color: #FFD700; font-weight: 600;">🎧 Listening:</span>
                        <span style="color: #a0aec0;"> {info['listening']}</span>
                    </div>
                    <div style="margin-bottom: 15px;">
                        <span style="color: #FFD700; font-weight: 600;">📚 Reading:</span>
                        <span style="color: #a0aec0;"> {info['reading']}</span>
                    </div>
                    <div style="margin-bottom: 15px;">
                        <span style="color: #FFD700; font-weight: 600;">🗣️ Speaking:</span>
                        <span style="color: #a0aec0;"> {info['speaking']}</span>
                    </div>
                    <div style="margin-bottom: 15px;">
                        <span style="color: #FFD700; font-weight: 600;">✍️ Writing:</span>
                        <span style="color: #a0aec0;"> {info['writing']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.03); border-radius: 12px; padding: 20px; text-align: center;">
                    <div style="font-size: 48px; margin-bottom: 10px;">{'🏆' if p['completed'] else '📈' if p['hours'] > 0 else '🔐'}</div>
                    <div style="font-size: 14px; color: #a0aec0; margin-bottom: 10px;">Progress</div>
                    <div style="font-size: 32px; font-weight: 700; color: {'#10b981' if p['completed'] else '#3b82f6'};">{pct:.0f}%</div>
                    <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(255,255,255,0.1);">
                        <div style="font-size: 12px; color: #6b7280;">Exam</div>
                        <div style="font-size: 13px; color: #e2e8f0; margin-top: 5px;">{info['exam']}</div>
                    </div>
                    <div style="margin-top: 15px;">
                        <div style="font-size: 12px; color: #6b7280;">Study Plan</div>
                        <div style="font-size: 13px; color: #e2e8f0; margin-top: 5px;">{info['weekly_plan']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
