import logging
import httpx
import json
import re
from langchain.tools import tool
from pydantic import BaseModel, Field
from settings import settings
from contextlib import asynccontextmanager
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from fastapi import FastAPI, Request
from psycopg.rows import dict_row
import psycopg

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Query(BaseModel):
    input: str

class MovieItem(BaseModel):
    imdbID: str = Field(description="영화 고유 ID (tt로 시작)") 
    title: str = Field(description="제목")
    poster: str = Field(description="포스터 이미지 URL")
    year: str = Field(description="개봉 년도")
    type: str = Field(default="movie", description="유형")
    director: str = Field(default="N/A", description="감독")
    actors: str = Field(default="N/A", description="출연 배우")
    plot: str = Field(default="N/A", description="상세 줄거리")

class MovieListResponse(BaseModel):
    movies: list[MovieItem] = Field(description="검색된 영화 리스트 또는 상세 정보")
    count: int = Field(description="데이터 개수")

# --- 도구 정의 (Tools) ---

@tool
async def search_movie_list(query: str) -> str:
    """
    영화 제목을 검색하여 결과 리스트를 반환하는 도구
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                settings.movie_api_url,
                params={"s": query, "apikey": settings.movie_api_key},
                timeout=10.0
            )
            data = response.json()
            if data.get("Response") == "True":
                return json.dumps(data.get("Search", []), ensure_ascii=False)
            return json.dumps([], ensure_ascii=False)
        except Exception as e:
            logger.error(f"목록 검색 중 오류: {e}")
            return "[]"

@tool
async def get_movie_detail(imdb_id: str) -> str:
    """
    영화 상세 정보를 반환하는 도구
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                settings.movie_api_url,
                params={"i": imdb_id, "apikey": settings.movie_api_key, "plot": "full"},
                timeout=10.0
            )
            data = response.json()
            if data.get("Response") == "True":
                detail = {
                    "imdbID": data.get("imdbID"),
                    "title": data.get("Title"),
                    "year": data.get("Year"),
                    "poster": data.get("Poster"),
                    "director": data.get("Director"),
                    "actors": data.get("Actors"),
                    "plot": data.get("Plot"),
                    "type": data.get("Type")
                }
                return json.dumps(detail, ensure_ascii=False)
            return json.dumps({"error": "상세 정보를 찾을 수 없습니다."}, ensure_ascii=False)
        except Exception as e:
            logger.error(f"상세 조회 중 오류: {e}")
            return json.dumps({"error": str(e)}, ensure_ascii=False)

@tool
async def save_movie_db(imdb_id: str) -> str:
    """
    영화 상세 정보를 db에 저장하는 도구
    """
    try:
        # 1. API 호출 (이 부분은 기존 httpx 비동기를 유지해도 문제없습니다)
        async with httpx.AsyncClient() as client:
            response = await client.get(
                settings.movie_api_url,
                params={"i": imdb_id, "apikey": settings.movie_api_key, "plot": "full"}
            )
            data = response.json()
            
        if data.get("Response") != "True":
            return json.dumps({"status": "error", "message": "영화를 찾을 수 없습니다."})

        # 2. PostgreSQL 연결 및 데이터 저장
        db_info = "dbname=esg_platform user=postgres password=esg1234 host=localhost port=5432"
        
        with psycopg.connect(db_info) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO movies (imdb_id, title, year, director, actors, plot, poster)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (imdb_id) DO UPDATE SET
                        title = EXCLUDED.title,
                        plot = EXCLUDED.plot;
                    """,
                    (
                        data.get("imdbID"), data.get("Title"), data.get("Year"),
                        data.get("Director"), data.get("Actors"), data.get("Plot"), data.get("Poster")
                    )
                )
                conn.commit() 

        return json.dumps({
            "status": "success", 
            "message": f"'{data.get('Title')}' 영화 정보가 PostgreSQL에 저장되었습니다."
        }, ensure_ascii=False)

    except Exception as e:
        logger.error(f"Postgres 저장 오류 (동기): {str(e)}")
        return json.dumps({"status": "error", "message": f"DB 저장 실패: {str(e)}"}, ensure_ascii=False)

movie_tools = [search_movie_list, get_movie_detail, save_movie_db]

# --- 유틸리티 함수 ---

def extract_json(text: str) -> dict:
    """텍스트에서 JSON 부분만 추출합니다."""
    match = re.search(r"(\{.*\})", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except:
            pass
    return json.loads(text)

def get_app_state(request: Request):
    """FastAPI의 app.state에 접근하기 위한 의존성 주입용 함수"""
    return request.app.state

# --- 에이전트 초기화 (Lifespan) ---

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        llm = ChatOllama(
            model=settings.ollama_model_name, 
            base_url=settings.ollama_base_url, 
            temperature=0
        )    
        schema = MovieListResponse.model_json_schema()
        system_message = (
            "당신은 영화 정보 전문가입니다.\n"
            "1. 목록 검색: 'search_movie_list'\n"
            "2. 상세 정보: 'get_movie_detail'\n"
            "3. DB 저장: 'save_movie_db'를 사용하세요.\n"
            "결과를 출력할 때는 '알겠습니다'나 '저장했습니다' 같은 설명은 절대 하지 마세요.\n" # 수다 방지 지시
            "반드시 지정된 JSON 스키마를 따르는 순수한 JSON 객체만 딱 하나 출력하세요.\n"
            f"응답 스키마: {schema}"
        )
        app.state.agent_executor = create_react_agent(llm, movie_tools, prompt=system_message)
        
        logger.info("영화 에이전트 공장이 가동되었습니다!")
        yield
    except Exception as e:
        logger.error(f"공장 초기화 중 에러 발생: {e}")
    finally:
        logger.info("공장 가동을 중단합니다.")