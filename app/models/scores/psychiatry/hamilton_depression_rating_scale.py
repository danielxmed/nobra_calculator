"""
Hamilton Depression Rating Scale Models

Request and response models for Hamilton Depression Rating Scale (HAM-D) calculation.

References (Vancouver style):
1. Hamilton M. A rating scale for depression. J Neurol Neurosurg Psychiatry. 
   1960 Feb;23(1):56-62. doi: 10.1136/jnnp.23.1.56.
2. Zimmerman M, Martinez JH, Young D, Chelminski I, Dalrymple K. Severity 
   classification on the Hamilton Depression Rating Scale. J Affect Disord. 
   2013 Sep 5;150(2):384-8. doi: 10.1016/j.jad.2013.04.028.
3. Williams JB. A structured interview guide for the Hamilton Depression Rating 
   Scale. Arch Gen Psychiatry. 1988 Aug;45(8):742-7. 
   doi: 10.1001/archpsyc.1988.01800320058007.
4. Bagby RM, Ryder AG, Schuller DR, Marshall MB. The Hamilton Depression Rating 
   Scale: has the gold standard become a lead weight? Am J Psychiatry. 
   2004 Dec;161(12):2163-77. doi: 10.1176/appi.ajp.161.12.2163.

The Hamilton Depression Rating Scale (HAM-D) is a clinician-administered assessment 
tool that measures the severity of depressive symptoms. The 17-item version evaluates 
symptoms over the past week across multiple domains including mood, guilt, suicidal 
ideation, insomnia, psychomotor symptoms, anxiety, somatic symptoms, and insight. 
It remains one of the most widely used depression severity scales in clinical trials 
and research settings.
"""

from pydantic import BaseModel, Field


class HamiltonDepressionRatingScaleRequest(BaseModel):
    """
    Request model for Hamilton Depression Rating Scale (HAM-D)
    
    The HAM-D-17 assesses depressive symptoms across 17 items:
    - Items scored 0-4: depressed mood, guilt, suicide, work/activities, 
      retardation, psychological anxiety, somatic anxiety, hypochondriasis
    - Items scored 0-2: insomnia (early/middle/late), agitation, GI symptoms, 
      general somatic symptoms, genital symptoms, weight loss, insight
    
    Total score range: 0-50 points
    
    Scoring for 0-4 items:
    - 0 = Absent
    - 1 = Mild or trivial
    - 2 = Moderate
    - 3 = Severe
    - 4 = Very severe/incapacitating
    
    Scoring for 0-2 items:
    - 0 = Absent
    - 1 = Mild to moderate
    - 2 = Severe
    
    References (Vancouver style):
    1. Hamilton M. A rating scale for depression. J Neurol Neurosurg Psychiatry. 
       1960 Feb;23(1):56-62. doi: 10.1136/jnnp.23.1.56.
    2. Zimmerman M, Martinez JH, Young D, Chelminski I, Dalrymple K. Severity 
       classification on the Hamilton Depression Rating Scale. J Affect Disord. 
       2013 Sep 5;150(2):384-8. doi: 10.1016/j.jad.2013.04.028.
    """
    
    depressed_mood: int = Field(
        ...,
        ge=0,
        le=4,
        description="Sadness, hopelessness, helplessness, worthlessness. 0=absent, 4=patient reports virtually only these feeling states",
        example=2
    )
    
    feelings_of_guilt: int = Field(
        ...,
        ge=0,
        le=4,
        description="Self-reproach, ideas of guilt or rumination over past errors. 0=absent, 4=hears accusatory voices and/or experiences threatening visual hallucinations",
        example=1
    )
    
    suicide: int = Field(
        ...,
        ge=0,
        le=4,
        description="Suicidal ideation and behavior. 0=absent, 1=feels life not worth living, 2=wishes were dead, 3=suicidal ideas/gestures, 4=attempts at suicide",
        example=0
    )
    
    insomnia_early: int = Field(
        ...,
        ge=0,
        le=2,
        description="Difficulty falling asleep. 0=no difficulty, 1=occasional difficulty (>30 min), 2=nightly difficulty",
        example=1
    )
    
    insomnia_middle: int = Field(
        ...,
        ge=0,
        le=2,
        description="Waking during the night. 0=no difficulty, 1=patient complains of being restless, 2=waking during night with difficulty returning to sleep",
        example=1
    )
    
    insomnia_late: int = Field(
        ...,
        ge=0,
        le=2,
        description="Early morning awakening. 0=no difficulty, 1=waking in early hours but goes back to sleep, 2=unable to fall asleep again if gets out of bed",
        example=1
    )
    
    work_and_activities: int = Field(
        ...,
        ge=0,
        le=4,
        description="Loss of interest in work, hobbies, or social activities. 0=no difficulty, 4=stopped working because of present illness",
        example=2
    )
    
    retardation: int = Field(
        ...,
        ge=0,
        le=4,
        description="Psychomotor retardation (slowness of thought/speech, impaired concentration). 0=normal, 4=complete stupor",
        example=1
    )
    
    agitation: int = Field(
        ...,
        ge=0,
        le=2,
        description="Psychomotor agitation. 0=none, 1=fidgetiness, 2=obvious restlessness",
        example=1
    )
    
    anxiety_psychological: int = Field(
        ...,
        ge=0,
        le=4,
        description="Psychological anxiety symptoms. 0=no difficulty, 4=fears expressed without questioning",
        example=2
    )
    
    anxiety_somatic: int = Field(
        ...,
        ge=0,
        le=4,
        description="Physical anxiety symptoms (GI, cardiovascular, respiratory). 0=absent, 4=incapacitating",
        example=1
    )
    
    somatic_symptoms_gastrointestinal: int = Field(
        ...,
        ge=0,
        le=2,
        description="Loss of appetite, GI symptoms. 0=none, 1=loss of appetite, 2=requires persuasion to eat",
        example=1
    )
    
    somatic_symptoms_general: int = Field(
        ...,
        ge=0,
        le=2,
        description="Heaviness in limbs/back/head, diffuse backache, fatigue. 0=none, 2=clear-cut symptoms",
        example=1
    )
    
    genital_symptoms: int = Field(
        ...,
        ge=0,
        le=2,
        description="Loss of libido, menstrual disturbances. 0=absent, 2=severe",
        example=0
    )
    
    hypochondriasis: int = Field(
        ...,
        ge=0,
        le=4,
        description="Preoccupation with health. 0=not present, 4=hypochondriacal delusions",
        example=1
    )
    
    loss_of_weight: int = Field(
        ...,
        ge=0,
        le=2,
        description="Weight loss. 0=none, 1=probable weight loss, 2=definite weight loss",
        example=0
    )
    
    insight: int = Field(
        ...,
        ge=0,
        le=2,
        description="Awareness of being depressed and ill. 0=acknowledges illness, 1=acknowledges but attributes to other causes, 2=denies being ill",
        example=0
    )
    
    class Config:
        schema_extra = {
            "example": {
                "depressed_mood": 2,
                "feelings_of_guilt": 1,
                "suicide": 0,
                "insomnia_early": 1,
                "insomnia_middle": 1,
                "insomnia_late": 1,
                "work_and_activities": 2,
                "retardation": 1,
                "agitation": 1,
                "anxiety_psychological": 2,
                "anxiety_somatic": 1,
                "somatic_symptoms_gastrointestinal": 1,
                "somatic_symptoms_general": 1,
                "genital_symptoms": 0,
                "hypochondriasis": 1,
                "loss_of_weight": 0,
                "insight": 0
            }
        }


class HamiltonDepressionRatingScaleResponse(BaseModel):
    """
    Response model for Hamilton Depression Rating Scale (HAM-D)
    
    The HAM-D total score ranges from 0 to 50 points:
    - 0-7: No Depression (normal range)
    - 8-16: Mild Depression
    - 17-23: Moderate Depression
    - 24-50: Severe Depression
    
    Clinical Significance:
    - Response to treatment: e50% reduction in score
    - Remission: Score <7
    - Score e20 typically required for clinical trial entry
    - Not intended as a diagnostic tool
    
    Important Notes:
    - Requires trained clinician administration
    - Assesses symptoms over past week
    - Administration takes 20-30 minutes
    - Additional items 18-21 may be recorded but not scored
    
    Reference: Hamilton M. J Neurol Neurosurg Psychiatry. 1960;23(1):56-62.
    """
    
    result: int = Field(
        ...,
        description="HAM-D total score (0-50 points) indicating severity of depressive symptoms",
        example=17
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and treatment recommendations based on score",
        example="Patient experiences moderate depressive symptoms that interfere with daily functioning. Consider psychotherapy and/or antidepressant medication."
    )
    
    stage: str = Field(
        ...,
        description="Depression severity category (No Depression, Mild, Moderate, or Severe)",
        example="Moderate Depression"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the depression severity level",
        example="Moderate depressive symptoms"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 17,
                "unit": "points",
                "interpretation": "Patient experiences moderate depressive symptoms that interfere with daily functioning. Consider psychotherapy and/or antidepressant medication.",
                "stage": "Moderate Depression",
                "stage_description": "Moderate depressive symptoms"
            }
        }