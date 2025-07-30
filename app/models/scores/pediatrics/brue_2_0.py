"""
Brief Resolved Unexplained Events 2.0 (BRUE 2.0) Criteria Models

Request and response models for BRUE 2.0 calculation.

References (Vancouver style):
1. Tieder JS, Bonkowsky JL, Etzel RA, et al. Brief resolved unexplained events 
   (formerly apparent life-threatening events) and evaluation of lower-risk infants. 
   Pediatrics. 2016;137(5):e20160590. doi: 10.1542/peds.2016-0590.
2. Merritt JL, Quinonez RA, Bonkowsky JL, et al. A framework for evaluation of the 
   higher-risk infant after a brief resolved unexplained event. Pediatrics. 
   2021;148(1):e2021050798. doi: 10.1542/peds.2021-050798.
3. Ramgopal S, Karim SA, Subramanian S, Kaderli AA, Fitzgerald M, Ramesh A. 
   Epidemiology of brief resolved unexplained events: a systematic review. 
   Arch Dis Child. 2019;104(11):1074-1081. doi: 10.1136/archdischild-2018-316866.

The BRUE 2.0 criteria improves on the original BRUE classification by providing 
sophisticated risk prediction models for serious underlying conditions and event 
recurrence. It uses derived mathematical models to calculate quantitative risk 
percentages rather than binary risk categories, enabling more nuanced clinical 
decision-making and resource allocation.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any


class Brue20Request(BaseModel):
    """
    Request model for Brief Resolved Unexplained Events 2.0 (BRUE 2.0) Criteria
    
    BRUE 2.0 Entry Criteria (ALL must be met):
    1. Infant <1 year old
    2. Asymptomatic on presentation (no URI symptoms, no fever)
    3. No explanation for event after history and physical exam
    4. History of sudden, brief, and now resolved episode
    
    Event Characteristics (≥1 must be present):
    - Cyanosis or pallor
    - Absent, decreased, or irregular breathing
    - Marked change in tone (hyper or hypotonia)
    - Altered level of responsiveness
    
    Risk Prediction Models:
    1. Serious Condition Risk: Uses age in days, history of similar events, and abnormal medical history
    2. Recurrence Risk: Uses multiple factors including prematurity, event clusters, and specific characteristics
    
    Key Improvements over Original BRUE:
    - Quantitative risk prediction rather than binary classification
    - Age as continuous variable (days) rather than categorical
    - Enhanced risk stratification for clinical decision-making
    - Validated prediction models for serious diagnoses and recurrence
    
    References (Vancouver style):
    1. Tieder JS, Bonkowsky JL, Etzel RA, et al. Brief resolved unexplained events 
    (formerly apparent life-threatening events) and evaluation of lower-risk infants. 
    Pediatrics. 2016;137(5):e20160590. doi: 10.1542/peds.2016-0590.
    2. Merritt JL, Quinonez RA, Bonkowsky JL, et al. A framework for evaluation of the 
    higher-risk infant after a brief resolved unexplained event. Pediatrics. 
    2021;148(1):e2021050798. doi: 10.1542/peds.2021-050798.
    3. Ramgopal S, Karim SA, Subramanian S, Kaderli AA, Fitzgerald M, Ramesh A. 
    Epidemiology of brief resolved unexplained events: a systematic review. 
    Arch Dis Child. 2019;104(11):1074-1081. doi: 10.1136/archdischild-2018-316866.
    """
    
    age_under_1_year: Literal["yes", "no"] = Field(
        ...,
        description="Is the infant less than 1 year old? Required entry criterion for BRUE classification",
        example="yes"
    )
    
    asymptomatic_on_presentation: Literal["yes", "no"] = Field(
        ...,
        description="Is the infant asymptomatic on presentation (no URI symptoms, no fever, no concerning vital signs)? Required entry criterion",
        example="yes"
    )
    
    no_explanation_after_exam: Literal["yes", "no"] = Field(
        ...,
        description="No explanation for the event after conducting comprehensive history and physical examination? Required entry criterion",
        example="yes"
    )
    
    sudden_brief_resolved_episode: Literal["yes", "no"] = Field(
        ...,
        description="History of sudden, brief, and now completely resolved episode? Required entry criterion",
        example="yes"
    )
    
    cyanosis_or_pallor: Literal["yes", "no"] = Field(
        ...,
        description="Did the episode include cyanosis (blue discoloration) or pallor (pale appearance)? (Event characteristic - at least one must be present)",
        example="yes"
    )
    
    breathing_changes: Literal["yes", "no"] = Field(
        ...,
        description="Did the episode include absent, decreased, or irregular breathing patterns? (Event characteristic)",
        example="no"
    )
    
    tone_changes: Literal["yes", "no"] = Field(
        ...,
        description="Did the episode include marked change in muscle tone (hypertonia/increased stiffness or hypotonia/floppy)? (Event characteristic)",
        example="no"
    )
    
    altered_responsiveness: Literal["yes", "no"] = Field(
        ...,
        description="Did the episode include altered level of responsiveness or consciousness? (Event characteristic)",
        example="no"
    )
    
    age_in_days: int = Field(
        ...,
        description="Age of infant in days (0-365 days, used in quantitative risk prediction models)",
        ge=0,
        le=365,
        example=90
    )
    
    history_similar_event: Literal["yes", "no"] = Field(
        ...,
        description="History of similar events or episodes in the past? (Major risk factor for both serious conditions and recurrence)",
        example="no"
    )
    
    abnormal_medical_history: Literal["yes", "no"] = Field(
        ...,
        description="Abnormal medical history, concerning findings, or underlying medical conditions? (Risk factor for serious conditions)",
        example="no"
    )
    
    multiple_event_clusters: Literal["yes", "no"] = Field(
        ...,
        description="Multiple event clusters or episodes occurring close together in time? (Risk factor for recurrence)",
        example="no"
    )
    
    prematurity: Literal["yes", "no"] = Field(
        ...,
        description="History of prematurity (born <37 weeks gestational age)? (Risk factor for recurrence and serious conditions)",
        example="no"
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
                "age_in_days": 90,
                "history_similar_event": "no",
                "abnormal_medical_history": "no",
                "multiple_event_clusters": "no",
                "prematurity": "no"
            }
        }


class Brue20Response(BaseModel):
    """
    Response model for Brief Resolved Unexplained Events 2.0 (BRUE 2.0) Criteria
    
    BRUE 2.0 Classification Results:
    - 0: Not BRUE (does not meet entry criteria or event characteristics)
    - 1-5: Very Low Risk (<2% serious condition risk)
    - 6-15: Low Risk (2-10% serious condition risk)
    - 16-30: Moderate Risk (10-20% serious condition risk)
    - 31-100: High Risk (>20% serious condition risk)
    
    Risk Predictions:
    - Serious Condition Risk: Quantitative percentage risk of underlying pathology
    - Recurrence Risk: Quantitative percentage risk of event recurrence
    - Overall Risk: Maximum of the two risk predictions for clinical decision-making
    
    Management Recommendations:
    - Very Low/Low Risk: Home management, education, shared decision-making
    - Moderate Risk: Consider observation, selective testing, close follow-up
    - High Risk: Comprehensive evaluation, hospitalization consideration, extensive workup
    
    Reference: Merritt JL, et al. Pediatrics. 2021;148(1):e2021050798.
    """
    
    result: int = Field(
        ...,
        description="BRUE 2.0 risk classification: 0=Not BRUE, 1-5=Very Low Risk, 6-15=Low Risk, 16-30=Moderate Risk, 31-100=High Risk",
        example=6
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement (empty for classification)",
        example=""
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and management recommendations based on BRUE 2.0 risk prediction models",
        example="Meets BRUE criteria with low risk (3.5% for serious condition, 15.0% recurrence). Consider brief observation, family education, and shared decision-making about diagnostic testing. Close follow-up recommended."
    )
    
    stage: str = Field(
        ...,
        description="BRUE 2.0 risk category",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk classification",
        example="BRUE with low risk for serious condition or recurrence"
    )
    
    risk_predictions: Dict[str, float] = Field(
        ...,
        description="Quantitative risk predictions from BRUE 2.0 models",
        example={
            "serious_condition_risk": 3.5,
            "recurrence_risk": 15.0,
            "overall_risk": 15.0
        }
    )
    
    risk_factors: Dict[str, Any] = Field(
        ...,
        description="Summary of risk factors present and patient age",
        example={
            "age_in_days": 90,
            "risk_factors_present": {
                "history_similar_event": False,
                "abnormal_medical_history": False,
                "multiple_event_clusters": False,
                "prematurity": False,
                "cyanosis_or_pallor": True,
                "breathing_changes": False,
                "tone_changes": False
            }
        }
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 6,
                "unit": "",
                "interpretation": "Meets BRUE criteria with low risk (3.5% for serious condition, 15.0% recurrence). Consider brief observation, family education, and shared decision-making about diagnostic testing. Close follow-up recommended.",
                "stage": "Low Risk",
                "stage_description": "BRUE with low risk for serious condition or recurrence",
                "risk_predictions": {
                    "serious_condition_risk": 3.5,
                    "recurrence_risk": 15.0,
                    "overall_risk": 15.0
                },
                "risk_factors": {
                    "age_in_days": 90,
                    "risk_factors_present": {
                        "history_similar_event": False,
                        "abnormal_medical_history": False,
                        "multiple_event_clusters": False,
                        "prematurity": False,
                        "cyanosis_or_pallor": True,
                        "breathing_changes": False,
                        "tone_changes": False
                    }
                }
            }
        }