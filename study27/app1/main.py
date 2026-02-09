from fastapi import FastAPI
from kafka import KafkaProducer
from settings import settings
from pydantic import EmailStr, BaseModel
import json

class EmailModel(BaseModel):
  email: EmailStr

app = FastAPI()

pd = KafkaProducer(
  bootstrap_servers=settings.kafka_server,
  value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

@app.get("/")
def root():
  return {"msg": "Producer"}

@app.post("/login")
def producer(model: EmailModel):
  pd.send(settings.kafka_topic, dict(model))
  pd.flush()
  return {"status": True}
