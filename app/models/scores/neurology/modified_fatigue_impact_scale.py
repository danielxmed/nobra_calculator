"""
Modified Fatigue Impact Scale (MFIS) Models

Request and response models for MFIS fatigue impact assessment.

References (Vancouver style):
1. Fisk JD, Ritvo PG, Ross L, Haase DA, Marrie TJ, Schlech WF. Measuring the 
   functional impact of fatigue: initial validation of the fatigue impact scale. 
   Clin Infect Dis. 1994 Jan;18 Suppl 1:S79-83. doi: 10.1093/clinids/18.supplement_1.s79.
2. Learmonth YC, Dlugonski D, Pilutti LA, Sandroff BM, Klaren R, Motl RW. 
   Psychometric properties of the Fatigue Severity Scale and the Modified Fatigue 
   Impact Scale. J Neurol Sci. 2013 Aug 15;331(1-2):102-7. doi: 10.1016/j.jns.2013.05.023.

The Modified Fatigue Impact Scale (MFIS) is a 21-item questionnaire that measures 
the impact of fatigue on physical, cognitive, and psychosocial functioning. 
Originally developed for multiple sclerosis patients, it is now used across various 
conditions. The scale uses a 5-point Likert scale (0-4) with a maximum score of 84. 
A cutoff of 38 points indicates clinically significant fatigue impact.
"""

from pydantic import BaseModel, Field
from typing import Literal


class ModifiedFatigueImpactScaleRequest(BaseModel):
    """
    Request model for Modified Fatigue Impact Scale (MFIS)
    
    The MFIS assesses fatigue impact across three domains:
    
    **Physical Subscale (Items 4,6,7,10,13,14,17,20,21 - Max 36 points):**
    - Physical coordination, motivation, endurance, weakness, discomfort
    
    **Cognitive Subscale (Items 1,2,3,5,11,12,15,16,18,19 - Max 40 points):** 
    - Alertness, attention, thinking, memory, decision-making, concentration
    
    **Psychosocial Subscale (Items 8,9 - Max 8 points):**
    - Social participation and activities away from home
    
    **Scoring for each item:**
    - 0 = Never
    - 1 = Rarely  
    - 2 = Sometimes
    - 3 = Often
    - 4 = Almost Always
    
    **Clinical Interpretation:**
    - Total score <38: Below clinical cutoff
    - Total score ≥38: Clinically significant fatigue impact
    - Changes ≥4 points predict significant effect on quality of life
    
    References (Vancouver style):
    1. Fisk JD, Ritvo PG, Ross L, Haase DA, Marrie TJ, Schlech WF. Measuring the 
       functional impact of fatigue: initial validation of the fatigue impact scale. 
       Clin Infect Dis. 1994 Jan;18 Suppl 1:S79-83. doi: 10.1093/clinids/18.supplement_1.s79.
    2. Learmonth YC, Dlugonski D, Pilutti LA, Sandroff BM, Klaren R, Motl RW. 
       Psychometric properties of the Fatigue Severity Scale and the Modified Fatigue 
       Impact Scale. J Neurol Sci. 2013 Aug 15;331(1-2):102-7. doi: 10.1016/j.jns.2013.05.023.
    """
    
    less_alert: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Item 1 (Cognitive): I have been less alert. 0=Never, 1=Rarely, 2=Sometimes, 3=Often, 4=Almost Always",
        example=1
    )
    
    difficulty_paying_attention: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Item 2 (Cognitive): I have had difficulty paying attention. 0=Never, 1=Rarely, 2=Sometimes, 3=Often, 4=Almost Always",
        example=1
    )
    
    unable_think_clearly: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Item 3 (Cognitive): I have been unable to think clearly. 0=Never, 1=Rarely, 2=Sometimes, 3=Often, 4=Almost Always",
        example=1
    )
    
    clumsy_uncoordinated: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Item 4 (Physical): I have been clumsy and uncoordinated. 0=Never, 1=Rarely, 2=Sometimes, 3=Often, 4=Almost Always",
        example=2
    )
    
    forgetful: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Item 5 (Cognitive): I have been forgetful. 0=Never, 1=Rarely, 2=Sometimes, 3=Often, 4=Almost Always",
        example=2
    )
    
    pace_physical_activities: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Item 6 (Physical): I have had to pace myself in my physical activities. 0=Never, 1=Rarely, 2=Sometimes, 3=Often, 4=Almost Always",
        example=3
    )
    
    less_motivated_physical: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Item 7 (Physical): I have been less motivated to do anything that requires physical effort. 0=Never, 1=Rarely, 2=Sometimes, 3=Often, 4=Almost Always",
        example=2
    )
    
    less_motivated_social: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Item 8 (Psychosocial): I have been less motivated to participate in social activities. 0=Never, 1=Rarely, 2=Sometimes, 3=Often, 4=Almost Always",
        example=1
    )
    
    limited_away_from_home: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Item 9 (Psychosocial): I have been limited in my ability to do things away from home. 0=Never, 1=Rarely, 2=Sometimes, 3=Often, 4=Almost Always",
        example=1
    )
    
    trouble_maintaining_effort: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Item 10 (Physical): I have had trouble maintaining physical effort for long periods. 0=Never, 1=Rarely, 2=Sometimes, 3=Often, 4=Almost Always",
        example=3
    )
    
    difficulty_making_decisions: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Item 11 (Cognitive): I have had difficulty making decisions. 0=Never, 1=Rarely, 2=Sometimes, 3=Often, 4=Almost Always",
        example=1
    )
    
    less_motivated_thinking: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Item 12 (Cognitive): I have been less motivated to do anything that requires thinking. 0=Never, 1=Rarely, 2=Sometimes, 3=Often, 4=Almost Always",
        example=1
    )
    
    muscles_weak: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Item 13 (Physical): My muscles have felt weak. 0=Never, 1=Rarely, 2=Sometimes, 3=Often, 4=Almost Always",
        example=2
    )
    
    physically_uncomfortable: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Item 14 (Physical): I have been physically uncomfortable. 0=Never, 1=Rarely, 2=Sometimes, 3=Often, 4=Almost Always",
        example=2
    )
    
    trouble_finishing_thinking_tasks: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Item 15 (Cognitive): I have had trouble finishing tasks that require thinking. 0=Never, 1=Rarely, 2=Sometimes, 3=Often, 4=Almost Always",
        example=1
    )
    
    difficulty_organizing: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Item 16 (Cognitive): I have had difficulty organizing things. 0=Never, 1=Rarely, 2=Sometimes, 3=Often, 4=Almost Always",
        example=1
    )
    
    less_able_physical_tasks: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Item 17 (Physical): I have been less able to complete tasks that require physical effort. 0=Never, 1=Rarely, 2=Sometimes, 3=Often, 4=Almost Always",
        example=2
    )
    
    thinking_slowed: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Item 18 (Cognitive): My thinking has been slowed down. 0=Never, 1=Rarely, 2=Sometimes, 3=Often, 4=Almost Always",
        example=2
    )
    
    trouble_concentrating: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Item 19 (Cognitive): I have had trouble concentrating. 0=Never, 1=Rarely, 2=Sometimes, 3=Often, 4=Almost Always",
        example=2
    )
    
    limited_physical_activities: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Item 20 (Physical): I have limited my physical activities. 0=Never, 1=Rarely, 2=Sometimes, 3=Often, 4=Almost Always",
        example=3
    )
    
    need_more_rest: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Item 21 (Physical): I have needed to rest more often or for longer periods of time. 0=Never, 1=Rarely, 2=Sometimes, 3=Often, 4=Almost Always",
        example=3
    )
    
    class Config:
        schema_extra = {
            "example": {
                "less_alert": 1,
                "difficulty_paying_attention": 1, 
                "unable_think_clearly": 1,
                "clumsy_uncoordinated": 2,
                "forgetful": 2,
                "pace_physical_activities": 3,
                "less_motivated_physical": 2,
                "less_motivated_social": 1,
                "limited_away_from_home": 1,
                "trouble_maintaining_effort": 3,
                "difficulty_making_decisions": 1,
                "less_motivated_thinking": 1,
                "muscles_weak": 2,
                "physically_uncomfortable": 2,
                "trouble_finishing_thinking_tasks": 1,
                "difficulty_organizing": 1,
                "less_able_physical_tasks": 2,
                "thinking_slowed": 2,
                "trouble_concentrating": 2,
                "limited_physical_activities": 3,
                "need_more_rest": 3
            }
        }


class ModifiedFatigueImpactScaleResponse(BaseModel):
    """
    Response model for Modified Fatigue Impact Scale (MFIS)
    
    The MFIS provides a total score (0-84) and three subscale scores:
    
    **Total Score Interpretation:**
    - 0-37: Below clinical cutoff - fatigue impact may not significantly affect quality of life
    - 38-84: Above clinical cutoff - clinically significant fatigue impact requiring intervention
    
    **Subscale Scores:**
    - Physical: 0-36 points (9 items assessing physical functioning and endurance)
    - Cognitive: 0-40 points (10 items assessing mental functioning and concentration)  
    - Psychosocial: 0-8 points (2 items assessing social participation and activities)
    
    **Clinical Significance:**
    - Changes ≥4 points on total MFIS predict significant effect on quality of life
    - Higher scores indicate greater fatigue impact across all domains
    - Subscale analysis helps identify primary areas of concern for targeted interventions
    
    **Management Recommendations:**
    - Score <38: Routine monitoring, lifestyle interventions
    - Score ≥38: Comprehensive fatigue management, energy conservation, regular follow-up
    
    Reference: Fisk JD, et al. Clin Infect Dis. 1994;18 Suppl 1:S79-83.
    """
    
    result: int = Field(
        ...,
        ge=0,
        le=84,
        description="Total MFIS score indicating overall fatigue impact on daily functioning (0-84 points)",
        example=38
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with total and subscale scores, dominant impact areas, and management recommendations",
        example="MFIS total score of 38 indicates clinically significant fatigue impact on daily functioning. Consider comprehensive fatigue management strategies including energy conservation techniques, exercise programs, and regular monitoring. Subscale scores: Physical=20/36, Cognitive=16/40, Psychosocial=2/8. Primary impact areas: physical functioning."
    )
    
    stage: str = Field(
        ...,
        description="Clinical significance category (Below Cutoff, Above Cutoff)",
        example="Above Cutoff"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the clinical significance level",
        example="Clinically significant fatigue impact"
    )
    
    physical_score: int = Field(
        ...,
        ge=0,
        le=36,
        description="Physical subscale score assessing impact on physical functioning and endurance (0-36 points)",
        example=20
    )
    
    cognitive_score: int = Field(
        ...,
        ge=0,
        le=40,
        description="Cognitive subscale score assessing impact on mental functioning and concentration (0-40 points)",
        example=16
    )
    
    psychosocial_score: int = Field(
        ...,
        ge=0,
        le=8,
        description="Psychosocial subscale score assessing impact on social participation and activities (0-8 points)",
        example=2
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 38,
                "unit": "points",
                "interpretation": "MFIS total score of 38 indicates clinically significant fatigue impact on daily functioning. Consider comprehensive fatigue management strategies including energy conservation techniques, exercise programs, and regular monitoring. Subscale scores: Physical=20/36, Cognitive=16/40, Psychosocial=2/8. Primary impact areas: physical functioning.",
                "stage": "Above Cutoff",
                "stage_description": "Clinically significant fatigue impact",
                "physical_score": 20,
                "cognitive_score": 16,
                "psychosocial_score": 2
            }
        }