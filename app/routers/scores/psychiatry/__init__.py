"""
Psychiatry score router endpoints
"""

from fastapi import APIRouter

from .aas import router as aas_router
from .ace_score import router as ace_score_router
from .aims import router as aims_router
from .asrs_v1_1_adhd import router as asrs_v1_1_adhd_router
from .audit_c import router as audit_c_router
from .bam import router as bam_router
from .baws import router as baws_router
from .behavioral_activity_rating_scale import router as behavioral_activity_rating_scale_router
from .bush_francis_catatonia_rating_scale import router as bush_francis_catatonia_rating_scale_router
from .cage_questions import router as cage_questions_router
from .ciwa_ar_alcohol_withdrawal import router as ciwa_ar_alcohol_withdrawal_router
from .c_ssrs import router as c_ssrs_router
from .cas import router as cas_router
from .cows_opiate_withdrawal import router as cows_opiate_withdrawal_router
from .comm import router as comm_router
from .dire_score import router as dire_score_router
from .edinburgh_postnatal_depression_scale import router as edinburgh_postnatal_depression_scale_router
from .dast_10 import router as dast_10_router
from .dsm5_binge_eating_disorder import router as dsm5_binge_eating_disorder_router
from .dsm5_bipolar_disorder import router as dsm5_bipolar_disorder_router
from .dsm5_major_depressive_disorder import router as dsm5_major_depressive_disorder_router
from .dsm5_ptsd import router as dsm5_ptsd_router
from .gad_7 import router as gad_7_router
from .gds_15 import router as gds_15_router
from .glasgow_modified_alcohol_withdrawal_scale import router as glasgow_modified_alcohol_withdrawal_scale_router
from .hamilton_anxiety_scale import router as hamilton_anxiety_scale_router
from .hamilton_depression_rating_scale import router as hamilton_depression_rating_scale_router

# Create main specialty router
router = APIRouter()

router.include_router(aas_router)
router.include_router(ace_score_router)
router.include_router(aims_router)
router.include_router(asrs_v1_1_adhd_router)
router.include_router(audit_c_router)
router.include_router(bam_router)
router.include_router(baws_router)
router.include_router(behavioral_activity_rating_scale_router)
router.include_router(bush_francis_catatonia_rating_scale_router)
router.include_router(cage_questions_router)
router.include_router(ciwa_ar_alcohol_withdrawal_router)
router.include_router(c_ssrs_router)
router.include_router(cas_router)
router.include_router(cows_opiate_withdrawal_router)
router.include_router(comm_router)
router.include_router(dire_score_router)
router.include_router(edinburgh_postnatal_depression_scale_router)
router.include_router(dast_10_router)
router.include_router(dsm5_binge_eating_disorder_router)
router.include_router(dsm5_bipolar_disorder_router)
router.include_router(dsm5_major_depressive_disorder_router)
router.include_router(dsm5_ptsd_router)
router.include_router(gad_7_router)
router.include_router(gds_15_router)
router.include_router(glasgow_modified_alcohol_withdrawal_scale_router)
router.include_router(hamilton_anxiety_scale_router)
router.include_router(hamilton_depression_rating_scale_router)
