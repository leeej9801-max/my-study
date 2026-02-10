from fastapi import APIRouter, Request, Response
from settings import settings
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
import redis
import uuid
import urllib.parse
import base64

def base64Decode(data):
  encoded = urllib.parse.unquote(data)
  return base64.b64decode(encoded).decode("utf-8")

router = APIRouter(prefix="/redis", tags=["Redis"])
client = redis.Redis( host="redis", port=6379, db=0 )

@router.get("/set")
def setRedis(value, response: Response):
  try:
    iat = datetime.now(timezone.utc) + (timedelta(hours=7))
    exp = iat + (timedelta(minutes=settings.access_token_expire_minutes))
    data = {
      "iss": "EDU",
      "sub": value,
      "iat": iat,
      "exp": exp
    }
    token = jwt.encode(data, settings.secret_key, algorithm=settings.algorithm)
    id = uuid.uuid4().hex
    keys = f"fastapi:{id}"
    ex = 60 * 60
    client.setex(keys, ex, token)
    response.set_cookie(
      key="data",
      value=keys,
      max_age=ex,
      expires=ex,
      path="/",
      # domain="react",
      secure=True,
      httponly=True,
      samesite="lax",
    )
  except JWTError as e:
    print(f"JWT ERROR : {e}")
  return {"status": True}

@router.get("/get")
def getRedis(request: Request):
  id = request.cookies.get("data")
  result = client.get(id)
  return {"result": result}

@router.get("/del")
def delete(request: Request, response: Response):
  id = request.cookies.get("data")
  client.delete(id)
  response.delete_cookie(key="data")
  return {"status": True}
