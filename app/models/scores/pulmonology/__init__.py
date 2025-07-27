"""
Pulmonology score models
"""

from .curb65 import Curb65Request, Curb65Response
from .six_minute_walk import SixMinuteWalkRequest, SixMinuteWalkResponse
from .aa_o2_gradient import AAO2GradientRequest, AAO2GradientResponse
from .four_peps import FourPepsRequest, FourPepsResponse

__all__ = [
    "Curb65Request",
    "Curb65Response",
    "SixMinuteWalkRequest",
    "SixMinuteWalkResponse",
    "AAO2GradientRequest",
    "AAO2GradientResponse",
    "FourPepsRequest",
    "FourPepsResponse",
]
