"""
Anc calculation models
"""

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class AncRequest(BaseModel):
    """
    Request model for Absolute Neutrophil Count (ANC) calculation
    
    The Absolute Neutrophil Count (ANC) is a critical hematological parameter used to assess 
    neutropenia and infection risk, particularly in oncology, hematology, and immunocompromised 
    patients. It is essential for determining chemotherapy safety and infection prophylaxis needs.
    
    **Clinical Applications**:
    - Neutropenia classification and grading
    - Chemotherapy safety assessment
    - Febrile neutropenia risk stratification
    - Infection prophylaxis decision-making
    - Bone marrow function evaluation
    - Drug-induced neutropenia monitoring
    
    **Calculation Formula**:
    ANC = WBC count × [(% Segmented Neutrophils + % Band Neutrophils) / 100]
    
    **Normal Range**: 1,500-8,000 cells/mm³
    
    **Neutropenia Classification**:
    - Mild: 1,000-1,500 cells/mm³ (Grade 2)
    - Moderate: 500-1,000 cells/mm³ (Grade 3)  
    - Severe: <500 cells/mm³ (Grade 4)
    
    **Clinical Significance**:
    - ANC <500: Very high infection risk, protective isolation
    - ANC 500-1,000: High infection risk, strict precautions
    - ANC 1,000-1,500: Moderate risk, basic precautions
    - ANC >1,500: Normal infection risk
    
    **References**:
    - National Cancer Institute. Common Terminology Criteria for Adverse Events (CTCAE) v5.0.
    - Crawford J, et al. Hematopoietic growth factors: ESMO Clinical Practice Guidelines. Ann Oncol. 2010;21(Suppl 5):v248-51.
    """
    white_blood_cells: float = Field(
        ..., 
        ge=0.1, 
        le=500.0, 
        description="White blood cell count in × 10³/μL. Normal range: 4.0-11.0 × 10³/μL. Critical for calculating absolute neutrophil count."
    )
    neutrophil_percentage: float = Field(
        ..., 
        ge=0.0, 
        le=100.0, 
        description="Segmented neutrophil percentage from CBC differential. Normal range: 50-70%. Mature neutrophils that provide primary bacterial defense."
    )
    band_percentage: Optional[float] = Field(
        0.0, 
        ge=0.0, 
        le=100.0, 
        description="Band neutrophil percentage (immature neutrophils). Normal range: 0-5%. Elevated bands may indicate bacterial infection or left shift."
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "white_blood_cells": 6.5,
                "neutrophil_percentage": 60.0,
                "band_percentage": 5.0
            }
        }


class AncResponse(BaseModel):
    """
    Response model for Absolute Neutrophil Count (ANC) calculation
    
    Provides comprehensive neutropenia assessment with infection risk stratification
    and clinical management recommendations based on current oncology guidelines.
    
    **Neutropenia Grading (CTCAE v5.0)**:
    - Grade 1: 1,500-2,000 cells/mm³ (Lower limit of normal)
    - Grade 2: 1,000-1,500 cells/mm³ (Mild neutropenia)
    - Grade 3: 500-1,000 cells/mm³ (Moderate neutropenia)
    - Grade 4: <500 cells/mm³ (Severe neutropenia)
    
    **Infection Risk Stratification**:
    - ANC <500: Very high risk (protective isolation, G-CSF, prophylaxis)
    - ANC 500-1,000: High risk (strict precautions, consider prophylaxis)
    - ANC 1,000-1,500: Moderate risk (basic precautions, monitoring)
    - ANC >1,500: Low risk (routine care)
    
    **Clinical Management**:
    - Severe neutropenia: Consider G-CSF, antimicrobial prophylaxis
    - Febrile neutropenia: Medical emergency requiring immediate antibiotics
    - Chemotherapy modification: Dose reduction or delay if ANC <1,000
    """
    result: float = Field(
        ..., 
        description="Calculated absolute neutrophil count in cells/mm³. Critical parameter for infection risk assessment and chemotherapy safety."
    )
    unit: str = Field(
        ..., 
        description="Unit of measurement for neutrophil count"
    )
    interpretation: str = Field(
        ..., 
        description="Evidence-based clinical interpretation with neutropenia grading, infection risk assessment, and management recommendations."
    )
    stage: str = Field(
        ..., 
        description="Neutropenia classification (Normal, Mild, Moderate, Severe) based on CTCAE criteria"
    )
    stage_description: str = Field(
        ..., 
        description="Detailed description of neutropenia severity with clinical implications"
    )
    infection_risk: str = Field(
        ..., 
        description="Infection risk level (Normal, Moderate, High, Very High) with corresponding precautions"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 4225,
                "unit": "cells/mm³",
                "interpretation": "Neutrophil count within normal range (1500-8000 cells/mm³). Infection risk not increased by neutropenia.",
                "stage": "Normal",
                "stage_description": "Normal count",
                "infection_risk": "normal"
            }
        }
