from bs4 import BeautifulSoup as bs
from requests import get

url = "https://www.melon.com/genre/song_list.htm?gnrCode=GN0100&orderBy=POP"

head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'}

res = get(url, headers=head)
print(res)
