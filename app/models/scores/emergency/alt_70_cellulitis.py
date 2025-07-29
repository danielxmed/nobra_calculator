"""
ALT-70 Score for Cellulitis Models

Request and response models for ALT-70 Score calculation.

References (Vancouver style):
1. Raff AB, Weng QY, Cohen JM, Gunasekera N, Okhovat JP, Vedak P, et al. A predictive 
   model for diagnosis of lower extremity cellulitis: a cross-sectional study. 
   J Am Acad Dermatol. 2017 Apr;76(4):618-625.e2. doi: 10.1016/j.jaad.2016.12.044.
2. Li DG, Dewan AK, Xia FD, Khosravi H, Joyce C, Mostaghimi A. The ALT-70 predictive 
   model outperforms thermal imaging for the diagnosis of lower extremity cellulitis: 
   a prospective evaluation. J Am Acad Dermatol. 2018 Dec;79(6):1076-1080.e1. 
   doi: 10.1016/j.jaad.2018.06.062.
3. Singer S, Li DG, Gunasekera N, Okhovat JP, Vedak P, Weng C, et al. The ALT-70 
   cellulitis model maintains predictive value at 24 and 48 hours after presentation. 
   J Am Acad Dermatol. 2019 Dec;81(6):1252-1256. doi: 10.1016/j.jaad.2019.04.008.
4. Weng QY, Raff AB, Cohen JM, Gunasekera N, Okhovat JP, Vedak P, et al. Costs and 
   Consequences Associated With Misdiagnosed Lower Extremity Cellulitis. JAMA Dermatol. 
   2017 Feb 1;153(2):141-146. doi: 10.1001/jamadermatol.2016.3816.

The ALT-70 Score is a validated clinical prediction rule that helps differentiate lower 
extremity cellulitis from its mimics (pseudocellulitis) in the emergency department. 
The score uses four simple clinical variables to stratify patients into risk categories, 
helping reduce the ~30% misdiagnosis rate of cellulitis. It has demonstrated 97.8% 
sensitivity and 47.6% specificity with a cutoff of ≥3 points.
"""

from pydantic import BaseModel, Field
from typing import Literal


class Alt70CellulitisRequest(BaseModel):
    """
    Request model for ALT-70 Score for Cellulitis
    
    The ALT-70 Score uses four clinical variables to predict cellulitis:
    
    Components (Maximum 7 points):
    - Asymmetric (unilateral) leg involvement: +3 points
    - Leukocytosis (WBC ≥10,000/µL): +1 point
    - Tachycardia (HR ≥90 bpm): +1 point
    - Age ≥70 years: +2 points
    
    The mnemonic ALT-70 stands for:
    - A: Asymmetric
    - L: Leukocytosis  
    - T: Tachycardia
    - 70: Age ≥70 years
    
    Exclusion Criteria (Do NOT use if patient has):
    - Visible abscess or fluctuance
    - Penetrating trauma
    - Burn injury
    - Diabetic ulcer
    - Hardware/device at the site
    - Post-operative patient (surgery within 30 days)
    - Recent IV antibiotic use (within 48 hours)
    - Known history of osteomyelitis
    
    The score was developed and validated specifically for use in the emergency 
    department setting for lower extremity presentations only.

    References (Vancouver style):
    1. Raff AB, Weng QY, Cohen JM, Gunasekera N, Okhovat JP, Vedak P, et al. A predictive 
    model for diagnosis of lower extremity cellulitis: a cross-sectional study. 
    J Am Acad Dermatol. 2017 Apr;76(4):618-625.e2. doi: 10.1016/j.jaad.2016.12.044.
    2. Li DG, Dewan AK, Xia FD, Khosravi H, Joyce C, Mostaghimi A. The ALT-70 predictive 
    model outperforms thermal imaging for the diagnosis of lower extremity cellulitis: 
    a prospective evaluation. J Am Acad Dermatol. 2018 Dec;79(6):1076-1080.e1. 
    doi: 10.1016/j.jaad.2018.06.062.
    """
    
    asymmetric: Literal["yes", "no"] = Field(
        ...,
        description="Asymmetric involvement (unilateral leg involvement). Common cellulitis mimics like venous stasis often present bilaterally. Scores +3 points if yes",
        example="yes"
    )
    
    leukocytosis: Literal["yes", "no"] = Field(
        ...,
        description="Leukocytosis defined as white blood cell count ≥10,000/µL (≥10 × 10⁹/L). Suggests systemic inflammatory response. Scores +1 point if yes",
        example="no"
    )
    
    tachycardia: Literal["yes", "no"] = Field(
        ...,
        description="Tachycardia defined as heart rate ≥90 beats per minute measured in the emergency department. May indicate systemic response to infection. Scores +1 point if yes",
        example="yes"
    )
    
    age_70_or_older: Literal["yes", "no"] = Field(
        ...,
        description="Patient age ≥70 years. Older patients have increased risk of cellulitis and decreased risk of mimics. Scores +2 points if yes",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "asymmetric": "yes",
                "leukocytosis": "no",
                "tachycardia": "yes",
                "age_70_or_older": "no"
            }
        }


class Alt70CellulitisResponse(BaseModel):
    """
    Response model for ALT-70 Score for Cellulitis
    
    The ALT-70 Score stratifies patients into three risk categories:
    
    Score 0-2 (Low Risk): 
    - 9% likelihood of cellulitis (91% pseudocellulitis)
    - NPV 90.9%, PPV 9.1%
    - Recommend: Reassess diagnosis, consider mimics
    
    Score 3-4 (Indeterminate):
    - 72% likelihood of cellulitis
    - Neither rules in nor rules out
    - Recommend: Consider dermatology consultation
    
    Score 5-7 (High Risk):
    - 95% likelihood of cellulitis
    - PPV 95.1%, NPV 52.4%
    - Recommend: Treat empirically for cellulitis
    
    Common cellulitis mimics include:
    - Venous stasis dermatitis (most common)
    - Contact dermatitis
    - Superficial thrombophlebitis
    - Gout
    - Lymphedema
    - Deep venous thrombosis
    - Necrotizing fasciitis
    
    Reference: Raff AB, et al. J Am Acad Dermatol. 2017;76(4):618-625.e2.
    """
    
    result: int = Field(
        ...,
        ge=0,
        le=7,
        description="ALT-70 score calculated from clinical variables (range: 0-7 points)",
        example=4
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with likelihood percentage and recommended next steps",
        example="Indeterminate (72% likelihood of cellulitis). Consider dermatology or infectious disease consultation to improve diagnostic accuracy, as clinical features alone are insufficient to rule in or rule out cellulitis."
    )
    
    stage: str = Field(
        ...,
        description="Risk category classification (Cellulitis Unlikely, Indeterminate, or Cellulitis Likely)",
        example="Indeterminate"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the probability category",
        example="Moderate probability of cellulitis"
    )
    
    likelihood_percent: str = Field(
        ...,
        description="Percentage likelihood of cellulitis based on the score",
        example="72%"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 4,
                "unit": "points",
                "interpretation": "Indeterminate (72% likelihood of cellulitis). Consider dermatology or infectious disease consultation to improve diagnostic accuracy, as clinical features alone are insufficient to rule in or rule out cellulitis.",
                "stage": "Indeterminate",
                "stage_description": "Moderate probability of cellulitis",
                "likelihood_percent": "72%"
            }
        }