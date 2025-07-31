"""
Hamilton Anxiety Scale Models

Request and response models for Hamilton Anxiety Scale (HAM-A) calculation.

References (Vancouver style):
1. Hamilton M. The assessment of anxiety states by rating. Br J Med Psychol. 
   1959;32(1):50-5. doi: 10.1111/j.2044-8341.1959.tb00467.x.
2. Matza LS, Morlock R, Sexton C, Malley K, Feltner D. Identifying HAM-A cutoffs 
   for mild, moderate, and severe generalized anxiety disorder. Int J Methods 
   Psychiatr Res. 2010 Dec;19(4):223-32. doi: 10.1002/mpr.323.
3. Shear MK, Vander Bilt J, Rucci P, Endicott J, Lydiard B, Otto MW, et al. 
   Reliability and validity of a structured interview guide for the Hamilton 
   Anxiety Rating Scale (SIGH-A). Depress Anxiety. 2001;13(4):166-78. 
   doi: 10.1002/da.1033.
4. Thompson E. Hamilton Rating Scale for Anxiety (HAM-A). Occup Med (Lond). 
   2015 Oct;65(7):601. doi: 10.1093/occmed/kqv054.

The Hamilton Anxiety Scale (HAM-A) is a clinician-rated scale that assesses the 
severity of anxiety symptoms across 14 domains. Each item is rated 0-4 (not present 
to very severe), with a total score range of 0-56. It was designed for patients 
already diagnosed with anxiety disorders and is widely used for monitoring treatment 
response and assessing symptom severity.
"""

from pydantic import BaseModel, Field, validator


class HamiltonAnxietyScaleRequest(BaseModel):
    """
    Request model for Hamilton Anxiety Scale (HAM-A)
    
    The HAM-A assesses 14 symptom domains, each rated on a 5-point scale:
    - 0 = Not Present
    - 1 = Mild
    - 2 = Moderate  
    - 3 = Severe
    - 4 = Very Severe
    
    The 14 domains cover:
    1. Anxious Mood: Worries, anticipation of worst, fearful anticipation, irritability
    2. Tension: Feelings of tension, fatigability, startle response, easily moved to tears, 
       trembling, restlessness, inability to relax
    3. Fears: Of dark, strangers, being left alone, animals, traffic, crowds
    4. Insomnia: Difficulty falling asleep, broken sleep, unsatisfying sleep, fatigue on 
       waking, dreams, nightmares, night terrors
    5. Intellectual: Difficulty concentrating, poor memory
    6. Depressed Mood: Loss of interest, lack of pleasure in hobbies, depression, early 
       waking, diurnal swing
    7. Somatic (Muscular): Pains, aches, twitching, stiffness, myoclonic jerks, teeth 
       grinding, unsteady voice, increased muscle tone
    8. Somatic (Sensory): Tinnitus, blurring vision, hot/cold flushes, feelings of weakness, 
       pricking sensation
    9. Cardiovascular: Tachycardia, palpitations, chest pain, throbbing vessels, fainting 
       feelings, missing heartbeat
    10. Respiratory: Pressure/constriction in chest, choking feelings, sighing, dyspnea
    11. Gastrointestinal: Swallowing difficulty, wind, abdominal pain, burning sensations, 
        fullness, nausea, vomiting, bowel changes, weight loss, constipation
    12. Genitourinary: Urinary frequency/urgency, menstrual changes, sexual dysfunction
    13. Autonomic Symptoms: Dry mouth, flushing, pallor, sweating, giddiness, tension 
        headache, hair raising
    14. Behavior at Interview: Fidgeting, restlessness, hand tremor, furrowed brow, 
        strained face, sighing, rapid respiration, facial pallor
    
    References (Vancouver style):
    1. Hamilton M. The assessment of anxiety states by rating. Br J Med Psychol. 1959;32(1):50-5.
    2. Matza LS, Morlock R, Sexton C, Malley K, Feltner D. Identifying HAM-A cutoffs for mild, 
       moderate, and severe generalized anxiety disorder. Int J Methods Psychiatr Res. 2010 
       Dec;19(4):223-32.
    """
    
    anxious_mood: int = Field(
        ...,
        ge=0,
        le=4,
        description="Worries, anticipation of worst, fearful anticipation, irritability. 0=not present, 4=very severe",
        example=2
    )
    
    tension: int = Field(
        ...,
        ge=0,
        le=4,
        description="Feelings of tension, fatigability, startle response, easily moved to tears, trembling, restlessness, inability to relax. 0=not present, 4=very severe",
        example=2
    )
    
    fears: int = Field(
        ...,
        ge=0,
        le=4,
        description="Of dark, strangers, being left alone, animals, traffic, crowds. 0=not present, 4=very severe",
        example=1
    )
    
    insomnia: int = Field(
        ...,
        ge=0,
        le=4,
        description="Difficulty falling asleep, broken sleep, unsatisfying sleep, fatigue on waking, dreams, nightmares, night terrors. 0=not present, 4=very severe",
        example=2
    )
    
    intellectual: int = Field(
        ...,
        ge=0,
        le=4,
        description="Difficulty concentrating, poor memory. 0=not present, 4=very severe",
        example=1
    )
    
    depressed_mood: int = Field(
        ...,
        ge=0,
        le=4,
        description="Loss of interest, lack of pleasure in hobbies, depression, early waking, diurnal swing. 0=not present, 4=very severe",
        example=1
    )
    
    somatic_muscular: int = Field(
        ...,
        ge=0,
        le=4,
        description="Pains, aches, twitching, stiffness, myoclonic jerks, teeth grinding, unsteady voice, increased muscle tone. 0=not present, 4=very severe",
        example=2
    )
    
    somatic_sensory: int = Field(
        ...,
        ge=0,
        le=4,
        description="Tinnitus, blurring vision, hot/cold flushes, feelings of weakness, pricking sensation. 0=not present, 4=very severe",
        example=1
    )
    
    cardiovascular: int = Field(
        ...,
        ge=0,
        le=4,
        description="Tachycardia, palpitations, chest pain, throbbing vessels, fainting feelings, missing heartbeat. 0=not present, 4=very severe",
        example=2
    )
    
    respiratory: int = Field(
        ...,
        ge=0,
        le=4,
        description="Pressure/constriction in chest, choking feelings, sighing, dyspnea. 0=not present, 4=very severe",
        example=1
    )
    
    gastrointestinal: int = Field(
        ...,
        ge=0,
        le=4,
        description="Swallowing difficulty, wind, abdominal pain, burning sensations, fullness, nausea, vomiting, bowel changes, weight loss, constipation. 0=not present, 4=very severe",
        example=1
    )
    
    genitourinary: int = Field(
        ...,
        ge=0,
        le=4,
        description="Urinary frequency/urgency, menstrual changes, sexual dysfunction. 0=not present, 4=very severe",
        example=0
    )
    
    autonomic_symptoms: int = Field(
        ...,
        ge=0,
        le=4,
        description="Dry mouth, flushing, pallor, sweating, giddiness, tension headache, hair raising. 0=not present, 4=very severe",
        example=2
    )
    
    behavior_at_interview: int = Field(
        ...,
        ge=0,
        le=4,
        description="Fidgeting, restlessness, hand tremor, furrowed brow, strained face, sighing, rapid respiration, facial pallor. 0=not present, 4=very severe",
        example=1
    )
    
    class Config:
        schema_extra = {
            "example": {
                "anxious_mood": 2,
                "tension": 2,
                "fears": 1,
                "insomnia": 2,
                "intellectual": 1,
                "depressed_mood": 1,
                "somatic_muscular": 2,
                "somatic_sensory": 1,
                "cardiovascular": 2,
                "respiratory": 1,
                "gastrointestinal": 1,
                "genitourinary": 0,
                "autonomic_symptoms": 2,
                "behavior_at_interview": 1
            }
        }


class HamiltonAnxietyScaleResponse(BaseModel):
    """
    Response model for Hamilton Anxiety Scale (HAM-A)
    
    The HAM-A total score ranges from 0 to 56 points:
    - 0-7: No/Minimal Anxiety
    - 8-14: Mild Anxiety
    - 15-23: Moderate Anxiety
    - 24-56: Severe Anxiety
    
    Clinical Significance:
    - Widely used for monitoring treatment response in anxiety disorders
    - Can help guide treatment decisions (psychotherapy vs medication)
    - Serial assessments can track symptom improvement over time
    - Originally designed for patients already diagnosed with anxiety
    
    Important Notes:
    - Clinician-rated scale requiring clinical interview
    - Administration typically takes 10-15 minutes
    - Not intended as a diagnostic tool
    - Should be interpreted in clinical context
    
    Reference: Hamilton M. Br J Med Psychol. 1959;32(1):50-5.
    """
    
    result: int = Field(
        ...,
        description="HAM-A total score (0-56 points) indicating severity of anxiety symptoms",
        example=19
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and treatment recommendations based on score",
        example="Patient experiences moderate anxiety symptoms that interfere with daily activities and quality of life. Consider psychotherapy and/or pharmacological intervention."
    )
    
    stage: str = Field(
        ...,
        description="Anxiety severity category (No/Minimal, Mild, Moderate, or Severe)",
        example="Moderate Anxiety"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the anxiety severity level",
        example="Moderate anxiety symptoms"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 19,
                "unit": "points",
                "interpretation": "Patient experiences moderate anxiety symptoms that interfere with daily activities and quality of life. Consider psychotherapy and/or pharmacological intervention.",
                "stage": "Moderate Anxiety",
                "stage_description": "Moderate anxiety symptoms"
            }
        }