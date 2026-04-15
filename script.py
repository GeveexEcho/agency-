import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://www.baira.org.bd"
PAGES = 25
FOLDER_PREFIX = "public"
MAX_FILES_PER_FOLDER = 1000 # It will create a new folder after every 1000 files

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def download_images():
    total_downloaded = 0
    
    for page in range(1, PAGES + 1):
        url = f"{BASE_URL}/dir/all-member-list/photo?page={page}"
        print(f"Scraping Page {page}...")
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            rows = soup.find_all('tr')
            
            for row in rows:
                row_text = row.get_text()
                
                rl_match = re.search(r'RL\s*No:\s*(\d+)', row_text, re.IGNORECASE)
                if rl_match:
                    rl_number = rl_match.group(1)
                    
                    img_tag = row.find('img')
                    if img_tag and img_tag.get('src'):
                        img_url = img_tag['src']
                        full_img_url = urljoin(BASE_URL, img_url)
                        
                        if "no_image" in full_img_url.lower() or "no-image" in full_img_url.lower():
                            continue
                            
                        ext = full_img_url.split('.')[-1].split('?')[0]
                        if len(ext) > 4:  
                            ext = "jpg"
                            
                        file_name = f"RL_{rl_number}.{ext}"
                        
                        # Determine which folder to put the file in based on the count
                        folder_index = (total_downloaded // MAX_FILES_PER_FOLDER) + 1
                        current_folder = f"{FOLDER_PREFIX}_{folder_index}"
                        
                        # Create the folder if it doesn't exist yet
                        if not os.path.exists(current_folder):
                            os.makedirs(current_folder)
                            print(f"\nCreated new folder: {current_folder}")
                            
                        file_path = os.path.join(current_folder, file_name)
                        
                        try:
                            img_data = requests.get(full_img_url, headers=headers).content
                            with open(file_path, 'wb') as handler:
                                handler.write(img_data)
                            print(f"Saved: {file_path}")
                            total_downloaded += 1
                        except Exception as e:
                            print(f"Failed to download image for RL {rl_number}: {e}")
        
        except Exception as e:
            print(f"Failed to load page {page}: {e}")

    print(f"\nScraping complete! Total images downloaded: {total_downloaded}")

if __name__ == "__main__":
    download_images()
                        
