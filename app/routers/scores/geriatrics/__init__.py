"""
Geriatrics score router endpoints
"""

from fastapi import APIRouter

from .abbey_pain import router as abbey_pain_router
from .amt_10 import router as amt_10_router
from .amt_4 import router as amt_4_router

# Create main specialty router
router = APIRouter()

router.include_router(abbey_pain_router)
router.include_router(amt_10_router)
router.include_router(amt_4_router)
