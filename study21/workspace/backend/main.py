from fastapi import FastAPI, Request, Response
import redis
import uuid
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

# docker run -d -p 6379:6379 --name redis redis:8.4.0
# docker exec -it redis redis-cli

SECRET_KEY = "your-extremely-secure-random-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

client = redis.Redis(
    host="localhost",
    port=6379,
    db=0
  )
print(type(client))

@app.get("/set")
def setRedis(value, response: Response):
  try:
    iat = datetime.now(timezone.utc) + (timedelta(hours=7))
    exp = iat + (timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    data = {
      "iss": "EDU", 
      "sub": value, 
      "iat": iat,
      "exp": exp
    }
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    id = uuid.uuid4().hex
    keys = f"fastapi:{id}"
    client.setex(keys, 60*60*24, token)
    response.set_cookie(
      key="data",
      value=keys,
      max_age=60 * 60,
      expires=60 * 60,
      path="/",
      domain="localhost",
      secure=True,
      httponly=True,
      samesite="lax",
    )
  except JWTError as e:
    print(f"JWT ERROR : {e}")
  return {"status": True}

@app.get("/get")
def getRedis(request: Request):
  id = request.cookies.get("data")
  result = client.get(id)
  return {"result": result}

@app.get("/del")
def delete(request: Request, response: Response):
  id = request.cookies.get("data")
  client.delete(id)
  response.delete_cookie(key="data")
  return {"status": True}

@app.get("/")
def read_root():
  return {"Hello": "World"}
