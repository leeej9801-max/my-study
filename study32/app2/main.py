from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.settings import settings

origins = [ settings.react_url ]

app = FastAPI(title="Consumer")
app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)
