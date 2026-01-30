from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from settings import settings
import urllib.parse
import base64

def base64Decode(data):
  encoded = urllib.parse.unquote(data)
  return base64.b64decode(encoded).decode("utf-8")

origins = [ settings.react_url ]

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
  return { "status": True }

@app.post("/board")
def board(request: Request):
  boardNo = request.cookies.get("boardNo")
  print(boardNo, base64Decode(boardNo))
  boardNo = int(base64Decode(boardNo))
  return {"boardNo": boardNo}
