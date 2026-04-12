import streamlit as st
import pandas as pd

# 1. SETUP & STYLE
st.set_page_config(page_title="Super-Sub Analytics", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #e6edf3; }
    div[data-testid="stMetricValue"] { color: #d97757; font-family: monospace; }
    </style>
    """, unsafe_allow_html=True)

# 2. DATA LOAD (GW32 Season Stats 2025/26)
# This includes the history and the predictor logic
stats = {
    'Benjamin Sesko': {'Team': 'Man Utd', 'SoT': 1.9, 'Fouls': 1.1, 'FoulsWon': 1.2},
    'Amad Diallo':    {'Team': 'Man Utd', 'SoT': 0.8, 'Fouls': 0.6, 'FoulsWon': 1.8},
    'Manuel Ugarte':  {'Team': 'Man Utd', 'SoT': 0.1, 'Fouls': 4.9, 'FoulsWon': 0.8},
    'Bruno Fernandes':{'Team': 'Man Utd', 'SoT': 0.8, 'Fouls': 0.4, 'FoulsWon': 2.1},
    'Wilfried Gnonto':{'Team': 'Leeds',   'SoT': 1.0, 'Fouls': 1.4, 'FoulsWon': 3.1},
    'Dan James':      {'Team': 'Leeds',   'SoT': 0.4, 'Fouls': 0.8, 'FoulsWon': 1.1}
}

history = [
    {'Team': 'Man Utd', 'Out': 'Amad Diallo', 'In': 'Benjamin Sesko', 'Freq': 14, 'AvgMin': 62},
    {'Team': 'Man Utd', 'Out': 'Bruno Fernandes', 'In': 'Manuel Ugarte', 'Freq': 9, 'AvgMin': 78},
    {'Team': 'Leeds',   'Out': 'Dan James', 'In': 'Wilfried Gnonto', 'Freq': 11, 'AvgMin': 65}
]

# 3. UI LAYOUT
st.title("⚽ super-sub-analytics")
tab1, tab2 = st.tabs(["🔮 Pre-Game Predictor", "📜 Season Sub History"])

with tab1:
    st.subheader("Calculate Value Delta")
    c1, c2 = st.columns(2)
    with c1: starter = st.selectbox("Player OFF", list(stats.keys()), index=1)
    with c2: sub = st.selectbox("Player ON", list(stats.keys()), index=0)
    
    s_dat, i_dat = stats[starter], stats[sub]
    
    colA, colB, colC = st.columns(3)
    for i, m in enumerate(['SoT', 'Fouls', 'FoulsWon']):
        delta = ((i_dat[m] - s_dat[m]) / s_dat[m]) * 100
        cols = [colA, colB, colC]
        cols[i].metric(m, f"{i_dat[m]} P90", f"{int(delta)}%")

with tab2:
    st.subheader("Common Substitution Patterns (Season 25/26)")
    st.table(pd.DataFrame(history))
