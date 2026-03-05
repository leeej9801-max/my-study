from bs4 import BeautifulSoup as bs
from requests import get
import pandas as pd
import streamlit as st
import json

st.set_page_config(
  page_title="yes24 수집",
  page_icon="💗",
  layout="wide",
)

# Yes24 베스트셀러 URL 예시
yes24 = "https://www.yes24.com/product/category/weekbestseller"
categoryNumber = "001"
pageNumber = 1
pageSize = 40
type = "week"
saleYear = 2026
weekNo = 1149
sex = "A"
viewMode = "thumb"

url = (
  f"{yes24}?"
  f"categoryNumber={categoryNumber}&"
  f"pageNumber={pageNumber}&"
  f"pageSize={pageSize}&"
  f"type={type}&"
  f"saleYear={saleYear}&"
  f"weekNo={weekNo}&"
  f"sex={sex}&"
  f"viewMode={viewMode}"
)

# 데이터 수집
def getData():
  try:
    url = ""
    st.text(f"URL: {url}")
    res = get(url)
    if res.status_code == 200:
      st.text("yes24 국내도서 주별 베스트 수집 시작!")
      books = [] # { 도서명, 저자, 별점 }
      tab1, tab2, tab3 = st.tabs(["HTML 데이터", "JSON 데이터", "DataFrame"])
      with tab1:
        st.text("html 출력")
      with tab2:
        st.text("JSON 출력")
      with tab3:
        st.text("DataFrame 출력")
  except Exception as e:
    return 0
  return 1

if st.button(f"수집하기"):
  getData()