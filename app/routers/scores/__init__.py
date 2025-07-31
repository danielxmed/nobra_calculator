"""
Main scores router that includes all specialty score routers
"""

from fastapi import APIRouter

# Import all specialty routers
from .anesthesiology import router as anesthesiology_router
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
from .oncology import router as oncology_router
from .toxicology import router as toxicology_router
from .urology import router as urology_router
from .endocrinology import router as endocrinology_router
from .hepatology import router as hepatology_router
from .gastroenterology import router as gastroenterology_router
from .general import router as general_router
from .gynecology import router as gynecology_router
from .ophthalmology import router as ophthalmology_router
from .dermatology import router as dermatology_router

# Create main scores router
router = APIRouter()

# Include all specialty routers
router.include_router(anesthesiology_router, tags=["anesthesiology"])
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
router.include_router(oncology_router, tags=["oncology"])
router.include_router(toxicology_router, tags=["toxicology"])
router.include_router(urology_router, tags=["urology"])
router.include_router(endocrinology_router, tags=["endocrinology"])
router.include_router(hepatology_router, tags=["hepatology"])
router.include_router(gastroenterology_router, tags=["gastroenterology"])
router.include_router(general_router, tags=["general"])
router.include_router(gynecology_router, tags=["gynecology"])
router.include_router(ophthalmology_router, tags=["ophthalmology"])
router.include_router(dermatology_router, tags=["dermatology"])
