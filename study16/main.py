from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
from controller import root, user, board

def urls():
  return [root.router, user.router, board.router]

app = FastAPI()

static_dir = os.path.join(os.path.dirname(__file__), "update")
app.mount("/update", StaticFiles(directory=static_dir), name="update")

apis = urls()
for r in apis:
  app.include_router(r)
