import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Base URL and the target folder
BASE_URL = "https://www.baira.org.bd"
PAGES = 25
FOLDER_NAME = "public"

# Create the public folder if it doesn't exist
if not os.path.exists(FOLDER_NAME):
    os.makedirs(FOLDER_NAME)
    print(f"Created folder: {FOLDER_NAME}")

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
            
            # Find all table rows that might contain member data
            rows = soup.find_all('tr')
            
            for row in rows:
                row_text = row.get_text()
                
                # Check if this row contains an RL number using regex
                rl_match = re.search(r'RL\s*No:\s*(\d+)', row_text, re.IGNORECASE)
                if rl_match:
                    rl_number = rl_match.group(1)
                    
                    # Find the image tag within this row
                    img_tag = row.find('img')
                    if img_tag and img_tag.get('src'):
                        img_url = img_tag['src']
                        
                        # Sometimes image URLs are relative, make sure it's an absolute URL
                        full_img_url = urljoin(BASE_URL, img_url)
                        
                        # We skip default "no image" placeholders if they are identifiable
                        if "no_image" in full_img_url.lower() or "no-image" in full_img_url.lower():
                            continue
                            
                        # Extract extension (usually .jpg or .png)
                        ext = full_img_url.split('.')[-1].split('?')[0]
                        if len(ext) > 4:  # Fallback if extension is not standard
                            ext = "jpg"
                            
                        file_name = f"RL_{rl_number}.{ext}"
                        file_path = os.path.join(FOLDER_NAME, file_name)
                        
                        # Download the image
                        try:
                            img_data = requests.get(full_img_url, headers=headers).content
                            with open(file_path, 'wb') as handler:
                                handler.write(img_data)
                            print(f"Saved: {file_name}")
                            total_downloaded += 1
                        except Exception as e:
                            print(f"Failed to download image for RL {rl_number}: {e}")
        
        except Exception as e:
            print(f"Failed to load page {page}: {e}")

    print(f"\nScraping complete! Total images downloaded: {total_downloaded}")

if __name__ == "__main__":
    download_images()
                      
