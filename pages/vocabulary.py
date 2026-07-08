"""Vocabulary management page."""

import streamlit as st
import random

def show_vocabulary():
    """Display vocabulary collection and flashcards."""
    
    st.markdown("""
    <div style="text-align: center; padding: 20px 0 30px 0;">
        <h1 style="font-size: 36px;">📚 Vocabulary</h1>
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
        # Flashcard practice
        flashcard_words = [
            {"german": "das Haus", "translation": "house", "example": "Das Haus ist groß."},
            {"german": "die Zeit", "translation": "time", "example": "Die Zeit vergeht schnell."},
            {"german": "der Mensch", "translation": "human/person", "example": "Der Mensch ist frei."},
            {"german": "die Arbeit", "translation": "work", "example": "Die Arbeit macht Spaß."},
            {"german": "das Leben", "translation": "life", "example": "Das Leben ist schön."},
        ] + st.session_state.vocabulary
        
        if flashcard_words:
            if "flashcard_index" not in st.session_state:
                st.session_state.flashcard_index = 0
                st.session_state.flashcard_flipped = False
            
            idx = st.session_state.flashcard_index % len(flashcard_words)
            word = flashcard_words[idx]
            
            # Flashcard display
            if st.session_state.flashcard_flipped:
                card_content = f"""
                <div style="background: linear-gradient(135deg, rgba(102,126,234,0.2) 0%, rgba(118,75,162,0.2) 100%); border-radius: 20px; padding: 60px 40px; text-align: center; border: 2px solid rgba(102,126,234,0.4); cursor: pointer; min-height: 250px; display: flex; flex-direction: column; justify-content: center;">
                    <div style="font-size: 14px; color: #667eea; margin-bottom: 15px;">TRANSLATION</div>
                    <div style="font-size: 32px; font-weight: 700; color: white; margin-bottom: 15px;">{word['translation']}</div>
                    <div style="font-size: 16px; color: #a0aec0; font-style: italic;">"{word.get('example', '')}"</div>
                </div>
                """
            else:
                card_content = f"""
                <div style="background: linear-gradient(135deg, rgba(255,215,0,0.1) 0%, rgba(255,107,107,0.1) 100%); border-radius: 20px; padding: 60px 40px; text-align: center; border: 2px solid rgba(255,215,0,0.3); cursor: pointer; min-height: 250px; display: flex; flex-direction: column; justify-content: center;">
                    <div style="font-size: 14px; color: #FFD700; margin-bottom: 15px;">GERMAN</div>
                    <div style="font-size: 42px; font-weight: 700; color: white; margin-bottom: 15px;">{word['german']}</div>
                    <div style="font-size: 14px; color: #6b7280;">Click to reveal</div>
                </div>
                """
            
            st.markdown(card_content, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🔄 Flip", use_container_width=True):
                    st.session_state.flashcard_flipped = not st.session_state.flashcard_flipped
                    st.rerun()
            with col2:
                if st.button("✅ Know it", use_container_width=True):
                    st.session_state.flashcard_index += 1
                    st.session_state.flashcard_flipped = False
                    st.success("+10 XP!")
                    st.rerun()
            with col3:
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
                        "german": german,
                        "translation": translation,
                        "example": example,
                        "category": category,
                        "date_added": str(date.today())
                    })
                    st.success(f"Added '{german}' to your collection!")
