from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_URL: str = "sqlite:///./study_planner.db"
    API_PREFIX: str = "/api/v1"
    # читаем .env и игнорируем лишние переменные окружения
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
