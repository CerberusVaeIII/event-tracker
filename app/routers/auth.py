from fastapi import APIRouter, Depends, Request, status, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app import database, models, schemas, utils, oauth2, config
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

# Initialize router for login.
router = APIRouter(
    prefix="/login",
    tags=["Authentication"]
)

@router.get("/", response_class=HTMLResponse, status_code=status.HTTP_200_OK) # Render the login page.
async def event_page(request: Request):
    return config.render_template(request, "login.html")

@router.post("/", status_code=status.HTTP_200_OK, response_model=schemas.Token) # Handle user login and return access token.
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    if not utils.verify(user_credentials.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    access_token = oauth2.create_access_token(data={"user_id": db_user.id})
    return {"access_token": access_token, "token_type": "bearer"}