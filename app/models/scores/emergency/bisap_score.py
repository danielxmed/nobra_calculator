"""
BISAP Score for Pancreatitis Mortality Models

Request and response models for BISAP Score calculation.

References (Vancouver style):
1. Wu BU, Johannes RS, Sun X, Tabak Y, Conwell DL, Banks PA. The early prediction of 
   mortality in acute pancreatitis: a large population-based study. Gut. 2008 Dec;57(12):1698-703.
2. Singh VK, Wu BU, Bollen TL, Repas K, Maurer R, Johannes RS, et al. A prospective 
   evaluation of the bedside index for severity in acute pancreatitis score in assessing 
   mortality and intermediate markers of severity in acute pancreatitis. Am J Gastroenterol. 
   2009 Apr;104(4):966-71.
3. Gao W, Yang HX, Ma CE. The Value of BISAP Score for Predicting Mortality and Severity 
   in Acute Pancreatitis: A Systematic Review and Meta-Analysis. PLoS One. 2015 Jun 22;10(6):e0130412.

The BISAP (Bedside Index for Severity in Acute Pancreatitis) score provides early 
identification of patients at increased risk for in-hospital mortality in acute pancreatitis.
"""

from pydantic import BaseModel, Field
from typing import Literal


class BisapScoreRequest(BaseModel):
    """
    Request model for BISAP Score for Pancreatitis Mortality
    
    The BISAP score consists of 5 variables (B-I-S-A-P), each worth 1 point:
    
    B - Blood Urea Nitrogen (BUN) > 25 mg/dL
    I - Impaired mental status or Glasgow Coma Scale (GCS) < 15
    S - SIRS (Systemic Inflammatory Response Syndrome) ≥2 criteria
    A - Age > 60 years
    P - Pleural effusion on imaging
    
    SIRS Criteria (≥2 required for positive):
    - Pulse > 90 beats per minute
    - Respirations > 20 per minute or PaCO2 < 32 mmHg
    - Temperature > 38°C or < 36°C
    - White blood cell count > 12,000 or < 4,000 cells/mm³, or > 10% immature neutrophils (bands)
    
    Score Interpretation:
    - 0-2 points: Low risk (mild pancreatitis, <2% mortality)
    - 3-5 points: High risk (severe pancreatitis, 15-20% mortality)
    
    The BISAP score was developed using data from ~18,000 cases and validated 
    in an additional 18,000 cases, demonstrating 56% sensitivity and 91% specificity 
    for mortality prediction at cutoff ≥3.
    """
    
    bun_elevated: Literal["yes", "no"] = Field(
        ...,
        description="Blood Urea Nitrogen (BUN) > 25 mg/dL. Elevated BUN indicates renal dysfunction and/or dehydration, common in severe pancreatitis",
        example="no"
    )
    
    impaired_mental_status: Literal["yes", "no"] = Field(
        ...,
        description="Impaired mental status or Glasgow Coma Scale (GCS) < 15. May indicate systemic complications or severe illness",
        example="no"
    )
    
    sirs_criteria: Literal["yes", "no"] = Field(
        ...,
        description="≥2 SIRS (Systemic Inflammatory Response Syndrome) criteria present. SIRS indicates systemic inflammatory response: pulse >90 bpm, respirations >20/min or PaCO2 <32 mmHg, temperature >38°C or <36°C, WBC >12,000 or <4,000 cells/mm³ or >10% bands",
        example="yes"
    )
    
    age_over_60: Literal["yes", "no"] = Field(
        ...,
        description="Patient age > 60 years. Advanced age is associated with increased mortality risk in acute pancreatitis",
        example="no"
    )
    
    pleural_effusion: Literal["yes", "no"] = Field(
        ...,
        description="Presence of pleural effusion on imaging (chest X-ray or CT scan). Indicates severe inflammatory response and possible complications",
        example="no"
    )
    
    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "title": "Low risk pancreatitis (BISAP = 1)",
                    "value": {
                        "bun_elevated": "no",
                        "impaired_mental_status": "no",
                        "sirs_criteria": "yes",
                        "age_over_60": "no",
                        "pleural_effusion": "no"
                    }
                },
                {
                    "title": "High risk pancreatitis (BISAP = 4)",
                    "value": {
                        "bun_elevated": "yes",
                        "impaired_mental_status": "yes",
                        "sirs_criteria": "yes",
                        "age_over_60": "yes",
                        "pleural_effusion": "no"
                    }
                },
                {
                    "title": "Maximum risk pancreatitis (BISAP = 5)",
                    "value": {
                        "bun_elevated": "yes",
                        "impaired_mental_status": "yes",
                        "sirs_criteria": "yes",
                        "age_over_60": "yes",
                        "pleural_effusion": "yes"
                    }
                }
            ]
        }


class BisapScoreResponse(BaseModel):
    """
    Response model for BISAP Score for Pancreatitis Mortality
    
    Returns the calculated BISAP score with detailed interpretation including:
    - Risk stratification (Low Risk: 0-2 points, High Risk: 3-5 points)
    - Mortality risk estimates (<2% for low risk, 15-20% for high risk)
    - Present criteria contributing to the score
    - Clinical management recommendations based on risk level
    
    The BISAP score provides early identification of high-risk patients who may 
    require intensive monitoring, ICU admission, and aggressive supportive care.
    """
    
    result: int = Field(
        ...,
        description="BISAP score (0-5 points). Each positive criterion contributes 1 point",
        ge=0,
        le=5,
        example=1
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Detailed clinical interpretation including risk level, mortality estimates, positive criteria, and management recommendations",
        example="BISAP score: 1/5 points. Low risk for mortality (<2% mortality rate). This suggests mild acute pancreatitis. Positive criteria: S - SIRS criteria (≥2 present). Management: Standard supportive care with fluid resuscitation, pain control, and nutritional support. Monitor for complications. Note: BISAP score should be used in conjunction with clinical judgment. The score has 56% sensitivity and 91% specificity for mortality prediction at cutoff ≥3."
    )
    
    stage: str = Field(
        ...,
        description="Risk classification (Low Risk or High Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Description of the risk level with mortality estimate",
        example="Mild acute pancreatitis with low mortality risk (<2%)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 1,
                "unit": "points",
                "interpretation": "BISAP score: 1/5 points. Low risk for mortality (<2% mortality rate). This suggests mild acute pancreatitis. Positive criteria: S - SIRS criteria (≥2 present). Management: Standard supportive care with fluid resuscitation, pain control, and nutritional support. Monitor for complications. Note: BISAP score should be used in conjunction with clinical judgment. The score has 56% sensitivity and 91% specificity for mortality prediction at cutoff ≥3.",
                "stage": "Low Risk",
                "stage_description": "Mild acute pancreatitis with low mortality risk (<2%)"
            }
        }