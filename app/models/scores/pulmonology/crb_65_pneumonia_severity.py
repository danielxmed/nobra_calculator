"""
CRB-65 Score for Pneumonia Severity Models

Request and response models for CRB-65 calculation.

References (Vancouver style):
1. Lim WS, van der Eerden MM, Laing R, Boersma WG, Karalus N, Town GI, et al. 
   Defining community acquired pneumonia severity on presentation to hospital: 
   an international derivation and validation study. Thorax. 2003;58(5):377-382. 
   doi:10.1136/thorax.58.5.377
2. Capelastegui A, España PP, Quintana JM, Areitio I, Gorordo I, Egurrola M, et al. 
   Validation of a predictive rule for the management of community-acquired pneumonia. 
   Eur Respir J. 2006;27(1):151-157.
3. McNally M, Curtain J, O'Brien KK, Dimitrov BD, Fahey T. Validity of British 
   Thoracic Society guidance (the CRB-65 rule) for predicting the severity of 
   pneumonia in general practice: systematic review and meta-analysis. 
   Br J Gen Pract. 2010;60(579):e423-433.

The CRB-65 score is a simplified clinical prediction rule for assessing severity 
of community-acquired pneumonia (CAP). It is derived from the CURB-65 score but 
excludes blood urea nitrogen measurement, making it particularly useful in primary 
care settings where laboratory tests may not be readily available.

The score uses 4 clinical criteria: Confusion, Respiratory rate ≥30/min, 
Blood pressure <90/<60 mmHg, and Age ≥65 years. Each criterion scores 1 point, 
with total scores ranging from 0-4 points, corresponding to different mortality 
risks and treatment recommendations.
"""

from pydantic import BaseModel, Field
from typing import Literal


class Crb65PneumoniaSeverityRequest(BaseModel):
    """
    Request model for CRB-65 Score for Pneumonia Severity
    
    The CRB-65 score uses 4 clinical criteria to assess pneumonia severity:
    
    Clinical Components (1 point each):
    - confusion: New onset confusion or altered mental status
    - respiratory_rate: Respiratory rate ≥30 breaths per minute
    - blood_pressure: Systolic <90 mmHg OR diastolic ≤60 mmHg
    - age: Age ≥65 years
    
    Score Interpretation:
    - 0 points: Very low risk (<1% mortality) - Home treatment appropriate
    - 1-2 points: Intermediate risk (1-10% mortality) - Consider hospital evaluation
    - 3-4 points: High risk (>10% mortality) - Hospital admission recommended
    
    Clinical Advantages:
    - No laboratory tests required (unlike CURB-65 which needs BUN)
    - Rapid assessment possible in primary care settings
    - Well-validated across multiple healthcare systems
    - Guides treatment location decisions (home vs. hospital vs. ICU)
    
    Clinical Applications:
    - Emergency department triage for pneumonia patients
    - Primary care decision-making for hospitalization
    - Resource allocation and bed management
    - Quality improvement initiatives for pneumonia care
    
    References (Vancouver style):
    1. Lim WS, van der Eerden MM, Laing R, Boersma WG, Karalus N, Town GI, et al. 
    Defining community acquired pneumonia severity on presentation to hospital: 
    an international derivation and validation study. Thorax. 2003;58(5):377-382. 
    doi:10.1136/thorax.58.5.377
    2. Capelastegui A, España PP, Quintana JM, Areitio I, Gorordo I, Egurrola M, et al. 
    Validation of a predictive rule for the management of community-acquired pneumonia. 
    Eur Respir J. 2006;27(1):151-157.
    3. McNally M, Curtain J, O'Brien KK, Dimitrov BD, Fahey T. Validity of British 
    Thoracic Society guidance (the CRB-65 rule) for predicting the severity of 
    pneumonia in general practice: systematic review and meta-analysis. 
    Br J Gen Pract. 2010;60(579):e423-433.
    """
    
    confusion: Literal["yes", "no"] = Field(
        ...,
        description="New onset confusion or altered mental status. Includes disorientation to person, place, or time. Scores 1 point if present",
        example="no"
    )
    
    respiratory_rate: Literal["<30", ">=30"] = Field(
        ...,
        description="Respiratory rate assessment. ≥30 breaths per minute scores 1 point. Normal adult respiratory rate is 12-20 breaths per minute",
        example=">=30"
    )
    
    blood_pressure: Literal["normal", "low"] = Field(
        ...,
        description="Blood pressure assessment. 'low' indicates systolic <90 mmHg OR diastolic ≤60 mmHg and scores 1 point. 'normal' indicates systolic ≥90 mmHg AND diastolic >60 mmHg",
        example="low"
    )
    
    age: Literal["<65", ">=65"] = Field(
        ...,
        description="Age category. Patients aged 65 years or older score 1 point. Age is a significant predictor of pneumonia mortality",
        example=">=65"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "confusion": "no",
                "respiratory_rate": ">=30",
                "blood_pressure": "low",
                "age": ">=65"
            }
        }


class Crb65PneumoniaSeverityResponse(BaseModel):
    """
    Response model for CRB-65 Score for Pneumonia Severity
    
    The CRB-65 score provides risk stratification for community-acquired pneumonia 
    to guide treatment decisions. It is particularly valuable in primary care and 
    emergency department settings for determining appropriate level of care.
    
    Risk Categories:
    - Score 0: Very low risk (<1% mortality) - Home treatment appropriate
    - Score 1-2: Intermediate risk (1-10% mortality) - Consider hospital evaluation
    - Score 3-4: High risk (>10% mortality) - Hospital admission recommended
    
    Clinical Benefits:
    - No laboratory tests required
    - Rapid bedside assessment
    - Evidence-based treatment guidance
    - Resource optimization
    
    Reference: Lim WS, et al. Thorax. 2003;58(5):377-382.
    """
    
    result: int = Field(
        ...,
        ge=0,
        le=4,
        description="Total CRB-65 score indicating pneumonia severity (0-4 points)",
        example=3
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the CRB-65 score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with treatment recommendations based on the CRB-65 score",
        example="CRB-65 score of 3 indicates high risk pneumonia. Hospital admission is recommended with consideration for ICU assessment. 30-day mortality risk exceeds 10%. Patient requires intensive monitoring, aggressive treatment, and prompt evaluation for complications."
    )
    
    stage: str = Field(
        ...,
        description="Risk category classification (Low Risk, Intermediate Risk, High Risk)",
        example="High Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="High risk of mortality"
    )
    
    calculation_details: dict = Field(
        ...,
        description="Detailed breakdown of component scores and clinical recommendations",
        example={
            "component_scores": {
                "confusion": 0,
                "respiratory_rate": 1,
                "blood_pressure": 1,
                "age": 1
            },
            "risk_assessment": "High risk requiring intensive monitoring and treatment",
            "treatment_recommendation": "Hospital admission recommended, consider ICU assessment",
            "mortality_risk": "30-day mortality risk >10%",
            "clinical_setting": "Inpatient admission with potential ICU evaluation"
        }
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 3,
                "unit": "points",
                "interpretation": "CRB-65 score of 3 indicates high risk pneumonia. Hospital admission is recommended with consideration for ICU assessment. 30-day mortality risk exceeds 10%. Patient requires intensive monitoring, aggressive treatment, and prompt evaluation for complications.",
                "stage": "High Risk",
                "stage_description": "High risk of mortality",
                "calculation_details": {
                    "component_scores": {
                        "confusion": 0,
                        "respiratory_rate": 1,
                        "blood_pressure": 1,
                        "age": 1
                    },
                    "risk_assessment": "High risk requiring intensive monitoring and treatment",
                    "treatment_recommendation": "Hospital admission recommended, consider ICU assessment",
                    "mortality_risk": "30-day mortality risk >10%",
                    "clinical_setting": "Inpatient admission with potential ICU evaluation"
                }
            }
        }