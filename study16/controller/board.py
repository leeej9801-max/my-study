from fastapi import APIRouter

router = APIRouter(prefix="/board", tags=["게시판"])

@router.get(path="")
def board():
  return {"Hello": "World"}

@router.post(path="")
def board():
  return {"Hello": "World"}

@router.put(path="")
def board():
  return {"Hello": "World"}

@router.delete(path="")
def board():
  return {"Hello": "World"}
