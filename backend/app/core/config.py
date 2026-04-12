from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DATABASE_URL: str
    NEWS_API_KEY: str

    # MT5 bridge (mt5linux socket server running under Wine)
    MT5_HOST: str = "127.0.0.1"
    MT5_PORT: int = 18812

    # MT5 demo account credentials
    MT5_LOGIN: Optional[int] = None
    MT5_PASSWORD: Optional[str] = None
    MT5_SERVER: Optional[str] = None


settings = Settings()
