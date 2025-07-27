"""
Emergency score models
"""

from .four_c_mortality import FourCMortalityRequest, FourCMortalityResponse
from .ais_inhalation_injury import AisInhalationInjuryRequest, AisInhalationInjuryResponse
from .emergency_medicine_coding_guide_2023 import EmergencyMedicineCodingGuide2023Request, EmergencyMedicineCodingGuide2023Response
from .abc_score import AbcScoreRequest, AbcScoreResponse

__all__ = [
    "FourCMortalityRequest",
    "FourCMortalityResponse",
    "AisInhalationInjuryRequest",
    "AisInhalationInjuryResponse",
    "EmergencyMedicineCodingGuide2023Request",
    "EmergencyMedicineCodingGuide2023Response",
    "AbcScoreRequest",
    "AbcScoreResponse",
]
