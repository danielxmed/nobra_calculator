"""
New Orleans/Charity Head Trauma/Injury Rule Models

Request and response models for New Orleans/Charity Head Trauma Rule calculation.

Reference (Vancouver style):
Haydel MJ, Preston CA, Mills TJ, Luber S, Blaudeau E, DeBlieux PM. Indications for 
computed tomography in patients with minor head injury. N Engl J Med. 2000 Jul 13;
343(2):100-5. doi: 10.1056/NEJM200007133430204.

The New Orleans/Charity Head Trauma/Injury Rule offers criteria for which patients 
are unlikely to require imaging after head trauma. It is designed for use ONLY in 
patients with head injury and loss of consciousness who are neurologically normal 
(GCS 15). The rule is 100% sensitive for detecting intracranial injuries requiring 
neurosurgical intervention.
"""

from pydantic import BaseModel, Field
from typing import Literal


class NewOrleansCharityHeadTraumaRequest(BaseModel):
    """
    Request model for New Orleans/Charity Head Trauma/Injury Rule
    
    The rule uses 7 clinical criteria to determine need for CT imaging in patients 
    with minor head injury. It applies to patients > 18 years of age with blunt 
    head trauma within 24 hours who had loss of consciousness, amnesia or 
    disorientation but present with GCS = 15.
    
    Criteria:
    1. Headache
    2. Vomiting
    3. Age > 60 years
    4. Alcohol or drug intoxication
    5. Persistent anterograde amnesia (short-term memory deficits)
    6. Visible trauma above the clavicle
    7. Seizure
    
    If ANY criterion is positive, CT scan is recommended.
    
    Reference (Vancouver style):
    Haydel MJ, Preston CA, Mills TJ, Luber S, Blaudeau E, DeBlieux PM. Indications for 
    computed tomography in patients with minor head injury. N Engl J Med. 2000 Jul 13;
    343(2):100-5. doi: 10.1056/NEJM200007133430204.
    """
    
    headache: Literal["yes", "no"] = Field(
        ...,
        description="Presence of headache after head trauma",
        example="no"
    )
    
    vomiting: Literal["yes", "no"] = Field(
        ...,
        description="Any episode of vomiting after head trauma",
        example="no"
    )
    
    age_over_60: Literal["yes", "no"] = Field(
        ...,
        description="Patient age greater than 60 years",
        example="no"
    )
    
    intoxication: Literal["yes", "no"] = Field(
        ...,
        description="Evidence of alcohol or drug intoxication",
        example="no"
    )
    
    persistent_amnesia: Literal["yes", "no"] = Field(
        ...,
        description="Persistent anterograde amnesia (short-term memory deficits). Patient cannot recall events after the injury",
        example="yes"
    )
    
    visible_trauma: Literal["yes", "no"] = Field(
        ...,
        description="Any visible trauma above the clavicle (e.g., lacerations, contusions, abrasions)",
        example="yes"
    )
    
    seizure: Literal["yes", "no"] = Field(
        ...,
        description="Any seizure activity after head trauma",
        example="no"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "headache": "no",
                "vomiting": "no",
                "age_over_60": "no",
                "intoxication": "no",
                "persistent_amnesia": "yes",
                "visible_trauma": "yes",
                "seizure": "no"
            }
        }


class NewOrleansCharityHeadTraumaResponse(BaseModel):
    """
    Response model for New Orleans/Charity Head Trauma/Injury Rule
    
    Returns CT scan recommendation based on presence of any of the 7 criteria.
    The rule has 100% sensitivity for detecting intracranial injuries requiring 
    neurosurgical intervention but relatively low specificity (25%).
    
    Reference: Haydel MJ, et al. N Engl J Med. 2000;343(2):100-5.
    """
    
    result: str = Field(
        ...,
        description="CT scan recommendation: 'CT recommended' if any criteria positive, 'CT not required' if all negative",
        example="CT recommended"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement (empty for this rule)",
        example=""
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of the rule with guidance on next steps",
        example="CT scan recommended. The patient meets 2 of the New Orleans criteria. Consider CT head imaging to rule out intracranial injury. This rule has 100% sensitivity for detecting intracranial injuries requiring neurosurgical intervention."
    )
    
    stage: str = Field(
        ...,
        description="Result classification: 'Positive' if any criteria met, 'Negative' if none met",
        example="Positive"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of criteria met",
        example="2 criteria met"
    )
    
    criteria_count: int = Field(
        ...,
        description="Number of positive criteria (0-7)",
        example=2
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": "CT recommended",
                "unit": "",
                "interpretation": "CT scan recommended. The patient meets 2 of the New Orleans criteria. Consider CT head imaging to rule out intracranial injury. This rule has 100% sensitivity for detecting intracranial injuries requiring neurosurgical intervention.",
                "stage": "Positive",
                "stage_description": "2 criteria met",
                "criteria_count": 2
            }
        }