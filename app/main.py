from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import Config

from .database import Base, engine
from .routes import users, books, health

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=Config.APP_NAME,
    description="A comprehensive CRUD API for managing users and books with PostgreSQL",
    version=Config.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(health.router)
app.include_router(users.router)
app.include_router(books.router)
