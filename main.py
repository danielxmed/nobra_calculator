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
    description="""
    ## 🩺 Medical Scores & Calculators API

    **nobra_calculator** is a comprehensive, production-ready API for medical calculations and clinical scores. 
    Built with FastAPI, it provides validated, evidence-based medical calculators with detailed clinical interpretations.

    ### 🚀 Key Features

    - **19+ Medical Scores**: Covering cardiology, nephrology, pulmonology, neurology, and more
    - **Clinical Interpretations**: Evidence-based recommendations for each calculation
    - **Robust Validation**: Comprehensive input validation with clinical ranges
    - **Production Ready**: Scalable architecture with comprehensive error handling
    - **Standards Compliant**: Following medical guidelines and best practices

    ### 📊 Available Categories

    | Category | Scores | Examples |
    |----------|--------|----------|
    | **Cardiology** | 2+ | CHA₂DS₂-VASc, ACC/AHA HF Staging |
    | **Nephrology** | 2+ | CKD-EPI 2021, ABIC Score |
    | **Pulmonology** | 3+ | CURB-65, 6MWT, A-a O₂ Gradient |
    | **Neurology** | 3+ | ABCD² Score, 4AT, 2HELPS2B |
    | **Hematology** | 1+ | 4Ts HIT Score |
    | **Emergency** | 1+ | 4C COVID-19 Mortality |
    | **Pediatrics** | 1+ | AAP Hypertension Guidelines |
    | **Geriatrics** | 1+ | Abbey Pain Scale |
    | **Psychiatry** | 1+ | AIMS Tardive Dyskinesia |

    ### 🔗 Quick Start

    1. **Browse Available Scores**: `GET /api/scores`
    2. **Get Score Details**: `GET /api/scores/{score_id}`
    3. **Calculate Score**: `POST /api/{score_id}`
    4. **Health Check**: `GET /health`

    ### 📚 Documentation

    - **Interactive API Docs**: [/docs](/docs) (Swagger UI)
    - **Alternative Docs**: [/redoc](/redoc) (ReDoc)
    - **OpenAPI Spec**: [/openapi.json](/openapi.json)

    ### ⚠️ Clinical Disclaimer

    This API is intended for educational and research purposes. Results should not replace 
    professional clinical judgment. Always consult qualified healthcare professionals for 
    medical diagnosis and treatment decisions.

    ### 🏥 Clinical Validation

    All scores are implemented according to peer-reviewed literature and established 
    clinical guidelines. Each calculation includes comprehensive references and 
    evidence-based interpretations.
    """,
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": "Daniel Nobrega Medeiros",
        "email": "daniel@nobregamedtech.com.br",
        "url": "https://github.com/danielxmed/nobra_calculator"
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
    },
    openapi_tags=[
        {
            "name": "scores",
            "description": "Medical scores and calculators with clinical interpretations"
        },
        {
            "name": "health",
            "description": "API health and status monitoring"
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
