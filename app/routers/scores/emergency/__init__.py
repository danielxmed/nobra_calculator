"""
Emergency score router endpoints
"""

from fastapi import APIRouter

from .four_c_mortality import router as four_c_mortality_router

# Create main specialty router
router = APIRouter()

router.include_router(four_c_mortality_router)
