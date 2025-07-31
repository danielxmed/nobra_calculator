"""
General medical calculator router endpoints
"""

from fastapi import APIRouter
from .bmi_calculator import router as bmi_calculator_router
from .body_roundness_index import router as body_roundness_index_router
from .fat_free_mass import router as fat_free_mass_router

# Create main specialty router
router = APIRouter()

router.include_router(bmi_calculator_router)
router.include_router(body_roundness_index_router)
router.include_router(fat_free_mass_router)