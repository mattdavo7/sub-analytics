import requests
import pandas as pd
import time
import os

# --- AUTH & CONFIG ---
API_KEY = "646723f7-64cf-4e49-b4e4-3f339d6edfe1"
HEADERS = {"Authorization": API_KEY}
BASE_URL = "https://api.balldontlie.io/epl/v2"

def get_full_season_subs():
    print("🛰️ Connecting to Ball Don't Lie...")
    
    # 1. Get all matches for the 2025 season
    # per_page=100 helps get more matches in one go
    match_res = requests.get(f"{BASE_URL}/matches", params={"season": 2025, "per_page": 100}, headers=HEADERS)
    matches = match_res.json().get('data', [])
    
    # Filter for 'Final' status games
    match_ids = [m['id'] for m in matches if m['status'] == 'Final']
    print(f"✅ Found {len(match_ids)} completed matches to process.")

    all_pairs = []

    # 2. Extract substitution events for every match
    for m_id in match_ids:
        # Rate limit safety: 1.2s sleep ensures we don't get a 429 error
        time.sleep(1.2)
        
        event_res = requests.get(f"{BASE_URL}/match_events", params={"match_ids[]": m_id}, headers=HEADERS)
        events = event_res.json().get('data', [])
        
        for e in events:
            if e['event_type'] == 'substitution':
                # ON player is in the 'player' object
                # OFF player is in the 'secondary_player' object
                p_on = e.get('player', {}).get('display_name', 'Unknown')
                p_off = e.get('secondary_player', {}).get('display_name', 'Unknown')
                
                all_pairs.append({
                    "Team_ID": e['team_id'],
                    "Match_ID": m_id,
                    "Min": e['event_time'],
                    "Off": p_off,
                    "On": p_on
                })
        print(f"Processed Match {m_id}...")

    # 3. Save to the main CSV file
    if all_pairs:
        df = pd.DataFrame(all_pairs)
        df.to_csv('all_subs_2026.csv', index=False)
        print(f"🚀 Success! Created 'all_subs_2026.csv' with {len(df)} sub events.")
    else:
        print("❌ No substitution data found. Check match statuses.")

if __name__ == "__main__":
    get_full_season_subs()
