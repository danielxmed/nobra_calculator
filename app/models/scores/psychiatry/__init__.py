"""
Psychiatry score models
"""

from .aas import AasRequest, AasResponse
from .ace_score import AceScoreRequest, AceScoreResponse
from .aims import AimsRequest, AimsResponse

__all__ = [
    "AasRequest",
    "AasResponse",
    "AceScoreRequest",
    "AceScoreResponse",
    "AimsRequest",
    "AimsResponse",
]
