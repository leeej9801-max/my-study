import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(
	page_title="2. 암환자수 통계",
	page_icon="💗",
	layout="wide",
)

url = "https://www.index.go.kr/unity/potal/eNara/sub/showStblGams3.do?stts_cd=277002&idx_cd=2770&freq=Y&period=N"

