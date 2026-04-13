import streamlit as st
import pandas as pd

st.set_page_config(page_title="Opta Sub Intelligence", layout="wide")
st.markdown("<style>.main { background-color: #050505; color: #ffffff; }</style>", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv('all_subs_2026.csv')

try:
    df = load_data()
    st.title("📊 opta-sub-intelligence")
    st.caption("Data Source: Ball Don't Lie API | Season 2025/26")

    # Select Player OFF
    player_off = st.selectbox("Select Player (Subbed OFF)", sorted(df['Off'].unique()))
    
    logs = df[df['Off'] == player_off]
    total = len(logs)
    
    if total > 0:
        counts = logs['On'].value_counts().reset_index()
        counts.columns = ['Replacement', 'Freq']
        
        st.subheader(f"Historical Habits for {player_off}")
        cols = st.columns(len(counts))
        for i, row in counts.iterrows():
            pct = int((row['Freq'] / total) * 100)
            avg_min = int(logs[logs['On'] == row['Replacement']]['Min'].mean())
            cols[i].metric(f"Replaced by {row['Replacement']}", f"{row['Freq']} Times", f"{pct}%")
            cols[i].caption(f"Avg Timing: {avg_min}'")
            
        st.write("### 📅 Match Timeline")
        st.dataframe(logs[['Min', 'On', 'Match_ID']], use_container_width=True)
except:
    st.info("Run the scraper to generate the CSV.")
