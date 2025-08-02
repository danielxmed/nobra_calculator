"""
Modified Early Warning Score (MEWS) for Clinical Deterioration Models

Request and response models for MEWS assessment.

References (Vancouver style):
1. Subbe CP, Kruger M, Rutherford P, Gemmel L. Validation of a modified Early Warning 
   Score in medical admissions. QJM. 2001 Oct;94(10):521-6. doi: 10.1093/qjmed/94.10.521.
2. Morgan RJM, Williams F, Wright MM. An early warning scoring system for detecting 
   developing critical illness. Clinical Intensive Care. 1997;8:100.
3. Goldhill DR, McNarry AF, Mandersloot G, McGinley A. A physiologically-based early 
   warning score for ward patients: the association between score and outcome. 
   Anaesthesia. 2005 Jun;60(6):547-53. doi: 10.1111/j.1365-2044.2005.04186.x.

The Modified Early Warning Score (MEWS) is a physiological scoring system that 
identifies patients at risk of clinical deterioration, ICU admission, or death. 
It uses 5 readily available parameters: systolic blood pressure, heart rate, 
respiratory rate, temperature, and level of consciousness (AVPU scale). The 
score ranges from 0-14 points, with scores ≥5 indicating high risk requiring 
immediate medical review and potential ICU consideration.
"""

from pydantic import BaseModel, Field, validator
from typing import Literal


class ModifiedEarlyWarningScoreRequest(BaseModel):
    """
    Request model for Modified Early Warning Score (MEWS) for Clinical Deterioration
    
    The MEWS uses 5 physiological parameters to assess risk of clinical deterioration:
    
    1. Systolic Blood Pressure (0-3 points):
       - ≤70 mmHg: 3 points
       - 71-80 mmHg: 2 points
       - 81-100 mmHg: 1 point
       - 101-199 mmHg: 0 points
       - ≥200 mmHg: 2 points
    
    2. Heart Rate (0-3 points):
       - <40 bpm: 2 points
       - 40-50 bpm: 1 point
       - 51-100 bpm: 0 points
       - 101-110 bpm: 1 point
       - 111-129 bpm: 2 points
       - ≥130 bpm: 3 points
    
    3. Respiratory Rate (0-3 points):
       - <9 breaths/min: 2 points
       - 9-14 breaths/min: 0 points
       - 15-20 breaths/min: 1 point
       - 21-29 breaths/min: 2 points
       - ≥30 breaths/min: 3 points
    
    4. Temperature (0-2 points):
       - <35°C (<95°F): 2 points
       - 35-38.4°C (95-101.1°F): 0 points
       - >38.5°C (>101.3°F): 2 points
    
    5. AVPU Consciousness Level (0-3 points):
       - Alert: 0 points
       - Responds to Voice: 1 point
       - Responds to Pain: 2 points
       - Unresponsive: 3 points
    
    Score Interpretation:
    - 0-2: Low risk, routine monitoring
    - 3-4: Moderate risk, increase monitoring frequency
    - ≥5: High risk, immediate medical review required
    - Any single parameter = 3 points: Consider higher level of care
    
    References (Vancouver style):
    1. Subbe CP, Kruger M, Rutherford P, Gemmel L. Validation of a modified Early Warning 
       Score in medical admissions. QJM. 2001 Oct;94(10):521-6. doi: 10.1093/qjmed/94.10.521.
    2. Morgan RJM, Williams F, Wright MM. An early warning scoring system for detecting 
       developing critical illness. Clinical Intensive Care. 1997;8:100.
    3. Goldhill DR, McNarry AF, Mandersloot G, McGinley A. A physiologically-based early 
       warning score for ward patients: the association between score and outcome. 
       Anaesthesia. 2005 Jun;60(6):547-53. doi: 10.1111/j.1365-2044.2005.04186.x.
    """
    
    systolic_bp: int = Field(
        ...,
        ge=50,
        le=300,
        description="Systolic blood pressure in mmHg. Use most recent stable reading. Avoid measurements during acute interventions",
        example=120
    )
    
    heart_rate: int = Field(
        ...,
        ge=20,
        le=200,
        description="Heart rate in beats per minute. Use most recent rhythm strip or monitor reading. Ensure measurement accuracy",
        example=85
    )
    
    respiratory_rate: int = Field(
        ...,
        ge=5,
        le=60,
        description="Respiratory rate in breaths per minute. Count for full 60 seconds if abnormal. Include assisted ventilation considerations",
        example=16
    )
    
    temperature: float = Field(
        ...,
        ge=30.0,
        le=45.0,
        description="Core body temperature in degrees Celsius. Use most accurate available method (core > oral > axillary)",
        example=37.2
    )
    
    consciousness_level: Literal["alert", "voice", "pain", "unresponsive"] = Field(
        ...,
        description="Level of consciousness using AVPU scale. Alert = awake and oriented, Voice = responds to verbal commands, Pain = responds only to painful stimuli, Unresponsive = no response to any stimulus",
        example="alert"
    )
    
    @validator('temperature')
    def validate_temperature_range(cls, v):
        """Validate temperature is within physiologically reasonable range"""
        if v < 32.0:
            raise ValueError("Temperature below 32°C indicates severe hypothermia - verify measurement")
        if v > 42.0:
            raise ValueError("Temperature above 42°C indicates severe hyperthermia - verify measurement")
        return v
    
    @validator('systolic_bp')
    def validate_blood_pressure(cls, v):
        """Validate blood pressure is physiologically reasonable"""
        if v < 60:
            raise ValueError("Systolic BP below 60mmHg indicates severe hypotension - verify measurement")
        if v > 250:
            raise ValueError("Systolic BP above 250mmHg indicates severe hypertension - verify measurement")
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "systolic_bp": 120,
                "heart_rate": 85,
                "respiratory_rate": 16,
                "temperature": 37.2,
                "consciousness_level": "alert"
            }
        }


class ModifiedEarlyWarningScoreResponse(BaseModel):
    """
    Response model for Modified Early Warning Score (MEWS) for Clinical Deterioration
    
    The MEWS score ranges from 0-14 points and stratifies clinical deterioration risk:
    
    Low Risk (0-2 points):
    - Low risk of clinical deterioration
    - Continue routine monitoring and standard nursing observations
    - Reassess vital signs according to hospital policy
    - No immediate intervention required
    
    Moderate Risk (3-4 points):
    - Moderate risk of clinical deterioration
    - Increase monitoring frequency (every 2-4 hours recommended)
    - Consider medical review within 1-2 hours
    - Alert healthcare team and document concerns
    - Ensure appropriate escalation protocols are followed
    
    High Risk (≥5 points):
    - High risk of clinical deterioration, ICU admission, or death
    - Immediate medical review required (within 30 minutes)
    - Consider ICU consultation and potential transfer
    - Implement continuous monitoring
    - Prepare for possible higher level of care
    - Associated with 5.4x increased risk of death (OR 5.4, 95% CI 2.8-10.7)
    
    Special Considerations:
    - Any single parameter scoring 3 points warrants consideration of higher level of care
    - Score should be calculated every 4-6 hours or with clinical status changes
    - Use as part of comprehensive clinical assessment, not in isolation
    - Some institutions may modify parameters or thresholds
    
    Clinical Actions by Score:
    - 0-2: Standard care, routine observations
    - 3-4: Increased observations, medical review within 2 hours
    - ≥5: Immediate medical review, consider ICU consultation
    - Single parameter = 3: Higher level of care consideration
    
    Reference: Subbe CP, et al. QJM. 2001;94(10):521-6.
    """
    
    result: int = Field(
        ...,
        ge=0,
        le=14,
        description="MEWS score indicating risk of clinical deterioration (0-14 points)",
        example=2
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with risk assessment and monitoring recommendations",
        example="MEWS score of 2 indicates low risk of clinical deterioration. Continue routine monitoring and standard nursing observations as per protocol. Reassess vital signs according to hospital policy."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, Moderate Risk, High Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk level",
        example="Low risk of deterioration"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 2,
                "unit": "points",
                "interpretation": "MEWS score of 2 indicates low risk of clinical deterioration. Continue routine monitoring and standard nursing observations as per protocol. Reassess vital signs according to hospital policy.",
                "stage": "Low Risk",
                "stage_description": "Low risk of deterioration"
            }
        }