"""
Alc calculation models
"""

from pydantic import BaseModel, Field

# ALC Models
class AlcRequest(BaseModel):
    """
    Request model for Absolute Lymphocyte Count (ALC) calculation
    
    The Absolute Lymphocyte Count (ALC) is a critical hematological parameter used primarily 
    in HIV medicine to predict CD4+ T-cell count and assess immunological status. It serves 
    as a surrogate marker for immune function, particularly in resource-limited settings.
    
    **Clinical Applications**:
    - HIV disease monitoring and staging
    - Opportunistic infection risk assessment  
    - Immune reconstitution evaluation
    - Resource-limited settings where CD4 testing unavailable
    - Hematological malignancy monitoring
    - Immunodeficiency evaluation
    
    **Calculation Formula**:
    ALC = WBC count (cells/mm³) × (Lymphocyte percentage / 100)
    
    **Normal Range**: 1,300-3,500 cells/mm³
    
    **CD4 Prediction Utility**:
    - ALC <1,000: High likelihood CD4 <200 cells/mm³
    - ALC ≥2,000: High likelihood CD4 ≥200 cells/mm³  
    - ALC 1,000-2,000: Indeterminate zone, direct CD4 needed
    
    **Clinical Significance**:
    - Strong predictor of opportunistic infections in HIV
    - Guides timing of prophylaxis initiation
    - Monitoring response to antiretroviral therapy
    - Assessment of immune recovery
    
    **References**:
    - Spacek LA, et al. Diagnostic accuracy of the absolute lymphocyte count in predicting CD4 count. J Acquir Immune Defic Syndr. 2006;42(5):595-601.
    - Balakrishnan P, et al. An inexpensive, simple, and manual method of CD4 T-cell quantitation in HIV-infected individuals for use in developing countries. J Acquir Immune Defic Syndr. 2004;36(5):1006-10.
    """
    white_blood_cells: float = Field(
        ..., 
        ge=0.1, 
        le=500.0, 
        description="White blood cell count in × 10³/μL. Normal range: 4.0-11.0 × 10³/μL. Values outside this range may indicate infection, hematological disorders, or medication effects."
    )
    lymphocyte_percentage: float = Field(
        ..., 
        ge=0.0, 
        le=100.0, 
        description="Lymphocyte percentage from complete blood count differential. Normal range: 20-40%. Low percentages may indicate immunosuppression, viral infections, or steroid use."
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "white_blood_cells": 6.5,
                "lymphocyte_percentage": 25.0
            }
        }


class AlcResponse(BaseModel):
    """
    Response model for Absolute Lymphocyte Count (ALC) calculation
    
    Provides comprehensive lymphocyte count assessment with CD4 prediction utility
    for HIV monitoring and immunological status evaluation.
    
    **Interpretation Ranges**:
    - <1,000 cells/mm³: Low CD4 likely (<200), high infection risk
    - 1,000-2,000 cells/mm³: Indeterminate zone, direct CD4 needed
    - ≥2,000 cells/mm³: Adequate CD4 likely (≥200), lower infection risk
    - Normal range: 1,300-3,500 cells/mm³
    
    **Clinical Decision Points**:
    - ALC <1,000: Consider opportunistic infection prophylaxis
    - ALC 1,000-2,000: Obtain direct CD4 count for accurate assessment
    - ALC ≥2,000: Continue routine HIV monitoring
    """
    result: float = Field(
        ..., 
        description="Calculated absolute lymphocyte count in cells/mm³ (× 10³/μL). Used as surrogate marker for CD4+ T-cell count in HIV patients."
    )
    unit: str = Field(
        ..., 
        description="Unit of measurement for the lymphocyte count"
    )
    interpretation: str = Field(
        ..., 
        description="Evidence-based clinical interpretation with CD4 prediction and infection risk assessment. Includes recommendations for monitoring and prophylaxis."
    )
    stage: str = Field(
        ..., 
        description="Classification category based on CD4 prediction utility (Low CD4, Indeterminate Zone, Adequate CD4, Normal)"
    )
    stage_description: str = Field(
        ..., 
        description="Detailed description of the lymphocyte count status with CD4 correlation"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 1625,
                "unit": "cells/mm³",
                "interpretation": "Indeterminate range for CD4 prediction. Specific CD4 count is necessary for accurate immunological status assessment.",
                "stage": "Indeterminate Zone", 
                "stage_description": "CD4 indeterminate"
            }
        }