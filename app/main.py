# app/main.py
from dotenv import load_dotenv
load_dotenv()
import uvicorn
from fastapi import FastAPI
from app.database import Base, engine
from app.routers import auth, leads, contacts, interactions, call_planning, performance, kams


# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify the allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(auth.router)
app.include_router(kams.router)
app.include_router(leads.router)
app.include_router(contacts.router)
app.include_router(interactions.router)
app.include_router(call_planning.router)
app.include_router(performance.router)

# if __name__ == "__main__":
#     uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
