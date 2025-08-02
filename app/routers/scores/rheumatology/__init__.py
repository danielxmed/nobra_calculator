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
from .das28_crp import router as das28_crp_router
from .das28_esr import router as das28_esr_router
from .orai import router as orai_router
from .ost import router as ost_router
from .pasi import router as pasi_router
from .fracture_index import router as fracture_index_router
from .hydroxychloroquine_dosing import router as hydroxychloroquine_dosing_router
from .itas_2010 import router as itas_2010_router
from .leiden_clinical_prediction_rule import router as leiden_clinical_prediction_rule_router
from .sledai_2k import router as sledai_2k_router

# Create main specialty router
router = APIRouter()

router.include_router(asdas_crp_router)
router.include_router(asdas_esr_router)
router.include_router(asas_axial_spa_criteria_router)
router.include_router(asas_peripheral_spa_criteria_router)
router.include_router(caroc_system_router)
router.include_router(caspar_criteria_router)
router.include_router(cdai_rheumatoid_arthritis_router)
router.include_router(das28_crp_router)
router.include_router(das28_esr_router)
router.include_router(orai_router)
router.include_router(ost_router)
router.include_router(pasi_router)
router.include_router(fracture_index_router)
router.include_router(hydroxychloroquine_dosing_router)
router.include_router(itas_2010_router)
router.include_router(leiden_clinical_prediction_rule_router)
router.include_router(sledai_2k_router)
