from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

origins = [
  "http://localhost:5173"
]

class LoginModel(BaseModel):
  email: str
  pwd: str

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
  response.set_cookie(
    key="user",
    value=loginModel.email,
    max_age=60 * 60,        # 1시간 (초)
    expires=60 * 60,        # max_age와 유사 (초)
    path="/",
    domain="localhost",
    secure=True,            # HTTPS에서만 전송
    httponly=True,          # JS 접근 차단 (⭐ 보안 중요)
    samesite="lax",         # 'lax' | 'strict' | 'none'
  )
  return {"status": True, "model": loginModel}

@app.get("/user")
def user(request: Request):
  email = request.cookies.get("user")
  if email:
    return {"status": True, "me": email}
  else:
    return {"status": False}
