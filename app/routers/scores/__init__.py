"""
Main scores router that includes all specialty score routers
"""

from fastapi import APIRouter

# Import all specialty routers
from .nephrology import router as nephrology_router
from .cardiology import router as cardiology_router
from .pulmonology import router as pulmonology_router
from .neurology import router as neurology_router
from .hematology import router as hematology_router
from .emergency import router as emergency_router
from .psychiatry import router as psychiatry_router
from .pediatrics import router as pediatrics_router
from .geriatrics import router as geriatrics_router
from .rheumatology import router as rheumatology_router
from .infectious_disease import router as infectious_disease_router

# Create main scores router
router = APIRouter()

# Include all specialty routers
router.include_router(nephrology_router, tags=["nephrology"])
router.include_router(cardiology_router, tags=["cardiology"])
router.include_router(pulmonology_router, tags=["pulmonology"])
router.include_router(neurology_router, tags=["neurology"])
router.include_router(hematology_router, tags=["hematology"])
router.include_router(emergency_router, tags=["emergency"])
router.include_router(psychiatry_router, tags=["psychiatry"])
router.include_router(pediatrics_router, tags=["pediatrics"])
router.include_router(geriatrics_router, tags=["geriatrics"])
router.include_router(rheumatology_router, tags=["rheumatology"])
router.include_router(infectious_disease_router, tags=["infectious_disease"])