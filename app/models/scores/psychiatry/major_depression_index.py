"""
Major Depression Inventory (MDI) Models

Request and response models for Major Depression Inventory calculation.

References (Vancouver style):
1. Bech P, Rasmussen NA, Olsen LR, Noerholm V, Abildgaard W. The sensitivity and 
   specificity of the Major Depression Inventory, using the Present State Examination 
   as the index of diagnostic validity. J Affect Disord. 2001 Oct;66(2-3):159-64. 
   doi: 10.1016/s0165-0327(00)00309-3.
2. Olsen LR, Jensen DV, Noerholm V, Martiny K, Bech P. The internal and external 
   validity of the Major Depression Inventory in measuring severity of depressive states. 
   Psychol Med. 2003 Feb;33(2):351-6. doi: 10.1017/s0033291702007041.
3. Cuijpers P, Li J, Hofmann SG, Andersson G. Self-reported versus clinician-rated 
   symptoms of depression as outcome measures in psychotherapy research on depression: 
   a meta-analysis. Clin Psychol Rev. 2010 Nov;30(7):768-78. 
   doi: 10.1016/j.cpr.2010.06.003.

The Major Depression Inventory (MDI) is a WHO-developed self-report questionnaire 
that uniquely provides both diagnostic assessment and severity grading for depression. 
Based on ICD-10 and DSM-IV criteria, it consists of 10 items covering core symptoms 
of major depression over the past 2 weeks. The MDI is available free of charge, 
translated into seven languages, and widely used in clinical practice and research.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any


class MajorDepressionIndexRequest(BaseModel):
    """
    Request model for Major Depression Inventory (MDI)
    
    The MDI assesses depression symptoms over the past 2 weeks using 10 items:
    
    Core Symptoms (DSM-IV/ICD-10 criteria):
    1. Depressed Mood: Feeling sad or depressed
    2. Lack of Interest: Lost interest in daily activities
    
    Additional Symptoms:
    3. Lack of Energy: Lacking in energy and strength
    4. Low Self-Confidence: Feeling less self-confident
    5. Bad Conscience: Bad conscience or feelings of guilt
    6. Life Not Worth Living: Feeling that life wasn't worth living (SUICIDE RISK)
    7. Concentration Problems: Difficulty concentrating
    8. Agitation/Restlessness: Feeling very restless
    9. Psychomotor Retardation: Movements have been slower
    10. Sleep Problems: Trouble sleeping at night
    
    Scoring System:
    - Not at all: 0 points
    - Some of the time: 1 point
    - Most of the time: 2 points
    - All the time: 3 points
    
    Diagnostic Criteria:
    - At least 1 core symptom present most/all of the time
    - Total of at least 5 symptoms present some/most/all of the time
    - Symptoms present for at least 2 weeks
    
    Severity Classification:
    - 0-13 points: No Depression
    - 14-20 points: Mild Depression
    - 21-25 points: Moderate Depression
    - 26-30 points: Severe Depression
    
    Clinical Applications:
    - Depression screening in primary care and mental health settings
    - Monitoring treatment response over time
    - Research on depression prevalence and outcomes
    - Clinical trial outcome assessment
    - Epidemiological studies

    References (Vancouver style):
    1. Bech P, Rasmussen NA, Olsen LR, Noerholm V, Abildgaard W. The sensitivity and 
    specificity of the Major Depression Inventory, using the Present State Examination 
    as the index of diagnostic validity. J Affect Disord. 2001 Oct;66(2-3):159-64. 
    doi: 10.1016/s0165-0327(00)00309-3.
    2. Olsen LR, Jensen DV, Noerholm V, Martiny K, Bech P. The internal and external 
    validity of the Major Depression Inventory in measuring severity of depressive states. 
    Psychol Med. 2003 Feb;33(2):351-6. doi: 10.1017/s0033291702007041.
    3. Cuijpers P, Li J, Hofmann SG, Andersson G. Self-reported versus clinician-rated 
    symptoms of depression as outcome measures in psychotherapy research on depression: 
    a meta-analysis. Clin Psychol Rev. 2010 Nov;30(7):768-78. 
    doi: 10.1016/j.cpr.2010.06.003.
    """
    
    depressed_mood: Literal["not_at_all", "some_of_time", "most_of_time", "all_the_time"] = Field(
        ...,
        description="How much of the time during the past 2 weeks have you felt sad or depressed? This is a core symptom required for depression diagnosis.",
        example="most_of_time"
    )
    
    lack_of_interest: Literal["not_at_all", "some_of_time", "most_of_time", "all_the_time"] = Field(
        ...,
        description="How much of the time during the past 2 weeks have you lost interest in your daily activities? This is a core symptom required for depression diagnosis.",
        example="most_of_time"
    )
    
    lack_of_energy: Literal["not_at_all", "some_of_time", "most_of_time", "all_the_time"] = Field(
        ...,
        description="How much of the time during the past 2 weeks have you felt lacking in energy and strength? Fatigue is a common depression symptom.",
        example="some_of_time"
    )
    
    low_self_confidence: Literal["not_at_all", "some_of_time", "most_of_time", "all_the_time"] = Field(
        ...,
        description="How much of the time during the past 2 weeks have you felt less self-confident? Low self-esteem is characteristic of depression.",
        example="some_of_time"
    )
    
    bad_conscience: Literal["not_at_all", "some_of_time", "most_of_time", "all_the_time"] = Field(
        ...,
        description="How much of the time during the past 2 weeks have you had a bad conscience or feelings of guilt? Guilt and self-blame are common in depression.",
        example="not_at_all"
    )
    
    life_not_worth_living: Literal["not_at_all", "some_of_time", "most_of_time", "all_the_time"] = Field(
        ...,
        description="How much of the time during the past 2 weeks have you felt that life wasn't worth living? CRITICAL: Positive responses require immediate suicide risk assessment.",
        example="not_at_all"
    )
    
    concentration_problems: Literal["not_at_all", "some_of_time", "most_of_time", "all_the_time"] = Field(
        ...,
        description="How much of the time during the past 2 weeks have you had difficulty concentrating? Cognitive symptoms are common in depression.",
        example="some_of_time"
    )
    
    agitation_restlessness: Literal["not_at_all", "some_of_time", "most_of_time", "all_the_time"] = Field(
        ...,
        description="How much of the time during the past 2 weeks have you felt very restless? Psychomotor agitation can accompany depression.",
        example="not_at_all"
    )
    
    psychomotor_retardation: Literal["not_at_all", "some_of_time", "most_of_time", "all_the_time"] = Field(
        ...,
        description="How much of the time during the past 2 weeks have you felt that your movements have been slower? Psychomotor retardation is a depression symptom.",
        example="not_at_all"
    )
    
    sleep_problems: Literal["not_at_all", "some_of_time", "most_of_time", "all_the_time"] = Field(
        ...,
        description="How much of the time during the past 2 weeks have you had trouble sleeping at night? Sleep disturbances are very common in depression.",
        example="some_of_time"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "depressed_mood": "most_of_time",
                "lack_of_interest": "most_of_time",
                "lack_of_energy": "some_of_time",
                "low_self_confidence": "some_of_time",
                "bad_conscience": "not_at_all",
                "life_not_worth_living": "not_at_all",
                "concentration_problems": "some_of_time",
                "agitation_restlessness": "not_at_all",
                "psychomotor_retardation": "not_at_all",
                "sleep_problems": "some_of_time"
            }
        }


class MajorDepressionIndexResponse(BaseModel):
    """
    Response model for Major Depression Inventory (MDI)
    
    The MDI provides comprehensive depression assessment including:
    - Total score (0-30 points)
    - Severity classification (No/Mild/Moderate/Severe Depression)
    - Diagnostic criteria assessment
    - Suicide risk flagging
    - Clinical recommendations for treatment and monitoring
    
    Severity Levels and Recommended Actions:
    - No Depression (0-13): Routine monitoring, preventive care, lifestyle factors
    - Mild Depression (14-20): Watchful waiting, psychosocial interventions, counseling
    - Moderate Depression (21-25): Treatment required, psychotherapy and/or medication
    - Severe Depression (26-30): Immediate treatment, combined therapy, psychiatric referral
    
    Reference: Bech P, et al. J Affect Disord. 2001;66(2-3):159-64.
    """
    
    result: Dict[str, Any] = Field(
        ...,
        description="MDI assessment results including total score, diagnostic criteria, and suicide risk flag",
        example={
            "total_score": 15,
            "diagnostic_criteria_met": True,
            "core_symptoms": 2,
            "additional_symptoms": 3,
            "suicide_risk_flag": False
        }
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with treatment recommendations and diagnostic assessment",
        example="Mild depression present. Consider watchful waiting, psychosocial interventions, counseling, or brief therapy. Monitor closely for symptom progression. Lifestyle modifications and social support may be beneficial. Diagnostic criteria for major depression are met (2 core symptoms, 3 additional symptoms)."
    )
    
    stage: str = Field(
        ...,
        description="Depression severity classification",
        example="Mild Depression"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the severity level",
        example="Mild depressive symptoms"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": {
                    "total_score": 15,
                    "diagnostic_criteria_met": True,
                    "core_symptoms": 2,
                    "additional_symptoms": 3,
                    "suicide_risk_flag": False
                },
                "unit": "points",
                "interpretation": "Mild depression present. Consider watchful waiting, psychosocial interventions, counseling, or brief therapy. Monitor closely for symptom progression. Lifestyle modifications and social support may be beneficial. Diagnostic criteria for major depression are met (2 core symptoms, 3 additional symptoms).",
                "stage": "Mild Depression",
                "stage_description": "Mild depressive symptoms"
            }
        }