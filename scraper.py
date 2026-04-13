import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import os

def get_subs():
    # 1. Get the 2025/26 Schedule
    url = "https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures"
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    
    # 2. Extract Match Report links
    links = [f"https://fbref.com{a['href']}" for a in soup.select('td[data-stat="match_report"] a')]
    
    all_subs = []
    # Rate limit: We only scrape the latest 20 games to stay under FBref's radar
    for link in links[-20:]:
        try:
            time.sleep(4) # Crucial: Don't remove this or you'll be blocked
            tables = pd.read_html(link)
            for table in tables:
                if 'Event' in table.columns and 'Time' in table.columns:
                    # Filter for substitutions
                    subs = table[table['Event'].str.contains('Substitution', na=False)].copy()
                    # Clean the names: "Player ON for Player OFF"
                    subs['On'] = subs['Event'].str.split(' for ').str[0].str.replace('Substitution', '').strip()
                    subs['Off'] = subs['Event'].str.split(' for ').str[1].strip()
                    subs['Match'] = link.split('/')[-1].replace('-Match-Report', '')
                    all_subs.append(subs[['Time', 'Off', 'On', 'Match']])
        except:
            continue

    if all_subs:
        new_df = pd.concat(all_subs)
        if os.path.exists('all_subs_2026.csv'):
            existing_df = pd.read_csv('all_subs_2026.csv')
            final_df = pd.concat([existing_df, new_df]).drop_duplicates()
        else:
            final_df = new_df
        final_df.to_csv('all_subs_2026.csv', index=False)
        print("✅ Data updated.")

if __name__ == "__main__":
    get_subs()
