import time
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def scrape_page(url: str, throttle: float = 3) -> dict:
    

    # Apply throttle
    time.sleep(throttle)

    # Headers to mimic a browser
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                             "(KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"}

    # Perform GET request with proper SSL certs
    response = requests.get(url, headers=headers, timeout=10, verify=False)
    response.raise_for_status()

    # Parse HTML
    soup = BeautifulSoup(response.text, "lxml")

    # Extract title safely
    title = soup.title.string.strip() if soup.title else None

    # Extract visible text
    text = soup.get_text(separator=" ", strip=True)

    # Extract links
    links = [a["href"] for a in soup.find_all("a", href=True)]

    return {
        "title": title,
        "text": text,
        "links": links
    }