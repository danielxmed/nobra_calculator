"""
Router for health check endpoints
"""

from fastapi import APIRouter
from app.models.score_models import HealthResponse

router = APIRouter(
    prefix="/health",
    tags=["health"],
    responses={404: {"description": "Not found"}}
)


@router.get("/", response_model=HealthResponse, summary="Health Check", description="Check if the API is running correctly", response_description="API status", operation_id="health_check")
async def health_check():
    """
    Endpoint to check API status
    
    Returns:
        HealthResponse: API status
    """
    return HealthResponse(
        status="healthy",
        message="nobra_calculator API is running correctly",
        version="1.0.0"
    )


@router.get("/status", response_model=HealthResponse, summary="Status Check", description="Alias for the health check endpoint", response_description="API status", operation_id="status_check")
async def get_status():
    """
    Alias for the health check endpoint
    
    Returns:
        HealthResponse: API status
    """
    return await health_check()
