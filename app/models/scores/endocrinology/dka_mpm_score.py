"""
Diabetic Ketoacidosis Mortality Prediction Model (DKA MPM) Score Models

Request and response models for DKA MPM Score calculation.

References (Vancouver style):
1. Efstathiou SP, Tsiakou AG, Tsioulos DI, et al. A mortality prediction model in 
   diabetic ketoacidosis. Clin Endocrinol (Oxf). 2002;57(5):595-601. 
   doi: 10.1046/j.1365-2265.2002.01636.x.
2. Kitabchi AE, Umpierrez GE, Miles JM, Fisher JN. Hyperglycemic crises in adult 
   patients with diabetes. Diabetes Care. 2009;32(7):1335-1343. 
   doi: 10.2337/dc09-9032.
3. Dhatariya KK, Glaser NS, Codner E, Umpierrez GE. Diabetic ketoacidosis. 
   Nat Rev Dis Primers. 2020;6(1):40. doi: 10.1038/s41572-020-0165-1.

The DKA MPM Score is a mortality prediction model for patients with diabetic 
ketoacidosis that uses clinical and laboratory parameters assessed at presentation, 
12 hours, and 24 hours to stratify patients into low, high, and very high risk 
categories for in-hospital mortality. It provides valuable prognostic information 
to guide intensive care decisions and family counseling.
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Any, Literal


class DkaMpmScoreRequest(BaseModel):
    """
    Request model for Diabetic Ketoacidosis Mortality Prediction Model (DKA MPM) Score
    
    The DKA MPM Score predicts in-hospital mortality in patients with diabetic 
    ketoacidosis using 6 clinical and laboratory parameters assessed at different 
    time points:
    
    **Assessment Timing:**
    
    **At Presentation (0 hours):**
    - Severe comorbidities (6 points if present)
    - pH < 7.0 (4 points if present)
    
    **At 12 Hours:**
    - >50 units regular insulin required (4 points if yes)
    - Serum glucose >300 mg/dL (16.7 mmol/L) (4 points if yes)
    
    **At 24 Hours:**
    - Depressed mental state (4 points if present)
    - Fever ≥38°C/100.4°F (3 points if present)
    
    **Severe Comorbidities Include:**
    - Immunosuppression
    - Previous myocardial infarction
    - Chronic obstructive pulmonary disease (COPD)
    - Cirrhosis
    - Congestive heart failure (CHF)
    - Previous stroke
    
    **Scoring:**
    - Total score range: 0-25 points
    - Low risk: 0-14 points (0.86% mortality)
    - High risk: 15-18 points (20.8% mortality)
    - Very high risk: 19-25 points (93.3% mortality)
    
    **Clinical Applications:**
    - Risk stratification of DKA patients
    - ICU admission decisions
    - Intensity of monitoring guidance
    - Prognostic counseling for families
    - Quality improvement initiatives
    
    **Important Limitations:**
    - Not externally validated - use with clinical judgment
    - APACHE II score may be superior predictor
    - Not intended as sole basis for clinical decisions
    - Requires assessment at multiple time points
    
    References:
    1. Efstathiou SP, et al. Clin Endocrinol (Oxf). 2002;57(5):595-601.
    2. Kitabchi AE, et al. Diabetes Care. 2009;32(7):1335-1343.
    3. Dhatariya KK, et al. Nat Rev Dis Primers. 2020;6(1):40.
    """
    
    severe_comorbidities: Literal["yes", "no"] = Field(
        ...,
        description="Presence of severe comorbidities: immunosuppression, previous MI, COPD, cirrhosis, CHF, and/or previous stroke (6 points if yes)",
        example="no"
    )
    
    ph_less_than_7: Literal["yes", "no"] = Field(
        ...,
        description="pH < 7.0 at presentation on arterial blood gas (4 points if yes)",
        example="no"
    )
    
    insulin_over_50_units: Literal["yes", "no"] = Field(
        ...,
        description="More than 50 units of regular insulin required over the first 12 hours (4 points if yes)",
        example="no"
    )
    
    glucose_over_300_at_12h: Literal["yes", "no"] = Field(
        ...,
        description="Serum glucose > 300 mg/dL (16.7 mmol/L) after 12 hours of treatment (4 points if yes)",
        example="no"
    )
    
    depressed_mental_state_24h: Literal["yes", "no"] = Field(
        ...,
        description="Depressed mental state at 24 hours after presentation as determined by clinical examination (4 points if yes)",
        example="no"
    )
    
    fever_24h: Literal["yes", "no"] = Field(
        ...,
        description="Fever at 24 hours after presentation, defined as axillary temperature ≥38°C (100.4°F) (3 points if yes)",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "severe_comorbidities": "no",
                "ph_less_than_7": "no",
                "insulin_over_50_units": "no",
                "glucose_over_300_at_12h": "no",
                "depressed_mental_state_24h": "no",
                "fever_24h": "no"
            }
        }


class DkaMpmScoreResponse(BaseModel):
    """
    Response model for Diabetic Ketoacidosis Mortality Prediction Model (DKA MPM) Score
    
    The DKA MPM Score provides comprehensive mortality risk stratification for patients 
    with diabetic ketoacidosis including:
    - Total score (0-25 points)
    - Risk category (Low, High, Very High)
    - Mortality rates by category
    - Detailed clinical recommendations
    - Monitoring guidance
    - Prognostic counseling guidance
    
    **Risk Categories:**
    - Low Risk (0-14 points): 0.86% in-hospital mortality
    - High Risk (15-18 points): 20.8% in-hospital mortality 
    - Very High Risk (19-25 points): 93.3% in-hospital mortality
    
    **Clinical Decision Support:**
    - ICU admission recommendations
    - Monitoring intensity guidance
    - Treatment intensity recommendations
    - Family communication guidance
    - Quality improvement considerations
    
    Reference: Efstathiou SP, et al. Clin Endocrinol (Oxf). 2002;57(5):595-601.
    """
    
    result: int = Field(
        ...,
        description="DKA MPM Score calculated from all parameters (range: 0-25 points)",
        example=6
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with risk category and management recommendations",
        example="DKA MPM Score of 6 points indicates Low Risk with 0.86% in-hospital mortality risk. Low risk of in-hospital mortality. Standard DKA management protocols are appropriate. Routine monitoring and care expected to be sufficient."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, High Risk, Very High Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Low risk of in-hospital mortality"
    )
    
    total_score: int = Field(
        ...,
        description="The calculated DKA MPM total score",
        example=6
    )
    
    risk_level: str = Field(
        ...,
        description="Risk level identifier (low_risk, high_risk, very_high_risk)",
        example="low_risk"
    )
    
    mortality_rate: str = Field(
        ...,
        description="In-hospital mortality rate for this risk category",
        example="0.86%"
    )
    
    detailed_assessment: Dict[str, Any] = Field(
        ...,
        description="Comprehensive clinical assessment including parameter analysis and timing breakdown",
        example={
            "total_score": 6,
            "risk_category": "Low Risk",
            "mortality_risk": "0.86%",
            "clinical_significance": False,
            "parameter_analysis": {
                "severe_comorbidities": {"value": "yes", "points": 6, "significant": True}
            },
            "risk_factors_present": [
                {"factor": "severe_comorbidities", "points": 6, "description": "Severe comorbidities present"}
            ],
            "timing_breakdown": {
                "presentation": {"score": 6, "significance": "Moderate early risk - enhanced monitoring recommended"}
            },
            "clinical_alerts": ["Multiple comorbidities present - consider multidisciplinary approach"]
        }
    )
    
    recommendations: Dict[str, List[str]] = Field(
        ...,
        description="Clinical recommendations including immediate actions, monitoring, and treatment",
        example={
            "immediate_actions": [
                "Standard DKA management protocols",
                "Regular monitoring of vital signs and laboratory values"
            ],
            "monitoring": [
                "Vital signs every 4-6 hours",
                "Laboratory monitoring every 4-6 hours initially"
            ],
            "treatment": [
                "Standard DKA insulin protocol",
                "Standard fluid replacement protocol"
            ]
        }
    )
    
    parameter_breakdown: Dict[str, Any] = Field(
        ...,
        description="Detailed breakdown of each parameter with points and significance",
        example={
            "severe_comorbidities": {
                "value": "yes",
                "points": 6,
                "description": "Severe comorbidities present",
                "significant": True,
                "timing": "presentation"
            }
        }
    )
    
    timing_assessment: Dict[str, Any] = Field(
        ...,
        description="Assessment of parameters by timing (presentation, 12h, 24h)",
        example={
            "presentation": {
                "score": 6,
                "assessment": "Moderate early risk - enhanced monitoring recommended",
                "parameters": {
                    "severe_comorbidities": {"value": "yes", "points": 6}
                }
            },
            "12_hours": {
                "score": 0,
                "assessment": "Good early response",
                "parameters": {
                    "insulin_over_50_units": {"value": "no", "points": 0}
                }
            },
            "24_hours": {
                "score": 0,
                "assessment": "No late complications",
                "parameters": {
                    "depressed_mental_state_24h": {"value": "no", "points": 0}
                }
            }
        }
    )
    
    clinical_considerations: Dict[str, Any] = Field(
        ...,
        description="Clinical considerations including admission recommendations and limitations",
        example={
            "admission_recommendation": "General medical ward admission typically appropriate",
            "monitoring_intensity": "Standard monitoring protocols",
            "family_communication": "Reassure family about good prognosis with standard treatment",
            "quality_improvement": ["Standard quality metrics monitoring"],
            "limitations": [
                "Score not externally validated - use clinical judgment",
                "APACHE II may be superior mortality predictor"
            ]
        }
    )
    
    monitoring_guidance: Dict[str, Any] = Field(
        ...,
        description="Detailed monitoring guidance including frequency and parameters",
        example={
            "frequency": {
                "vital_signs": "Every 4-6 hours",
                "laboratory": "Every 4-6 hours initially",
                "glucose": "Every 2-4 hours",
                "neurological": "Every 4-6 hours"
            },
            "parameters": [
                "Blood glucose",
                "Serum electrolytes",
                "Arterial blood gas",
                "Vital signs",
                "Mental status"
            ],
            "escalation_criteria": [
                "Worsening mental status",
                "Hemodynamic instability",
                "Worsening acidosis despite treatment"
            ],
            "duration": "Until acidosis resolves and patient stable for 12-24 hours"
        }
    )
    
    prognosis_counseling: Dict[str, Any] = Field(
        ...,
        description="Prognostic counseling guidance for clinicians and families",
        example={
            "mortality_discussion": "Excellent prognosis with appropriate treatment (>99% survival expected)",
            "prognostic_factors": [
                "Favorable prognostic profile",
                "Expected good response to treatment"
            ],
            "goals_of_care": "Focus on recovery and diabetes management education",
            "family_preparation": "Prepare family for standard recovery course"
        }
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 6,
                "unit": "points",
                "interpretation": "DKA MPM Score of 6 points indicates Low Risk with 0.86% in-hospital mortality risk. Low risk of in-hospital mortality. Standard DKA management protocols are appropriate. Routine monitoring and care expected to be sufficient.",
                "stage": "Low Risk",
                "stage_description": "Low risk of in-hospital mortality",
                "total_score": 6,
                "risk_level": "low_risk",
                "mortality_rate": "0.86%",
                "detailed_assessment": {
                    "total_score": 6,
                    "risk_category": "Low Risk",
                    "mortality_risk": "0.86%",
                    "clinical_significance": False,
                    "parameter_analysis": {
                        "severe_comorbidities": {
                            "value": "yes",
                            "points": 6,
                            "significant": True
                        },
                        "ph_less_than_7": {
                            "value": "no",
                            "points": 0,
                            "significant": False
                        }
                    },
                    "risk_factors_present": [
                        {
                            "factor": "severe_comorbidities",
                            "points": 6,
                            "description": "Severe comorbidities (immunosuppression, MI, COPD, cirrhosis, CHF, stroke)"
                        }
                    ],
                    "timing_breakdown": {
                        "presentation": {
                            "score": 6,
                            "parameters": ["severe_comorbidities", "ph_less_than_7"],
                            "significance": "Moderate early risk - enhanced monitoring recommended"
                        },
                        "12_hours": {
                            "score": 0,
                            "parameters": ["insulin_over_50_units", "glucose_over_300_at_12h"],
                            "significance": "Good early response"
                        },
                        "24_hours": {
                            "score": 0,
                            "parameters": ["depressed_mental_state_24h", "fever_24h"],
                            "significance": "No late complications"
                        }
                    },
                    "clinical_alerts": [
                        "Multiple comorbidities present - consider multidisciplinary approach"
                    ]
                },
                "recommendations": {
                    "immediate_actions": [
                        "Standard DKA management protocols",
                        "Regular monitoring of vital signs and laboratory values",
                        "Routine fluid and electrolyte replacement",
                        "Monitor for improvement in acidosis and ketosis",
                        "Consider general medical ward admission",
                        "Standard frequency laboratory monitoring (q4-6h initially)"
                    ],
                    "monitoring": [
                        "Vital signs every 4-6 hours",
                        "Laboratory monitoring every 4-6 hours initially",
                        "Blood glucose monitoring every 2-4 hours",
                        "Neurological checks every 4-6 hours",
                        "Fluid balance monitoring"
                    ],
                    "treatment": [
                        "Standard DKA insulin protocol",
                        "Standard fluid replacement protocol",
                        "Electrolyte replacement as needed",
                        "Monitor for improvement in acidosis"
                    ]
                },
                "parameter_breakdown": {
                    "severe_comorbidities": {
                        "value": "yes",
                        "points": 6,
                        "description": "Severe comorbidities (immunosuppression, MI, COPD, cirrhosis, CHF, stroke)",
                        "significant": True,
                        "timing": "presentation"
                    },
                    "ph_less_than_7": {
                        "value": "no",
                        "points": 0,
                        "description": "Severe acidosis (pH < 7.0)",
                        "significant": False,
                        "timing": "presentation"
                    },
                    "insulin_over_50_units": {
                        "value": "no",
                        "points": 0,
                        "description": "High insulin requirement (>50 units in 12h)",
                        "significant": False,
                        "timing": "12_hours"
                    },
                    "glucose_over_300_at_12h": {
                        "value": "no",
                        "points": 0,
                        "description": "Persistent hyperglycemia (>300 mg/dL at 12h)",
                        "significant": False,
                        "timing": "12_hours"
                    },
                    "depressed_mental_state_24h": {
                        "value": "no",
                        "points": 0,
                        "description": "Altered mental status at 24h",
                        "significant": False,
                        "timing": "24_hours"
                    },
                    "fever_24h": {
                        "value": "no",
                        "points": 0,
                        "description": "Fever at 24h (≥38°C/100.4°F)",
                        "significant": False,
                        "timing": "24_hours"
                    }
                },
                "timing_assessment": {
                    "presentation": {
                        "score": 6,
                        "assessment": "Moderate early risk - enhanced monitoring recommended",
                        "parameters": {
                            "severe_comorbidities": {"value": "yes", "points": 6},
                            "ph_less_than_7": {"value": "no", "points": 0}
                        }
                    },
                    "12_hours": {
                        "score": 0,
                        "assessment": "Good early response",
                        "parameters": {
                            "insulin_over_50_units": {"value": "no", "points": 0},
                            "glucose_over_300_at_12h": {"value": "no", "points": 0}
                        }
                    },
                    "24_hours": {
                        "score": 0,
                        "assessment": "No late complications",
                        "parameters": {
                            "depressed_mental_state_24h": {"value": "no", "points": 0},
                            "fever_24h": {"value": "no", "points": 0}
                        }
                    }
                },
                "clinical_considerations": {
                    "admission_recommendation": "General medical ward admission typically appropriate",
                    "monitoring_intensity": "Standard monitoring protocols",
                    "family_communication": "Reassure family about good prognosis with standard treatment",
                    "quality_improvement": [
                        "Standard quality metrics monitoring",
                        "Routine outcome tracking"
                    ],
                    "limitations": [
                        "Score not externally validated - use clinical judgment",
                        "APACHE II may be superior mortality predictor",
                        "Not intended as sole basis for clinical decisions",
                        "Requires assessment at multiple time points"
                    ]
                },
                "monitoring_guidance": {
                    "frequency": {
                        "vital_signs": "Every 4-6 hours",
                        "laboratory": "Every 4-6 hours initially",
                        "glucose": "Every 2-4 hours",
                        "neurological": "Every 4-6 hours"
                    },
                    "parameters": [
                        "Blood glucose",
                        "Serum electrolytes (Na, K, Cl, CO2)",
                        "Arterial blood gas",
                        "Serum ketones or urine ketones",
                        "Vital signs (BP, HR, RR, temp)",
                        "Mental status",
                        "Fluid balance"
                    ],
                    "escalation_criteria": [
                        "Worsening mental status",
                        "Hemodynamic instability",
                        "Worsening acidosis despite treatment",
                        "Persistent severe hyperglycemia",
                        "Development of complications",
                        "Any parameter suggesting higher risk category"
                    ],
                    "duration": "Until acidosis resolves and patient stable for 12-24 hours"
                },
                "prognosis_counseling": {
                    "mortality_discussion": "Excellent prognosis with appropriate treatment (>99% survival expected)",
                    "prognostic_factors": [
                        "Favorable prognostic profile",
                        "Expected good response to treatment"
                    ],
                    "goals_of_care": "Focus on recovery and diabetes management education",
                    "family_preparation": "Prepare family for standard recovery course"
                }
            }
        }