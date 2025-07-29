"""
General medical calculator models
"""

from .bmi_calculator import BmiCalculatorRequest, BmiCalculatorResponse
from .body_roundness_index import BodyRoundnessIndexRequest, BodyRoundnessIndexResponse

__all__ = [
    "BmiCalculatorRequest",
    "BmiCalculatorResponse",
    "BodyRoundnessIndexRequest",
    "BodyRoundnessIndexResponse",
]