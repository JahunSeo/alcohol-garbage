import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
import xml.etree.ElementTree as elemTree

tree = elemTree.parse("keys.xml")
MONGO_DB_URL = tree.find('string[@name="MONGO_DB_URL"]').text
# MONGO_DB_URL = "localhost"

client = MongoClient(MONGO_DB_URL, 27017)
db = client.beerdb

url = "http://www.beerforum.co.kr/index.php?mid=beer_tastingreply"
headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"}


data = requests.get(url, headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')


rows = soup.select("tbody > tr")
print(len(rows))
for row in rows:
    beer = {}
    atag = row.select_one("td:nth-child(1) > a")
    names = atag.text.split("/")
    beer["original_name"] = names[0].strip()
    beer["name"] = names[1].strip()

    # 링크
    beer["url"] = atag["href"]
    print(beer["url"])
    subdata = requests.get(beer["url"], headers=headers)
    subsoup = BeautifulSoup(subdata.text, 'html.parser')
    table = subsoup.select_one("div.boardRead")
    table = table.select_one("table table")

    abv = table.select_one("tr:nth-child(2) > td > span").text
    beer["abv"] = float(abv.split("%")[0])
    manufacturer = table.select_one("tr:nth-child(3) > td > span").text
    beer["manufacturer"] = manufacturer.replace("\xa0", "")
    country = table.select_one("tr:nth-child(4) > td > span").text
    beer["country"] = country.replace("\xa0", "")
    image = subsoup.select_one("table img")
    beer["image"] = image["src"]
    print(beer)
    db.beers.insert_one(beer)
