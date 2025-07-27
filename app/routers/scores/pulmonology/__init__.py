"""
Pulmonology score router endpoints
"""

from fastapi import APIRouter

from .curb_65 import router as curb_65_router
from .six_minute_walk import router as six_minute_walk_router
from .aa_o2_gradient import router as aa_o2_gradient_router
from .four_peps import router as four_peps_router

# Create main specialty router
router = APIRouter()

router.include_router(curb_65_router)
router.include_router(six_minute_walk_router)
router.include_router(aa_o2_gradient_router)
router.include_router(four_peps_router)
