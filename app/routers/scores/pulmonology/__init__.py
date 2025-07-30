"""
Pulmonology score router endpoints
"""

from fastapi import APIRouter

from .curb_65 import router as curb_65_router
from .six_minute_walk import router as six_minute_walk_router
from .aa_o2_gradient import router as aa_o2_gradient_router
from .four_peps import router as four_peps_router
from .airq import router as airq_router
from .bap_65 import router as bap_65_router
from .berlin_criteria_ards import router as berlin_criteria_ards_router
from .bode_index_copd import router as bode_index_copd_router
from .bova_score import router as bova_score_router
from .cpis import router as cpis_router
from .copd_cat import router as copd_cat_router
from .crb_65_pneumonia_severity import router as crb_65_pneumonia_severity_router
from .decaf_score import router as decaf_score_router

# Create main specialty router
router = APIRouter()

router.include_router(curb_65_router)
router.include_router(six_minute_walk_router)
router.include_router(aa_o2_gradient_router)
router.include_router(four_peps_router)
router.include_router(airq_router)
router.include_router(bap_65_router)
router.include_router(berlin_criteria_ards_router)
router.include_router(bode_index_copd_router)
router.include_router(bova_score_router)
router.include_router(cpis_router)
router.include_router(copd_cat_router)
router.include_router(crb_65_pneumonia_severity_router)
router.include_router(decaf_score_router)
