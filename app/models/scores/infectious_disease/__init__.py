"""
Infectious_Disease score models
"""

from .helps2b import Helps2bRequest, Helps2bResponse
from .duke_iscvid_2023 import DukeIscvid2023Request, DukeIscvid2023Response
from .atlas_score import AtlasScoreRequest, AtlasScoreResponse
from .bacterial_meningitis_score import BacterialMeningitisScoreRequest, BacterialMeningitisScoreResponse

__all__ = [
    "Helps2bRequest",
    "Helps2bResponse",
    "DukeIscvid2023Request",
    "DukeIscvid2023Response",
    "AtlasScoreRequest",
    "AtlasScoreResponse",
    "BacterialMeningitisScoreRequest",
    "BacterialMeningitisScoreResponse",
]
