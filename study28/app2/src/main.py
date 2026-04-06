from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from src.settings import settings
from kafka import KafkaConsumer
import threading
import asyncio
import redis
import json
import random
import string
from src.logger import log

origins = [ settings.react_url, settings.fastapi1_url ]

app = FastAPI(title="Consumer")
app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

conf = ConnectionConfig(
  MAIL_USERNAME = settings.mail_username,
  MAIL_PASSWORD = settings.mail_password,
  MAIL_FROM = settings.mail_from,
  MAIL_PORT = settings.mail_port,
  MAIL_SERVER = settings.mail_server,
  MAIL_FROM_NAME = settings.mail_from_name,
  MAIL_STARTTLS = settings.mail_starttls,
  MAIL_SSL_TLS = settings.mail_ssl_tls,
  USE_CREDENTIALS = settings.use_credentials,
  VALIDATE_CERTS = settings.validate_certs
)

client = redis.Redis(
  host=settings.redis_host,
  port=settings.redis_port,
  db=settings.redis_db
)

async def simple_send(email: str):
  id = ''.join(random.choices(string.digits, k=6))
  client.setex(id, 60*3, email)
  html = f"""
    <h1>Login Service</h1>
    <p>{id}</p>
  """

  message = MessageSchema(
    subject="일회용 인증 코드 발급",
    recipients=[ email ],
    body=html,
    subtype=MessageType.html)

  fm = FastMail(conf)
  await fm.send_message(message)

def consumer():
  cs = KafkaConsumer(
    settings.kafka_topic, 
    bootstrap_servers=settings.kafka_server, 
    enable_auto_commit=True,
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
  )
  for msg in cs:
    log().info(msg)
    asyncio.run(simple_send(msg.value["email"]))

@app.on_event("startup")
def startConsumer():
  thread = threading.Thread(target=consumer, daemon=True)
  thread.start()

@app.get("/")
def read_root():
  return {"status": True}
