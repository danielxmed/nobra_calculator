"""
Geriatrics score router endpoints
"""

from fastapi import APIRouter

from .abbey_pain import router as abbey_pain_router
from .amt_10 import router as amt_10_router
from .amt_4 import router as amt_4_router
from .barthel_index import router as barthel_index_router
from .berg_balance_scale import router as berg_balance_scale_router
from .braden_score import router as braden_score_router
from .charlson_comorbidity_index import router as charlson_comorbidity_index_router
from .clinical_frailty_scale import router as clinical_frailty_scale_router
from .cirs_g import router as cirs_g_router
from .edmonton_symptom_assessment_system_revised import router as edmonton_symptom_assessment_system_revised_router
from .g8_geriatric_screening_tool import router as g8_geriatric_screening_tool_router

# Create main specialty router
router = APIRouter()

router.include_router(abbey_pain_router)
router.include_router(amt_10_router)
router.include_router(amt_4_router)
router.include_router(barthel_index_router)
router.include_router(berg_balance_scale_router)
router.include_router(braden_score_router)
router.include_router(charlson_comorbidity_index_router)
router.include_router(clinical_frailty_scale_router)
router.include_router(cirs_g_router)
router.include_router(edmonton_symptom_assessment_system_revised_router)
router.include_router(g8_geriatric_screening_tool_router)
