import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import os

def get_subs():
    # 1. Target the 2025/26 Season Schedule
    url = "https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures"
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.content, 'html.parser')
    
    # 2. Get the latest 10 Match Reports (to avoid getting blocked)
    links = [f"https://fbref.com{a['href']}" for a in soup.select('td[data-stat="match_report"] a')]
    
    all_subs = []
    for link in links[-10:]:
        try:
            print(f"Scraping: {link}")
            time.sleep(5) # Respect the robot limits
            
            # Read ALL tables on the page
            tables = pd.read_html(link)
            
            # Find the "Match Summary" table (where the sub icons live)
            for df in tables:
                # We are looking for columns that usually contain events
                if any(col in df.columns for col in ['Event', 'Time', 'Score']):
                    # Filter rows that look like substitutions
                    # FBref uses 'Substitution' text in the Event column
                    mask = df.stack().str.contains('Substitution', na=False).unstack().any(axis=1)
                    subs_df = df[mask].copy()
                    
                    if not subs_df.empty:
                        # Extract the data
                        # Note: We take the first 3 columns as they usually hold Time and Names
                        subs_df['Match'] = link.split('/')[-1]
                        all_subs.append(subs_df)
        except Exception as e:
            print(f"Skipping {link} due to {e}")
            continue

    if all_subs:
        final_data = pd.concat(all_subs, ignore_index=True)
        # Convert to CSV format
        final_data.to_csv('all_subs_2026.csv', index=False)
        print("✅ Data Found and Saved!")
    else:
        print("❌ No new substitutions found in these match reports.")

if __name__ == "__main__":
    get_subs()
