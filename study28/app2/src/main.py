from fastapi import FastAPI
from src.settings import settings
from kafka import KafkaConsumer
import threading
import asyncio
import redis
import json
from src.logger import log

app = FastAPI(title="Consumer")

client = redis.Redis(
  host=settings.redis_host,
  port=settings.redis_port,
  db=settings.redis_db
)

def consumer():
  cs = KafkaConsumer(
    settings.kafka_topic, 
    bootstrap_servers=settings.kafka_server, 
    enable_auto_commit=True,
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
  )
  log().info(client.get("test"))
  for msg in cs:
    log().info(msg)

@app.on_event("startup")
def startConsumer():
  thread = threading.Thread(target=consumer, daemon=True)
  thread.start()

@app.get("/")
def read_root():
  return {"status": True}
