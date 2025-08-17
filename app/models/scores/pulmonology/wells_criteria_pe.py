"""
Wells' Criteria for Pulmonary Embolism Models

Request and response models for Wells' Criteria calculation.

References (Vancouver style):
1. Wells PS, Anderson DR, Rodger M, et al. Excluding pulmonary embolism at the bedside without
   diagnostic imaging: management of patients with suspected pulmonary embolism presenting to the
   emergency department by using a simple clinical model and D-dimer. Ann Intern Med. 2001;135(2):98-107.
2. van Belle A, Büller HR, Huisman MV, et al. Effectiveness of managing suspected pulmonary embolism
   using an algorithm combining clinical probability, D-dimer testing, and computed tomography. JAMA.
   2006;295(2):172-179.
3. Konstantinides SV, Meyer G, Becattini C, et al. 2019 ESC Guidelines for the diagnosis and management
   of acute pulmonary embolism. Eur Heart J. 2020;41(4):543-603.
"""

from pydantic import BaseModel, Field
from typing import Literal


class WellsCriteriaPeRequest(BaseModel):
    """
    Request model for Wells' Criteria for Pulmonary Embolism

    The Wells' Criteria uses seven clinical items to estimate pretest probability of PE.
    Supports both 3-tier (low/intermediate/high) and 2-tier (PE unlikely/likely) interpretations
    to guide D-dimer testing and imaging decisions.
    """

    clinical_signs_dvt: Literal["yes", "no"] = Field(
        ..., description="Clinical signs and symptoms of DVT (unilateral leg swelling and pain with deep venous palpation)", example="no"
    )
    pe_most_likely: Literal["yes", "no"] = Field(
        ..., description="Pulmonary embolism is the most likely diagnosis (alternative diagnosis less likely than PE)", example="yes"
    )
    heart_rate_over_100: Literal["yes", "no"] = Field(
        ..., description="Heart rate greater than 100 beats per minute", example="no"
    )
    immobilization_surgery_recent: Literal["yes", "no"] = Field(
        ..., description="Immobilization for ≥3 days or surgery within the previous 4 weeks", example="no"
    )
    previous_dvt_pe: Literal["yes", "no"] = Field(
        ..., description="Previous history of deep vein thrombosis or pulmonary embolism", example="no"
    )
    hemoptysis: Literal["yes", "no"] = Field(
        ..., description="Hemoptysis (coughing up blood)", example="no"
    )
    active_malignancy: Literal["yes", "no"] = Field(
        ..., description="Active cancer (treatment ongoing, within 6 months, or palliative)", example="no"
    )

    class Config:
        schema_extra = {
            "example": {
                "clinical_signs_dvt": "no",
                "pe_most_likely": "yes",
                "heart_rate_over_100": "no",
                "immobilization_surgery_recent": "no",
                "previous_dvt_pe": "no",
                "hemoptysis": "no",
                "active_malignancy": "no"
            }
        }


class WellsCriteriaPeResponse(BaseModel):
    """
    Response model for Wells' Criteria for Pulmonary Embolism

    Provides the calculated Wells score in points with both 3-tier and 2-tier classification and
    evidence-based interpretation guiding use of D-dimer and CT pulmonary angiography (CT-PA).
    """

    result: float = Field(
        ..., description="Wells' PE score (0-12.5 points)", ge=0.0, le=12.5, example=4.5
    )
    unit: str = Field(
        ..., description="Unit of measurement for the score", example="points"
    )
    interpretation: str = Field(
        ..., description="Clinical interpretation and recommended management based on 3-tier and 2-tier frameworks",
        example="Wells' Criteria: 4.5 points. Present risk factors: PE most likely diagnosis (3.0), previous DVT/PE (1.5). Intermediate clinical probability of pulmonary embolism. Two-tier classification: PE Likely. Management: Obtain D-dimer; if positive, proceed to CT-PA."
    )
    stage: str = Field(
        ..., description="3-tier classification (Low Risk, Intermediate Risk, High Risk)", example="Intermediate Risk"
    )
    stage_description: str = Field(
        ..., description="Brief description of 3-tier category", example="Intermediate clinical probability of PE"
    )
    two_tier: str = Field(
        ..., description="2-tier label (PE Unlikely vs PE Likely)", example="PE Likely"
    )

    class Config:
        schema_extra = {
            "example": {
                "result": 4.5,
                "unit": "points",
                "interpretation": "Wells' Criteria: 4.5 points. Present risk factors: PE most likely diagnosis (3.0), previous DVT/PE (1.5). Intermediate clinical probability of pulmonary embolism. Two-tier classification: PE Likely. Management: Obtain D-dimer; if positive, proceed to CT-PA.",
                "stage": "Intermediate Risk",
                "stage_description": "Intermediate clinical probability of PE",
                "two_tier": "PE Likely"
            }
        }

