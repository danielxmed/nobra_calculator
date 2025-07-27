"""
Pediatrics score router endpoints
"""

from fastapi import APIRouter

from .aap_pediatric_hypertension import router as aap_pediatric_hypertension_router

# Create main specialty router
router = APIRouter()

router.include_router(aap_pediatric_hypertension_router)
