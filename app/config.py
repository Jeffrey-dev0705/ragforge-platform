from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = 'postgresql://ragforge:ragforge@postgres:5432/ragforge'
    openai_api_key: str | None = None
    embedding_provider: str = 'local'
    chunk_size: int = 700
    chunk_overlap: int = 100
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

@lru_cache
def get_settings(): return Settings()
