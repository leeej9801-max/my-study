import os
import mariadb
from dotenv import load_dotenv
load_dotenv()
conn_params = {
  "user" : os.getenv('DB_USER'),
  "password" : os.getenv('DB_PASSWORD'),
  "host" : os.getenv('DB_HOST'),
  "database" : os.getenv('DB_DATABASE'),
  "port" : int(os.getenv('DB_PORT'))
}

def getConn():
  try:
    conn = mariadb.connect(**conn_params)
    if conn == None:
      return None
    return conn
  except mariadb.Error as e:
    print(f"접속 오류 : {e}")
    return None
