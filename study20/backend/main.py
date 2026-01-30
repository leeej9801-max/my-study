from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from settings import settings

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
