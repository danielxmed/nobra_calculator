"""
National Early Warning Score (NEWS) Models

Request and response models for NEWS calculation.

References (Vancouver style):
1. Royal College of Physicians. National Early Warning Score (NEWS): Standardising 
   the assessment of acute-illness severity in the NHS. Report of a working party. 
   London: RCP, 2012.
2. Smith GB, Prytherch DR, Meredith P, Schmidt PE, Featherstone PI. The ability 
   of the National Early Warning Score (NEWS) to discriminate patients at risk of 
   early cardiac arrest, unanticipated intensive care unit admission, and death. 
   Resuscitation. 2013 Apr;84(4):465-70. doi: 10.1016/j.resuscitation.2012.12.016.
3. Prytherch DR, Smith GB, Schmidt PE, Featherstone PI. ViEWS--Towards a national 
   early warning score for detecting adult inpatient deterioration. Resuscitation. 
   2010 Aug;81(8):932-7. doi: 10.1016/j.resuscitation.2010.06.004.

The NEWS is a track-and-trigger early warning score system used to identify acutely 
ill patients, including those with sepsis, who require urgent intervention. It 
aggregates 7 physiological parameters into a single score to determine the degree 
of clinical risk and urgency of response needed.
"""

from pydantic import BaseModel, Field
from typing import Literal


class NewsRequest(BaseModel):
    """
    Request model for National Early Warning Score (NEWS)
    
    The NEWS uses 7 physiological parameters to assess acute illness severity:
    
    Respiratory Rate (breaths per minute):
    - ≤8: +3 points (dangerously low)
    - 9-11: +1 point (low)
    - 12-20: 0 points (normal)
    - 21-24: +2 points (elevated)
    - ≥25: +3 points (dangerously high)
    
    Oxygen Saturation (%):
    - ≤91: +3 points (severe hypoxemia)
    - 92-93: +2 points (moderate hypoxemia)
    - 94-95: +1 point (mild hypoxemia)
    - ≥96: 0 points (normal)
    
    Supplemental Oxygen:
    - No: 0 points
    - Yes: +2 points (indicates respiratory compromise)
    
    Temperature (°C):
    - ≤35.0: +3 points (severe hypothermia)
    - 35.1-36.0: +1 point (mild hypothermia)
    - 36.1-38.0: 0 points (normal)
    - 38.1-39.0: +1 point (mild fever)
    - ≥39.1: +2 points (high fever)
    
    Systolic Blood Pressure (mmHg):
    - ≤90: +3 points (severe hypotension)
    - 91-100: +2 points (moderate hypotension)
    - 101-110: +1 point (mild hypotension)
    - 111-219: 0 points (normal)
    - ≥220: +3 points (severe hypertension)
    
    Heart Rate (beats per minute):
    - ≤40: +3 points (severe bradycardia)
    - 41-50: +1 point (bradycardia)
    - 51-90: 0 points (normal)
    - 91-110: +1 point (mild tachycardia)
    - 111-130: +2 points (moderate tachycardia)
    - ≥131: +3 points (severe tachycardia)
    
    AVPU Score (neurological assessment):
    - Alert (A): 0 points (normal consciousness)
    - Voice/Pain/Unresponsive (V/P/U): +3 points (altered consciousness)

    References (Vancouver style):
    1. Royal College of Physicians. National Early Warning Score (NEWS): Standardising 
    the assessment of acute-illness severity in the NHS. Report of a working party. 
    London: RCP, 2012.
    2. Smith GB, Prytherch DR, Meredith P, Schmidt PE, Featherstone PI. The ability 
    of the National Early Warning Score (NEWS) to discriminate patients at risk of 
    early cardiac arrest, unanticipated intensive care unit admission, and death. 
    Resuscitation. 2013 Apr;84(4):465-70. doi: 10.1016/j.resuscitation.2012.12.016.
    """
    
    respiratory_rate: Literal["8_or_less", "9_to_11", "12_to_20", "21_to_24", "25_or_more"] = Field(
        ...,
        description="Respiratory rate in breaths per minute. ≤8 scores +3, 9-11 scores +1, 12-20 scores 0, 21-24 scores +2, ≥25 scores +3",
        example="12_to_20"
    )
    
    oxygen_saturation: Literal["91_or_less", "92_to_93", "94_to_95", "96_or_more"] = Field(
        ...,
        description="Oxygen saturation percentage. ≤91% scores +3, 92-93% scores +2, 94-95% scores +1, ≥96% scores 0",
        example="96_or_more"
    )
    
    supplemental_oxygen: Literal["yes", "no"] = Field(
        ...,
        description="Whether patient is receiving any supplemental oxygen. Yes scores +2, No scores 0",
        example="no"
    )
    
    temperature: Literal["35_or_less", "35_1_to_36", "36_1_to_38", "38_1_to_39", "39_1_or_more"] = Field(
        ...,
        description="Body temperature in °C. ≤35.0 scores +3, 35.1-36.0 scores +1, 36.1-38.0 scores 0, 38.1-39.0 scores +1, ≥39.1 scores +2",
        example="36_1_to_38"
    )
    
    systolic_bp: Literal["90_or_less", "91_to_100", "101_to_110", "111_to_219", "220_or_more"] = Field(
        ...,
        description="Systolic blood pressure in mmHg. ≤90 scores +3, 91-100 scores +2, 101-110 scores +1, 111-219 scores 0, ≥220 scores +3",
        example="111_to_219"
    )
    
    heart_rate: Literal["40_or_less", "41_to_50", "51_to_90", "91_to_110", "111_to_130", "131_or_more"] = Field(
        ...,
        description="Heart rate in beats per minute. ≤40 scores +3, 41-50 scores +1, 51-90 scores 0, 91-110 scores +1, 111-130 scores +2, ≥131 scores +3",
        example="51_to_90"
    )
    
    avpu_score: Literal["alert", "voice_pain_unresponsive"] = Field(
        ...,
        description="AVPU neurological assessment. Alert (A) scores 0, Voice/Pain/Unresponsive (V/P/U) scores +3",
        example="alert"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "respiratory_rate": "12_to_20",
                "oxygen_saturation": "96_or_more",
                "supplemental_oxygen": "no",
                "temperature": "36_1_to_38",
                "systolic_bp": "111_to_219",
                "heart_rate": "51_to_90",
                "avpu_score": "alert"
            }
        }


class NewsResponse(BaseModel):
    """
    Response model for National Early Warning Score (NEWS)
    
    The NEWS score ranges from 0 to 20 points and classifies patients into risk categories:
    - 0: Very low risk - Continue routine monitoring
    - 1-4: Low risk - Nurse assessment for monitoring frequency changes
    - 5-6 or RED score: Medium risk - Urgent clinical review required
    - ≥7: High risk - Emergency assessment and critical care involvement
    
    A RED score indicates any single parameter scoring 3 points, requiring urgent review 
    even if total score is <5.
    
    Reference: Royal College of Physicians. National Early Warning Score (NEWS) 2012.
    """
    
    result: int = Field(
        ...,
        description="NEWS score calculated from physiological parameters (range: 0-20 points)",
        example=0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended response based on the score",
        example="Continue routine monitoring."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, Medium Risk, High Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Description of the early warning score level",
        example="Very low early warning score"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 0,
                "unit": "points",
                "interpretation": "Continue routine monitoring.",
                "stage": "Low Risk",
                "stage_description": "Very low early warning score"
            }
        }