"""
Geriatrics score router endpoints
"""

from fastapi import APIRouter

from .abbey_pain import router as abbey_pain_router

# Create main specialty router
router = APIRouter()

router.include_router(abbey_pain_router)
