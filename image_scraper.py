import requests
from bs4 import BeautifulSoup
import os
import re
import time

folder = 'agency_photos'
os.makedirs(folder, exist_ok=True)

session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Referer': 'https://www.baira.org.bd/'
}

for page_num in range(1, 26):
    url = f"https://www.baira.org.bd/dir/all-member-list/photo?page={page_num}"
    print(f"--- Processing Page: {page_num} ---")
    try:
        response = session.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # টেবিল রো খুঁজে বের করা
        rows = soup.select('table tr')
        if not rows:
            print(f"Warning: No rows found on page {page_num}")
            continue

        for row in rows:
            cols = row.find_all('td')
            if len(cols) < 4: continue
            
            # RL Number বের করা (Agency Name কলাম থেকে)
            agency_text = cols[1].get_text(strip=True)
            rl_match = re.search(r'RL-(\d+)', agency_text)
            if not rl_match: continue
            rl_no = rl_match.group(0).replace("/", "-") # ফাইলের নামে সমস্যা এড়াতে
            
            # ইমেজ সোর্স (src) খুঁজে বের করা
            img_tag = cols[3].find('img')
            if img_tag and img_tag.get('src'):
                img_url = img_tag['src']
                if not img_url.startswith('http'):
                    img_url = "https://www.baira.org.bd" + img_url
                
                # ইমেজ ফাইল ডাউনলোড
                try:
                    img_res = session.get(img_url, headers=headers, timeout=15)
                    if img_res.status_code == 200:
                        with open(f"{folder}/{rl_no}.jpg", 'wb') as f:
                            f.write(img_res.content)
                        print(f"Download Success: {rl_no}.jpg")
                    else:
                        print(f"Failed to fetch image: {rl_no} (Status: {img_res.status_code})")
                except:
                    print(f"Connection error for RL: {rl_no}")
        
        time.sleep(1.5) # সার্ভার ব্লকিং এড়াতে কিছুটা বিরতি
    except Exception as e:
        print(f"Major error on page {page_num}: {e}")

print("\n--- ALL TASKS FINISHED! Check your folder now. ---")
