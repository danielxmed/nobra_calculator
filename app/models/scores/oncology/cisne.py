"""
Clinical Index of Stable Febrile Neutropenia (CISNE) Models

Request and response models for CISNE calculation.

References (Vancouver style):
1. Carmona-Bayonas A, Gómez J, González-Billalabeitia E, Canteras M, Navarrete A, 
   Gonzálvez ML, et al. Prognostic evaluation of febrile neutropenia in apparently 
   stable adult cancer patients. Br J Cancer. 2011 Aug 23;105(5):612-7. 
   doi: 10.1038/bjc.2011.284.
2. Carmona-Bayonas A, Jiménez-Fonseca P, Virizuela Echaburu J, Antonio M, Font C, 
   Biosca M, et al. Prediction of serious complications in patients with seemingly 
   stable febrile neutropenia: validation of the Clinical Index of Stable Febrile 
   Neutropenia in a prospective cohort of patients from the FINITE study. J Clin 
   Oncol. 2015 Feb 10;33(5):465-71. doi: 10.1200/JCO.2014.57.2347.

The CISNE score identifies febrile neutropenia patients at low risk for serious 
complications, allowing for potential outpatient management in selected cases.
"""

from pydantic import BaseModel, Field
from typing import Literal


class CisneRequest(BaseModel):
    """
    Request model for Clinical Index of Stable Febrile Neutropenia (CISNE)
    
    The CISNE score is used for stable adult outpatients with:
    - Solid tumor
    - Fever ≥38°C (100.4°F) over 1 hour
    - Neutropenia (≤500 cells/mm³ or ≤1,000 cells/mm³ with expected decrease to 500)
    
    Scoring (0-8 points total):
    - ECOG Performance Status ≥2: 2 points
    - Stress-induced hyperglycemia: 2 points
    - COPD: 1 point
    - Cardiovascular disease: 1 point
    - NCI mucositis grade ≥2: 1 point
    - Monocytes <200/µL: 1 point
    
    Note: This tool should NOT be used in patients who are considered high risk 
    on initial assessment (hemodynamically unstable, severe infection signs, etc.)
    
    References (Vancouver style):
    1. Carmona-Bayonas A, Gómez J, González-Billalabeitia E, Canteras M, Navarrete A, 
       Gonzálvez ML, et al. Prognostic evaluation of febrile neutropenia in apparently 
       stable adult cancer patients. Br J Cancer. 2011 Aug 23;105(5):612-7. 
       doi: 10.1038/bjc.2011.284.
    """
    
    ecog_performance_status: Literal["<2", "≥2"] = Field(
        ...,
        description="ECOG Performance Status. <2 means fully active to restricted in physically strenuous activity. ≥2 means ambulatory and capable of self-care or worse. Scores 2 points if ≥2",
        example="<2"
    )
    
    stress_induced_hyperglycemia: Literal["yes", "no"] = Field(
        ...,
        description="Stress-induced hyperglycemia defined as glucose >250 mg/dL (>13.9 mmol/L) without diabetes, or glucose >121 mg/dL (>6.7 mmol/L) with diabetes. Scores 2 points if yes",
        example="no"
    )
    
    copd: Literal["yes", "no"] = Field(
        ...,
        description="Chronic obstructive pulmonary disease (COPD) diagnosis. Scores 1 point if yes",
        example="no"
    )
    
    cardiovascular_disease: Literal["yes", "no"] = Field(
        ...,
        description="History of cardiovascular disease including heart failure, ischemic heart disease, or arrhythmia. Scores 1 point if yes",
        example="no"
    )
    
    nci_mucositis_grade: Literal["yes", "no"] = Field(
        ...,
        description="NCI mucositis grade ≥2 (moderate to severe mucositis with painful erythema, edema, or ulcers but able to eat or swallow). Scores 1 point if yes",
        example="no"
    )
    
    monocytes: Literal["≥200/µL", "<200/µL"] = Field(
        ...,
        description="Monocyte count. Scores 1 point if <200/µL",
        example="≥200/µL"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "ecog_performance_status": "<2",
                "stress_induced_hyperglycemia": "no",
                "copd": "no",
                "cardiovascular_disease": "no",
                "nci_mucositis_grade": "no",
                "monocytes": "≥200/µL"
            }
        }


class CisneResponse(BaseModel):
    """
    Response model for Clinical Index of Stable Febrile Neutropenia (CISNE)
    
    The CISNE score stratifies patients into three risk categories:
    - Low risk (0 points): 1.1% complication rate
    - Intermediate risk (1-2 points): 6.2% complication rate  
    - High risk (≥3 points): 36% complication rate
    
    Complications include: hypotension, acute organ failure, arrhythmia, 
    major bleeding, acute abdomen, DIC, delirium
    
    Reference: Carmona-Bayonas A, et al. J Clin Oncol. 2015;33(5):465-71.
    """
    
    result: int = Field(
        ...,
        description="CISNE score (0-8 points)",
        example=0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and management recommendations based on risk category",
        example="Low risk of complications (1.1%). May be appropriate for outpatient management with close monitoring."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low, Intermediate, or High)",
        example="Low"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Low risk"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 0,
                "unit": "points",
                "interpretation": "Low risk of complications (1.1%). May be appropriate for outpatient management with close monitoring.",
                "stage": "Low",
                "stage_description": "Low risk"
            }
        }