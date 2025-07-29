"""
Rheumatology score models
"""

from .asdas_crp import AsdasCrpRequest, AsdasCrpResponse
from .asdas_esr import AsdasEsrRequest, AsdasEsrResponse
from .asas_axial_spa_criteria import AsasAxialSpaCriteriaRequest, AsasAxialSpaCriteriaResponse
from .asas_peripheral_spa_criteria import AsasPeripheralSpaCriteriaRequest, AsasPeripheralSpaCriteriaResponse

__all__ = [
    "AsdasCrpRequest",
    "AsdasCrpResponse",
    "AsdasEsrRequest",
    "AsdasEsrResponse",
    "AsasAxialSpaCriteriaRequest",
    "AsasAxialSpaCriteriaResponse",
    "AsasPeripheralSpaCriteriaRequest",
    "AsasPeripheralSpaCriteriaResponse"
]
