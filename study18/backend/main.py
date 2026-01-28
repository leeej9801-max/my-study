from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
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
app.add_middleware(
    SessionMiddleware, 
    secret_key="your-long-random-secret-key",
    # Optional parameters:
    same_site="none",
    https_only=False,
    max_age=3600, # (1 hour)
)

@app.get("/")
def read_root():
  return {"status": True, "result": ["공유는 해드림"]}

@app.post("/login")
def login(loginModel: LoginModel, request: Request):
  request.session["email"] = loginModel.email
  return {"status": True, "model": loginModel}

@app.get("/user")
def user(request: Request):
  email = request.session.get("email")
  if email:
    return {"status": True, "me": email}
  else:
    return {"status": False}
