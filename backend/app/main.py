"""
FastAPI Main Application - AI-Based Pothole Detection System
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os

from app.config import settings
from app.config.database import db
from app.routes import auth, reports, zones, repairs


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    await db.connect_db()
    
    # Seed Test Users
    from app.utils.auth import get_password_hash
    from datetime import datetime
    
    # Test Citizen
    if not await db.database.users.find_one({"email": settings.TEST_CITIZEN_EMAIL}):
        citizen = {
            "name": "Test Citizen",
            "email": settings.TEST_CITIZEN_EMAIL,
            "password": get_password_hash(settings.TEST_CITIZEN_PASSWORD),
            "phone": "1234567890",
            "role": "user",
            "created_at": datetime.utcnow()
        }
        await db.database.users.insert_one(citizen)
        print(f"✅ Created Test Citizen: {settings.TEST_CITIZEN_EMAIL}")
        
    # Test Authority
    if not await db.database.users.find_one({"email": settings.TEST_AUTHORITY_EMAIL}):
        authority = {
            "name": "City Admin",
            "email": settings.TEST_AUTHORITY_EMAIL,
            "password": get_password_hash(settings.TEST_AUTHORITY_PASSWORD),
            "phone": "9876543210",
            "role": "authority",
            "created_at": datetime.utcnow()
        }
        await db.database.users.insert_one(authority)
        print(f"✅ Created Test Authority: {settings.TEST_AUTHORITY_EMAIL}")

    print("🚀 Application started successfully!")
    
    yield
    
    # Shutdown
    await db.close_db()
    print("👋 Application shut down")


# Create FastAPI application
app = FastAPI(
    title="Pothole Detection API",
    description="AI-Based Road Damage & Pothole Detection System Backend",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount uploads directory for serving images
if os.path.exists(settings.UPLOAD_DIR):
    app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Include routers
app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(reports.router, prefix=settings.API_V1_PREFIX)
app.include_router(zones.router, prefix=settings.API_V1_PREFIX)
app.include_router(repairs.router, prefix=settings.API_V1_PREFIX)


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "AI-Based Pothole Detection System API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected" if db.database is not None else "disconnected"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
