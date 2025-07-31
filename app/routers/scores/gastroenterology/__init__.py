"""
Gastroenterology score router endpoints
"""

from fastapi import APIRouter

from .bristol_stool_form_scale import router as bristol_stool_form_scale_router
from .car_olt import router as car_olt_router
from .child_pugh_score import router as child_pugh_score_router
from .choles_score import router as choles_score_router
from .clif_c_aclf import router as clif_c_aclf_router
from .cdai_crohns import router as cdai_crohns_router
from .nafld_activity_score import router as nafld_activity_score_router
from .nafld_fibrosis_score import router as nafld_fibrosis_score_router
from .erefs import router as erefs_router
from .evendo_score import router as evendo_score_router
from .fatty_liver_index import router as fatty_liver_index_router
from .fibrosis_4_index import router as fibrosis_4_index_router
from .fibrotic_nash_index import router as fibrotic_nash_index_router

# Create main specialty router
router = APIRouter()

router.include_router(bristol_stool_form_scale_router)
router.include_router(car_olt_router)
router.include_router(child_pugh_score_router)
router.include_router(choles_score_router)
router.include_router(clif_c_aclf_router)
router.include_router(cdai_crohns_router)
router.include_router(nafld_activity_score_router)
router.include_router(nafld_fibrosis_score_router)
router.include_router(erefs_router)
router.include_router(evendo_score_router)
router.include_router(fatty_liver_index_router)
router.include_router(fibrosis_4_index_router)
router.include_router(fibrotic_nash_index_router)