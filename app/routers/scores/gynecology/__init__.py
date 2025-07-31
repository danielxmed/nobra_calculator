"""
Gynecology and Reproductive Medicine score router endpoints
"""

from fastapi import APIRouter

from .bwh_egg_freezing_counseling_tool import router as bwh_egg_freezing_counseling_tool_router
from .fetal_bpp_score import router as fetal_bpp_score_router
from .figo_staging_ovarian_cancer_2014 import router as figo_staging_ovarian_cancer_2014_router

# Create main specialty router
router = APIRouter()

router.include_router(bwh_egg_freezing_counseling_tool_router)
router.include_router(fetal_bpp_score_router)
router.include_router(figo_staging_ovarian_cancer_2014_router)