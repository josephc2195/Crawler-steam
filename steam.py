import requests
from bs4 import BeautifulSoup as soup
import json
import sys

resp = requests.get("https://store.steampowered.com").content
page = soup(resp, 'lxml')

containers = page.findAll("a", {"class": "store_capsule"})
obj = []

for i, cop in enumerate(containers):
    id_to_find = cop["data-ds-appid"]
    title = page.find("div", {"id": f"hover_app_{id_to_find}"}).find("h4").text if page.find("div", {"id": f"hover_app_{id_to_find}"}) != None else id_to_find
    if cop.find("div", {"class": "discount_pct"}):
        price_bd = cop.find("div", {"class": "discount_original_price"}).text.strip() if cop.find("div", {"class": "discount_original_price"}) else ""
        price_ad = cop.find("div", {"class": "discount_final_price"}).text.strip() if cop.find("div", {"class": "discount_final_price"}) else ""
        promo_pct = cop.find("div", {"class": "discount_pct"}).text.strip() if cop.find("div", {"class": "discount_pct"}) else ""
    else:
        price_bd = cop.find("div", {"class": "discount_original_price"}).text.strip() if cop.find("div", {"class": "discount_original_price"}) else ""
        price_ad = price_bd
        promo_pct = "0%"
    img = cop.find("img")["src"]
    time_left = cop.find("dailydeal_desc").text if cop.find("dailydeal_desc") else "NA"
    id_name = "".join(title.split(" "))
    obj.append({"id": f"{i}", f"{id_name}" : {"title": f"{title}", "price before deal": f"{price_bd}", "price after deal": f"{price_ad}",  "promo": f"{promo_pct}", "time left": f"{time_left}" }})

data = {"Products": []}
for i in obj:
    data["Products"].append(i)

with open ("new.text", "w") as pipe:
    json.dump(data, pipe)
