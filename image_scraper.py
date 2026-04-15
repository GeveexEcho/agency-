import requests
from bs4 import BeautifulSoup
import os
import re

os.makedirs('agency_photos', exist_ok=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def get_rl_number(text):
    match = re.search(r'RL-(\d+)', text)
    return match.group(0) if match else None

for page_num in range(1, 26):
    url = f"https://www.baira.org.bd/dir/all-member-list/photo?page={page_num}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')
    
    table = soup.find('table')
    if not table:
        continue
        
    rows = table.find_all('tr')[1:]
    
    for row in rows:
        cols = row.find_all('td')
        if len(cols) < 4:
            continue
            
        agency_info = cols[1].get_text(strip=True)
        rl_no = get_rl_number(agency_info)
        
        img_tag = cols[3].find('img')
        if img_tag and img_tag.get('src') and rl_no:
            img_url = img_tag['src']
            if not img_url.startswith('http'):
                img_url = "https://www.baira.org.bd" + img_url
            
            try:
                img_data = requests.get(img_url, headers=headers).content
                filename = f"agency_photos/{rl_no}.jpg"
                with open(filename, 'wb') as handler:
                    handler.write(img_data)
            except Exception:
                pass
              
