"""
Infectious_Disease score router endpoints
"""

from fastapi import APIRouter

from .helps2b import router as helps2b_router

# Create main specialty router
router = APIRouter()

router.include_router(helps2b_router)
