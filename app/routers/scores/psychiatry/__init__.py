"""
Psychiatry score router endpoints
"""

from fastapi import APIRouter

from .aas import router as aas_router
from .ace_score import router as ace_score_router
from .aims import router as aims_router
from .asrs_v1_1_adhd import router as asrs_v1_1_adhd_router

# Create main specialty router
router = APIRouter()

router.include_router(aas_router)
router.include_router(ace_score_router)
router.include_router(aims_router)
router.include_router(asrs_v1_1_adhd_router)
