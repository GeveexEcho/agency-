import requests
from bs4 import BeautifulSoup
import os
import re
import time

folder = 'agency_photos'
os.makedirs(folder, exist_ok=True)

# ব্রাউজার সেশন সিমুলেশন
session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.baira.org.bd/dir/all-member-list/photo'
}

for page_num in range(1, 26):
    url = f"https://www.baira.org.bd/dir/all-member-list/photo?page={page_num}"
    print(f"\n>>> Scanning Page {page_num}...")
    
    try:
        response = session.get(url, headers=headers, timeout=20)
        # যদি সাইট থেকে ব্লক করে
        if response.status_code != 200:
            print(f"!!! Access Denied for Page {page_num} (Status: {response.status_code})")
            continue

        soup = BeautifulSoup(response.content, 'lxml')
        rows = soup.find_all('tr')
        
        found_on_page = 0
        for row in rows:
            cols = row.find_all('td')
            if len(cols) < 4: continue
            
            # RL No বের করা
            agency_info = cols[1].get_text(strip=True)
            rl_match = re.search(r'RL-(\d+)', agency_info)
            if not rl_match: continue
            rl_no = rl_match.group(0).replace("/", "-")
            
            # ইমেজের আসল লিঙ্ক খুঁজে বের করা
            img_tag = cols[3].find('img')
            if img_tag:
                img_src = img_tag.get('src') or img_tag.get('data-src')
                if img_src:
                    if not img_src.startswith('http'):
                        img_src = "https://www.baira.org.bd" + img_src
                    
                    # ইমেজটি ডাউনলোড করা
                    try:
                        img_data = session.get(img_src, headers=headers, timeout=10).content
                        if len(img_data) > 500: # নিশ্চিত হওয়া যে এটি কোনো ছোট পিক্সেল বা ব্ল্যাঙ্ক ইমেজ নয়
                            with open(f"{folder}/{rl_no}.jpg", 'wb') as f:
                                f.write(img_data)
                            print(f"Saved: {rl_no}.jpg")
                            found_on_page += 1
                    except:
                        pass
        
        print(f"Total saved from Page {page_num}: {found_on_page}")
        time.sleep(2) # সার্ভারকে সময় দেওয়া

    except Exception as e:
        print(f"Error: {e}")

print("\n--- JOB FINISHED! ---")
