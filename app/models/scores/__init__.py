"""
Medical score models organized by specialty
"""

# Import all models from each specialty
from .nephrology import *
from .cardiology import *
from .pulmonology import *
from .neurology import *
from .hematology import *
from .emergency import *
from .psychiatry import *
from .pediatrics import *
from .geriatrics import *
from .rheumatology import *
from .infectious_disease import *
from .oncology import *

# Import shared models
from ..shared import (
    ScoreListResponse,
    ScoreMetadataResponse,
    ErrorResponse,
    HealthResponse,
    SexType,
    YesNoType,
    HospitalizationFrequencyType
)

# Re-export everything
__all__ = [
    # Nephrology
    "CKDEpi2021Request",
    "CKDEpi2021Response", 
    "AbicScoreRequest",
    "AbicScoreResponse",
    
    # Cardiology
    "Cha2ds2VascRequest",
    "Cha2ds2VascResponse",
    "AccAhaHfStagingRequest",
    "AccAhaHfStagingResponse",
    "AcefIiRequest",
    "AcefIiResponse",
    
    # Pulmonology
    "Curb65Request",
    "Curb65Response",
    "SixMinuteWalkRequest",
    "SixMinuteWalkResponse", 
    "AAO2GradientRequest",
    "AAO2GradientResponse",
    
    # Neurology
    "Abcd2Request",
    "Abcd2Response",
    "FourAtRequest",
    "FourAtResponse",
    
    # Hematology
    "FourTsRequest", 
    "FourTsResponse",
    "AlcRequest",
    "AlcResponse",
    "AncRequest",
    "AncResponse",
    
    # Emergency Medicine
    "FourCMortalityRequest",
    "FourCMortalityResponse",
    "AcepEdCovid19ManagementToolRequest",
    "AcepEdCovid19ManagementToolResponse",
    
    # Psychiatry
    "AasRequest",
    "AasResponse",
    "AimsRequest", 
    "AimsResponse",
    
    # Pediatrics
    "AapPediatricHypertensionRequest",
    "AapPediatricHypertensionResponse",
    
    # Geriatrics
    "AbbeyPainRequest",
    "AbbeyPainResponse",
    
    # Rheumatology
    "EularAcrPmrRequest",
    "EularAcrPmrResponse",
    
    # Infectious Disease
    "Helps2bRequest",
    "Helps2bResponse",
    
    # Oncology
    "Leibovich2018RccRequest",
    "Leibovich2018RccResponse",
    
    # Shared/Common
    "ScoreListResponse",
    "ScoreMetadataResponse", 
    "ErrorResponse",
    "HealthResponse",
    "SexType",
    "YesNoType",
    "HospitalizationFrequencyType"
]