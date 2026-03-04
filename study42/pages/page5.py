import streamlit as st
import trafilatura as tra

st.set_page_config(
	page_title="4. 뉴스기사 요약",
	page_icon="💗",
	layout="wide",
)

st.title("[4] 뉴스기사 요약")

def extract_txt_image(url: str):
	html = tra.fetch_url(url)
	text = tra.extract(html, output_format="markdown", include_comments=False)
	image = tra.extract_metadata(html).image
	return text, image

# 예시 : https://www.koreaherald.com/article/10685727
# 예시 : https://www.koreaherald.com/article/10686698
if url := st.text_input("주소 입력", placeholder="URL을 입력하세요"):
	text, image = extract_txt_image(url)
	message = text
	st.image(image)
	st.markdown(message)
	