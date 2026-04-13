import streamlit as st
import pandas as pd

# 1. UI Setup (Dark/Clean Theme)
st.set_page_config(page_title="PL Sub Tracker", layout="wide")
st.markdown("<style>.main { background-color: #0d1117; color: #e6edf3; }</style>", unsafe_allow_html=True)

# 2. Historical Data (The "Scripted" History)
# This will be replaced by your CSV once the scraper runs.
@st.cache_data
def get_historical_data():
    data = [
        {'Team': 'Man Utd', 'Match': 'vs Leeds', 'Date': '2026-04-12', 'Min': 62, 'Off': 'Amad Diallo', 'On': 'Benjamin Sesko'},
        {'Team': 'Man Utd', 'Match': 'vs Arsenal', 'Date': '2026-04-05', 'Min': 65, 'Off': 'Amad Diallo', 'On': 'Benjamin Sesko'},
        {'Team': 'Leeds', 'Match': 'vs Utd', 'Date': '2026-04-12', 'Min': 68, 'Off': 'Dan James', 'On': 'Wilfried Gnonto'},
        {'Team': 'Arsenal', 'Match': 'vs Everton', 'Date': '2026-04-11', 'Min': 64, 'Off': 'Gabriel Jesus', 'On': 'Viktor Gyokeres'}
    ]
    return pd.DataFrame(data)

df = get_historical_data()

st.title("📜 Premier League Historical Sub Tracker")

# 3. Interactive Dropdowns (Your specific request)
col1, col2 = st.columns(2)

with col1:
    team_choice = st.selectbox("1. Pick a Team", sorted(df['Team'].unique()))
    team_df = df[df['Team'] == team_choice]

with col2:
    # Get all players who were either subbed ON or OFF for that team
    players = sorted(list(set(team_df['Off'].tolist() + team_df['On'].tolist())))
    player_choice = st.selectbox("2. Pick a Player", players)

st.divider()

# 4. Results Section
st.subheader(f"Substitution Logs: {player_choice}")

# Find every instance where this player was involved in a sub
history = team_df[(team_df['Off'] == player_choice) | (team_df['On'] == player_choice)]

if not history.empty:
    # Highlight the row if they were the one coming OFF (The "Starter")
    st.table(history[['Date', 'Min', 'Match', 'Off', 'On']])
    
    # Logic: If they are often subbed OFF, tell us the average minute
    off_only = history[history['Off'] == player_choice]
    if not off_only.empty:
        avg_min = int(off_only['Min'].mean())
        st.info(f"💡 Manager Habit: {player_choice} is usually subbed OFF around the **{avg_min}'** minute.")
else:
    st.write("No historical data found for this player in the 2025/26 logs.")
