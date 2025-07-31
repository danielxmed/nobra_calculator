"""
Pulmonology score models
"""

from .curb65 import Curb65Request, Curb65Response
from .six_minute_walk import SixMinuteWalkRequest, SixMinuteWalkResponse
from .aa_o2_gradient import AAO2GradientRequest, AAO2GradientResponse
from .four_peps import FourPepsRequest, FourPepsResponse
from .airq import AIRQRequest, AIRQResponse
from .bap_65 import Bap65Request, Bap65Response
from .berlin_criteria_ards import BerlinCriteriaArdsRequest, BerlinCriteriaArdsResponse
from .bode_index_copd import BodeIndexCopdRequest, BodeIndexCopdResponse
from .bova_score import BovaScoreRequest, BovaScoreResponse
from .cpis import CpisRequest, CpisResponse
from .copd_cat import CopdCatRequest, CopdCatResponse
from .crb_65_pneumonia_severity import Crb65PneumoniaSeverityRequest, Crb65PneumoniaSeverityResponse
from .decaf_score import DecafScoreRequest, DecafScoreResponse
from .du_bois_ipf_mortality import DuBoisIpfMortalityRequest, DuBoisIpfMortalityResponse
from .expected_peak_expiratory_flow import ExpectedPeakExpiratoryFlowRequest, ExpectedPeakExpiratoryFlowResponse

__all__ = [
    "Curb65Request",
    "Curb65Response",
    "SixMinuteWalkRequest",
    "SixMinuteWalkResponse",
    "AAO2GradientRequest",
    "AAO2GradientResponse",
    "FourPepsRequest",
    "FourPepsResponse",
    "AIRQRequest",
    "AIRQResponse",
    "Bap65Request",
    "Bap65Response",
    "BerlinCriteriaArdsRequest",
    "BerlinCriteriaArdsResponse",
    "BodeIndexCopdRequest",
    "BodeIndexCopdResponse",
    "BovaScoreRequest",
    "BovaScoreResponse",
    "CpisRequest",
    "CpisResponse",
    "CopdCatRequest",
    "CopdCatResponse",
    "Crb65PneumoniaSeverityRequest",
    "Crb65PneumoniaSeverityResponse",
    "DecafScoreRequest",
    "DecafScoreResponse",
    "DuBoisIpfMortalityRequest",
    "DuBoisIpfMortalityResponse",
    "ExpectedPeakExpiratoryFlowRequest",
    "ExpectedPeakExpiratoryFlowResponse",
]
