from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings
from contextlib import asynccontextmanager
from .routes.query import router as query_router
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    app_name: str = "Torva RAG Service"
    debug: bool = False
    
    class Config:
        env_file = ".env"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load models, initialize connections etc.
    print("Starting up RAG service...")
    yield
    # Shutdown: Clean up resources
    print("Shutting down RAG service...")


app = FastAPI(
    title="Torva RAG API",
    description="RAG Service for Torva platform",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(query_router)


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "rag"} 