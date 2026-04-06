from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  react_url: str
  kafka_topic: str
  kafka_server: str
  redis_host: str
  redis_port: int
  redis_db1: int
  redis_db2: int
  mail_username: str
  mail_password: str
  mail_from: str
  mail_port: int = 587
  mail_server: str = "smtp.gmail.com"
  mail_from_name: str = "edu"
  mail_starttls: bool = True
  mail_ssl_tls: bool = False
  use_credentials: bool = True
  validate_certs: bool = True

  model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
  )

settings = Settings()
