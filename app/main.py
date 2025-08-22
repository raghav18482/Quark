"""Application entrypoint: creates FastAPI app, initializes DB tables, and mounts routers."""
from fastapi import FastAPI

from .config import settings
from .database import Base, engine
from .routers import auth as auth_router
from .routers import users as users_router


# Create tables on startup (simple projects). For larger apps, prefer Alembic migrations.
Base.metadata.create_all(bind=engine)

# Initialize the FastAPI application with a friendly title
app = FastAPI(title=settings.project_name)

# Mount feature routers
app.include_router(auth_router.router)
app.include_router(users_router.router)


@app.get("/")
def index():
	"""Lightweight health-check endpoint."""
	return {"status": "ok"}
