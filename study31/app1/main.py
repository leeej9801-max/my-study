from fastapi import FastAPI
from pathlib import Path
app = FastAPI()

UPLOAD_DIR = Path("uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
MAX_FILE_SIZE = 10 * 1024

def checkDir():
  UPLOAD_DIR.mkdir(exist_ok=True)

@app.get("/")
def root():
  return {"status": True}
