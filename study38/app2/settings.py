from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  title: str ="FastAPI App2"
  root_path: str
  client_id: str
  client_secret: str

  model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
  )

settings = Settings()
