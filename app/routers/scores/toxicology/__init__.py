"""
Toxicology Score Routers

This module contains API endpoints for toxicology-related calculators.
"""

from fastapi import APIRouter
from .atropine_dosing import router as atropine_dosing_router
from .estimated_ethanol_concentration import router as estimated_ethanol_concentration_router

# Create the specialty router
router = APIRouter()

# Include individual score routers
router.include_router(atropine_dosing_router)
router.include_router(estimated_ethanol_concentration_router)