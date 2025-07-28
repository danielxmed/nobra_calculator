"""
Cardiology score router endpoints
"""

from fastapi import APIRouter

from .cha2ds2_vasc import router as cha2ds2_vasc_router
from .acc_aha_hf_staging import router as acc_aha_hf_staging_router
from .acef_ii import router as acef_ii_router

# Create main specialty router
router = APIRouter()

router.include_router(cha2ds2_vasc_router)
router.include_router(acc_aha_hf_staging_router)
router.include_router(acef_ii_router)
