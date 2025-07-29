"""
Hepatology Routers

Router endpoints for hepatology/liver-related medical scores.
"""

from fastapi import APIRouter
from .bard_score import router as bard_score_router

router = APIRouter()

# Include all hepatology score routers
router.include_router(bard_score_router)

__all__ = ["router"]