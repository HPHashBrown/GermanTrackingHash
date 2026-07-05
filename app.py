import streamlit as st
import pandas as pd
import os
import datetime

# File setup
DATA_FILE = 'german_data.csv'

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=['Date', 'Level', 'Minutes', 'Focus'])

# UI Setup
st.set_page_config(page_title="German B1 Tracker", layout="wide")
st.title("🇩🇪 German Fluency Tracker")

data = load_data()

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "B1 Tracker", "B2 Tracker", "C1 Tracker"])

with tab1:
    st.header("Overall Growth")
    if not data.empty:
        # Group by level
        progress = data.groupby('Level')['Minutes'].sum().reset_index()
        st.bar_chart(progress.set_index('Level'))
        st.write("Total minutes studied:", data['Minutes'].sum())
    else:
        st.write("No data yet. Start studying!")

def input_form(level):
    with st.form(f"{level}_form"):
        minutes = st.number_input("Minutes Studied", min_value=1, max_value=300)
        focus = st.text_input("What did you focus on? (e.g., Grammar, Listening)")
        if st.form_submit_button("Log Session"):
            new_entry = pd.DataFrame([[datetime.date.today(), level, minutes, focus]], 
                                     columns=['Date', 'Level', 'Minutes', 'Focus'])
            updated_data = pd.concat([data, new_entry], ignore_index=True)
            updated_data.to_csv(DATA_FILE, index=False)
            st.success(f"Logged {minutes} mins for {level}!")
            st.rerun()

with tab2:
    st.header("B1: The Goal")
    input_form("B1")
with tab3:
    st.header("B2: Consolidation")
    input_form("B2")
with tab4:
    st.header("C1: Fluency")
    input_form("C1")
