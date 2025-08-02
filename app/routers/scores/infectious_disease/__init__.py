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
from .hiri_msm import router as hiri_msm_router
from .hiv_needle_stick_rasp import router as hiv_needle_stick_rasp_router
from .vaco_index_covid19 import router as vaco_index_covid19_router
from .indications_for_paxlovid import router as indications_for_paxlovid_router
from .menza_score import router as menza_score_router
from .vacs_1_0_index import router as vacs_1_0_index_router
from .vacs_2_0_index import router as vacs_2_0_index_router
from .vacs_cci import router as vacs_cci_router

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
router.include_router(hiri_msm_router)
router.include_router(hiv_needle_stick_rasp_router)
router.include_router(vaco_index_covid19_router)
router.include_router(indications_for_paxlovid_router)
router.include_router(menza_score_router)
router.include_router(vacs_1_0_index_router)
router.include_router(vacs_2_0_index_router)
router.include_router(vacs_cci_router)
