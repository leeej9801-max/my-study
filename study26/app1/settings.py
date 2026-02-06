from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  kafka_topic: str = "test"
  kafka_server: str = "localhost:9092"

  model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
  )

settings = Settings()
