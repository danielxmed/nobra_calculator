"""
Gynecology and Reproductive Medicine score router endpoints
"""

from fastapi import APIRouter

from .bwh_egg_freezing_counseling_tool import router as bwh_egg_freezing_counseling_tool_router

# Create main specialty router
router = APIRouter()

router.include_router(bwh_egg_freezing_counseling_tool_router)