from langchain.tools import tool
from settings import settings
from fastapi import APIRouter
from src.core import Query, logger
import httpx
import json

@tool
async def search_movie_info(query: str) -> str:
    """영화 제목을(query)을 입력받아 검색된 영화들의 리스트를 JSON 형식의 문자열로 반환합니다.
    반환 구조: [{'idmbID': ..., 'title': ...,'poster': ...,'year': ...,'type': ...,}, ...]"""

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                settings.movie_api_url,
                params={"s": query, "apikey": settings.movie_api_key},
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()

            if data.get("Response") == "True":
                search_results = data.get("Search", [])
                formatted_data = [
                    {
                        "idmbID": movie.get("imdbID"),
                        "title": movie.get("Title"),
                        "poster": movie.get("Poster"),
                        "year": movie.get("Year"),
                        "type": movie.get("Type")
                    } for movie in search_results 
                ]
                return json.dumps(formatted_data, ensure_ascii=False)
            else:
                return json.dumps({"error": f"'{query}' 영화 검색 결과가 없습니다."}, ensure_ascii=False)

        except httpx.HTTPStatusError as e:
            logger.error(f"API 요청 오류: {e.response.status_code}")
            return json.dumps({"error": "영화 서버 응답 오류가 발생했습니다."}, ensure_ascii=False)
        except Exception as e:
            logger.error(f"예상치 못한 오류: {str(e)}")
            return json.dumps({"error": "네트워크 연결이 원활하지 않습니다."}, ensure_ascii=False)
        
tool = [search_movie_info]