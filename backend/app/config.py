from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "SimpleChatApp"
    DEBUG: bool = True
    #DATABASE_URL: str
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"

settings = Settings()
