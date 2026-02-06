from fastapi import FastAPI
from kafka import KafkaProducer
from settings import settings

app = FastAPI()

pd = KafkaProducer(bootstrap_servers=settings.kafka_server)

@app.get("/")
def root():
  return {"msg": "Producer"}

@app.post("/pd")
def producer(msg: str):
  pd.send(settings.kafka_topic, msg.encode("utf-8"))
  pd.flush()
  return {"status": True}
