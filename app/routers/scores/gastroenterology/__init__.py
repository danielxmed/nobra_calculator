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

# Create main specialty router
router = APIRouter()

router.include_router(bristol_stool_form_scale_router)
router.include_router(car_olt_router)
router.include_router(child_pugh_score_router)
router.include_router(choles_score_router)
router.include_router(clif_c_aclf_router)
router.include_router(cdai_crohns_router)