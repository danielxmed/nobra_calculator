"""
Pediatrics score router endpoints
"""

from fastapi import APIRouter

from .aap_pediatric_hypertension import router as aap_pediatric_hypertension_router
from .apgar_score import router as apgar_score_router

# Create main specialty router
router = APIRouter()

router.include_router(aap_pediatric_hypertension_router)
router.include_router(apgar_score_router)
