"""
Neurology score router endpoints
"""

from fastapi import APIRouter

from .abcd2 import router as abcd2_router
from .four_at import router as four_at_router

# Create main specialty router
router = APIRouter()

router.include_router(abcd2_router)
router.include_router(four_at_router)
