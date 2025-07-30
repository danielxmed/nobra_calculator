"""
Pediatrics score router endpoints
"""

from fastapi import APIRouter

from .aap_pediatric_hypertension import router as aap_pediatric_hypertension_router
from .apgar_score import router as apgar_score_router
from .asthma_predictive_index import router as asthma_predictive_index_router
from .bacterial_meningitis_score import router as bacterial_meningitis_score_router
from .behavioral_observational_pain_scale import router as behavioral_observational_pain_scale_router
from .bishop_score import router as bishop_score_router
from .brue import router as brue_router
from .brue_2_0 import router as brue_2_0_router
from .catch_rule import router as catch_rule_router
from .chalice_rule import router as chalice_rule_router
from .cheops_pain_scale import router as cheops_pain_scale_router
from .capd import router as capd_router
from .dhaka_score import router as dhaka_score_router

# Create main specialty router
router = APIRouter()

router.include_router(aap_pediatric_hypertension_router)
router.include_router(apgar_score_router)
router.include_router(asthma_predictive_index_router)
router.include_router(bacterial_meningitis_score_router)
router.include_router(behavioral_observational_pain_scale_router)
router.include_router(bishop_score_router)
router.include_router(brue_router)
router.include_router(brue_2_0_router)
router.include_router(catch_rule_router)
router.include_router(chalice_rule_router)
router.include_router(cheops_pain_scale_router)
router.include_router(capd_router)
router.include_router(dhaka_score_router)
