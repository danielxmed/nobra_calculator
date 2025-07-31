"""
Urology score router endpoints
"""

from fastapi import APIRouter
from .ipss_aua_si import router as ipss_aua_si_router
from .gleason_score_prostate import router as gleason_score_prostate_router
from .fuhrman_nuclear_grade import router as fuhrman_nuclear_grade_router

# Create main specialty router
router = APIRouter()

router.include_router(ipss_aua_si_router)
router.include_router(gleason_score_prostate_router)
router.include_router(fuhrman_nuclear_grade_router)