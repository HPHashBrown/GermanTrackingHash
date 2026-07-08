"""Learning resources page."""

import streamlit as st

def show_resources():
    """Display curated German learning resources."""
    
    st.markdown("""
    <div style="text-align: center; padding: 20px 0 30px 0;">
        <h1 style="font-size: 36px;">🔗 Free German Resources</h1>
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
                <div style="background: rgba(255,255,255,0.03); border-radius: 16px; padding: 20px; margin-bottom: 15px; border: 1px solid rgba(255,255,255,0.08); transition: all 0.3s ease;">
                    <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 8px;">
                        <a href="{item['url']}" target="_blank" style="font-size: 16px; font-weight: 600; color: #667eea; text-decoration: none;">{item['name']}</a>
                        <span style="background: rgba(102,126,234,0.2); color: #667eea; padding: 2px 10px; border-radius: 12px; font-size: 11px;">{item['level']}</span>
                    </div>
                    <p style="color: #a0aec0; font-size: 13px; margin: 0; line-height: 1.5;">{item['desc']}</p>
                </div>
                """, unsafe_allow_html=True)
