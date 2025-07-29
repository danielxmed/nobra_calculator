"""
Emergency score models
"""

from .four_c_mortality import FourCMortalityRequest, FourCMortalityResponse
from .ais_inhalation_injury import AisInhalationInjuryRequest, AisInhalationInjuryResponse
from .emergency_medicine_coding_guide_2023 import EmergencyMedicineCodingGuide2023Request, EmergencyMedicineCodingGuide2023Response
from .abc_score import AbcScoreRequest, AbcScoreResponse
from .acep_ed_covid19_management_tool import (
    AcepEdCovid19ManagementToolRequest,
    AcepEdCovid19ManagementToolResponse,
)
from .acetaminophen_overdose_nac import (
    AcetaminophenOverdoseNacRequest,
    AcetaminophenOverdoseNacResponse,
)
from .adapt_protocol import AdaptProtocolRequest, AdaptProtocolResponse
from .age_adjusted_d_dimer import AgeAdjustedDDimerRequest, AgeAdjustedDDimerResponse
from .aims65 import Aims65Request, Aims65Response
from .alt_70_cellulitis import Alt70CellulitisRequest, Alt70CellulitisResponse
from .altitude_adjusted_perc import AltitudeAdjustedPercRequest, AltitudeAdjustedPercResponse
from .alvarado_score import AlvaradoScoreRequest, AlvaradoScoreResponse
from .antivenom_dosing_algorithm import AntivenomDosingAlgorithmRequest, AntivenomDosingAlgorithmResponse
from .apache_ii_score import ApacheIiScoreRequest, ApacheIiScoreResponse
from .air_score import AirScoreRequest, AirScoreResponse
from .abg_analyzer import AbgAnalyzerRequest, AbgAnalyzerResponse

__all__ = [
    "FourCMortalityRequest",
    "FourCMortalityResponse",
    "AisInhalationInjuryRequest",
    "AisInhalationInjuryResponse",
    "EmergencyMedicineCodingGuide2023Request",
    "EmergencyMedicineCodingGuide2023Response",
    "AbcScoreRequest",
    "AbcScoreResponse",
    "AcepEdCovid19ManagementToolRequest",
    "AcepEdCovid19ManagementToolResponse",
    "AcetaminophenOverdoseNacRequest",
    "AcetaminophenOverdoseNacResponse",
    "AdaptProtocolRequest",
    "AdaptProtocolResponse",
    "AgeAdjustedDDimerRequest",
    "AgeAdjustedDDimerResponse",
    "Aims65Request",
    "Aims65Response",
    "Alt70CellulitisRequest",
    "Alt70CellulitisResponse",
    "AltitudeAdjustedPercRequest",
    "AltitudeAdjustedPercResponse",
    "AlvaradoScoreRequest",
    "AlvaradoScoreResponse",
    "AntivenomDosingAlgorithmRequest",
    "AntivenomDosingAlgorithmResponse",
    "ApacheIiScoreRequest",
    "ApacheIiScoreResponse",
    "AirScoreRequest",
    "AirScoreResponse",
    "AbgAnalyzerRequest",
    "AbgAnalyzerResponse",
]
