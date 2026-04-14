import streamlit as st
import pandas as pd

st.set_page_config(page_title="Opta Sub Intelligence", layout="wide")

# Custom Dark Mode Styling
st.markdown("""
    <style>
    .main { background-color: #050505; color: #ffffff; }
    .stMetric { background-color: #111111; padding: 15px; border-radius: 10px; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# Navigation Tabs at the top
tab1, tab2 = st.tabs(["🏆 Premier League", "⚽ Championship"])

def run_analysis(csv_file, league_name):
    try:
        df = pd.read_csv(csv_file)
        
        col1, col2 = st.columns(2)
        with col1:
            team = st.selectbox(f"Select Club ({league_name})", sorted(df['team'].unique()), key=f"{league_name}_t")
            team_df = df[df['team'] == team]
        with col2:
            player_off = st.selectbox(f"Select Player OFF ({league_name})", sorted(team_df['off'].unique()), key=f"{league_name}_p")
        
        logs = team_df[team_df['off'] == player_off]
        
        if len(logs) > 0:
            st.subheader(f"Tactical Habits for {player_off}")
            counts = logs['on'].value_counts().reset_index()
            counts.columns = ['Replacement', 'Freq']
            
            # Display metrics for top replacements
            metric_cols = st.columns(len(counts))
            for i, row in counts.iterrows():
                pct = int((row['Freq'] / len(logs)) * 100)
                avg_min = int(logs[logs['on'] == row['Replacement']]['min'].mean())
                with metric_cols[i]:
                    st.metric(label=f"In: {row['Replacement']}", value=f"{row['Freq']} Games", delta=f"{pct}% Frequency")
                    st.caption(f"Avg Timing: {avg_min}'")
            
            st.write("### 📅 Match Timeline")
            st.dataframe(logs[['min', 'on', 'opp', 'date']].sort_values(by='date', ascending=False), use_container_width=True)
        else:
            st.info("No data found for this player.")
            
    except FileNotFoundError:
        st.error(f"File '{csv_file}' not found on GitHub. Please upload it to see {league_name} data.")

with tab1:
    st.title("Premier League Sub Intel")
    run_analysis('all_subs_2026.csv', "PL")

with tab2:
    st.title("Championship Sub Intel")
    run_analysis('championship_subs_2026.csv', "EFL")
