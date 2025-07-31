"""
Nephrology score router endpoints
"""

from fastapi import APIRouter

from .ckd_epi_2021 import router as ckd_epi_2021_router
from .abic_score import router as abic_score_router
from .ain_risk_calculator import router as ain_risk_calculator_router
from .akin import router as akin_router
from .body_fluid_balance import router as body_fluid_balance_router
from .bun_creatinine_ratio import router as bun_creatinine_ratio_router
from .ckid_u25_egfr import router as ckid_u25_egfr_router
from .ckd_prediction_hiv_patients import router as ckd_prediction_hiv_patients_router
from .cisplatin_aki import router as cisplatin_aki_router
from .creatinine_clearance_cockcroft_gault import router as creatinine_clearance_cockcroft_gault_router
from .fractional_excretion_sodium import router as fractional_excretion_sodium_router
from .fractional_excretion_urea import router as fractional_excretion_urea_router
from .free_water_deficit import router as free_water_deficit_router

# Create main specialty router
router = APIRouter()

router.include_router(ckd_epi_2021_router)
router.include_router(abic_score_router)
router.include_router(ain_risk_calculator_router)
router.include_router(akin_router)
router.include_router(body_fluid_balance_router)
router.include_router(bun_creatinine_ratio_router)
router.include_router(ckid_u25_egfr_router)
router.include_router(ckd_prediction_hiv_patients_router)
router.include_router(cisplatin_aki_router)
router.include_router(creatinine_clearance_cockcroft_gault_router)
router.include_router(fractional_excretion_sodium_router)
router.include_router(fractional_excretion_urea_router)
router.include_router(free_water_deficit_router)
