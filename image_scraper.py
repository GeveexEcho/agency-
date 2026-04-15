import requests
from bs4 import BeautifulSoup
import os
import re
import time

folder = 'agency_photos'
os.makedirs(folder, exist_ok=True)

session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.baira.org.bd/'
}

for page_num in range(1, 26):
    url = f"https://www.baira.org.bd/dir/all-member-list/photo?page={page_num}"
    print(f"Checking Page {page_num}...")
    try:
        response = session.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.content, 'lxml')
        rows = soup.find_all('tr')
        
        for row in rows:
            cols = row.find_all('td')
            if len(cols) < 4: continue
            
            agency_text = cols[1].get_text(strip=True)
            rl_match = re.search(r'RL-(\d+)', agency_text)
            if not rl_match: continue
            rl_no = rl_match.group(0)
            
            img_tag = cols[3].find('img')
            if img_tag and img_tag.get('src'):
                img_url = img_tag['src']
                if not img_url.startswith('http'):
                    img_url = "https://www.baira.org.bd" + img_url
                
                # ইমেজ ডাউনলোড
                img_res = session.get(img_url, headers=headers, timeout=10)
                if img_res.status_code == 200:
                    with open(f"{folder}/{rl_no}.jpg", 'wb') as f:
                        f.write(img_res.content)
                    print(f"Success: {rl_no}.jpg")
                else:
                    print(f"Failed to download image for {rl_no}")
        
        time.sleep(1) # সার্ভারকে চাপ না দিতে ১ সেকেন্ড বিরতি
    except Exception as e:
        print(f"Error on page {page_num}: {e}")

print("--- ALL DONE! ---")
