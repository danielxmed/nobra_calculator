"""
Urology score models
"""

from .ipss_aua_si import IpssAuaSiRequest, IpssAuaSiResponse
from .gleason_score_prostate import GleasonScoreProstateRequest, GleasonScoreProstateResponse
from .fuhrman_nuclear_grade import FuhrmanNuclearGradeRequest, FuhrmanNuclearGradeResponse

__all__ = [
    "IpssAuaSiRequest",
    "IpssAuaSiResponse",
    "GleasonScoreProstateRequest",
    "GleasonScoreProstateResponse",
    "FuhrmanNuclearGradeRequest",
    "FuhrmanNuclearGradeResponse"
]