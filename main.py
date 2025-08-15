"""
nobra_calculator - Main API

Modular API for medical calculations and scores developed with FastAPI.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mcp import FastApiMCP
import uvicorn
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the root directory to the path for imports
sys.path.insert(0, str(Path(__file__).parent))

from app import __version__, __description__
from app.routers import scores_router, health_router
from app.routers.api_routes import router as api_router
# Import specialty scores router from the scores package
import app.routers.scores
specialty_scores_router = app.routers.scores.router
from app.middleware import RateLimitMiddleware, create_redis_client, parse_whitelist

# FastAPI application configuration
app = FastAPI(
    title="nobra_calculator",
    description="""
    ## 🩺 Medical Scores & Calculators API

    **nobra_calculator** is a comprehensive, production-ready API for medical calculations and clinical scores. 
    Built with FastAPI, it provides validated, evidence-based medical calculators with detailed clinical interpretations.

    ### 🚀 Key Features

    - **Medical Scores**: Covering cardiology, nephrology, pulmonology, neurology, and more
    - **Clinical Interpretations**: Evidence-based recommendations for each calculation
    - **Robust Validation**: Comprehensive input validation with clinical ranges
    - **Production Ready**: Scalable architecture with comprehensive error handling
    - **Standards Compliant**: Following medical guidelines and best practices

    ### 🔗 Quick Start

    1. **Browse Available Scores**: `GET /api/scores`
    2. **Get Score Details**: `GET /api/scores/{score_id}`
    3. **Health Check**: `GET /health`
    4. **Get scores list**: `GET /api/scores`
    5. **Get scores categories**: `GET /api/categories`
    6. **Reload scores**: 'POST /api/reload'

    ### 📚 Documentation

    - **Interactive API Docs**: [/docs](/docs) (Swagger UI)


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
# Get CORS origins from environment variables, fallback to localhost for development
cors_origins_str = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:3001,http://127.0.0.1:3000,http://127.0.0.1:3001")
cors_origins = [origin.strip() for origin in cors_origins_str.split(",") if origin.strip()]

# In production, you can set CORS_ORIGINS environment variable with specific domains
# Example: CORS_ORIGINS="https://nobra-calculator.com,https://www.nobra-calculator.com"
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Rate limiting configuration
redis_url = os.getenv("REDIS_URL")
redis_password = os.getenv("REDIS_PASSWORD")

# Initialize Redis client
redis_client = create_redis_client(redis_url, redis_password)

# Log CORS configuration
print(f"🌐 CORS enabled for origins: {', '.join(cors_origins)}")

if redis_client:
    # Add rate limiting middleware (both req_per_sec and whitelist will be read from env)
    app.add_middleware(
        RateLimitMiddleware,
        redis_client=redis_client
    )
    
    # Get configuration for logging
    req_per_sec = os.getenv("REQ_PER_SEC")
    whitelist_str = os.getenv("WHITE_LIST", "[]")
    whitelist = parse_whitelist(whitelist_str)
    
    if req_per_sec:
        print(f"✅ Rate limiting enabled: {req_per_sec} req/sec, {len(whitelist)} whitelisted IPs")
    else:
        print("⚠️  REQ_PER_SEC not set in environment variables")
else:
    print("⚠️  Rate limiting disabled: Redis connection failed")

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
app.include_router(api_router)
# Include specialty scores at root level for individual endpoints
app.include_router(specialty_scores_router)

# Create and mount the MCP server
mcp = FastApiMCP(
    app,
    name="Nobra Calculator MCP",
    description="MCP server exposing medical scores and calculators from nobra_calculator API",
    exclude_operations=["reload_scores", "acep_ed_covid19_management_tool"]
)

# Mount the MCP server onto the same FastAPI app
mcp.mount()

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
    print("🔧 MCP server available at: /mcp")
    print("🛠️  MCP tools: All FastAPI endpoints exposed as MCP tools (except reload_scores)")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """
    Event executed on application shutdown
    """
    print("👋 nobra_calculator shutting down...")

if __name__ == "__main__":
    # Configuration for local execution
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,  # Automatic reload during development
        log_level="info"
    )
