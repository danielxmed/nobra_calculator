"""
nobra_calculator - Main API

Modular API for medical calculations and scores developed with FastAPI.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import sys
from pathlib import Path

# Add the root directory to the path for imports
sys.path.insert(0, str(Path(__file__).parent))

from app import __version__, __description__
from app.routers import scores_router, health_router

# FastAPI application configuration
app = FastAPI(
    title="nobra_calculator",
    description=__description__,
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS configuration to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware to catch unhandled errors
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global handler to catch unhandled exceptions
    """
    return JSONResponse(
        status_code=500,
        content={
            "error": "InternalServerError",
            "message": "Internal server error",
            "details": {
                "path": str(request.url),
                "method": request.method,
                "error": str(exc) if app.debug else "Internal error"
            }
        }
    )

# Mount static files for interactive documentation
app.mount("/docs-interactive", StaticFiles(directory="docs"), name="docs-interactive")

# Register routers
app.include_router(health_router)
app.include_router(scores_router)

# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint of the API
    
    Returns:
        Dict: Basic API information
    """
    return {
        "name": "nobra_calculator",
        "description": __description__,
        "version": __version__,
        "docs": "/docs",
        "redoc": "/redoc",
        "interactive_docs": "/docs-interactive",
        "health": "/health",
        "api": "/api"
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    """
    Event executed on application startup
    """
    print(f"🚀 nobra_calculator v{__version__} started!")
    print("📋 Documentation available at: /docs")
    print("🔍 Redoc available at: /redoc")
    print("❤️  Health check available at: /health")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """
    Event executed on application shutdown
    """
    print("👋 nobra_calculator shutting down...")

if __name__ == "__main__":
    # Configuration for local execution
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Automatic reload during development
        log_level="info"
    )
