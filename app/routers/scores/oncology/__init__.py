"""
Oncology Routers

Router endpoints for oncology/cancer-related medical scores.
"""

from fastapi import APIRouter
from .leibovich_2018_rcc import router as leibovich_2018_rcc_router
from .asymptomatic_myeloma_prognosis import router as asymptomatic_myeloma_prognosis_router
from .bclc_staging import router as bclc_staging_router
from .bmv_model import router as bmv_model_router
from .carg_tt import router as carg_tt_router
from .crash_score import router as crash_score_router
from .cisne import router as cisne_router
from .ctcae import router as ctcae_router
from .crs_grading import router as crs_grading_router
from .damico_risk_classification import router as damico_risk_classification_router

router = APIRouter()

# Include all oncology score routers
router.include_router(leibovich_2018_rcc_router)
router.include_router(asymptomatic_myeloma_prognosis_router)
router.include_router(bclc_staging_router)
router.include_router(bmv_model_router)
router.include_router(carg_tt_router)
router.include_router(crash_score_router)
router.include_router(cisne_router)
router.include_router(ctcae_router)
router.include_router(crs_grading_router)
router.include_router(damico_risk_classification_router)

__all__ = ["router"]
