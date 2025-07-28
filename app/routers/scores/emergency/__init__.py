"""
Emergency score router endpoints
"""

from fastapi import APIRouter

from .four_c_mortality import router as four_c_mortality_router
from .ais_inhalation_injury import router as ais_inhalation_injury_router
from .emergency_medicine_coding_guide_2023 import router as emergency_medicine_coding_guide_2023_router
from .abc_score import router as abc_score_router
from .acep_ed_covid19_management_tool import router as acep_ed_covid19_management_tool_router

# Create main specialty router
router = APIRouter()

router.include_router(four_c_mortality_router)
router.include_router(ais_inhalation_injury_router)
router.include_router(emergency_medicine_coding_guide_2023_router)
router.include_router(abc_score_router)
router.include_router(acep_ed_covid19_management_tool_router)
