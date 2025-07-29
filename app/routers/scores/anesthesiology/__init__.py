"""
Anesthesiology Score Routers

Routers for anesthesiology-related clinical scores and calculators.
"""

from fastapi import APIRouter
from .apfel_score_ponv import router as apfel_score_ponv_router
from .ariscat_score import router as ariscat_score_router
from .asa_physical_status import router as asa_physical_status_router

# Create the anesthesiology router
router = APIRouter()

# Include the Apfel Score router
router.include_router(apfel_score_ponv_router)

# Include the ARISCAT Score router
router.include_router(ariscat_score_router)

# Include the ASA Physical Status router
router.include_router(asa_physical_status_router)

# Export the router
__all__ = ["router"]
