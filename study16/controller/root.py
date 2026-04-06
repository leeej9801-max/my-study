from fastapi import APIRouter
from configs.db import getConn
import mariadb

router = APIRouter(prefix="/root", tags=["기본"])

@router.get(path="")
def root():
  try:
    conn = getConn()
    if conn:
      cur = conn.cursor()
      sql = "select 1 as no"
      cur.execute(sql)
      columns = [desc[0] for desc in cur.description]
      row = cur.fetchone()
      result = dict(zip(columns, row)) if row else None
      cur.close()
      conn.close()
      return {"status": True, "result": result}
  except mariadb.Error as e:
    print(f"SQL 오류 : {e}")
  return {"status": False}
