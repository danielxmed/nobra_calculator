"""
Endocrinology score router endpoints
"""

from fastapi import APIRouter
from .ada_risk_calculator import router as ada_risk_calculator_router
from .ausdrisk import router as ausdrisk_router
from .basal_energy_expenditure import router as basal_energy_expenditure_router
from .beam_value import router as beam_value_router
from .c_peptide_to_glucose_ratio import router as c_peptide_to_glucose_ratio_router
from .calcium_correction import router as calcium_correction_router
from .cambridge_diabetes_risk_score import router as cambridge_diabetes_risk_score_router
from .canrisk import router as canrisk_router
from .diabetes_distress_scale import router as diabetes_distress_scale_router
from .dka_mpm_score import router as dka_mpm_score_router

# Create main specialty router
router = APIRouter()

router.include_router(ada_risk_calculator_router)
router.include_router(ausdrisk_router)
router.include_router(basal_energy_expenditure_router)
router.include_router(beam_value_router)
router.include_router(c_peptide_to_glucose_ratio_router)
router.include_router(calcium_correction_router)
router.include_router(cambridge_diabetes_risk_score_router)
router.include_router(canrisk_router)
router.include_router(diabetes_distress_scale_router)
router.include_router(dka_mpm_score_router)