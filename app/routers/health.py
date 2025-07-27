"""
Router para endpoints de health check
"""

from fastapi import APIRouter
from app.models.score_models import HealthResponse

router = APIRouter(
    prefix="/health",
    tags=["health"],
    responses={404: {"description": "Not found"}}
)


@router.get("/", response_model=HealthResponse)
async def health_check():
    """
    Endpoint para verificar o status da API
    
    Returns:
        HealthResponse: Status da API
    """
    return HealthResponse(
        status="healthy",
        message="nobra_calculator API está funcionando corretamente",
        version="1.0.0"
    )


@router.get("/status", response_model=HealthResponse)
async def get_status():
    """
    Alias para o endpoint de health check
    
    Returns:
        HealthResponse: Status da API
    """
    return await health_check()
