"""
Hematology score router endpoints
"""

from fastapi import APIRouter

from .four_ts import router as four_ts_router
from .alc import router as alc_router
from .anc import router as anc_router
from .additional_nodal_metastasis_nomogram import router as additional_nodal_metastasis_nomogram_router
from .albi_hcc import router as albi_hcc_router

# Create main specialty router
router = APIRouter()

router.include_router(four_ts_router)
router.include_router(alc_router)
router.include_router(anc_router)
router.include_router(additional_nodal_metastasis_nomogram_router)
router.include_router(albi_hcc_router)
