"""
nobra_calculator - Main API

Modular API for medical calculations and scores developed with FastAPI.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import sys
from pathlib import Path

# Add the root directory to the path for imports
sys.path.insert(0, str(Path(__file__).parent))

from app import __version__, __description__
from app.routers import scores_router, health_router

# Enhanced FastAPI application configuration
app = FastAPI(
    title="nobra_calculator",
    description=__description__,
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": "nobra_calculator Team",
        "email": "daniel@nobregamedtech.com.br",
        "url": "https://github.com/danielxmed/nobra_calculator"
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
    },
    terms_of_service="https://github.com/danielxmed/nobra_calculator/blob/main/LICENSE",
    openapi_tags=[
        {
            "name": "health",
            "description": "**System Health & Status**\n\nEndpoints for monitoring API health and status. Use these endpoints to verify that the API is running correctly and all services are operational."
        },
        {
            "name": "scores",
            "description": "**Medical Score Calculations**\n\nComprehensive collection of medical calculators and clinical scoring systems. Each endpoint provides:\n\n- **Detailed parameter validation** with clinical ranges\n- **Evidence-based calculations** following published formulas\n- **Clinical interpretations** with actionable recommendations\n- **Comprehensive metadata** including references and notes\n\n**Available Categories:**\n- 🫀 Cardiology (CHA₂DS₂-VASc, Heart Failure Staging)\n- 🫘 Nephrology (CKD-EPI 2021 eGFR)\n- 🫁 Pulmonology (CURB-65, A-a Gradient)\n- 🧠 Neurology (ABCD² Score, Delirium Screening)\n- 🩸 Hematology (ANC, HIT Score)\n- 👶 Pediatrics (AAP Hypertension Guidelines)\n- 🧓 Geriatrics (Abbey Pain Scale)\n- And more...\n\n**Usage Patterns:**\n1. Use `GET /api/scores` to browse available calculators\n2. Use `GET /api/scores/{score_id}` for detailed parameter information\n3. Use specific POST endpoints for calculations with enhanced validation\n4. Use `POST /api/{score_id}/calculate` for generic calculations"
        }
    ],
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Development server"
        },
        {
            "url": "https://api.nobra-calculator.com",
            "description": "Production server"
        }
    ]
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
