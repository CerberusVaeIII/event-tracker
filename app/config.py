from fastapi import Request
from fastapi.templating import Jinja2Templates
from pydantic_settings import BaseSettings
import os
#Set up Jinja templates for HTML
templates = Jinja2Templates(directory="templates")

BASE_URL = os.getenv("ORIGIN", "http://localhost:8000")

def render_template(request: Request, template_name: str, context: dict = {}):
    base_context = {"request": request, "base_url": BASE_URL}
    base_context.update(context)
    return templates.TemplateResponse(template_name, base_context)

class Settings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: str

    class Config:
        env_file = ".env"

settings = Settings()