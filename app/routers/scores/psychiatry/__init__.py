"""
Psychiatry score router endpoints
"""

from fastapi import APIRouter

from .aas import router as aas_router
from .aims import router as aims_router

# Create main specialty router
router = APIRouter()

router.include_router(aas_router)
router.include_router(aims_router)
