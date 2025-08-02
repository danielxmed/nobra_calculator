"""
Dermatology score models
"""

from .eczema_area_severity_index import EczemaAreaSeverityIndexRequest, EczemaAreaSeverityIndexResponse
from .urticaria_activity_score import UrticariaActivityScoreRequest, UrticariaActivityScoreResponse

__all__ = [
    "EczemaAreaSeverityIndexRequest",
    "EczemaAreaSeverityIndexResponse",
    "UrticariaActivityScoreRequest",
    "UrticariaActivityScoreResponse",
]