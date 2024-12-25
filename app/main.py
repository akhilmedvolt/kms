from fastapi import FastAPI
from .routers import auth, leads, contacts, interactions, performance
from .database import Base, engine

# Create all tables in the DB if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="KAM Lead Management System",
    description="A system to manage leads, contacts, interactions, and performance for Key Account Managers.",
    version="1.0.0"
)

# Include Routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(leads.router, prefix="/leads", tags=["Leads"])
app.include_router(contacts.router, prefix="/contacts", tags=["Contacts"])
app.include_router(interactions.router, prefix="/interactions", tags=["Interactions"])
app.include_router(performance.router, prefix="/performance", tags=["Performance"])

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to KAM Lead Management System!"}
