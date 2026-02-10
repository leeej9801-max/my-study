from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.settings import settings
from kafka import KafkaProducer
import redis
import json
from src.logger import log
from pydantic import EmailStr, BaseModel

origins = [ settings.react_url ]

app = FastAPI(title="Producer")
app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

pd = KafkaProducer(
  bootstrap_servers=settings.kafka_server,
  value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

client = redis.Redis(
  host=settings.redis_host,
  port=settings.redis_port,
  db=settings.redis_db,
  decode_responses=True
)

class EmailModel(BaseModel):
  email: EmailStr

class CodeModel(BaseModel):
  id: str

@app.get("/")
def read_root():
  data = {"email": "test@test.com"}
  log().info(data["email"])
  client.setex("test", 60*3, data["email"])
  pd.send(settings.kafka_topic, data)
  pd.flush()
  return {"status": True}

@app.post("/login")
def producer(model: EmailModel):
  pd.send(settings.kafka_topic, dict(model))
  pd.flush()
  return {"status": True}
