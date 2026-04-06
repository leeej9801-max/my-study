from settings import settings
import mariadb
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()

conn_params = {
  "user" : settings.mariadb_user,
  "password" : settings.mariadb_password,
  "host" : settings.mariadb_host,
  "database" : settings.mariadb_database,
  "port" : settings.mariadb_port
}

def etl(year:int, month: int):
  print("db_air 에서 db_to_air 데이터 이관 작업")
  try:
    conn = mariadb.connect(**conn_params)
    if conn:
      where = f"where 년도 = {year} and 월 = {month}"
      sql1 = f"delete from db_to_air.`비행` {where}"
      sql2 = f"insert into db_to_air.`비행` select * from db_air.`비행` {where}"
      sql3 = f"select count(*) as cnt from db_to_air.`비행` {where}"
      print("SQL 실행")
      cur = conn.cursor()
      cur.execute(sql1)
      cur.execute(sql2)
      conn.commit()
      cur.execute(sql3)
      row = cur.fetchone()
      print(f"적재 : {row[0]} 건")
      cur.close()
      conn.close()
  except mariadb.Error as e:
    print(f"접속 오류 : {e}")

def etl2(table: str, year:int = 0, month: int = 0):
  print("db_air 에서 db_to_air 데이터 이관 작업")
  try:
    conn = mariadb.connect(**conn_params)
    if conn:
      where = ""
      if year > 0 and month > 0:
        where = f"where 년도 = {year} and 월 = {month}"
      sql1 = f"delete from db_to_air.`{table}` {where}"
      sql2 = f"insert into db_to_air.`{table}` select * from db_air.`{table}` {where}"
      sql3 = f"select count(*) as cnt from db_to_air.`{table}` {where}"
      print("SQL 실행")
      cur = conn.cursor()
      cur.execute(sql1)
      cur.execute(sql2)
      conn.commit()
      cur.execute(sql3)
      row = cur.fetchone()
      print(f"{table} 적재 : {row[0]} 건")
      cur.close()
      conn.close()
  except mariadb.Error as e:
    print(f"접속 오류 : {e}")

def etl3(data: dict):
  print("db_air 에서 db_to_air 데이터 이관 작업")
  try:
    conn = mariadb.connect(**conn_params)
    if conn:
      no = data["no"]
      year = data["year"]
      month = data["month"]
      table = data["table"]
      where = ""
      if year > 0 and month > 0:
        where = f"where 년도 = {year} and 월 = {month}"
      sql1 = f"delete from db_to_air.`{table}` {where}"
      sql2 = f"insert into db_to_air.`{table}` select * from db_air.`{table}` {where}"
      sql3 = f"select count(*) as cnt from db_to_air.`{table}` {where}"
      print("SQL 실행")
      cur = conn.cursor()
      cur.execute(sql1)
      cur.execute(sql2)
      conn.commit()
      cur.execute(sql3)
      row = cur.fetchone()
      print(f"{table} 적재 : {row[0]} 건")
      sql4 = f"update db_to_air.jobs set `cnt` = {row[0]}, `modDate` = now() where `no` = {no}"
      cur.execute(sql4)
      conn.commit()
      cur.close()
      conn.close()
  except mariadb.Error as e:
    print(f"접속 오류 : {e}")

def jobs(useYn: tuple):
  try:
    conn = mariadb.connect(**conn_params)
    if conn:
      if isinstance(useYn, (list, tuple)):
        keys = ",".join(map(str, useYn))
      else:
        keys = useYn
      sql = f"select `no`, `table`, `year`, `month` from db_to_air.jobs where useYn in ({keys})"
      cur = conn.cursor()
      cur.execute(sql)
      rows = cur.fetchall()
      columns = [desc[0] for desc in cur.description]
      cur.close()
      conn.close()
      result = [dict(zip(columns, row)) for row in rows]
      return result
  except mariadb.Error as e:
    print(f"접속 오류 : {e}")
  return []

@app.post("/run")
def etlRun(useYn: tuple[int,...] = ()):
  for row in jobs(useYn):
    if row: etl3(row)
  return RedirectResponse(url="/list")

@app.post("/list")
def jobList():
  try:
    conn = mariadb.connect(**conn_params)
    if conn:
      sql = f"select * from db_to_air.jobs"
      cur = conn.cursor()
      cur.execute(sql)
      rows = cur.fetchall()
      columns = [desc[0] for desc in cur.description]
      cur.close()
      conn.close()
      result = [dict(zip(columns, row)) for row in rows]
      return {"status": True, "result": result}
  except mariadb.Error as e:
    print(f"접속 오류 : {e}")
  return {"status": False}

@app.post("/set")
def jobSet(type: bool = False, jobNo: list[int] = []):
  try:
    conn = mariadb.connect(**conn_params)
    if conn:
      if isinstance(jobNo, (list, tuple)):
        keys = ",".join(map(str, jobNo))
      else:
        keys = jobNo
      sql = f"update db_to_air.jobs set `useYn` = {type} where `no` in ({keys})"
      cur = conn.cursor()
      cur.execute(sql)
      conn.commit()
      cur.close()
      conn.close()
      return RedirectResponse(url="/list")
  except mariadb.Error as e:
    print(f"접속 오류 : {e}")
  return {"status": False}

#if "__main__" == __name__:
#  useYn = tuple([0])
#  for row in jobs(useYn):
#    if row: etl3(row)
  # etl2("비행", 1987, 10)
  # etl2("운반대")
  # etl2("항공사")
