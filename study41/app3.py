from bs4 import BeautifulSoup as bs
from requests import get
import json

url = "https://www.melon.com/genre/song_list.htm?gnrCode=GN0100&orderBy=POP"
url2 = "https://www.melon.com/commonlike/getSongLike.json?contsIds=600287375%2C33241003%2C600299706%2C38733032%2C38429074%2C32061975%2C1121123%2C4446485%2C600359330%2C38104031%2C37228861%2C38123338%2C34752757%2C30962526%2C36699489%2C37390939%2C601273260%2C38635449%2C37145732%2C34657844%2C37375706%2C34061322%2C33496587%2C600493407%2C30877002%2C39051429%2C39430660%2C36382580%2C34451383%2C39721328%2C37023625%2C38583620%2C600668850%2C37069064%2C600906246%2C34360855%2C600035196%2C4352438%2C34908740%2C600791038%2C35008524%2C39765727%2C601379618%2C33411344%2C600447153%2C39765728%2C31742666%2C33855085%2C418168%2C601358454"

head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'}

res = get(url, headers=head)
res2 = get(url2, headers=head)

ids = []
titles = []
imgs = []
albums = []
likes = []
cnts = []

if res2.status_code == 200:
  jData = json.loads(res2.text)
  for row in jData["contsLike"]:
    cnts.append({"CONTSID": row["CONTSID"], "SUMMCNT": row["SUMMCNT"]})

if res.status_code == 200:
  data = bs(res.text)
  title = data.title.text
  trs = data.select("#frm tbody > tr")
   
  for i in range(len(trs)):
    imgs.append(trs[i].select("td")[2].select_one("img")["src"])
    titles.append(trs[i].select("td")[4].select_one("div[class='ellipsis rank01']").text.replace("\n", "").replace("\xa0", " ").strip())
    albums.append(trs[i].select("td")[5].select_one("div[class='ellipsis rank03']").text.replace("\xa0", " ").strip())
    #likes.append(trs[i].select("td")[6].select_one("span[class='cnt']").text.replace("\n", "").replace("\r", "").replace("\t", "").replace("총건수", "").strip())
    ids.append(int(trs[i].select("td")[0].select_one("input[type='checkbox']").get("value")))

  for id in ids:
    for row in cnts:
      if id == row["CONTSID"]:
        likes.append(row["SUMMCNT"])

print(imgs)
print(titles)
print(albums)
print(likes)
