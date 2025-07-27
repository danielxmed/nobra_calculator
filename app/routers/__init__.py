"""
Routers da API nobra_calculator
"""

from .scores import router as scores_router
from .health import router as health_router

__all__ = [
    "scores_router",
    "health_router"
]
