from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List
from enum import Enum

class YesNoResponse(str, Enum):
    """Yes/No response options for AIRQ questions."""
    YES = "yes"
    NO = "no"

class AIRQRequest(BaseModel):
    """
    Request model for Asthma Impairment and Risk Questionnaire (AIRQ) calculation.
    
    The AIRQ is a validated 10-item questionnaire that assesses both symptom impairment 
    (7 items, 2-week recall) and exacerbation risk (3 items, 12-month recall) in patients 
    aged 12 years and older with asthma.
    """
    
    # Impairment domain questions (past 2 weeks)
    daytime_symptoms: YesNoResponse = Field(
        ...,
        description="In the past 2 weeks, has coughing, wheezing, shortness of breath, or chest tightness bothered you during the day on more than 4 days?",
        example="no"
    )
    
    nighttime_awakenings: YesNoResponse = Field(
        ...,
        description="In the past 2 weeks, has coughing, wheezing, shortness of breath, or chest tightness woke you up from sleep more than 1 time?",
        example="no"
    )
    
    activity_limitation: YesNoResponse = Field(
        ...,
        description="In the past 2 weeks, has coughing, wheezing, shortness of breath, or chest tightness limited the activities you want to do every day?",
        example="no"
    )
    
    rescue_medication_daily: YesNoResponse = Field(
        ...,
        description="In the past 2 weeks, has coughing, wheezing, shortness of breath, or chest tightness caused you to use your rescue inhaler or nebulizer every day?",
        example="no"
    )
    
    social_activity_limitation: YesNoResponse = Field(
        ...,
        description="In the past 2 weeks, did you have to limit your social activities (such as visiting with friends/relatives or playing with pets/children) because of your asthma?",
        example="no"
    )
    
    exercise_limitation: YesNoResponse = Field(
        ...,
        description="In the past 2 weeks, did coughing, wheezing, shortness of breath, or chest tightness limit your ability to exercise?",
        example="no"
    )
    
    difficult_control: YesNoResponse = Field(
        ...,
        description="In the past 2 weeks, did you feel that it was difficult to control your asthma?",
        example="no"
    )
    
    # Risk domain questions (past 12 months)
    oral_steroids: YesNoResponse = Field(
        ...,
        description="In the past 12 months, has coughing, wheezing, shortness of breath, or chest tightness caused you to take steroid pills or shots, such as prednisone or methylprednisolone?",
        example="no"
    )
    
    emergency_visits: YesNoResponse = Field(
        ...,
        description="In the past 12 months, has coughing, wheezing, shortness of breath, or chest tightness caused you to go to the emergency room or have unplanned visits to a health care provider?",
        example="no"
    )
    
    hospitalization: YesNoResponse = Field(
        ...,
        description="In the past 12 months, has coughing, wheezing, shortness of breath, or chest tightness caused you to stay in the hospital overnight?",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "daytime_symptoms": "no",
                "nighttime_awakenings": "no",
                "activity_limitation": "yes",
                "rescue_medication_daily": "no",
                "social_activity_limitation": "no",
                "exercise_limitation": "yes",
                "difficult_control": "no",
                "oral_steroids": "no",
                "emergency_visits": "no",
                "hospitalization": "no"
            }
        }

class AIRQResult(BaseModel):
    """Result model for AIRQ calculation."""
    
    airq_score: int = Field(
        ...,
        description="Total AIRQ score (0-10 points)",
        ge=0,
        le=10
    )
    
    category: str = Field(
        ...,
        description="Asthma control category based on AIRQ score"
    )
    
    description: str = Field(
        ...,
        description="Brief description of the control category"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of the AIRQ score"
    )
    
    risk_level: str = Field(
        ...,
        description="Risk level (Low, Moderate, High)"
    )
    
    impairment_score: int = Field(
        ...,
        description="Impairment domain score (0-7 points)",
        ge=0,
        le=7
    )
    
    risk_score: int = Field(
        ...,
        description="Risk domain score (0-3 points)",
        ge=0,
        le=3
    )
    
    details: Dict[str, Any] = Field(
        ...,
        description="Detailed breakdown of the calculation"
    )
    
    recommendations: List[str] = Field(
        ...,
        description="Clinical recommendations based on AIRQ score"
    )
    
    validation_notes: List[str] = Field(
        ...,
        description="Validation information and performance metrics"
    )

class AIRQResponse(BaseModel):
    """Response model for AIRQ calculation."""
    
    calculator_name: str = Field(default="AIRQ", description="Calculator identifier")
    version: str = Field(default="2020", description="AIRQ version")
    timestamp: str = Field(..., description="Calculation timestamp")
    inputs: AIRQRequest = Field(..., description="Input parameters")
    result: AIRQResult = Field(..., description="Calculation result")
    
    class Config:
        schema_extra = {
            "example": {
                "calculator_name": "AIRQ",
                "version": "2020",
                "timestamp": "2024-01-15T10:30:00Z",
                "inputs": {
                    "daytime_symptoms": "no",
                    "nighttime_awakenings": "no",
                    "activity_limitation": "yes",
                    "rescue_medication_daily": "no",
                    "social_activity_limitation": "no",
                    "exercise_limitation": "yes",
                    "difficult_control": "no",
                    "oral_steroids": "no",
                    "emergency_visits": "no",
                    "hospitalization": "no"
                },
                "result": {
                    "airq_score": 2,
                    "category": "Not well-controlled",
                    "description": "Not well-controlled asthma",
                    "interpretation": "Asthma control is suboptimal. Consider step-up therapy, review inhaler technique and adherence. Increased risk of exacerbations compared to well-controlled patients.",
                    "risk_level": "Moderate",
                    "impairment_score": 2,
                    "risk_score": 0,
                    "details": {
                        "total_questions": 10,
                        "yes_responses": 2,
                        "no_responses": 8,
                        "impairment_domain": "2/7 (past 2 weeks symptoms)",
                        "risk_domain": "0/3 (past 12 months exacerbations)",
                        "cut_points": {
                            "well_controlled": "0-1 points",
                            "not_well_controlled": "2-4 points",
                            "very_poorly_controlled": "5-10 points"
                        }
                    },
                    "recommendations": [
                        "Discuss individual question responses with healthcare provider",
                        "Use AIRQ results as part of comprehensive clinical assessment",
                        "Consider shared decision-making for treatment planning",
                        "Consider step-up therapy according to guidelines",
                        "Review and optimize inhaler technique",
                        "Assess medication adherence",
                        "Evaluate environmental triggers",
                        "Consider more frequent monitoring (every 3-6 months)",
                        "Update asthma action plan"
                    ],
                    "validation_notes": [
                        "Validated for patients aged 12 years and older with physician-diagnosed asthma",
                        "ROC AUC 0.94 for identifying well-controlled vs not well-/very poorly controlled",
                        "ROC AUC 0.93 for identifying well-/not well-controlled vs very poorly controlled",
                        "Sensitivity 0.90 and specificity 0.79 for cut-point ≥2",
                        "Specificity 0.95 for cut-point ≥5 (very poorly controlled)"
                    ]
                }
            }
        }
