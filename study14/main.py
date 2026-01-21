import os
import mariadb
from dotenv import load_dotenv
load_dotenv()

def getConn():
  try:
    return mariadb.connect(
      user=os.getenv('USER'),
      password=os.getenv('PASSWORD'),
      host=os.getenv('HOST'),
      port=int(os.getenv('PORT')),
      database=os.getenv('DATABASE')
    )
  except mariadb.Error as e:
    print(f"MariaDB Error : {e}")
    return None

def findOne(sql):
  result = None
  try:
    conn = getConn()
    if conn:
      cur = conn.cursor()
      cur.execute(sql)
      row = cur.fetchone() 
      columns = [desc[0] for desc in cur.description]
      cur.close()
      conn.close()
      result = dict(zip(columns, row)) if row else None
  except mariadb.Error as e:
    print(f"MariaDB Error : {e}")
  return result
  
def findAll(sql):
  result = []
  try:
    conn = getConn()
    if conn:
      cur = conn.cursor()
      cur.execute(sql)
      rows = cur.fetchall() 
      columns = [desc[0] for desc in cur.description]
      cur.close()
      conn.close()
      result = [dict(zip(columns, row)) for row in rows]
  except mariadb.Error as e:
    print(f"MariaDB Error : {e}")
  return result

def save(sql):
  result = False
  try:
    conn = getConn()
    if conn:
      cur = conn.cursor()
      cur.execute(sql)
      conn.commit()
      cur.close()
      conn.close()
      result = True
  except mariadb.Error as e:
    print(f"MariaDB Error : {e}")
  return result

deptNo1 = "d001"
deptNo2 = "d002"
deptNo3 = "d009"
arr = [deptNo1,deptNo2,deptNo3]
sql = f"""
    SELECT dept_no, COUNT(emp_no) AS cnt 
      FROM edu.dept_emp 
    WHERE dept_no IN { tuple(arr) }
    GROUP BY dept_no
    ORDER BY 2 DESC
    """
# print(sql)
# print( findOne(sql) )
# print( findAll(sql) )

sql1 = "SELECT * FROM edu.test"
print( findAll(sql1) )

name = "둘리"
sql2 = f"""
        INSERT INTO edu.test 
          (`name`, `regDate`) 
        VALUE 
          ('{name}', NOW())
      """
print( save(sql2) )
print( findAll(sql1) )