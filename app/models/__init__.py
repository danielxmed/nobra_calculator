"""
Modelos Pydantic para a API nobra_calculator
"""

from .score_models import (
    CKDEpi2021Request,
    CKDEpi2021Response,
    ScoreListResponse,
    ScoreMetadataResponse,
    ErrorResponse
)

__all__ = [
    "CKDEpi2021Request",
    "CKDEpi2021Response", 
    "ScoreListResponse",
    "ScoreMetadataResponse",
    "ErrorResponse"
]
