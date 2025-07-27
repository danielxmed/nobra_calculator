"""
Hematology score router endpoints
"""

from fastapi import APIRouter

from .four_ts import router as four_ts_router
from .alc import router as alc_router
from .anc import router as anc_router

# Create main specialty router
router = APIRouter()

router.include_router(four_ts_router)
router.include_router(alc_router)
router.include_router(anc_router)
