from fastapi import FastAPI
from settings import settings

app = FastAPI(title=settings.title, root_path=settings.root_path)

@app.get("/")
def read_root():
  return {"service": "App3"}
