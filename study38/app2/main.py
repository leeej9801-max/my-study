from fastapi import FastAPI, Request
from settings import settings
from authlib.integrations.starlette_client import OAuth
from starlette.middleware.sessions import SessionMiddleware

oauth = OAuth()
oauth.register(
  name='kakao',
  client_id=settings.client_id,
  client_secret=settings.client_secret,
  authorize_url="https://kauth.kakao.com/oauth/authorize",
  access_token_url="https://kauth.kakao.com/oauth/token",
  api_base_url="https://kapi.kakao.com",
  client_kwargs={"scope": "profile_nickname profile_image"}
)
app = FastAPI(title=settings.title, root_path=settings.root_path)
app.add_middleware(
  SessionMiddleware,
  secret_key="your-secret-key-here"
)

@app.get("/")
def read_root():
  return {"service": "App2"}

@app.get("/login/kakao")
async def kakaoLogin(request: Request):
  redirect_uri = "http://localhost:8000/app1/oauth/callback/kakao"
  return await oauth.kakao.authorize_redirect(request, redirect_uri)

@app.get("/oauth/callback/kakao")
async def kakaoCallback(code: str):
  return {"code": code}
