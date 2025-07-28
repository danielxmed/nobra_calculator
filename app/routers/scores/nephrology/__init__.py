"""
Nephrology score router endpoints
"""

from fastapi import APIRouter

from .ckd_epi_2021 import router as ckd_epi_2021_router
from .abic_score import router as abic_score_router
from .ain_risk_calculator import router as ain_risk_calculator_router
from .akin import router as akin_router

# Create main specialty router
router = APIRouter()

router.include_router(ckd_epi_2021_router)
router.include_router(abic_score_router)
router.include_router(ain_risk_calculator_router)
router.include_router(akin_router)
