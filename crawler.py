import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
import xml.etree.ElementTree as elemTree

tree = elemTree.parse("keys.xml")
MONGO_DB_URL = tree.find('string[@name="MONGO_DB_URL"]').text

client = MongoClient(MONGO_DB_URL, 27017)
db = client.beerdb

# url = "http://www.beerforum.co.kr/index.php?mid=beer_tastingreply"
base_url = "https://www.ratebeer.com"
url = base_url + "/top"
headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"}

# data = requests.get(url, headers=headers)
# soup = BeautifulSoup(data.text, 'html.parser')

# rows = soup.select("#main-content > table > tbody > tr")
# for row in rows:
#     atag = row.select_one("td:nth-child(2) > a")

#     beer = {}
#     beer["name"] = atag.text
#     beer["suburl"] = atag["href"]
#     beer["abv"] = row.select_one("td:nth-child(4)").text.replace("%", "")
#     print(beer)

#     db.beers.insert_one(beer)

