from fastapi import APIRouter, HTTPException, Depends
from src.core import get_app_state, Query, logger, extract_json, MovieListResponse

router = APIRouter(
    prefix="/step05",
    tags=["자유 실습 - 영화 상세 에이전트"],
)

@router.post("/chat")
async def chat(query: Query, state=Depends(get_app_state)):
    try:
        # core 공장에서 미리 만들어둔 에이전트를 가져옵니다.
        agent = state.agent_executor 
        
        inputs = {"messages": [{"role": "user", "content": query.input}]}
        result = await agent.ainvoke(inputs)
        
        raw_content = result["messages"][-1].content
        json_data = extract_json(raw_content)
        
        return json_data
        
    except Exception as e:
        logger.error(f"실행 중 에러: {str(e)}")
        raise HTTPException(status_code=500, detail=f"에이전트 오류: {str(e)}")