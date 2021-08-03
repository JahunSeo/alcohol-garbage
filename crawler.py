import requests
from bs4 import BeautifulSoup

url = "http://www.beerforum.co.kr/index.php?mid=beer_tastingreply"
headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"}
data = requests.get(url, headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

print(soup)
