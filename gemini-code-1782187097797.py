import requests
from bs4 import BeautifulSoup
import csv
import time
import os
import re
from urllib.parse import urljoin
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE_URL = "https://crackmes.one"
START_URL = f"{BASE_URL}/lasts/1"
OUTPUT_FILE = os.path.join("_source_crackmesone", "crackme_writeups.csv")
REQUEST_TIMEOUT = 15
REQUEST_DELAY_SECONDS = 1

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def build_session():
    retry = Retry(
        total=3,
        connect=3,
        read=3,
        status=3,
        backoff_factor=0.75,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=("GET",),
    )
    adapter = HTTPAdapter(max_retries=retry)
    session = requests.Session()
    session.headers.update(HEADERS)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

def fetch_html(session, url):
    response = session.get(url, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.text

def parse_number(value):
    match = re.search(r"\d+(?:\.\d+)?", value or "")
    if not match:
        raise ValueError(f"missing numeric value in {value!r}")
    number = float(match.group(0))
    return int(number) if number.is_integer() else number

def get_writeup_link(session, challenge_url):
    """
    Navigates to the individual crackme detail page,
    finds the writeup section, and extracts the zip download URL.
    """
    try:
        soup = BeautifulSoup(fetch_html(session, challenge_url), 'html.parser')
        
        # Look for the solution download links visible under the Writeups tab
        for anchor in soup.find_all('a', href=True):
            href = anchor['href']
            if '/static/solution/' in href and href.endswith('.zip'):
                return urljoin(BASE_URL, href)
    except requests.RequestException as e:
        print(f"[-] Error fetching writeup page details for {challenge_url}: {e}")
    return None

def scrape_crackmes(max_pages=5):
    session = build_session()
    extracted_challenges = []
    seen_challenge_urls = set()
    skipped_rows = 0
    
    # Track the current page URL or use pagination loops if needed
    page_urls = [f"{BASE_URL}/lasts/{page}" for page in range(1, max_pages + 1)]
    
    print("[+] Initializing crackmes.one target crawl...")

    for page_number, current_url in enumerate(page_urls, start=1):
        try:
            soup = BeautifulSoup(fetch_html(session, current_url), 'html.parser')
        except requests.RequestException as e:
            print(f"[-] Failed to access page {page_number}: {current_url} ({e})")
            continue
        
        # Locate the rows inside the 'Latest Crackmes' table
        table = soup.find('table') or soup.find(class_='table')
        rows = table.find_all('tr') if table else soup.find_all('tr')

        print(f"[+] Processing page {page_number}: {len(rows)} potential challenge items found...")

        for row in rows:
            cols = row.find_all('td')
            if len(cols) < 11:  # Skips table headers/empty rows
                continue
                
            try:
                # Table schema: Name | Author | Language | Arch | Difficulty | Quality | Platform | Size | Date | Downloads | Writeups | Comments
                title_cell = cols[0]
                author = cols[1].get_text(" ", strip=True)
                language = cols[2].get_text(" ", strip=True)
                arch = cols[3].get_text(" ", strip=True)
                difficulty = parse_number(cols[4].get_text(" ", strip=True))
                quality = parse_number(cols[5].get_text(" ", strip=True))
                platform = cols[6].get_text(" ", strip=True)
                writeups_count = int(parse_number(cols[10].get_text(" ", strip=True)))
                
                # Prefer the challenge link, not profile links that may appear earlier in the row.
                link_element = title_cell.find('a', href=lambda href: href and '/crackme/' in href)
                if not link_element:
                    skipped_rows += 1
                    continue
                    
                challenge_route = link_element['href']
                challenge_url = urljoin(BASE_URL, challenge_route)
                if challenge_url in seen_challenge_urls:
                    continue
                seen_challenge_urls.add(challenge_url)

                challenge_title = link_element.get_text(" ", strip=True) or f"Crackme_{challenge_route.rstrip('/').split('/')[-1]}"

                # Condition 1: Quality must be 3.5 or above
                # Condition 2: Must have at least 1 writeup available
                if quality >= 3.5 and writeups_count > 0:
                    print(f"[+] Match found! Extracting details for: {challenge_title} (Quality: {quality})")
                    
                    # Polite rate-limiting delay before jumping to the secondary page crawl
                    time.sleep(REQUEST_DELAY_SECONDS)
                    
                    writeup_download_url = get_writeup_link(session, challenge_url)
                    
                    if writeup_download_url:
                        extracted_challenges.append({
                            'Platform': platform,
                            'Title': challenge_title,
                            'Author': author,
                            'Language': language,
                            'Architecture': arch,
                            'Difficulty': difficulty,
                            'Quality': quality,
                            'Challenge_URL': challenge_url,
                            'Writeup_URL': writeup_download_url
                        })
                    else:
                        print(f"[!] Writeup link reported missing inside individual detail page for {challenge_title}")
                        
            except (ValueError, IndexError) as e:
                skipped_rows += 1
                print(f"[!] Skipping row with unexpected format: {e}")
                continue

        time.sleep(REQUEST_DELAY_SECONDS)

    # Cleanly sort the dataset alphabetically by platform (Groups Windows vs Unix/linux etc.)
    sorted_challenges = sorted(extracted_challenges, key=lambda x: (x['Platform'].lower(), x['Title'].lower()))
    print(f"[+] Finished crawl: {len(sorted_challenges)} matching challenges, {skipped_rows} skipped rows.")
    return sorted_challenges

def save_to_csv(data, filename=OUTPUT_FILE):
    if not data:
        print("[-] No challenges met your high-quality or writeup-available filters.")
        return

    fields = ['Platform', 'Title', 'Author', 'Language', 'Architecture', 'Difficulty', 'Quality', 'Challenge_URL', 'Writeup_URL']
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for item in data:
            writer.writerow(item)
            
    print(f"\n[+] Success! Created organized sheet mapping data pipeline output to: {os.path.abspath(filename)}")

if __name__ == "__main__":
    dataset = scrape_crackmes()
    save_to_csv(dataset)
