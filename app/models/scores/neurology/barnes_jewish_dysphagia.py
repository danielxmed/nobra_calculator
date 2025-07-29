"""
Barnes Jewish Hospital Stroke Dysphagia Screen Models

Request and response models for Barnes Jewish Hospital dysphagia screen calculation.

References (Vancouver style):
1. Edmiaston J, Connor LT, Loehr L, Nassief A. Validation of a dysphagia screening 
   tool in acute stroke patients. Am J Crit Care. 2010 Jul;19(4):357-64. 
   doi: 10.4037/ajcc2009961.
2. Donovan NJ, Daniels SK, Edmiaston J, Weinhardt J, Summers D, Mitchell PH; 
   American Heart Association Council on Cardiovascular Nursing and Stroke Council. 
   Dysphagia screening: state of the art: invitational conference proceeding from 
   the State-of-the-Art Nursing Symposium, International Stroke Conference 2012. 
   Stroke. 2013 Apr;44(4):e24-31. doi: 10.1161/STR.0b013e3182877f57.

The Barnes Jewish Hospital Stroke Dysphagia Screen is a validated bedside screening 
tool designed for use by non-speech pathology trained healthcare professionals to 
identify stroke patients at risk for dysphagia and aspiration. It consists of 
preliminary neurological screening questions followed by a water swallow test if 
the preliminary screen is passed.
"""

from pydantic import BaseModel, Field, validator
from typing import Literal, Optional


class BarnesJewishDysphagiaRequest(BaseModel):
    """
    Request model for Barnes Jewish Hospital Stroke Dysphagia Screen
    
    The screening consists of two parts:
    
    1. Preliminary Screening (ALL must be NO to proceed):
       - Glasgow Coma Scale < 13
       - Facial asymmetry/weakness
       - Tongue asymmetry/weakness
       - Palatal asymmetry/weakness
    
    2. Water Swallow Test (if preliminary passed):
       - 3 oz water in sequential drinks
       - Assess for throat clearing, cough, voice change
       - During initial swallow and 1 minute after
    
    Sensitivity: 91-95% for detecting dysphagia and aspiration risk
    Interrater reliability: 93.6%
    
    References (Vancouver style):
    1. Edmiaston J, Connor LT, Loehr L, Nassief A. Validation of a dysphagia screening 
    tool in acute stroke patients. Am J Crit Care. 2010 Jul;19(4):357-64. 
    doi: 10.4037/ajcc2009961.
    """
    
    # Preliminary screening questions
    gcs_less_than_13: Literal["yes", "no"] = Field(
        ...,
        description="Is the Glasgow Coma Scale (GCS) less than 13? If yes, screen fails",
        example="no"
    )
    
    facial_asymmetry: Literal["yes", "no"] = Field(
        ...,
        description="Is there facial asymmetry or weakness present? If yes, screen fails",
        example="no"
    )
    
    tongue_asymmetry: Literal["yes", "no"] = Field(
        ...,
        description="Is there tongue asymmetry or weakness present? If yes, screen fails",
        example="no"
    )
    
    palatal_asymmetry: Literal["yes", "no"] = Field(
        ...,
        description="Is there palatal asymmetry or weakness present? If yes, screen fails",
        example="no"
    )
    
    water_test_performed: Literal["yes", "no", "not_applicable"] = Field(
        ...,
        description="Was the water swallow test performed? Only done if all preliminary questions are NO",
        example="yes"
    )
    
    # Water test results (optional - only if water test performed)
    throat_clearing_initial: Optional[Literal["yes", "no"]] = Field(
        None,
        description="Throat clearing during initial swallow. If yes, screen fails",
        example="no"
    )
    
    cough_initial: Optional[Literal["yes", "no"]] = Field(
        None,
        description="Cough during initial swallow. If yes, screen fails",
        example="no"
    )
    
    voice_change_initial: Optional[Literal["yes", "no"]] = Field(
        None,
        description="Voice change during initial swallow. If yes, screen fails",
        example="no"
    )
    
    throat_clearing_delayed: Optional[Literal["yes", "no"]] = Field(
        None,
        description="Throat clearing 1 minute after swallowing. If yes, screen fails",
        example="no"
    )
    
    cough_delayed: Optional[Literal["yes", "no"]] = Field(
        None,
        description="Cough 1 minute after swallowing. If yes, screen fails",
        example="no"
    )
    
    voice_change_delayed: Optional[Literal["yes", "no"]] = Field(
        None,
        description="Voice change 1 minute after swallowing. If yes, screen fails",
        example="no"
    )
    
    @validator('throat_clearing_initial', 'cough_initial', 'voice_change_initial',
               'throat_clearing_delayed', 'cough_delayed', 'voice_change_delayed')
    def validate_water_test_fields(cls, v, values):
        """Ensure water test fields are provided if water test was performed"""
        if 'water_test_performed' in values and values['water_test_performed'] == 'yes':
            if v is None:
                raise ValueError('Water test results must be provided when water test is performed')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "gcs_less_than_13": "no",
                "facial_asymmetry": "no",
                "tongue_asymmetry": "no",
                "palatal_asymmetry": "no",
                "water_test_performed": "yes",
                "throat_clearing_initial": "no",
                "cough_initial": "no",
                "voice_change_initial": "no",
                "throat_clearing_delayed": "no",
                "cough_delayed": "no",
                "voice_change_delayed": "no"
            }
        }


class BarnesJewishDysphagiaResponse(BaseModel):
    """
    Response model for Barnes Jewish Hospital Stroke Dysphagia Screen
    
    Results:
    - Pass: No dysphagia detected, can start regular diet
    - Fail: Dysphagia risk identified, keep NPO and refer to speech pathology
    
    Reference: Edmiaston J, et al. Am J Crit Care. 2010;19(4):357-64.
    """
    
    result: Literal["Pass", "Fail"] = Field(
        ...,
        description="Dysphagia screening result",
        example="Pass"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement (empty for pass/fail result)",
        example=""
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommendations based on screening result",
        example="Patient passed dysphagia screen. Can be started on regular diet. Continue to monitor for any changes in swallowing ability."
    )
    
    stage: str = Field(
        ...,
        description="Screening result (Pass or Fail)",
        example="Pass"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the result",
        example="No dysphagia detected"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "Pass",
                "unit": "",
                "interpretation": "Patient passed dysphagia screen. Can be started on regular diet. Continue to monitor for any changes in swallowing ability.",
                "stage": "Pass",
                "stage_description": "No dysphagia detected"
            }
        }