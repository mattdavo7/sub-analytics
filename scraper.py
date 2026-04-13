import requests
import pandas as pd
import time
import os

# --- CONFIG ---
API_KEY = "646723f7-64cf-4e49-b4e4-3f339d6edfe1"
HEADERS = {"Authorization": API_KEY}
BASE_URL = "https://api.balldontlie.io/epl/v2"

def get_all_subs():
    # 1. Get all matches for the 2025/26 season
    print("🛰️ Connecting to Ball Don't Lie...")
    match_res = requests.get(f"{BASE_URL}/matches", params={"season": 2025}, headers=HEADERS)
    matches = match_res.json().get('data', [])
    
    # Filter for games that are finished (Status: 'Final')
    match_ids = [m['id'] for m in matches if m['status'] == 'Final']
    print(f"✅ Found {len(match_ids)} completed matches to analyze.")

    all_pairs = []

    # 2. Get events for each match
    for m_id in match_ids:
        # Respect API rate limits (1.2s sleep for ~50 requests per minute)
        time.sleep(1.2) 
        
        event_res = requests.get(f"{BASE_URL}/match_events", params={"match_ids[]": m_id}, headers=HEADERS)
        events = event_res.json().get('data', [])
        
        for e in events:
            if e['event_type'] == 'substitution':
                # BDL Logic: 'player' is ON, 'secondary_player' is OFF
                p_on = e.get('player', {}).get('display_name', 'Unknown')
                p_off = e.get('secondary_player', {}).get('display_name', 'Unknown')
                
                all_pairs.append({
                    "Team_ID": e['team_id'],
                    "Match_ID": m_id,
                    "Min": e['event_time'],
                    "Off": p_off,
                    "On": p_on
                })

    # 3. Save to CSV
    if all_pairs:
        df = pd.DataFrame(all_pairs)
        df.to_csv('all_subs_2026.csv', index=False)
        print(f"🚀 Success! Created 'all_subs_2026.csv' with {len(df)} sub events.")
    else:
        print("❌ No sub data found. Check match status.")

if __name__ == "__main__":
    get_all_subs()
