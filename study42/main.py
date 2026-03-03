import streamlit as st
import time

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
  "https://www.melon.com/genre/song_list.htm?gnrCode=GN0100&orderBy=POP",
  "https://www.melon.com/genre/song_list.htm?gnrCode=GN0200&orderBy=POP",
  "https://www.melon.com/genre/song_list.htm?gnrCode=GN0300&orderBy=POP",
  "https://www.melon.com/genre/song_list.htm?gnrCode=GN0400&orderBy=POP",
  "https://www.melon.com/genre/song_list.htm?gnrCode=GN0500&orderBy=POP",
  "https://www.melon.com/genre/song_list.htm?gnrCode=GN0600&orderBy=POP",
  "https://www.melon.com/genre/song_list.htm?gnrCode=GN0700&orderBy=POP",
  "https://www.melon.com/genre/song_list.htm?gnrCode=GN0800&orderBy=POP",
]
options = ("발라드","댄스","랩/힙합","R&B/Soul","인디음악","록/메탈","트로트","포크/블루스")

def main():
  try:
    st.text("데이터 수집을 시작 합니다.")
    time.sleep(2)
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