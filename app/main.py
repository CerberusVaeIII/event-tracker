from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app import database, models
from app.routers import event, user, auth

app = FastAPI()

#models.Base.metadata.create_all(bind=database.engine)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", status_code=status.HTTP_200_OK)
def root():
    return {"status": "ok"}

app.include_router(event.router)
app.include_router(user.router)
app.include_router(auth.router)

