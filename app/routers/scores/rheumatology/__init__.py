"""
Rheumatology score router endpoints
"""

from fastapi import APIRouter

from .eular_acr_pmr import router as eular_acr_pmr_router
from .acr_eular_2010_ra import router as acr_eular_2010_ra_router
from .acr_eular_gout import router as acr_eular_gout_router
from .acute_gout_diagnosis_rule import router as acute_gout_diagnosis_rule_router
from .age_adjusted_esr_crp import router as age_adjusted_esr_crp_router

# Create main specialty router
router = APIRouter()

router.include_router(eular_acr_pmr_router)
router.include_router(acr_eular_2010_ra_router)
router.include_router(acr_eular_gout_router)
router.include_router(acute_gout_diagnosis_rule_router)
router.include_router(age_adjusted_esr_crp_router)
