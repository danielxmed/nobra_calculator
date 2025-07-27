"""
Geriatrics score models
"""

from .abbey_pain import AbbeyPainRequest, AbbeyPainResponse
from .amt_10 import Amt10Request, Amt10Response
from .amt_4 import Amt4Request, Amt4Response

__all__ = [
    "AbbeyPainRequest",
    "AbbeyPainResponse",
    "Amt10Request",
    "Amt10Response",
    "Amt4Request",
    "Amt4Response",
]
