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

# Create main specialty router
router = APIRouter()

router.include_router(aap_pediatric_hypertension_router)
router.include_router(apgar_score_router)
router.include_router(asthma_predictive_index_router)
router.include_router(bacterial_meningitis_score_router)
router.include_router(behavioral_observational_pain_scale_router)
router.include_router(bishop_score_router)
