"""
Infectious_Disease score router endpoints
"""

from fastapi import APIRouter

from .helps2b import router as helps2b_router
from .duke_iscvid_2023 import router as duke_iscvid_2023_router
from .atlas_score import router as atlas_score_router
from .bacterial_meningitis_score import router as bacterial_meningitis_score_router
from .denver_hiv_risk_score import router as denver_hiv_risk_score_router
from .drip_score import router as drip_score_router
from .duke_criteria_infective_endocarditis import router as duke_criteria_infective_endocarditis_router
from .feverpain_score import router as feverpain_score_router
from .vaco_index_covid19 import router as vaco_index_covid19_router

# Create main specialty router
router = APIRouter()

router.include_router(helps2b_router)
router.include_router(duke_iscvid_2023_router)
router.include_router(atlas_score_router)
router.include_router(bacterial_meningitis_score_router)
router.include_router(denver_hiv_risk_score_router)
router.include_router(drip_score_router)
router.include_router(duke_criteria_infective_endocarditis_router)
router.include_router(feverpain_score_router)
router.include_router(vaco_index_covid19_router)
