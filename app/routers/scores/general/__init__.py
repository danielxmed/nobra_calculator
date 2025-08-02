"""
General medical calculator router endpoints
"""

from fastapi import APIRouter
from .bmi_calculator import router as bmi_calculator_router
from .body_roundness_index import router as body_roundness_index_router
from .fat_free_mass import router as fat_free_mass_router
from .hospital_score import router as hospital_score_router
from .ideal_body_weight_adjusted import router as ideal_body_weight_adjusted_router
from .mme_calculator import router as mme_calculator_router
from .surgical_apgar_score import router as surgical_apgar_score_router
from .visual_acuity_testing_snellen_chart import router as visual_acuity_testing_snellen_chart_router
from .wound_closure_classification import router as wound_closure_classification_router

# Create main specialty router
router = APIRouter()

router.include_router(bmi_calculator_router)
router.include_router(body_roundness_index_router)
router.include_router(fat_free_mass_router)
router.include_router(hospital_score_router)
router.include_router(ideal_body_weight_adjusted_router)
router.include_router(mme_calculator_router)
router.include_router(surgical_apgar_score_router)
router.include_router(visual_acuity_testing_snellen_chart_router)
router.include_router(wound_closure_classification_router)