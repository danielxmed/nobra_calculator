"""
Endocrinology score router endpoints
"""

from fastapi import APIRouter
from .ada_risk_calculator import router as ada_risk_calculator_router
from .ausdrisk import router as ausdrisk_router
from .basal_energy_expenditure import router as basal_energy_expenditure_router
from .beam_value import router as beam_value_router

# Create main specialty router
router = APIRouter()

router.include_router(ada_risk_calculator_router)
router.include_router(ausdrisk_router)
router.include_router(basal_energy_expenditure_router)
router.include_router(beam_value_router)