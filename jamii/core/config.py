from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    postgres_user: str
    postgres_password: str
    postgres_db: str
    jwt_secret_key: str
    jwt_algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings()