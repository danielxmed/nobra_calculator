"""
Endocrinology score router endpoints
"""

from fastapi import APIRouter
from .ada_risk_calculator import router as ada_risk_calculator_router

# Create main specialty router
router = APIRouter()

router.include_router(ada_risk_calculator_router)