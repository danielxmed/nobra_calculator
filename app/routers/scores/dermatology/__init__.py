"""
Dermatology score router endpoints
"""

from fastapi import APIRouter

from .eczema_area_severity_index import router as eczema_area_severity_index_router

# Create main specialty router
router = APIRouter()

router.include_router(eczema_area_severity_index_router)