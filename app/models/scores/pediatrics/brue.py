"""
Brief Resolved Unexplained Events (BRUE) Criteria Models

Request and response models for BRUE calculation.

References (Vancouver style):
1. Tieder JS, Bonkowsky JL, Etzel RA, et al. Brief resolved unexplained events 
   (formerly apparent life-threatening events) and evaluation of lower-risk infants. 
   Pediatrics. 2016;137(5):e20160590. doi: 10.1542/peds.2016-0590.
2. American Academy of Pediatrics Subcommittee on Apparent Life-Threatening Events. 
   Apparent life-threatening events in infants: an evidence-based review. 
   Pediatrics. 2003;111(2):361-7. doi: 10.1542/peds.111.2.361.
3. Mittal MK, Sun G, Baren JM. A clinical decision rule to identify infants with 
   apparent life-threatening event who can be safely discharged from the emergency 
   department. Pediatr Emerg Care. 2012;28(7):599-605. doi: 10.1097/PEC.0b013e31825cf576.

The BRUE criteria replaces the previous Apparent Life-Threatening Event (ALTE) 
classification and provides a systematic approach to evaluating infants <1 year 
who have experienced brief, resolved episodes of concerning symptoms. The criteria 
help determine risk stratification and appropriate management strategies.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any


class BrueRequest(BaseModel):
    """
    Request model for Brief Resolved Unexplained Events (BRUE) Criteria
    
    BRUE Entry Criteria (ALL must be met):
    1. Infant <1 year old
    2. Asymptomatic on presentation (no URI symptoms, no fever)
    3. No explanation for event after history and physical exam
    4. History of sudden, brief, and now resolved episode
    
    Event Characteristics (≥1 must be present):
    - Cyanosis or pallor
    - Absent, decreased, or irregular breathing
    - Marked change in tone (hyper or hypotonia)
    - Altered level of responsiveness
    
    Lower Risk BRUE Classification (ALL must be met):
    1. Episode duration <1 minute
    2. Age >2 months
    3. No history of prematurity (≥32 weeks GA or ≥45 weeks postconceptional age if born <32 weeks)
    4. No prior BRUE events
    5. No need for CPR by medical provider
    
    Clinical Management:
    - Lower Risk BRUE: Observation, education, CPR training, shared decision-making
    - Higher Risk BRUE: Further evaluation, monitoring, potential hospitalization
    - Not BRUE: Consider alternative diagnoses
    
    References (Vancouver style):
    1. Tieder JS, Bonkowsky JL, Etzel RA, et al. Brief resolved unexplained events 
    (formerly apparent life-threatening events) and evaluation of lower-risk infants. 
    Pediatrics. 2016;137(5):e20160590. doi: 10.1542/peds.2016-0590.
    2. American Academy of Pediatrics Subcommittee on Apparent Life-Threatening Events. 
    Apparent life-threatening events in infants: an evidence-based review. 
    Pediatrics. 2003;111(2):361-7. doi: 10.1542/peds.111.2.361.
    3. Mittal MK, Sun G, Baren JM. A clinical decision rule to identify infants with 
    apparent life-threatening event who can be safely discharged from the emergency 
    department. Pediatr Emerg Care. 2012;28(7):599-605. doi: 10.1097/PEC.0b013e31825cf576.
    """
    
    age_under_1_year: Literal["yes", "no"] = Field(
        ...,
        description="Is the infant less than 1 year old? Required entry criterion for BRUE classification",
        example="yes"
    )
    
    asymptomatic_on_presentation: Literal["yes", "no"] = Field(
        ...,
        description="Is the infant asymptomatic on presentation (no URI symptoms, no fever)? Required entry criterion",
        example="yes"
    )
    
    no_explanation_after_exam: Literal["yes", "no"] = Field(
        ...,
        description="No explanation for the event after conducting history and physical examination? Required entry criterion",
        example="yes"
    )
    
    sudden_brief_resolved_episode: Literal["yes", "no"] = Field(
        ...,
        description="History of sudden, brief, and now resolved episode? Required entry criterion",
        example="yes"
    )
    
    cyanosis_or_pallor: Literal["yes", "no"] = Field(
        ...,
        description="Did the episode include cyanosis or pallor? (Event characteristic - at least one must be present)",
        example="yes"
    )
    
    breathing_changes: Literal["yes", "no"] = Field(
        ...,
        description="Did the episode include absent, decreased, or irregular breathing? (Event characteristic)",
        example="no"
    )
    
    tone_changes: Literal["yes", "no"] = Field(
        ...,
        description="Did the episode include marked change in tone (hyper or hypotonia)? (Event characteristic)",
        example="no"
    )
    
    altered_responsiveness: Literal["yes", "no"] = Field(
        ...,
        description="Did the episode include altered level of responsiveness? (Event characteristic)",
        example="no"
    )
    
    episode_duration_under_1_min: Literal["yes", "no"] = Field(
        ...,
        description="Was the episode duration less than 1 minute? (Lower risk criterion)",
        example="yes"
    )
    
    age_over_2_months: Literal["yes", "no"] = Field(
        ...,
        description="Is the infant older than 2 months? (Lower risk criterion)",
        example="yes"
    )
    
    no_history_prematurity: Literal["yes", "no"] = Field(
        ...,
        description="No history of prematurity (≥32 weeks gestational age or ≥45 weeks postconceptional age if born <32 weeks)? (Lower risk criterion)",
        example="yes"
    )
    
    no_prior_brue: Literal["yes", "no"] = Field(
        ...,
        description="No prior BRUE events in the patient's history? (Lower risk criterion)",
        example="yes"
    )
    
    no_cpr_by_provider: Literal["yes", "no"] = Field(
        ...,
        description="No need for CPR by medical provider during or after the event? (Lower risk criterion)",
        example="yes"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age_under_1_year": "yes",
                "asymptomatic_on_presentation": "yes",
                "no_explanation_after_exam": "yes",
                "sudden_brief_resolved_episode": "yes",
                "cyanosis_or_pallor": "yes",
                "breathing_changes": "no",
                "tone_changes": "no",
                "altered_responsiveness": "no",
                "episode_duration_under_1_min": "yes",
                "age_over_2_months": "yes",
                "no_history_prematurity": "yes",
                "no_prior_brue": "yes",
                "no_cpr_by_provider": "yes"
            }
        }


class BrueResponse(BaseModel):
    """
    Response model for Brief Resolved Unexplained Events (BRUE) Criteria
    
    BRUE Classification Results:
    - 0: Not BRUE (does not meet entry criteria or event characteristics)
    - 1: BRUE - Higher Risk (meets BRUE criteria but not all lower-risk criteria)
    - 2: BRUE - Lower Risk (meets all BRUE and lower-risk criteria)
    
    Management Recommendations:
    - Lower Risk BRUE: Brief observation, parental education, CPR training resources
    - Higher Risk BRUE: Further evaluation, monitoring, potential hospitalization
    - Routine diagnostic testing NOT recommended for lower-risk BRUE
    
    Reference: Tieder JS, et al. Pediatrics. 2016;137(5):e20160590.
    """
    
    result: int = Field(
        ...,
        description="BRUE classification result: 0=Not BRUE, 1=BRUE Higher Risk, 2=BRUE Lower Risk",
        example=2
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement (empty for classification)",
        example=""
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and management recommendations based on BRUE classification",
        example="Meets criteria for lower-risk BRUE. May be managed with observation, parental education, CPR training resources, and shared decision-making. Routine diagnostic testing (chest x-rays, blood gas, sleep studies, ECG, etc.) is NOT recommended."
    )
    
    stage: str = Field(
        ...,
        description="BRUE classification category",
        example="BRUE - Lower Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the classification",
        example="Meets BRUE criteria and classified as lower risk"
    )
    
    criteria_summary: Dict[str, Dict[str, bool]] = Field(
        ...,
        description="Summary of which criteria were met in each category",
        example={
            "entry_criteria": {
                "age_under_1_year": True,
                "asymptomatic_on_presentation": True,
                "no_explanation_after_exam": True,
                "sudden_brief_resolved_episode": True
            },
            "event_characteristics": {
                "cyanosis_or_pallor": True,
                "breathing_changes": False,
                "tone_changes": False,
                "altered_responsiveness": False
            },
            "lower_risk_criteria": {
                "episode_duration_under_1_min": True,
                "age_over_2_months": True,
                "no_history_prematurity": True,
                "no_prior_brue": True,
                "no_cpr_by_provider": True
            }
        }
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 2,
                "unit": "",
                "interpretation": "Meets criteria for lower-risk BRUE. May be managed with observation, parental education, CPR training resources, and shared decision-making. Routine diagnostic testing (chest x-rays, blood gas, sleep studies, ECG, etc.) is NOT recommended. Assess social risk factors and provide family support.",
                "stage": "BRUE - Lower Risk",
                "stage_description": "Meets BRUE criteria and classified as lower risk",
                "criteria_summary": {
                    "entry_criteria": {
                        "age_under_1_year": True,
                        "asymptomatic_on_presentation": True,
                        "no_explanation_after_exam": True,
                        "sudden_brief_resolved_episode": True
                    },
                    "event_characteristics": {
                        "cyanosis_or_pallor": True,
                        "breathing_changes": False,
                        "tone_changes": False,
                        "altered_responsiveness": False
                    },
                    "lower_risk_criteria": {
                        "episode_duration_under_1_min": True,
                        "age_over_2_months": True,
                        "no_history_prematurity": True,
                        "no_prior_brue": True,
                        "no_cpr_by_provider": True
                    }
                }
            }
        }