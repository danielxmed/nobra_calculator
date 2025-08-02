"""
Trauma Score and Injury Severity Score (TRISS) Models

Request and response models for TRISS calculation.

References (Vancouver style):
1. Boyd CR, Tolson MA, Copes WS. Evaluating trauma care: the TRISS method. 
   Trauma Score and the Injury Severity Score. J Trauma. 1987 Apr;27(4):370-8. 
   PMID: 3106646.
2. Champion HR, Copes WS, Sacco WJ, Lawnick MM, Keast SL, Bain LW Jr, et al. 
   The Major Trauma Outcome Study: establishing national norms for trauma care. 
   J Trauma. 1990 Nov;30(11):1356-65. PMID: 2231804.
3. Schluter PJ. The Trauma and Injury Severity Score (TRISS) revised. 
   Injury. 2011 Jan;42(1):90-6. doi: 10.1016/j.injury.2010.08.040.

The TRISS methodology combines physiological (Revised Trauma Score) and anatomical 
(Injury Severity Score) indices with patient age to predict probability of survival 
in trauma patients. It is primarily used for quality assurance and benchmarking 
in trauma care systems.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal


class TrissRequest(BaseModel):
    """
    Request model for Trauma Score and Injury Severity Score (TRISS)
    
    TRISS estimates probability of survival using:
    - Trauma mechanism (blunt vs penetrating)
    - Revised Trauma Score (RTS): physiological derangement
    - Injury Severity Score (ISS): anatomical injury severity
    - Age (dichotomized at 54 years)
    
    Formula: Probability = 1/(1 + e^(-b))
    where b = b0 + b1(RTS) + b2(ISS) + b3(Age factor)
    
    Coefficients differ between blunt and penetrating trauma:
    - Blunt: b0=-1.2470, b1=0.9544, b2=-0.0768, b3=-1.9052
    - Penetrating: b0=-0.6029, b1=1.1430, b2=-0.1516, b3=-2.6676
    
    References (Vancouver style):
    1. Boyd CR, Tolson MA, Copes WS. Evaluating trauma care: the TRISS method. 
       Trauma Score and the Injury Severity Score. J Trauma. 1987 Apr;27(4):370-8.
    2. Champion HR, Copes WS, Sacco WJ, Lawnick MM, Keast SL, Bain LW Jr, et al. 
       The Major Trauma Outcome Study: establishing national norms for trauma care. 
       J Trauma. 1990 Nov;30(11):1356-65.
    """
    
    trauma_type: Literal["blunt", "penetrating"] = Field(
        ...,
        description="Type of trauma mechanism. Blunt trauma includes motor vehicle crashes, "
                    "falls, and assault with blunt objects. Penetrating trauma includes "
                    "gunshot wounds, stab wounds, and impalement injuries.",
        example="blunt"
    )
    
    rts_score: float = Field(
        ...,
        ge=0,
        le=8,
        description="Revised Trauma Score (RTS). Calculated from Glasgow Coma Scale, "
                    "systolic blood pressure, and respiratory rate. Range 0-8, with "
                    "higher scores indicating better physiological status. Normal is 7.84.",
        example=6.5
    )
    
    iss_score: int = Field(
        ...,
        ge=0,
        le=75,
        description="Injury Severity Score (ISS). Sum of squares of three highest AIS scores "
                    "from different body regions. Range 0-75, with higher scores indicating "
                    "more severe anatomical injury. Score of 75 is automatically assigned "
                    "for any AIS 6 (unsurvivable) injury.",
        example=25
    )
    
    age_over_54: Literal["yes", "no"] = Field(
        ...,
        description="Whether patient is over 54 years old. Age dichotomization at 54 years "
                    "was determined from the original MTOS (Major Trauma Outcome Study) data.",
        example="no"
    )
    
    @field_validator('rts_score')
    @classmethod
    def validate_rts_score(cls, v: float) -> float:
        if not 0 <= v <= 8:
            raise ValueError("RTS score must be between 0 and 8")
        # RTS is typically calculated to 3 decimal places
        return round(v, 3)
    
    @field_validator('iss_score')
    @classmethod
    def validate_iss_score(cls, v: int) -> int:
        if not 0 <= v <= 75:
            raise ValueError("ISS score must be between 0 and 75")
        # ISS of 75 indicates unsurvivable injury (any AIS 6)
        return v
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "trauma_type": "blunt",
                "rts_score": 6.5,
                "iss_score": 25,
                "age_over_54": "no"
            }
        }
    }


class TrissResponse(BaseModel):
    """
    Response model for Trauma Score and Injury Severity Score (TRISS)
    
    Returns probability of survival as a percentage with clinical interpretation.
    TRISS is intended for quality assurance and benchmarking, not individual 
    patient prognostication.
    
    Interpretation categories:
    - Very High (≥90%): Continue aggressive trauma care
    - High (75-89%): Continue full resuscitation
    - Moderate (50-74%): Aggressive care with close monitoring
    - Low (25-49%): Consider goals of care discussion
    - Very Low (<25%): Critical condition, consider resource allocation
    
    Reference: Boyd CR, et al. J Trauma. 1987;27(4):370-8.
    """
    
    result: float = Field(
        ...,
        ge=0,
        le=100,
        description="Predicted probability of survival as a percentage (0-100%)",
        example=85.3
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement (percentage)",
        example="%"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of survival probability and recommendations",
        example="Patient has 85.3% probability of survival. Continue full trauma resuscitation and care."
    )
    
    stage: str = Field(
        ...,
        description="Survival probability category (Very High, High, Moderate, Low, Very Low)",
        example="High"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the survival probability category",
        example="High probability of survival"
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "result": 85.3,
                "unit": "%",
                "interpretation": "Patient has 85.3% probability of survival. Continue full trauma resuscitation and care.",
                "stage": "High",
                "stage_description": "High probability of survival"
            }
        }
    }