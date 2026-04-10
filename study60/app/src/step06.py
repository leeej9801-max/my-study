from fastapi import APIRouter, HTTPException, Depends
from src.core import get_app_state, Query, logger, extract_json, MovieListResponse

router = APIRouter(
    prefix="/step06",
    tags=["실습 06 - 영화 정보 DB 수집 에이전트"],
)

@router.post("/collect")
async def collect_movie(query: Query, state=Depends(get_app_state)):
    try:
        agent = state.agent_executor 
        enforced_query = f"{query.input} (이 영화를 찾아서 상세 정보를 출력하고, 반드시 DB에 저장까지 완료해줘)"

        inputs = {"messages": [{"role": "user", "content": enforced_query}]}
        result = await agent.ainvoke(inputs)
        
        raw_content = result["messages"][-1].content
        return extract_json(raw_content)
        
    except Exception as e:
        logger.error(f"Step06 수집 프로세스 에러: {str(e)}")
        raise HTTPException(status_code=500, detail=f"수집 실패: {str(e)}")