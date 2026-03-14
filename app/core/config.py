from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Organizations Catalog API"
    API_V1_PREFIX: str = "/api/v1"
    API_KEY: str = "super-secret-key"
    DATABASE_URL: str = "postgresql+psycopg://postgres:postgres@db:5432/org_catalog"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()