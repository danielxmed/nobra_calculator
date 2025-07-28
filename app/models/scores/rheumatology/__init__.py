"""
Rheumatology score models
"""

from .eular_acr_pmr import EularAcrPmrRequest, EularAcrPmrResponse
from .acr_eular_2010_ra import AcrEular2010RaRequest, AcrEular2010RaResponse
from .acr_eular_gout import AcrEularGoutRequest, AcrEularGoutResponse
from .acute_gout_diagnosis_rule import AcuteGoutDiagnosisRuleRequest, AcuteGoutDiagnosisRuleResponse

__all__ = [
    "EularAcrPmrRequest",
    "EularAcrPmrResponse",
    "AcrEular2010RaRequest",
    "AcrEular2010RaResponse",
    "AcrEularGoutRequest",
    "AcrEularGoutResponse",
    "AcuteGoutDiagnosisRuleRequest",
    "AcuteGoutDiagnosisRuleResponse"
]
