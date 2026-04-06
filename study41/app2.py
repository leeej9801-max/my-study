from bs4 import BeautifulSoup
import requests

url = 'http://127.0.0.1/study41/index.html'
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

lis = soup.find_all("li")

for li in lis:
  print( li.find("a").text )