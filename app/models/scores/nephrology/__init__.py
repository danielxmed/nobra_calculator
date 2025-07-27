"""
Nephrology score models
"""

from .ckd_epi_2021 import CKDEpi2021Request, CKDEpi2021Response
from .abic_score import AbicScoreRequest, AbicScoreResponse

__all__ = [
    "CKDEpi2021Request",
    "CKDEpi2021Response",
    "AbicScoreRequest",
    "AbicScoreResponse"
]