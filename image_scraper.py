import requests
from bs4 import BeautifulSoup
import os
import re

os.makedirs('agency_photos', exist_ok=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

print("Starting Scraper...")

for page_num in range(1, 26):
    url = f"https://www.baira.org.bd/dir/all-member-list/photo?page={page_num}"
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table')
        
        if not table:
            print(f"Page {page_num}: No table found!")
            continue
            
        rows = table.find_all('tr')[1:]
        print(f"Page {page_num}: Found {len(rows)} rows.")

        for row in rows:
            cols = row.find_all('td')
            if len(cols) < 4: continue
            
            agency_info = cols[1].get_text(strip=True)
            rl_match = re.search(r'RL-(\d+)', agency_info)
            rl_no = rl_match.group(0) if rl_match else None
            
            img_tag = cols[3].find('img')
            if img_tag and img_tag.get('src') and rl_no:
                img_url = img_tag['src']
                if not img_url.startswith('http'):
                    img_url = "https://www.baira.org.bd" + img_url
                
                img_data = requests.get(img_url, headers=headers).content
                with open(f"agency_photos/{rl_no}.jpg", 'wb') as f:
                    f.write(img_data)
                print(f"Success: {rl_no}.jpg")
    except Exception as e:
        print(f"Error on page {page_num}: {e}")

print("Done!")
