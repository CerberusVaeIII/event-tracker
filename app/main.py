from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routers import event, user, auth

app = FastAPI() # Generate the FastAPI instance

app.mount("/static", StaticFiles(directory="static"), name="static")

# Add CORS
app.add_middleware(CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root path
@app.get("/", status_code=status.HTTP_200_OK)
def root():
    return {"status": "ok"}

# Link the routers
app.include_router(event.router)
app.include_router(user.router)
app.include_router(auth.router)

