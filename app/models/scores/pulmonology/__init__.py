"""
Pulmonology score models
"""

from .curb65 import Curb65Request, Curb65Response
from .sixminutewalk import SixMinuteWalkRequest, SixMinuteWalkResponse
from .aao2gradient import AAO2GradientRequest, AAO2GradientResponse

__all__ = [
    "Curb65Request",
    "Curb65Response",
    "SixMinuteWalkRequest",
    "SixMinuteWalkResponse",
    "AAO2GradientRequest",
    "AAO2GradientResponse",
]
