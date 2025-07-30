"""
Ophthalmology score router endpoints
"""

from fastapi import APIRouter

from .color_vision_screening import router as color_vision_screening_router

# Create main specialty router
router = APIRouter()

router.include_router(color_vision_screening_router)