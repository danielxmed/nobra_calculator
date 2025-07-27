"""
Pulmonology score models
"""

from .curb65 import Curb65Request, Curb65Response
from .six_minute_walk import SixMinuteWalkRequest, SixMinuteWalkResponse
from .aa_o2_gradient import AAO2GradientRequest, AAO2GradientResponse

__all__ = [
    "Curb65Request",
    "Curb65Response",
    "SixMinuteWalkRequest",
    "SixMinuteWalkResponse",
    "AAO2GradientRequest",
    "AAO2GradientResponse",
]
