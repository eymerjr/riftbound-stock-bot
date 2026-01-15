import requests
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook
import time

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1461503471843934372/EKiVTmee9-VPm2v5eGhXWf2rGP5nFsp2MvOIixPRLsYbneYTj0XdH4sjabtB3yjygivU"

PRODUCTS = {
    "Riftbound Spiritforge Booster Display Box": "https://merch.riotgames.com/en-us/product/riftbound-spiritforged-booster-display/",
    "Riftbound Booster Display Box": "https://merch.riotgames.com/en-us/product/riftbound-origins-booster-display/"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

already_notified = {name: False for name in PRODUCTS}

def is_purchasable(html):
    soup = BeautifulSoup(html, "html.parser")
    btn = soup.find("button", {"type": "submit"})
    if not btn:
        return False
    text = btn.get_text(strip=True).lower()
    return "add to cart" in text and not btn.has_attr("disabled")

while True:
    for name, url in PRODUCTS.items():
        try:
            r = requests.get(url, headers=HEADERS, timeout=10)
            if r.status_code == 200:
                purchasable = is_purchasable(r.text)

                if purchasable and not already_notified[name]:
                    DiscordWebhook(
                        url=DISCORD_WEBHOOK_URL,
                        content=f"🟢 {name} is AVAILABLE NOW!\n👉 {url}"
                    ).execute()
                    already_notified[name] = True

                if not purchasable:
                    already_notified[name] = False

        except Exception as e:
            print("Error:", e)

    time.sleep(300)  # 5 minutes
