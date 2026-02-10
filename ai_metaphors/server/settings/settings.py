from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Metaphors"

    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "postgres"

    # Storage configuration
    BUCKET_NAME: str = "ai-metaphors-videos"
    KEY_JSON: str = "key.json"
    URL_EXPIRATION: int = 604800 # 604800 sec = 24 h * 7 = 1 week

    API_KEYS: str

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def VALID_API_KEYS(self) -> list[str]:
        return self.API_KEYS.splitlines()

settings = Settings()