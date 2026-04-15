import requests
from bs4 import BeautifulSoup
import os

os.makedirs('baira_directory', exist_ok=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

for page_num in range(1, 26):
    url = f"https://www.baira.org.bd/dir/all-member-list/photo?page={page_num}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    file_path = f"baira_directory/agency_part_{page_num}.md"
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("| SL No. | Agency Name & RL No. | Owner Name & Designation | Photo | Address | Mobile, Phone & Fax | Email & Web |\n")
        f.write("|---|---|---|---|---|---|---|\n")
        
        table = soup.find('table')
        if table:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if not cols:
                    continue
                
                row_data = [col.get_text(separator=" ", strip=True).replace('\n', ' ').replace('|', '\\|') for col in cols]
                
                while len(row_data) < 7:
                    row_data.append("")
                    
                row_data = row_data[:7]
                row_data[3] = "N/A"
                
                f.write(f"| {' | '.join(row_data)} |\n")
              
