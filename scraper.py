import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "https://t.me/"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def detect_profile_type(html):
    if "tgme_channel_info" in html:
        return "📢 Channel"
    elif "tgme_group_info" in html:
        return "👥 Group"
    else:
        return "👤 User"

def scrape_members(soup, profile_type):
    if profile_type in ["📢 Channel", "👥 Group"]:
        counter = soup.find("div", class_="tgme_page_extra")
        if counter:
            return counter.text.strip()
    return "Not Public"

def telegram_info(username):
    start = time.time()
    url = BASE_URL + username

    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
    except:
        return {"error": "Request gagal"}

    if r.status_code != 200:
        return {"error": "Username private / tidak valid"}

    soup = BeautifulSoup(r.text, "html.parser")
    profile_type = detect_profile_type(r.text)

    title = soup.find("div", class_="tgme_page_title")
    bio = soup.find("div", class_="tgme_page_description")
    photo = soup.find("img", class_="tgme_page_photo_image")

    return {
        "Username": f"@{username}",
        "Nama": title.text.strip() if title else "-",
        "Bio": bio.text.strip() if bio else "-",
        "Tipe": profile_type,
        "Verified": "Yes" if "tgme_icon_verified" in r.text else "No",
        "Members": scrape_members(soup, profile_type),
        "Link": url,
        "Waktu": f"{round(time.time() - start, 2)}s"
    }