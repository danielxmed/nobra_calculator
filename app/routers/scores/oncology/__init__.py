"""
Oncology Routers

Router endpoints for oncology/cancer-related medical scores.
"""

from fastapi import APIRouter
from .leibovich_2018_rcc import router as leibovich_2018_rcc_router

router = APIRouter()

# Include all oncology score routers
router.include_router(leibovich_2018_rcc_router)

__all__ = ["router"]