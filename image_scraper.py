import requests
from bs4 import BeautifulSoup
import os
import re

# ফোল্ডার তৈরি নিশ্চিত করা
folder = 'agency_photos'
if not os.path.exists(folder):
    os.makedirs(folder)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

for page_num in range(1, 26):
    url = f"https://www.baira.org.bd/dir/all-member-list/photo?page={page_num}"
    print(f"Checking Page {page_num}...")
    try:
        response = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.content, 'html.parser')
        rows = soup.find_all('tr')[1:] # Header বাদ দিয়ে
        
        for row in rows:
            cols = row.find_all('td')
            if len(cols) < 4: continue
            
            # RL Number বের করা
            agency_text = cols[1].get_text(strip=True)
            rl_match = re.search(r'RL-(\d+)', agency_text)
            rl_no = rl_match.group(0) if rl_match else None
            
            # ইমেজ ট্যাগ খোঁজা
            img_tag = cols[3].find('img')
            if img_tag and img_tag.get('src') and rl_no:
                img_url = img_tag['src']
                if not img_url.startswith('http'):
                    img_url = "https://www.baira.org.bd" + img_url
                
                # ইমেজ ডাউনলোড এবং সেভ
                img_data = requests.get(img_url, headers=headers).content
                with open(f"{folder}/{rl_no}.jpg", 'wb') as f:
                    f.write(img_data)
                print(f"Saved: {rl_no}.jpg")
    except Exception as e:
        print(f"Error: {e}")

print("--- FINISHED ---")
