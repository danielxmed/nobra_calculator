"""
Diabetes Distress Scale (DDS17) Models

Request and response models for DDS17 calculation.

References (Vancouver style):
1. Polonsky WH, Fisher L, Earles J, et al. Assessing psychosocial distress in diabetes: 
   development of the diabetes distress scale. Diabetes Care. 2005;28(3):626-631. 
   doi: 10.2337/diacare.28.3.626.
2. Fisher L, Hessler DM, Polonsky WH, Mullan J. When is diabetes distress clinically 
   meaningful?: establishing cut points for the Diabetes Distress Scale. Diabetes Care. 
   2012;35(2):259-264. doi: 10.2337/dc11-1572.
3. Fisher L, Glasgow RE, Mullan JT, Skaff MM, Polonsky WH. Development of a brief 
   diabetes distress screening instrument. Ann Fam Med. 2008;6(3):246-252. 
   doi: 10.1370/afm.842.
4. Hessler D, Fisher L, Polonsky W, et al. Diabetes distress is linked with worsening 
   diabetes management over time in adults with Type 1 diabetes. Diabet Med. 
   2017;34(9):1228-1234. doi: 10.1111/dme.13381.

The Diabetes Distress Scale (DDS17) is a validated 17-item questionnaire that measures 
diabetes-related emotional distress across four domains: emotional burden, physician 
distress, regimen distress, and interpersonal distress. It provides both a total score 
and subscale scores to identify specific sources of distress for targeted intervention.
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Any


class DiabetesDistressScaleRequest(BaseModel):
    """
    Request model for Diabetes Distress Scale (DDS17)
    
    The DDS17 measures diabetes-related emotional distress using 17 items rated on a 
    6-point Likert scale. Each item asks about problems experienced in the past month:
    
    Rating Scale:
    - 1 = Not a problem
    - 2 = A slight problem  
    - 3 = A moderate problem
    - 4 = Somewhat serious problem
    - 5 = A serious problem
    - 6 = A very serious problem
    
    Four Subscales:
    
    **Emotional Burden (5 items):** Emotional distress related to living with diabetes
    - Feeling overwhelmed by diabetes demands
    - Feeling discouraged with diabetes regimen
    - Feeling like failing with diabetes regimen
    - Feeling angry, scared, or depressed about diabetes
    - Diabetes taking too much mental/physical energy
    
    **Physician Distress (4 items):** Distress related to healthcare provider relationship
    - Feeling unsatisfied with diabetes physician
    - Physician doesn't know enough about diabetes
    - Physician doesn't give clear directions
    - Physician doesn't take concerns seriously
    
    **Regimen Distress (5 items):** Distress related to diabetes management regimen
    - Feeling regimen is overwhelming
    - Blood sugar checking is stressful
    - Diabetes interferes with diet
    - Regimen doesn't make sense
    - Not having clear diabetes care goals
    
    **Interpersonal Distress (3 items):** Distress related to family and social support
    - Friends/family not supportive enough
    - Friends/family act like 'diabetes police'
    - Friends/family don't understand diabetes difficulties
    
    Scoring:
    - Total Score: Sum of all 17 items divided by 17 (range 1.0-6.0)
    - Subscale Scores: Sum of subscale items divided by number of items in subscale
    - Clinical Significance: Total score ≥3.0 indicates high distress requiring intervention
    
    References:
    1. Polonsky WH, et al. Diabetes Care. 2005;28(3):626-631.
    2. Fisher L, et al. Diabetes Care. 2012;35(2):259-264.
    3. Fisher L, et al. Ann Fam Med. 2008;6(3):246-252.
    4. Hessler D, et al. Diabet Med. 2017;34(9):1228-1234.
    """
    
    overwhelming_demands: int = Field(
        ...,
        ge=1, le=6,
        description="Feeling overwhelmed by the demands of living with diabetes (1=Not a problem, 6=Very serious problem)",
        example=3
    )
    
    feeling_discouraged: int = Field(
        ...,
        ge=1, le=6,
        description="Feeling discouraged with your diabetes regimen (1=Not a problem, 6=Very serious problem)",
        example=2
    )
    
    failure_regimen: int = Field(
        ...,
        ge=1, le=6,
        description="Feeling that I am often failing with my diabetes regimen (1=Not a problem, 6=Very serious problem)",
        example=2
    )
    
    clear_concrete_goals: int = Field(
        ...,
        ge=1, le=6,
        description="Not having clear and concrete goals for your diabetes care (1=Not a problem, 6=Very serious problem)",
        example=2
    )
    
    not_motivated: int = Field(
        ...,
        ge=1, le=6,
        description="Not feeling motivated to keep up your diabetes self-management (1=Not a problem, 6=Very serious problem)",
        example=3
    )
    
    angry_frustrated: int = Field(
        ...,
        ge=1, le=6,
        description="Feeling angry, scared, and/or depressed when you think about living with diabetes (1=Not a problem, 6=Very serious problem)",
        example=3
    )
    
    unsatisfied_care: int = Field(
        ...,
        ge=1, le=6,
        description="Feeling unsatisfied with your diabetes physician (1=Not a problem, 6=Very serious problem)",
        example=1
    )
    
    physician_communication: int = Field(
        ...,
        ge=1, le=6,
        description="Feeling that your physician doesn't know enough about diabetes and diabetes care (1=Not a problem, 6=Very serious problem)",
        example=1
    )
    
    physician_doesnt_give_direction: int = Field(
        ...,
        ge=1, le=6,
        description="Feeling that your physician doesn't give you clear enough directions for managing your diabetes (1=Not a problem, 6=Very serious problem)",
        example=1
    )
    
    physician_doesnt_take_seriously: int = Field(
        ...,
        ge=1, le=6,
        description="Feeling that your physician doesn't take your concerns seriously enough (1=Not a problem, 6=Very serious problem)",
        example=1
    )
    
    regimen_overwhelming: int = Field(
        ...,
        ge=1, le=6,
        description="Feeling that the regimen my physician has given me is overwhelming (1=Not a problem, 6=Very serious problem)",
        example=2
    )
    
    constant_thoughts: int = Field(
        ...,
        ge=1, le=6,
        description="Feeling that diabetes is taking up too much mental and physical energy every day (1=Not a problem, 6=Very serious problem)",
        example=4
    )
    
    blood_sugar_checking: int = Field(
        ...,
        ge=1, le=6,
        description="Feeling that checking my blood sugars is stressful (1=Not a problem, 6=Very serious problem)",
        example=2
    )
    
    regimen_burden: int = Field(
        ...,
        ge=1, le=6,
        description="Feeling that diabetes interferes with my diet (1=Not a problem, 6=Very serious problem)",
        example=3
    )
    
    friends_family_nagging: int = Field(
        ...,
        ge=1, le=6,
        description="Feeling that friends or family are not supportive enough of self-care efforts (1=Not a problem, 6=Very serious problem)",
        example=2
    )
    
    friends_family_interference: int = Field(
        ...,
        ge=1, le=6,
        description="Feeling that friends or family act like 'diabetes police' (1=Not a problem, 6=Very serious problem)",
        example=1
    )
    
    friends_family_dont_understand: int = Field(
        ...,
        ge=1, le=6,
        description="Feeling that friends or family don't understand how difficult living with diabetes can be (1=Not a problem, 6=Very serious problem)",
        example=3
    )
    
    class Config:
        schema_extra = {
            "example": {
                "overwhelming_demands": 3,
                "feeling_discouraged": 2,
                "failure_regimen": 2,
                "clear_concrete_goals": 2,
                "not_motivated": 3,
                "angry_frustrated": 3,
                "unsatisfied_care": 1,
                "physician_communication": 1,
                "physician_doesnt_give_direction": 1,
                "physician_doesnt_take_seriously": 1,
                "regimen_overwhelming": 2,
                "constant_thoughts": 4,
                "blood_sugar_checking": 2,
                "regimen_burden": 3,
                "friends_family_nagging": 2,
                "friends_family_interference": 1,
                "friends_family_dont_understand": 3
            }
        }


class DiabetesDistressScaleResponse(BaseModel):
    """
    Response model for Diabetes Distress Scale (DDS17)
    
    The DDS17 provides comprehensive assessment of diabetes-related distress including:
    - Total DDS17 score (1.0-6.0 scale)
    - Four subscale scores (Emotional Burden, Physician Distress, Regimen Distress, Interpersonal Distress)
    - Clinical significance determination (≥3.0 indicates high distress)
    - Targeted intervention recommendations based on subscale patterns
    - Follow-up and monitoring guidance
    
    Score Interpretation:
    - 1.0-1.9: Little or No Distress (minimal intervention needed)
    - 2.0-2.9: Moderate Distress (targeted support recommended)
    - 3.0-6.0: High Distress (clinical intervention warranted)
    
    Reference: Polonsky WH, et al. Diabetes Care. 2005;28(3):626-631.
    """
    
    result: float = Field(
        ...,
        description="DDS17 total score calculated from all 17 items (range: 1.0-6.0)",
        example=2.24
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="DDS17 Score (1-6 scale)"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with distress level and intervention recommendations",
        example="DDS17 total score of 2.24 indicates Moderate Distress. Moderate diabetes-related distress. Highest distress areas: Emotional Burden, Regimen Distress. Monitor for progression and consider targeted support for identified areas of concern."
    )
    
    stage: str = Field(
        ...,
        description="Distress level classification (Little or No Distress, Moderate Distress, High Distress)",
        example="Moderate Distress"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the distress level",
        example="Moderate diabetes-related distress"
    )
    
    total_score: float = Field(
        ...,
        description="The calculated DDS17 total score",
        example=2.24
    )
    
    distress_level: str = Field(
        ...,
        description="Distress level identifier (little_no_distress, moderate_distress, high_distress)",
        example="moderate_distress"
    )
    
    subscale_scores: Dict[str, float] = Field(
        ...,
        description="Scores for each of the four DDS17 subscales",
        example={
            "emotional_burden": 2.80,
            "physician_distress": 1.00,
            "regimen_distress": 2.20,
            "interpersonal_distress": 2.00
        }
    )
    
    clinical_assessment: Dict[str, Any] = Field(
        ...,
        description="Comprehensive clinical assessment including subscale breakdown and indicators",
        example={
            "total_score": 2.24,
            "distress_level": "moderate_distress",
            "clinical_significance": False,
            "subscale_breakdown": {
                "emotional_burden": {"score": 2.80, "level": "Moderate", "description": "Emotional distress related to living with diabetes"},
                "physician_distress": {"score": 1.00, "level": "Low", "description": "Distress related to healthcare provider relationship"}
            },
            "highest_distress_areas": [
                {"subscale": "emotional_burden", "score": 2.80, "description": "Emotional distress related to living with diabetes"}
            ],
            "clinical_indicators": ["Monitor for progression to high distress level"]
        }
    )
    
    recommendations: Dict[str, List[str]] = Field(
        ...,
        description="Clinical recommendations including immediate actions and subscale-specific interventions",
        example={
            "immediate_actions": [
                "Consider targeted support and intervention",
                "Discuss specific sources of diabetes distress with patient"
            ],
            "subscale_specific": [
                "Address emotional burden through stress management techniques"
            ],
            "long_term_strategies": [
                "Maintain supportive diabetes care environment",
                "Periodic reassessment of diabetes distress levels"
            ]
        }
    )
    
    subscale_analysis: Dict[str, Any] = Field(
        ...,
        description="Detailed analysis of each subscale with intervention recommendations",
        example={
            "emotional_burden": {
                "score": 2.80,
                "level": "Moderate",
                "clinical_significance": False,
                "intervention_focus": ["Stress management and coping skills training"]
            }
        }
    )
    
    intervention_priorities: List[Dict[str, Any]] = Field(
        ...,
        description="Prioritized list of intervention areas based on subscale scores",
        example=[
            {
                "priority": 1,
                "subscale": "emotional_burden",
                "score": 2.80,
                "priority_level": "High",
                "intervention_needed": False,
                "focus_areas": ["Stress management and coping skills training"]
            }
        ]
    )
    
    follow_up_recommendations: Dict[str, Any] = Field(
        ...,
        description="Follow-up recommendations including frequency and monitoring tools",
        example={
            "frequency": "Every 3-6 months",
            "monitoring_tools": ["DDS17 re-administration", "Routine diabetes care visits"],
            "care_coordination": "Primary care provider with diabetes education support",
            "response_indicators": ["Stable or reduced distress scores", "Maintained diabetes outcomes"]
        }
    )
    
    referral_considerations: List[str] = Field(
        ...,
        description="Referral considerations based on distress level and subscale patterns",
        example=["Continue with current care team"]
    )
    
    monitoring_guidance: Dict[str, Any] = Field(
        ...,
        description="Monitoring guidance including reassessment intervals and success indicators",
        example={
            "reassessment_interval": "Every 6 months",
            "monitoring_parameters": [
                "DDS17 score trends over time",
                "Glycemic control (HbA1c)",
                "Diabetes self-care behaviors"
            ],
            "red_flags": [
                "Increasing DDS17 scores over time",
                "Worsening glycemic control"
            ],
            "success_indicators": [
                "Stable or decreasing distress scores",
                "Improved diabetes self-management"
            ]
        }
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 2.24,
                "unit": "DDS17 Score (1-6 scale)",
                "interpretation": "DDS17 total score of 2.24 indicates Moderate Distress. Moderate diabetes-related distress. Highest distress areas: Emotional Burden, Regimen Distress. Monitor for progression and consider targeted support for identified areas of concern.",
                "stage": "Moderate Distress",
                "stage_description": "Moderate diabetes-related distress",
                "total_score": 2.24,
                "distress_level": "moderate_distress",
                "subscale_scores": {
                    "emotional_burden": 2.80,
                    "physician_distress": 1.00,
                    "regimen_distress": 2.20,
                    "interpersonal_distress": 2.00
                },
                "clinical_assessment": {
                    "total_score": 2.24,
                    "distress_level": "moderate_distress",
                    "clinical_significance": False,
                    "subscale_breakdown": {
                        "emotional_burden": {
                            "score": 2.80,
                            "level": "Moderate",
                            "description": "Emotional distress related to living with diabetes"
                        },
                        "physician_distress": {
                            "score": 1.00,
                            "level": "Low",
                            "description": "Distress related to healthcare provider relationship"
                        },
                        "regimen_distress": {
                            "score": 2.20,
                            "level": "Moderate",
                            "description": "Distress related to diabetes management regimen"
                        },
                        "interpersonal_distress": {
                            "score": 2.00,
                            "level": "Moderate",
                            "description": "Distress related to family and social support"
                        }
                    },
                    "highest_distress_areas": [
                        {
                            "subscale": "emotional_burden",
                            "score": 2.80,
                            "description": "Emotional distress related to living with diabetes"
                        },
                        {
                            "subscale": "regimen_distress",
                            "score": 2.20,
                            "description": "Distress related to diabetes management regimen"
                        }
                    ],
                    "individual_item_analysis": {
                        "highest_scoring_items": [
                            {
                                "item_number": 12,
                                "parameter": "constant_thoughts",
                                "score": 4,
                                "severity": "Moderate"
                            }
                        ],
                        "items_needing_attention": [
                            {
                                "item_number": 12,
                                "parameter": "constant_thoughts",
                                "score": 4,
                                "severity": "Moderate"
                            }
                        ]
                    },
                    "clinical_indicators": []
                },
                "recommendations": {
                    "immediate_actions": [
                        "Consider targeted support and intervention",
                        "Discuss specific sources of diabetes distress with patient",
                        "Develop targeted coping strategies for identified stressors",
                        "Consider diabetes education or support group referral",
                        "Monitor distress levels more frequently (every 3-6 months)",
                        "Address specific subscale areas with elevated scores"
                    ],
                    "subscale_specific": [],
                    "long_term_strategies": [
                        "Maintain supportive diabetes care environment",
                        "Periodic reassessment of diabetes distress levels",
                        "Continue diabetes education and skill building",
                        "Promote diabetes self-efficacy and empowerment"
                    ]
                },
                "subscale_analysis": {
                    "emotional_burden": {
                        "score": 2.80,
                        "level": "Moderate",
                        "description": "Emotional distress related to living with diabetes",
                        "clinical_significance": False,
                        "intervention_focus": ["Continue current support in this area"]
                    },
                    "physician_distress": {
                        "score": 1.00,
                        "level": "Low",
                        "description": "Distress related to healthcare provider relationship",
                        "clinical_significance": False,
                        "intervention_focus": ["Continue current support in this area"]
                    },
                    "regimen_distress": {
                        "score": 2.20,
                        "level": "Moderate",
                        "description": "Distress related to diabetes management regimen",
                        "clinical_significance": False,
                        "intervention_focus": ["Continue current support in this area"]
                    },
                    "interpersonal_distress": {
                        "score": 2.00,
                        "level": "Moderate",
                        "description": "Distress related to family and social support",
                        "clinical_significance": False,
                        "intervention_focus": ["Continue current support in this area"]
                    }
                },
                "intervention_priorities": [
                    {
                        "priority": 1,
                        "subscale": "emotional_burden",
                        "score": 2.80,
                        "priority_level": "High",
                        "description": "Emotional distress related to living with diabetes",
                        "intervention_needed": False,
                        "focus_areas": ["Continue current support in this area"]
                    },
                    {
                        "priority": 2,
                        "subscale": "regimen_distress",
                        "score": 2.20,
                        "priority_level": "Medium",
                        "description": "Distress related to diabetes management regimen",
                        "intervention_needed": False,
                        "focus_areas": ["Continue current support in this area"]
                    },
                    {
                        "priority": 3,
                        "subscale": "interpersonal_distress",
                        "score": 2.00,
                        "priority_level": "Low",
                        "description": "Distress related to family and social support",
                        "intervention_needed": False,
                        "focus_areas": ["Continue current support in this area"]
                    },
                    {
                        "priority": 4,
                        "subscale": "physician_distress",
                        "score": 1.00,
                        "priority_level": "Low",
                        "description": "Distress related to healthcare provider relationship",
                        "intervention_needed": False,
                        "focus_areas": ["Continue current support in this area"]
                    }
                ],
                "follow_up_recommendations": {
                    "frequency": "Every 3-6 months",
                    "monitoring_tools": [
                        "DDS17 re-administration",
                        "Routine diabetes care visits"
                    ],
                    "care_coordination": "Primary care provider with diabetes education support",
                    "response_indicators": [
                        "Stable or reduced distress scores",
                        "Maintained diabetes outcomes"
                    ]
                },
                "referral_considerations": [
                    "Continue with current care team"
                ],
                "monitoring_guidance": {
                    "reassessment_interval": "Every 6 months",
                    "monitoring_parameters": [
                        "DDS17 score trends over time",
                        "Glycemic control (HbA1c)",
                        "Diabetes self-care behaviors",
                        "Quality of life indicators",
                        "Healthcare utilization patterns"
                    ],
                    "red_flags": [
                        "Increasing DDS17 scores over time",
                        "Worsening glycemic control",
                        "Decreased self-care adherence",
                        "New or worsening mental health symptoms",
                        "Social isolation or family conflict"
                    ],
                    "success_indicators": [
                        "Stable or decreasing distress scores",
                        "Improved diabetes self-management",
                        "Enhanced patient-provider relationship",
                        "Better family/social support",
                        "Increased diabetes self-efficacy"
                    ]
                }
            }
        }