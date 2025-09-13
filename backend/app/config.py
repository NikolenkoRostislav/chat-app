from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]
    APP_NAME: str = "SimpleChatApp"
    SECURE_COOKIES: bool = False #set to true in production!!!
    TELEGRAM_NOTIFICATIONS: bool = True #set to true if you want to use the telegram notifications bot
    DEBUG: bool = True
    ALGORITHM: str
    DATABASE_URL: str
    SECRET_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()
