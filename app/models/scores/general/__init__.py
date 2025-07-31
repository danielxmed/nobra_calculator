"""
General medical calculator models
"""

from .bmi_calculator import BmiCalculatorRequest, BmiCalculatorResponse
from .body_roundness_index import BodyRoundnessIndexRequest, BodyRoundnessIndexResponse
from .fat_free_mass import FatFreeMassRequest, FatFreeMassResponse

__all__ = [
    "BmiCalculatorRequest",
    "BmiCalculatorResponse",
    "BodyRoundnessIndexRequest",
    "BodyRoundnessIndexResponse",
    "FatFreeMassRequest",
    "FatFreeMassResponse",
]