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
from .das28_crp import Das28CrpRequest, Das28CrpResponse
from .das28_esr import Das28EsrRequest, Das28EsrResponse
from .orai import OraiRequest, OraiResponse
from .ost import OstRequest, OstResponse
from .fracture_index import FractureIndexRequest, FractureIndexResponse

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
    "CdaiRheumatoidArthritisResponse",
    "Das28CrpRequest",
    "Das28CrpResponse",
    "Das28EsrRequest",
    "Das28EsrResponse",
    "OraiRequest",
    "OraiResponse",
    "OstRequest",
    "OstResponse",
    "FractureIndexRequest",
    "FractureIndexResponse"
]
