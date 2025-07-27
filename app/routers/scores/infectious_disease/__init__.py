"""
Infectious_Disease score router endpoints
"""

from fastapi import APIRouter

from .helps2b import router as helps2b_router
from .duke_iscvid_2023 import router as duke_iscvid_2023_router

# Create main specialty router
router = APIRouter()

router.include_router(helps2b_router)
router.include_router(duke_iscvid_2023_router)
