"""
Neurology score models
"""

from .abcd2 import Abcd2Request, Abcd2Response
from .fourat import FourAtRequest, FourAtResponse

__all__ = [
    "Abcd2Request",
    "Abcd2Response",
    "FourAtRequest",
    "FourAtResponse",
]
