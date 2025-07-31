from fastapi import Request
from fastapi.templating import Jinja2Templates
from pydantic_settings import BaseSettings
#Set up Jinja templates for HTML
templates = Jinja2Templates(directory="templates")

# Default settings, hardcoded origin url in case the app is hosted locally, in the absence of an origin environment variable.
class Settings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: str
    origin: str = "http://localhost:8000"

    class Config:
        env_file = ".env"

# Initialize settings object
settings = Settings()

BASE_URL = settings.origin

# Function to reuse for each path that serves a HTML, /events, /login, /signup
def render_template(request: Request, template_name: str, context: dict = {}):
    base_context = {"request": request, "base_url": BASE_URL}
    base_context.update(context)
    return templates.TemplateResponse(template_name, base_context)

