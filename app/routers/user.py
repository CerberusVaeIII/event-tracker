from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from app import oauth2
from app import database, models, schemas, utils, config


# Initialize router for user management. Lack of prefix due to using multiple paths.
router = APIRouter(
    tags=["User Management"]
)

@router.get("/signup", response_class=HTMLResponse, status_code=status.HTTP_200_OK)
# Render the signup page.
async def signup_page(request: Request):
    return config.render_template(request, "signup.html")

@router.post("/signup", status_code = status.HTTP_201_CREATED)
# Handle user signup and create a new user.
async def create_user(user: schemas.UserBase, db: Session = Depends(database.get_db)):
    user_data = models.User(**user.dict())
    user_data.password = utils.hash(user.password)
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    if not user_data.password:
        return {"message": "Password is required"}, 400
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "User created successfully"}
    )


@router.get("/admin/users/", status_code=status.HTTP_200_OK)
# Admin route to get all users, used in testing through /docs.
async def get_users(db: Session = Depends(database.get_db)):
    users = db.query(models.User).all()
    return users

@router.get("/users/current", status_code=status.HTTP_200_OK)
# Get the current user's information. Used through events_script.js, and extracts from the token in localStorage.
async def get_user(user_id: int = Depends(oauth2.get_current_user), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return {"message": "User not found"}
    return user

@router.delete("/users/delete", status_code=status.HTTP_204_NO_CONTENT)
# Deletes the current user, used through events_script.js.
async def delete_user(db: Session = Depends(database.get_db), current_user_id: int = Depends(oauth2.get_current_user)): 
    user_query = db.query(models.User).filter(models.User.id == current_user_id)
    user = user_query.first()
    if not user:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "User not found"}
        )
    user_query.delete(synchronize_session=False)
    db.commit()
    return JSONResponse(
        status_code=status.HTTP_204_NO_CONTENT,
        content=None
    )