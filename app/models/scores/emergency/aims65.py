"""
AIMS65 Score for Upper GI Bleeding Mortality Models

Request and response models for AIMS65 Score calculation.

References (Vancouver style):
1. Saltzman JR, Tabak YP, Hyett BH, Sun X, Travis AC, Johannes RS. A simple risk score 
   accurately predicts in-hospital mortality, length of stay, and cost in acute upper 
   GI bleeding. Gastrointest Endosc. 2011;74(6):1215-24. doi: 10.1016/j.gie.2011.07.049.
2. Hyett BH, Abougergi MS, Charpentier JP, Kumar NL, Brozovic S, Claggett BL, et al. 
   The AIMS65 score compared with the Glasgow-Blatchford score in predicting outcomes 
   in upper GI bleeding. Gastrointest Endosc. 2013;77(4):551-7. 
   doi: 10.1016/j.gie.2012.11.022.
3. Thandassery RB, Sharma M, John AK, Al-Ejji KM, Wani H, Sultan K, et al. Clinical 
   application of AIMS65 scores to predict outcomes in patients with upper gastrointestinal 
   hemorrhage. Clin Endosc. 2015;48(5):380-4. doi: 10.5946/ce.2015.48.5.380.
4. Park SW, Song YW, Tak DH, Ahn BM, Kang SH, Moon HS, et al. The AIMS65 score is a 
   useful predictor of mortality in patients with nonvariceal upper gastrointestinal 
   bleeding: urgent endoscopy in patients with high AIMS65 scores. Clin Endosc. 
   2015;48(6):522-7. doi: 10.5946/ce.2015.48.6.522.

The AIMS65 score is a simple, non-endoscopic risk stratification tool for predicting 
in-hospital mortality in patients with acute upper gastrointestinal bleeding. It consists 
of 5 components that can be rapidly assessed in the emergency department:

A - Albumin <3.0 g/dL (1 point)
I - INR >1.5 (1 point)
M - Mental status altered (1 point)
S - Systolic BP ≤90 mmHg (1 point)
65 - Age ≥65 years (1 point)

The score ranges from 0-5 points and has been validated in multiple studies, showing 
superior performance compared to other scoring systems in predicting mortality.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any


class Aims65Request(BaseModel):
    """
    Request model for AIMS65 Score for Upper GI Bleeding Mortality
    
    The AIMS65 score is a simple, non-endoscopic risk stratification tool that 
    predicts in-hospital mortality in patients with acute upper gastrointestinal 
    bleeding using 5 clinical variables that can be rapidly assessed.
    
    Components:
    - A: Albumin <3.0 g/dL (1 point)
    - I: INR >1.5 (1 point)
    - M: Mental status altered (1 point)
    - S: Systolic BP ≤90 mmHg (1 point)
    - 65: Age ≥65 years (1 point)
    
    Score Interpretation:
    - 0-1: Low risk (0.3-7.8% mortality)
    - 2: Moderate risk (~20% mortality)
    - 3-5: High risk (36-50% mortality)
    
    Clinical Applications:
    - Emergency department triage
    - Risk stratification for upper GI bleeding
    - Resource allocation decisions
    - Early identification of high-risk patients
    - Guidance for urgent endoscopy timing
    
    Advantages:
    - Simple and rapid calculation
    - No endoscopic findings required
    - Can be applied within 12 hours of admission
    - Superior to other scores for mortality prediction
    - Validated across multiple populations

    References (Vancouver style):
    1. Saltzman JR, Tabak YP, Hyett BH, Sun X, Travis AC, Johannes RS. A simple risk score 
    accurately predicts in-hospital mortality, length of stay, and cost in acute upper 
    GI bleeding. Gastrointest Endosc. 2011;74(6):1215-24. doi: 10.1016/j.gie.2011.07.049.
    2. Hyett BH, Abougergi MS, Charpentier JP, Kumar NL, Brozovic S, Claggett BL, et al. 
    The AIMS65 score compared with the Glasgow-Blatchford score in predicting outcomes 
    in upper GI bleeding. Gastrointest Endosc. 2013;77(4):551-7. 
    doi: 10.1016/j.gie.2012.11.022.
    3. Thandassery RB, Sharma M, John AK, Al-Ejji KM, Wani H, Sultan K, et al. Clinical 
    application of AIMS65 scores to predict outcomes in patients with upper gastrointestinal 
    hemorrhage. Clin Endosc. 2015;48(5):380-4. doi: 10.5946/ce.2015.48.5.380.
    4. Park SW, Song YW, Tak DH, Ahn BM, Kang SH, Moon HS, et al. The AIMS65 score is a 
    useful predictor of mortality in patients with nonvariceal upper gastrointestinal 
    bleeding: urgent endoscopy in patients with high AIMS65 scores. Clin Endosc. 
    2015;48(6):522-7. doi: 10.5946/ce.2015.48.6.522.
    """
    
    albumin: float = Field(
        ...,
        description="Serum albumin level in g/dL (A component: <3.0 g/dL = 1 point)",
        ge=1.0,
        le=6.0,
        example=2.5
    )
    
    inr: float = Field(
        ...,
        description="International Normalized Ratio (I component: >1.5 = 1 point)",
        ge=0.5,
        le=10.0,
        example=1.8
    )
    
    mental_status_altered: Literal["yes", "no"] = Field(
        ...,
        description="Altered mental status - confusion, disorientation, or altered consciousness (M component: altered = 1 point)",
        example="no"
    )
    
    systolic_bp: int = Field(
        ...,
        description="Systolic blood pressure in mmHg (S component: ≤90 mmHg = 1 point)",
        ge=50,
        le=250,
        example=85
    )
    
    age: int = Field(
        ...,
        description="Patient age in years (65 component: ≥65 years = 1 point)",
        ge=18,
        le=120,
        example=72
    )
    
    class Config:
        schema_extra = {
            "example": {
                "albumin": 2.5,
                "inr": 1.8,
                "mental_status_altered": "no",
                "systolic_bp": 85,
                "age": 72
            }
        }


class Aims65Response(BaseModel):
    """
    Response model for AIMS65 Score for Upper GI Bleeding Mortality
    
    The response provides the calculated AIMS65 score with detailed clinical 
    interpretation and risk stratification for in-hospital mortality in patients 
    with upper gastrointestinal bleeding.
    
    Score Interpretation:
    - 0-1 points: Low risk (0.3-7.8% mortality)
      * Consider outpatient management or early discharge
      * Routine monitoring may be sufficient
    
    - 2 points: Moderate risk (~20% mortality)
      * Consider inpatient monitoring and early endoscopy
      * Increased vigilance required
    
    - 3-5 points: High risk (36-50% mortality)
      * Requires intensive monitoring and urgent endoscopy
      * Consider ICU admission and aggressive management
    
    Clinical Decision Support:
    - Emergency department triage
    - Resource allocation
    - Timing of endoscopic intervention
    - Need for intensive care monitoring
    - Risk communication with patients/families
    
    Important Notes:
    - Score ≥2 indicates need for urgent intervention
    - Can be calculated early without endoscopic findings
    - Superior to other scores for mortality prediction
    - Should be used with clinical judgment
    
    Reference: Saltzman JR, et al. Gastrointest Endosc. 2011;74(6):1215-24.
    """
    
    result: int = Field(
        ...,
        description="AIMS65 score (0-5 points)",
        ge=0,
        le=5,
        example=4
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with risk assessment and management recommendations",
        example="AIMS65 score: 4/5 points (High Risk). Estimated in-hospital mortality risk: 40.0%. Positive criteria: Albumin <3.0 g/dL, INR >1.5, Systolic BP ≤90 mmHg, Age ≥65 years. HIGH RISK: Requires intensive monitoring, urgent endoscopy, and aggressive management. Consider ICU admission and multidisciplinary care. AIMS65 score helps guide triage decisions and resource allocation in upper GI bleeding."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, Moderate Risk, High Risk)",
        example="High Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="High mortality risk"
    )
    
    components: Dict[str, int] = Field(
        ...,
        description="Individual component scores (0 or 1 for each)",
        example={
            "albumin_low": 1,
            "inr_elevated": 1,
            "mental_status_altered": 0,
            "systolic_bp_low": 1,
            "age_65_or_older": 1
        }
    )
    
    mortality_risk: float = Field(
        ...,
        description="Estimated in-hospital mortality risk percentage",
        example=40.0
    )
    
    risk_category: str = Field(
        ...,
        description="Overall risk category classification",
        example="High Risk"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 4,
                "unit": "points",
                "interpretation": "AIMS65 score: 4/5 points (High Risk). Estimated in-hospital mortality risk: 40.0%. Positive criteria: Albumin <3.0 g/dL, INR >1.5, Systolic BP ≤90 mmHg, Age ≥65 years. HIGH RISK: Requires intensive monitoring, urgent endoscopy, and aggressive management. Consider ICU admission and multidisciplinary care. AIMS65 score helps guide triage decisions and resource allocation in upper GI bleeding.",
                "stage": "High Risk",
                "stage_description": "High mortality risk",
                "components": {
                    "albumin_low": 1,
                    "inr_elevated": 1,
                    "mental_status_altered": 0,
                    "systolic_bp_low": 1,
                    "age_65_or_older": 1
                },
                "mortality_risk": 40.0,
                "risk_category": "High Risk"
            }
        }