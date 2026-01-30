from fastapi import FastAPI, Header, Depends, Request, Response, Cookie
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from settings import settings
from db import findOne, findAll, save
import mariadb
import uuid

SECRET_KEY = "your-extremely-secure-random-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def set_token(no: int, name: str):
  try:
    iat = datetime.now(timezone.utc) + (timedelta(hours=7))
    exp = iat + (timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    data = {
      "name": name,
      "iss": "EDU", 
      "sub": str(no), 
      "iat": iat,
      "exp": exp
    }
    id = uuid.uuid4().hex
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    sql = f"INSERT INTO edu.`login` (`id`, `userNo`, `token`) VALUE ('{id}', {no}, '{token}')"
    if save(sql): return id
  except JWTError as e:
    print(f"JWT ERROR : {e}")
  return None

def get_user(user: str = Cookie(None)):
  if user:
    sql = f"select * from edu.`login` where `id` = '{user}'"
    result = findOne(sql)
    if result:
      return jwt.decode(result["token"], SECRET_KEY, algorithms=ALGORITHM)
  return None

origins = [ settings.react_url ]

class LoginModel(BaseModel):
  email: str = Field(..., title="이메일 주소", description="로그인를 위한 이메일 주소 입니다.")
  pwd: str = Field(..., title="비밀번호", description="로그인를 위한 비밀번호 입니다.")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
  return {"status": True, "msg": "공유해 드림"}

@app.post("/login")
def login(model : LoginModel, response : Response):
  sql = settings.login_sql.replace("{email}", model.email).replace("{pwd}", model.pwd)
  data = findOne(sql)
  if data:
    access_token = set_token(data["no"], data["name"])
    print(access_token)
    response.set_cookie(
        key="user",
        value=access_token,
        max_age=60 * 60,        # 1시간 (초)
        expires=60 * 60,        # max_age와 유사 (초)
        path="/",
        domain="localhost",
        secure=True,            # HTTPS에서만 전송
        httponly=True,          # JS 접근 차단 (⭐ 보안 중요)
        samesite="lax",         # 'lax' | 'strict' | 'none'
      )
    return {"status": True}
  else:
    return {"status": False}

@app.get("/me")
def me(payload = Depends(get_user)):
  if payload:
    return {"status": True, "me": payload["name"]}
  else:
    return {"status": False}

@app.post("/logout")
def logout(response: Response):
  response.delete_cookie(key="user")
  return {"status": True}
