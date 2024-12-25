from fastapi import FastAPI
from app.database import Base, engine
from app.routers import auth, leads, contacts, interactions, call_planning, performance

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="KAM Lead Management System")


@app.get("/")
def hello():
    return {"message": "Welcome"}


# Register routers
app.include_router(auth.router)
app.include_router(leads.router)
app.include_router(contacts.router)
app.include_router(interactions.router)
app.include_router(call_planning.router)
app.include_router(performance.router)
