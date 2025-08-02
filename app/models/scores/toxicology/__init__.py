"""
Toxicology Score Models

This module contains request and response models for toxicology-related calculators.
"""

# Import score models here as they are created
from .atropine_dosing import AtropineDosingRequest, AtropineDosingResponse
from .estimated_ethanol_concentration import EstimatedEthanolConcentrationRequest, EstimatedEthanolConcentrationResponse
from .hiet import HietRequest, HietResponse, HietProtocol

__all__ = [
    "AtropineDosingRequest",
    "AtropineDosingResponse",
    "EstimatedEthanolConcentrationRequest",
    "EstimatedEthanolConcentrationResponse",
    "HietRequest",
    "HietResponse",
    "HietProtocol",
]