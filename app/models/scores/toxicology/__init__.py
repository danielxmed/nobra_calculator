"""
Toxicology Score Models

This module contains request and response models for toxicology-related calculators.
"""

# Import score models here as they are created
from .atropine_dosing import AtropineDosingRequest, AtropineDosingResponse

__all__ = [
    "AtropineDosingRequest",
    "AtropineDosingResponse",
]