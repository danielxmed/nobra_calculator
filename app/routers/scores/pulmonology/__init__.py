"""
Pulmonology score router endpoints
"""

from fastapi import APIRouter

from .curb_65 import router as curb_65_router
from .six_minute_walk import router as six_minute_walk_router
from .aa_o2_gradient import router as aa_o2_gradient_router
from .four_peps import router as four_peps_router
from .airq import router as airq_router
from .bap_65 import router as bap_65_router
from .berlin_criteria_ards import router as berlin_criteria_ards_router
from .bode_index_copd import router as bode_index_copd_router
from .bova_score import router as bova_score_router
from .cpis import router as cpis_router
from .copd_cat import router as copd_cat_router
from .crb_65_pneumonia_severity import router as crb_65_pneumonia_severity_router
from .decaf_score import router as decaf_score_router
from .du_bois_ipf_mortality import router as du_bois_ipf_mortality_router
from .expected_peak_expiratory_flow import router as expected_peak_expiratory_flow_router
from .fleischner_guidelines import router as fleischner_guidelines_router
from .gap_index_ipf_mortality import router as gap_index_ipf_mortality_router
from .geneva_score_revised_pe import router as geneva_score_revised_pe_router
from .gold_copd_criteria import router as gold_copd_criteria_router
from .horowitz_index import router as horowitz_index_router
from .lights_criteria import router as lights_criteria_router
from .manchester_score_prognosis_sclc import router as manchester_score_prognosis_sclc_router
from .mmrc_dyspnea_scale import router as mmrc_dyspnea_scale_router
from .mulbsta_score import router as mulbsta_score_router
from .murray_score import router as murray_score_router

# Create main specialty router
router = APIRouter()

router.include_router(curb_65_router)
router.include_router(six_minute_walk_router)
router.include_router(aa_o2_gradient_router)
router.include_router(four_peps_router)
router.include_router(airq_router)
router.include_router(bap_65_router)
router.include_router(berlin_criteria_ards_router)
router.include_router(bode_index_copd_router)
router.include_router(bova_score_router)
router.include_router(cpis_router)
router.include_router(copd_cat_router)
router.include_router(crb_65_pneumonia_severity_router)
router.include_router(decaf_score_router)
router.include_router(du_bois_ipf_mortality_router)
router.include_router(expected_peak_expiratory_flow_router)
router.include_router(fleischner_guidelines_router)
router.include_router(gap_index_ipf_mortality_router)
router.include_router(geneva_score_revised_pe_router)
router.include_router(gold_copd_criteria_router)
router.include_router(horowitz_index_router)
router.include_router(lights_criteria_router)
router.include_router(manchester_score_prognosis_sclc_router)
router.include_router(mmrc_dyspnea_scale_router)
router.include_router(mulbsta_score_router)
router.include_router(murray_score_router)
