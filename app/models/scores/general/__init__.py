"""
General medical calculator models
"""

from .bmi_calculator import BmiCalculatorRequest, BmiCalculatorResponse
from .body_roundness_index import BodyRoundnessIndexRequest, BodyRoundnessIndexResponse
from .fat_free_mass import FatFreeMassRequest, FatFreeMassResponse
from .hospital_score import HospitalScoreRequest, HospitalScoreResponse
from .ideal_body_weight_adjusted import IdealBodyWeightAdjustedRequest, IdealBodyWeightAdjustedResponse
from .mme_calculator import MmeCalculatorRequest, MmeCalculatorResponse
from .surgical_apgar_score import SurgicalApgarScoreRequest, SurgicalApgarScoreResponse
from .visual_acuity_testing_snellen_chart import VisualAcuityTestingSnellenChartRequest, VisualAcuityTestingSnellenChartResponse
from .wound_closure_classification import WoundClosureClassificationRequest, WoundClosureClassificationResponse

__all__ = [
    "BmiCalculatorRequest",
    "BmiCalculatorResponse",
    "BodyRoundnessIndexRequest",
    "BodyRoundnessIndexResponse",
    "FatFreeMassRequest",
    "FatFreeMassResponse",
    "HospitalScoreRequest",
    "HospitalScoreResponse",
    "IdealBodyWeightAdjustedRequest",
    "IdealBodyWeightAdjustedResponse",
    "MmeCalculatorRequest",
    "MmeCalculatorResponse",
    "SurgicalApgarScoreRequest",
    "SurgicalApgarScoreResponse",
    "VisualAcuityTestingSnellenChartRequest",
    "VisualAcuityTestingSnellenChartResponse",
    "WoundClosureClassificationRequest",
    "WoundClosureClassificationResponse"
]