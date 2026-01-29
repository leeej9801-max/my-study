from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from db import findOne, findAll, save
import mariadb
from settings import settings

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
  return {"status": True, "result": ["공유는 해드림"]}

@app.post("/login")
def login(loginModel: LoginModel, response: Response):
  msg = "잘못된 정보 입니다."
  try:
    sql = f"""
      select * from edu.user 
       WHERE `delYn` = 0 
         AND `email` = '{loginModel.email}' 
         AND `password` = '{loginModel.pwd}'
    """
    data = findOne(sql)
    if data:
      response.set_cookie(
        key="user",
        value=data["no"],
        max_age=60 * 60,        # 1시간 (초)
        expires=60 * 60,        # max_age와 유사 (초)
        path="/",
        domain="localhost",
        secure=True,            # HTTPS에서만 전송
        httponly=True,          # JS 접근 차단 (⭐ 보안 중요)
        samesite="lax",         # 'lax' | 'strict' | 'none'
      )
      return {"status": True}
  except mariadb.Error as e:
    print(f"SQL 오류 : {e}")
  return {"status": False, "message": msg}

@app.post("/logout")
def logout(response: Response):
  response.delete_cookie(key="user")
  return {"status": True}

@app.get("/user")
def user(request: Request):
  email = request.cookies.get("user")
  if email:
    return {"status": True, "me": email}
  else:
    return {"status": False}
