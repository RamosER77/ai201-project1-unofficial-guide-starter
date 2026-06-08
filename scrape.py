import requests
from bs4 import BeautifulSoup
import os

os.makedirs("documents", exist_ok=True)

# This makes our request look like a real browser
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

urls = {
    "csusm_dining_home": "https://www.csusm.edu/dining/index.html",
    "csusm_dining_locations": "https://www.csusm.edu/dining/locations/index.html",
    "csusm_campus_way_cafe": "https://www.csusm.edu/dining/locations/cafe.html",
}

for filename, url in urls.items():
    print(f"Scraping {url}...")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["nav", "header", "footer", "script", "style"]):
            tag.decompose()

        text = soup.get_text(separator="\n", strip=True)

        with open(f"documents/{filename}.txt", "w") as f:
            f.write(f"SOURCE: {url}\n\n")
            f.write(text)

        print(f"✅ Saved documents/{filename}.txt")

    except Exception as e:
        print(f"❌ Failed {filename}: {e}")

print("\nDone!")
