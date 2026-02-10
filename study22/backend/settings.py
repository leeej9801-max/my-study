from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  mariadb_user: str
  mariadb_password: str
  mariadb_host: str
  mariadb_database: str
  mariadb_port: int
  react_url: str
  secret_key: str
  algorithm: str
  access_token_expire_minutes: int
  login_sql: str = "select `no`, `name` from edu.user where `email` = '{email}' and `password` = '{pwd}'"

  model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
  )

settings = Settings()
