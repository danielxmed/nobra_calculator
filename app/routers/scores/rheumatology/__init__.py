"""
Rheumatology score router endpoints
"""

from fastapi import APIRouter
from .asdas_crp import router as asdas_crp_router
from .asdas_esr import router as asdas_esr_router
from .asas_axial_spa_criteria import router as asas_axial_spa_criteria_router
from .asas_peripheral_spa_criteria import router as asas_peripheral_spa_criteria_router
from .caroc_system import router as caroc_system_router
from .caspar_criteria import router as caspar_criteria_router
from .cdai_rheumatoid_arthritis import router as cdai_rheumatoid_arthritis_router

# Create main specialty router
router = APIRouter()

router.include_router(asdas_crp_router)
router.include_router(asdas_esr_router)
router.include_router(asas_axial_spa_criteria_router)
router.include_router(asas_peripheral_spa_criteria_router)
router.include_router(caroc_system_router)
router.include_router(caspar_criteria_router)
router.include_router(cdai_rheumatoid_arthritis_router)
