from fastapi import Depends, APIRouter, Request, status
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.oauth2 import get_current_user
from app import database, models, schemas, config
import datetime

router = APIRouter(
    prefix="/events",
    tags=["Events"]
)

@router.get("/", response_class=HTMLResponse, status_code=status.HTTP_200_OK) 
# Render the events page for the current user
async def event_page(request: Request):
    return config.templates.TemplateResponse("events.html", {"request": request})

@router.post("/", status_code=status.HTTP_201_CREATED) 
# Creates a new event for the current user, called from events_script.js
async def create_item(event: schemas.EventCreate, user_id: int = Depends(get_current_user), db: Session = Depends(database.get_db)):
    print(event)
    event_data = models.Event(owner_id = user_id, **event.dict())
    if event_data.date < datetime.datetime.now():
        return {"message": "Event date cannot be in the past"}
    db.add(event_data)
    db.commit()
    db.refresh(event_data)
    return { "message": "Event created successfully", "event": event_data }

@router.get("/show", response_model=list[schemas.EventOut], status_code=status.HTTP_200_OK) 
# User route to extract events from API and display onto page. Queried by events_script.js
async def read_items(user_id: int = Depends(get_current_user), db: Session = Depends(database.get_db)):
    events = db.query(models.Event).filter(models.Event.owner_id == user_id).all()
    return events

@router.get("/admin/show", response_model=list[schemas.EventOutAdmin], status_code=status.HTTP_200_OK) 
# Admin route to view events, from /docs in fastapi, used in testing
async def read_items(db: Session = Depends(database.get_db)):
    return db.query(models.Event).all()

@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
# Deletes requested event for the current user, called from events_script.js
async def delete_item(event_id: int, user_id: int = Depends(get_current_user), db: Session = Depends(database.get_db)):
    event_query = db.query(models.Event).filter(models.Event.id == event_id, models.Event.owner_id == user_id)
    event = event_query.first()
    if not event:
        return {"message": "Event not found or you do not have permission to do that"}
    event_query.delete(synchronize_session=False)
    db.commit()
    return {"message": "Event deleted successfully"}

@router.put("/{event_id}", status_code=status.HTTP_200_OK)
# Updates an existing, requested event for the current user, called from events_script.js
async def update_item(event_id: int, event: schemas.EventBase, user_id: int = Depends(get_current_user), db: Session = Depends(database.get_db)):
    event_query = db.query(models.Event).filter(models.Event.id == event_id, models.Event.owner_id == user_id)
    existing_event = event_query.first()
    if not existing_event:
        return {"message": "Event not found or you do not have permission to do that"}
    
    for key, value in event.dict().items():
        setattr(existing_event, key, value)
    
    db.commit()
    db.refresh(existing_event)
    return {"message": "Event updated successfully", "event": existing_event}