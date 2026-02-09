from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  react_url: str
  kafka_topic: str
  kafka_server: str
  redis_host: str
  redis_port: int
  redis_db: int

  model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
  )

settings = Settings()
