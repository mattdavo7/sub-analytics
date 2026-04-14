import streamlit as st
import pandas as pd
import urllib.parse

# 1. Page Configuration
st.set_page_config(page_title="Football Sub Intel", layout="wide")

# 2. Custom Dark Theme Styling
st.markdown("""
    <style>
    .main { background-color: #050505; color: #ffffff; }
    div[data-testid="stMetric"] {
        background-color: #111111;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #333;
        transition: 0.3s;
    }
    div[data-testid="stMetric"]:hover {
        border-color: #4CAF50;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #111111;
        border-radius: 5px;
        padding: 10px 20px;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Helper Function for WhoScored Links
def get_whoscored_link(player_name, team_name):
    # Creates a search query specifically for the WhoScored profile
    query = f"site:whoscored.com {player_name} {team_name} player profile"
    return f"https://www.google.com/search?q={urllib.parse.quote(query)}"

# 4. Main Analysis Engine
def run_analysis(csv_file, league_label):
    try:
        # Load the data
        df = pd.read_csv(csv_file)
        
        # Ensure 'gw' (Game Week) is treated as a string for clean display
        df['gw'] = df['gw'].astype(str)

        # Filters
        col1, col2 = st.columns(2)
        with col1:
            team_list = sorted(df['team'].unique())
            team = st.selectbox(f"Select Club", team_list, key=f"{league_label}_team")
            team_df = df[df['team'] == team]
        with col2:
            player_off_list = sorted(team_df['off'].unique())
            player_off = st.selectbox(f"Select Player OFF", player_off_list, key=f"{league_label}_off")
        
        # Filter data for specific player
        logs = team_df[team_df['off'] == player_off]
        
        if len(logs) > 0:
            st.subheader(f"Tactical Habits for {player_off}")
            st.markdown(f"🔗 [Open {player_off} Profile on WhoScored]({get_whoscored_link(player_off, team)})")
            
            # Sub Frequency Analysis
            counts = logs['on'].value_counts().reset_index()
            counts.columns = ['Replacement', 'Freq']
            
            # Display metrics in columns
            metric_cols = st.columns(min(len(counts), 5)) # Show up to 5 main subs
            for i, row in counts.iterrows():
                if i < 5:
                    pct = int((row['Freq'] / len(logs)) * 100)
                    avg_min = int(logs[logs['on'] == row['Replacement']]['min'].mean())
                    with metric_cols[i]:
                        st.metric(label=f"In: {row['Replacement']}", value=f"{row['Freq']} Games", delta=f"{pct}% Frequency")
                        st.link_button(f"📊 {row['Replacement']} Stats", get_whoscored_link(row['Replacement'], team))
                        st.caption(f"Avg Time: {avg_min}'")
            
            # Raw Data Table
            st.write("---")
            st.write("### 📅 Seasonal Match Timeline")
            # Sort by date descending so newest games are at the top
            display_df = logs[['gw', 'min', 'on', 'opp', 'date']].sort_values(by='date', ascending=False)
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
        else:
            st.info(f"No substitution data found for {player_off} in the {league_label}.")
            
    except FileNotFoundError:
        st.error(f"⚠️ Data file '{csv_file}' missing. Please upload to GitHub.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# 5. Navigation Tabs
st.title("⚽ Football Substitution Intelligence")
tab1, tab2, tab3 = st.tabs(["🏆 Premier League", "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Championship", "⭐ Champions League"])

with tab1:
    run_analysis('all_subs_2026.csv', "Premier League")

with tab2:
    run_analysis('championship_subs_2026.csv', "Championship")

with tab3:
    run_analysis('champions_league_subs_2026.csv', "Champions League")
