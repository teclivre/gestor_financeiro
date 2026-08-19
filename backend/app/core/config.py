from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Gestor Financeiro Pessoal"
    env: str = "development"
    database_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/gestor_financeiro"
    secret_key: str = "troque-por-uma-chave-forte-e-aleatoria"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24
    google_client_id: str | None = None
    google_issuer: str = "https://accounts.google.com"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
