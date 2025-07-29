"""
Urology score router endpoints
"""

from fastapi import APIRouter
from .ipss_aua_si import router as ipss_aua_si_router

# Create main specialty router
router = APIRouter()

router.include_router(ipss_aua_si_router)