"""
Rheumatology score router endpoints
"""

from fastapi import APIRouter

from .eular_acr_pmr import router as eular_acr_pmr_router

# Create main specialty router
router = APIRouter()

router.include_router(eular_acr_pmr_router)
