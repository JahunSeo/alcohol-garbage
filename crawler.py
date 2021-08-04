import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
import xml.etree.ElementTree as elemTree

tree = elemTree.parse("keys.xml")
MONGO_DB_URL = tree.find('string[@name="MONGO_DB_URL"]').text

client = MongoClient(MONGO_DB_URL, 27017)
db = client.beerdb

# url = "http://www.beerforum.co.kr/index.php?mid=beer_tastingreply"
base_url = "https://www.beeradvocate.com/beer"
url = base_url + "/top-rated"
headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"}


data = requests.get(url, headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

rows = soup.select("#ba-content > table > tbody > tr")
print(len(rows))
rows = rows[1:]
for row in rows:
    atag = row.select_one("td:nth-child(2) > a > b")


    beer = {}
    beer["name"] = atag.text
    beer["suburl"] = atag["href"]
    beer["manufacturer"] = row.select_one("td:nth-child(2) > span > a:nth-child(2)").text
    abv = row.select_one("td:nth-child(4)").text.replace("%", "")

    print(row.select_one("td:nth-child(2) > span").text)
    beer["abv"] = float(abv)
    print(beer)

    break

    # db.beers.insert_one(beer)


# beers = db.beers.find({}, {"_id": False})
# beers = list(beers)
# for beer in beers:
#     url = base_url + beer["suburl"]
#     data = requests.get(url, headers=headers)
#     soup = BeautifulSoup(data.text, 'html.parser')
#     print(url)

#     imgtag = soup.select_one("img")
#     image = imgtag["src"]
#     print(image)
#     result = db.beers.update_one({"name": beer["name"]}, {"$set": {"image": image}})
#     break
