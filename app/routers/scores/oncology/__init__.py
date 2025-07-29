"""
Oncology Routers

Router endpoints for oncology/cancer-related medical scores.
"""

from fastapi import APIRouter
from .leibovich_2018_rcc import router as leibovich_2018_rcc_router
from .asymptomatic_myeloma_prognosis import router as asymptomatic_myeloma_prognosis_router
from .bclc_staging import router as bclc_staging_router

router = APIRouter()

# Include all oncology score routers
router.include_router(leibovich_2018_rcc_router)
router.include_router(asymptomatic_myeloma_prognosis_router)
router.include_router(bclc_staging_router)

__all__ = ["router"]
