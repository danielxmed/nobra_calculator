"""
Neurology score router endpoints
"""

from fastapi import APIRouter

from .abcd2 import router as abcd2_router
from .four_at import router as four_at_router
from .abc2_ich_volume import router as abc2_ich_volume_router
from .aspects import router as aspects_router
from .ascod_algorithm import router as ascod_algorithm_router
from .astral_score import router as astral_score_router
from .awol_score import router as awol_score_router
from .barnes_jewish_dysphagia import router as barnes_jewish_dysphagia_router
from .canadian_tia_score import router as canadian_tia_score_router
from .cerebral_perfusion_pressure import router as cerebral_perfusion_pressure_router
from .clinical_dementia_rating import router as clinical_dementia_rating_router
from .ndi import router as ndi_router
from .disease_steps_ms import router as disease_steps_ms_router
from .dragon_score import router as dragon_score_router
from .embolic_stroke_undetermined_source_esus_criteria import router as embolic_stroke_undetermined_source_esus_criteria_router
from .neuropathic_pain_scale import router as neuropathic_pain_scale_router
from .new_orleans_charity_head_trauma import router as new_orleans_charity_head_trauma_router
from .edss import router as edss_router

# Create main specialty router
router = APIRouter()

router.include_router(abcd2_router)
router.include_router(four_at_router)
router.include_router(abc2_ich_volume_router)
router.include_router(aspects_router)
router.include_router(ascod_algorithm_router)
router.include_router(astral_score_router)
router.include_router(awol_score_router)
router.include_router(barnes_jewish_dysphagia_router)
router.include_router(canadian_tia_score_router)
router.include_router(cerebral_perfusion_pressure_router)
router.include_router(clinical_dementia_rating_router)
router.include_router(ndi_router)
router.include_router(disease_steps_ms_router)
router.include_router(dragon_score_router)
router.include_router(embolic_stroke_undetermined_source_esus_criteria_router)
router.include_router(neuropathic_pain_scale_router)
router.include_router(new_orleans_charity_head_trauma_router)
router.include_router(edss_router)
