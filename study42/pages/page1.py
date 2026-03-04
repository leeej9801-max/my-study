import streamlit as st
import time
from bs4 import BeautifulSoup as bs
from requests import get
import json
import pandas as pd
from db import saveMany

st.set_page_config(
    page_title="수집 프로젝트",
    page_icon="💗",
    layout="wide",
    # initial_sidebar_state="collapsed"
)

if 'link_index' not in st.session_state:
	st.session_state.link_index = 0

st.markdown("<h1 style='text-align: center;'>수집 목록</h1>", unsafe_allow_html=True)

links = [
  "GN0100",
  "GN0200",
  "GN0300",
  "GN0400",
  "GN0500",
  "GN0600",
  "GN0700",
  "GN0800",
]
options = ("발라드","댄스","랩/힙합","R&B/Soul","인디음악","록/메탈","트로트","포크/블루스")

def getLikes(list, head=None):
  ids = ""
  ids = ",".join(str(item["id"]) for item in list)
  if ids:
    url = f"https://www.melon.com/commonlike/getSongLike.json?contsIds={ids}"
    res = get(url, headers=head)
    if res.status_code == 200:
      data = json.loads(res.text)
      for row in data["contsLike"]:
        for i in range(len(list)):
          if list[i]["id"] == row["CONTSID"]:
            list[i]["cnt"] = row["SUMMCNT"]
            break
  return list

def cleanData(txt):
  list = ["\n", "\xa0", "\r", "\t", "총건수"]
  for target in list:
    txt = txt.replace(target, "")
  txt = txt.replace("'", '"')
  return txt.strip()

def getData(data):
  arr = []
  trs = data.select("#frm tbody > tr")
  if trs:
    for i in range(len(trs)):
      id = int(trs[i].select("td")[0].select_one("input[type='checkbox']").get("value"))
      img = cleanData(trs[i].select("td")[2].select_one("img")["src"])
      title = cleanData(trs[i].select("td")[4].select_one("div[class='ellipsis rank01']").text)
      album = cleanData(trs[i].select("td")[5].select_one("div[class='ellipsis rank03']").text)
      arr.append( {"id": id, "img": img, "title": title, "album": album, "cnt": 0} )
  return arr

def main():
  try:
    st.text("데이터 수집을 시작 합니다.")
    # time.sleep(2)
    # url = links[st.session_state.link_index]
    code = links[st.session_state.link_index]
    url = f"https://www.melon.com/genre/song_list.htm?gnrCode={code}&orderBy=POP"
    head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'}
    st.text(url)
    res = get(url, headers=head)
    if res.status_code == 200:
      # st.html(res.text)
      data = bs(res.text)
      arr = getData(data)
      arr = getLikes(arr, head)
      # df = pd.DataFrame(arr)
      # st.dataframe(df.head(5))
      if len(arr) > 0:
        sql1 = f"DELETE FROM edu.`melon` WHERE `code` = '{code}'"
        sql2 = f"""
            INSERT INTO edu.`melon` 
            (`code`, `id`, `img`, `title`, `album`, `cnt`)
            VALUE
            (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
              id=VALUES(id),
              img=VALUES(img),
              title=VALUES(title),
              album=VALUES(album),
              cnt=VALUES(cnt)
        """
        values = [(code, row["id"], row["img"], row["title"], row["album"], row["cnt"]) for row in arr]
        saveMany(sql1, sql2, values)
    st.text("데이터 수집이 완료 되었습니다.")
  except Exception as e:
    return 0
  return 1

selected = st.selectbox(
  label="음원 장르를 선택하세요",
  options=options,
  index=None,
  placeholder="수집 대상을 선택하세요."
)

if selected:
  st.write("선택한 장르 :", selected)
  st.session_state.link_index = options.index(selected)
  if st.button(f"'{options[st.session_state.link_index]}' 수집"):
    if main() == 0:
      st.text("수집된 데이터가 없습니다.")