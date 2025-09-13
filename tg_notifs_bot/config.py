from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DEBUG: bool = True
    API_KEY: str
    BACKEND_URL: str

    class Config:
        env_file = ".env"

settings = Settings()
