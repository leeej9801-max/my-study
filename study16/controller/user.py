from fastapi import APIRouter
from configs.db import getConn
import mariadb

router = APIRouter(prefix="/user", tags=["사용자"])

@router.get(
  path="", 
  summary="사용자 목록", 
  description="edu.user 테이블 전체 가져오기")
def user():
  try:
    conn = getConn()
    if conn:
      cur = conn.cursor()
      sql = "SELECT * FROM edu.user"
      cur.execute(sql)
      columns = [desc[0] for desc in cur.description]
      rows = cur.fetchall()
      result = [dict(zip(columns, row)) for row in rows]
      cur.close()
      conn.close()
      return {"status": True, "result": result}
  except mariadb.Error as e:
    print(f"SQL 오류 : {e}")
  return {"status": False}

@router.post(path="")
def user():
  return {"Hello": "World"}

@router.put(path="")
def user():
  return {"Hello": "World"}

@router.delete(path="")
def user():
  return {"Hello": "World"}
