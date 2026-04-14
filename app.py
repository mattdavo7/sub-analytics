import streamlit as st
import pandas as pd

# 1. Page Styling
st.set_page_config(page_title="Opta Sub Intelligence", layout="wide")
st.markdown("<style>.main { background-color: #050505; color: #ffffff; }</style>", unsafe_allow_html=True)

# 2. Data Loading - Updated to use the correct file name
@st.cache_data
def load_data():
    # Make sure this filename matches exactly what you uploaded to GitHub
    return pd.read_csv('all_subs_2026.csv') 

try:
    df = load_data()
    st.title("📊 opta-sub-intelligence")
    st.caption("Data Source: SofaScore / Opta | Season 2025/26")

    # 3. Selectors - UPDATED to lowercase to match SofaScore scraper
    col1, col2 = st.columns(2)
    with col1:
        team = st.selectbox("Select Club", sorted(df['team'].unique()))
        team_df = df[df['team'] == team]
    with col2:
        player_off = st.selectbox("Select Player (OFF)", sorted(team_df['off'].unique()))
    
    # 4. Habit Analysis
    logs = team_df[team_df['off'] == player_off]
    total = len(logs)
    
    if total > 0:
        counts = logs['on'].value_counts().reset_index()
        counts.columns = ['Replacement', 'Freq']
        
        st.subheader(f"Tactical Habits for {player_off}")
        cols = st.columns(len(counts))
        for i, row in counts.iterrows():
            pct = int((row['Freq'] / total) * 100)
            avg_min = int(logs[logs['on'] == row['Replacement']]['min'].mean())
            
            with cols[i]:
                st.metric(f"In: {row['Replacement']}", f"{row['Freq']} Games", f"{pct}% Freq")
                st.caption(f"Avg Timing: {avg_min}'")
            
        st.write("### 📅 Seasonal Match Timeline")
        # Displaying lowercase columns from the new scraper
        st.dataframe(logs[['min', 'on', 'opp', 'date']], use_container_width=True)
    else:
        st.info(f"No substitution history found for {player_off}.")

except Exception as e:
    st.error(f"Error loading data: {e}")
    st.info("Check that all_subs_2026.csv is uploaded and column names are correct.")
