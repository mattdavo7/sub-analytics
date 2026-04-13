import streamlit as st
import pandas as pd

st.set_page_config(page_title="Opta Sub Intel", layout="wide")
st.markdown("<style>.main { background-color: #050505; color: #ffffff; }</style>", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv('all_subs_2026.csv')

try:
    df = load_data()
    st.title("📊 opta-sub-intelligence")
    
    # Simple dropdown logic for all teams/players in the CSV
    player_off = st.selectbox("Select Player (The one being subbed OFF)", sorted(df['Off'].unique()))
    
    logs = df[df['Off'] == player_off]
    total = len(logs)
    
    if total > 0:
        counts = logs['On'].value_counts().reset_index()
        counts.columns = ['Replacement', 'Freq']
        
        st.subheader(f"Historical Habits for {player_off}")
        cols = st.columns(len(counts))
        for i, row in counts.iterrows():
            pct = int((row['Freq'] / total) * 100)
            cols[i].metric(f"Replaced by {row['Replacement']}", f"{row['Freq']} Times", f"{pct}%")
            
        st.write("### 📅 Match-by-Match Logs")
        st.dataframe(logs[['Time', 'On', 'Match']], use_container_width=True)
except:
    st.info("Waiting for first scrape to complete. Go to 'Actions' tab in GitHub to run manually.")
