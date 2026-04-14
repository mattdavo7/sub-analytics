import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="Football Sub Intel", layout="wide")

# Custom Dark Mode Styling
st.markdown("""
    <style>
    .main { background-color: #050505; color: #ffffff; }
    div[data-testid="stMetric"] {
        background-color: #111111;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #333;
    }
    </style>
    """, unsafe_allow_html=True)

# Helper function to generate WhoScored search links
def get_whoscored_link(player_name, team_name):
    query = f"site:whoscored.com {player_name} {team_name} player profile"
    return f"https://www.google.com/search?q={urllib.parse.quote(query)}"

def run_analysis(csv_file, league_label):
    try:
        df = pd.read_csv(csv_file)
        
        col1, col2 = st.columns(2)
        with col1:
            team = st.selectbox(f"Select Club ({league_label})", sorted(df['team'].unique()), key=f"{league_label}_t")
            team_df = df[df['team'] == team]
        with col2:
            player_off = st.selectbox(f"Select Player OFF ({league_label})", sorted(team_df['off'].unique()), key=f"{league_label}_p")
        
        logs = team_df[team_df['off'] == player_off]
        
        if len(logs) > 0:
            st.subheader(f"Tactical Habits for {player_off}")
            # Link for the main player being analyzed
            st.markdown(f"🔗 [View {player_off} on WhoScored]({get_whoscored_link(player_off, team)})")
            
            counts = logs['on'].value_counts().reset_index()
            counts.columns = ['Replacement', 'Freq']
            
            # Display metrics with WhoScored buttons for replacements
            metric_cols = st.columns(len(counts))
            for i, row in counts.iterrows():
                pct = int((row['Freq'] / len(logs)) * 100)
                avg_min = int(logs[logs['on'] == row['Replacement']]['min'].mean())
                with metric_cols[i]:
                    st.metric(label=f"In: {row['Replacement']}", value=f"{row['Freq']} Games", delta=f"{pct}% Freq")
                    # THE BUTTON:
                    st.link_button(f"📊 {row['Replacement']} Stats", get_whoscored_link(row['Replacement'], team))
                    st.caption(f"Avg Timing: {avg_min}'")
            
            st.write("### 📅 Match Timeline")
            st.dataframe(logs[['min', 'on', 'opp', 'date']].sort_values(by='date', ascending=False), use_container_width=True)
        else:
            st.info("No data found.")
    except Exception as e:
        st.warning(f"Waiting for {csv_file} to be uploaded...")

# Navigation Tabs
tab1, tab2 = st.tabs(["🏆 Premier League", "⚽ Championship"])

with tab1:
    run_analysis('all_subs_2026.csv', "PL")

with tab2:
    run_analysis('championship_subs_2026.csv', "EFL")
