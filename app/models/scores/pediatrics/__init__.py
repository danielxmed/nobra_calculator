"""
Pediatrics score models
"""

from .aap_pediatric_hypertension import AapPediatricHypertensionRequest, AapPediatricHypertensionResponse
from .apgar_score import ApgarScoreRequest, ApgarScoreResponse

__all__ = [
    "AapPediatricHypertensionRequest",
    "AapPediatricHypertensionResponse",
    "ApgarScoreRequest",
    "ApgarScoreResponse",
]
