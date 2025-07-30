"""
Rheumatology score models
"""

from .asdas_crp import AsdasCrpRequest, AsdasCrpResponse
from .asdas_esr import AsdasEsrRequest, AsdasEsrResponse
from .asas_axial_spa_criteria import AsasAxialSpaCriteriaRequest, AsasAxialSpaCriteriaResponse
from .asas_peripheral_spa_criteria import AsasPeripheralSpaCriteriaRequest, AsasPeripheralSpaCriteriaResponse
from .caroc_system import CAROCSystemRequest, CAROCSystemResponse
from .caspar_criteria import CasparCriteriaRequest, CasparCriteriaResponse
from .cdai_rheumatoid_arthritis import CdaiRheumatoidArthritisRequest, CdaiRheumatoidArthritisResponse

__all__ = [
    "AsdasCrpRequest",
    "AsdasCrpResponse",
    "AsdasEsrRequest",
    "AsdasEsrResponse",
    "AsasAxialSpaCriteriaRequest",
    "AsasAxialSpaCriteriaResponse",
    "AsasPeripheralSpaCriteriaRequest",
    "AsasPeripheralSpaCriteriaResponse",
    "CAROCSystemRequest",
    "CAROCSystemResponse",
    "CasparCriteriaRequest",
    "CasparCriteriaResponse",
    "CdaiRheumatoidArthritisRequest",
    "CdaiRheumatoidArthritisResponse"
]
