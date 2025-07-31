from fastapi.templating import Jinja2Templates
from pydantic_settings import BaseSettings
#Set up Jinja templates for HTML
templates = Jinja2Templates(directory="templates")

class Settings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: str

    class Config:
        env_file = ".env"

settings = Settings()