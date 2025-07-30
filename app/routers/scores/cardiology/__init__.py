"""
Cardiology score router endpoints
"""

from fastapi import APIRouter

from .cha2ds2_vasc import router as cha2ds2_vasc_router
from .acc_aha_hf_staging import router as acc_aha_hf_staging_router
from .acef_ii import router as acef_ii_router
from .action_icu_nstemi import router as action_icu_nstemi_router
from .adhere_algorithm import router as adhere_algorithm_router
from .thakar_score import router as thakar_score_router
from .aub_has2_cardiovascular_risk_index import router as aub_has2_cardiovascular_risk_index_router
from .aortic_dissection_detection_risk_score import router as aortic_dissection_detection_risk_score_router
from .ascvd_2013 import router as ascvd_2013_router
from .atria_bleeding import router as atria_bleeding_router
from .atria_stroke import router as atria_stroke_router
from .brugada_criteria_vt import router as brugada_criteria_vt_router
from .cahp_score import router as cahp_score_router
from .ccs_angina_grade import router as ccs_angina_grade_router
from .care_score import router as care_score_router
from .cardiac_output_fick import router as cardiac_output_fick_router
from .cardiac_power_output import router as cardiac_power_output_router
from .chads_65 import router as chads_65_router
from .chads2_score import router as chads2_score_router
from .cha2ds2_va_score import router as cha2ds2_va_score_router
from .corrected_qt_interval import router as corrected_qt_interval_router
from .crusade_bleeding_risk import router as crusade_bleeding_risk_router

# Create main specialty router
router = APIRouter()

router.include_router(cha2ds2_vasc_router)
router.include_router(acc_aha_hf_staging_router)
router.include_router(acef_ii_router)
router.include_router(action_icu_nstemi_router)
router.include_router(adhere_algorithm_router)
router.include_router(thakar_score_router)
router.include_router(aub_has2_cardiovascular_risk_index_router)
router.include_router(aortic_dissection_detection_risk_score_router)
router.include_router(ascvd_2013_router)
router.include_router(atria_bleeding_router)
router.include_router(atria_stroke_router)
router.include_router(brugada_criteria_vt_router)
router.include_router(cahp_score_router)
router.include_router(ccs_angina_grade_router)
router.include_router(care_score_router)
router.include_router(cardiac_output_fick_router)
router.include_router(cardiac_power_output_router)
router.include_router(chads_65_router)
router.include_router(chads2_score_router)
router.include_router(cha2ds2_va_score_router)
router.include_router(corrected_qt_interval_router)
router.include_router(crusade_bleeding_risk_router)
