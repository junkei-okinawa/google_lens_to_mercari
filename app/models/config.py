from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SERP_API_KEY: str
    GEMINI_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
