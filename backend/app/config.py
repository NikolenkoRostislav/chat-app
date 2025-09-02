from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]
    APP_NAME: str = "SimpleChatApp"
    SECURE_COOKIES: bool = False #set to true in production!!!
    DEBUG: bool = True
    USE_TG_NOTIFS: bool = True #set to true if you want to send users notifications via telegram
    ALGORITHM: str
    DATABASE_URL: str
    SECRET_KEY: str
    TG_API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()
