"""
Anesthesiology Score Models

Models for anesthesiology-related clinical scores and calculators.
"""

# Import the Apfel Score models
from .apfel_score_ponv import ApfelScorePonvRequest, ApfelScorePonvResponse

# Import the ARISCAT Score models
from .ariscat_score import AriscatScoreRequest, AriscatScoreResponse

# Import the ASA Physical Status models
from .asa_physical_status import AsaPhysicalStatusRequest, AsaPhysicalStatusResponse

# Export all models
__all__ = [
    "ApfelScorePonvRequest",
    "ApfelScorePonvResponse",
    "AriscatScoreRequest",
    "AriscatScoreResponse",
    "AsaPhysicalStatusRequest",
    "AsaPhysicalStatusResponse",
]
