"""
DSM-5 Criteria for Binge Eating Disorder Models

Request and response models for DSM-5 Binge Eating Disorder diagnostic evaluation.

References (Vancouver style):
1. American Psychiatric Association. Diagnostic and statistical manual of mental disorders: 
   DSM-5. 5th ed. Washington, DC: American Psychiatric Association; 2013.
2. Grilo CM, Ivezaj V, White MA. Evaluation of the DSM-5 severity indicator for binge eating 
   disorder in a clinical sample. Behav Res Ther. 2015;71:110-4. doi: 10.1016/j.brat.2015.05.003.
3. Wonderlich SA, Gordon KH, Mitchell JE, et al. The validity and clinical utility of binge 
   eating disorder. Int J Eat Disord. 2009;42(8):687-705. doi: 10.1002/eat.20719.

The DSM-5 diagnostic criteria for Binge Eating Disorder requires all of the following:
(A) Recurrent episodes of binge eating, (B) ≥3 associated behavioral/emotional features, 
(C) Marked distress, (D) ≥1 episode/week for 3 months, and (E) Absence of compensatory 
behaviors and not exclusively during other eating disorders. Severity is based on episode 
frequency: Mild (1-3/week), Moderate (4-7/week), Severe (8-13/week), Extreme (≥14/week).
"""

from pydantic import BaseModel, Field
from typing import Literal


class Dsm5BingeEatingDisorderRequest(BaseModel):
    """
    Request model for DSM-5 Criteria for Binge Eating Disorder
    
    The DSM-5 diagnostic criteria for Binge Eating Disorder consists of 5 main criteria:
    
    Criterion A: Recurrent episodes of binge eating characterized by:
    - Eating unusually large amounts of food in a discrete period
    - Experiencing a feeling of loss of control during the episode
    
    Criterion B: Binge eating episodes include at least 3 of the following 5 features:
    1. Eating much more rapidly than normal
    2. Eating until feeling uncomfortably full
    3. Eating large amounts when not feeling physically hungry
    4. Eating alone due to embarrassment about eating behavior
    5. Feeling disgusted, depressed, or very guilty afterward
    
    Criterion C: Marked distress regarding binge eating is present
    
    Criterion D: Binge eating occurs, on average, at least once a week for 3 months
    
    Criterion E: Exclusion criteria (both must be met):
    - Binge eating is NOT associated with recurrent compensatory behavior
    - Does NOT occur exclusively during anorexia nervosa, bulimia nervosa, or ARFID
    
    Severity Specifiers (based on episode frequency per week):
    - Mild: 1-3 episodes per week
    - Moderate: 4-7 episodes per week
    - Severe: 8-13 episodes per week
    - Extreme: 14 or more episodes per week
    
    Important Notes:
    - Weight or appearance is NOT part of the diagnostic criteria
    - Clinical judgment by qualified mental health professional is essential
    - This tool aids diagnosis but does not replace comprehensive clinical evaluation

    References (Vancouver style):
    1. American Psychiatric Association. Diagnostic and statistical manual of mental disorders: 
       DSM-5. 5th ed. Washington, DC: American Psychiatric Association; 2013.
    2. Grilo CM, Ivezaj V, White MA. Evaluation of the DSM-5 severity indicator for binge eating 
       disorder in a clinical sample. Behav Res Ther. 2015;71:110-4. doi: 10.1016/j.brat.2015.05.003.
    3. Wonderlich SA, Gordon KH, Mitchell JE, et al. The validity and clinical utility of binge 
       eating disorder. Int J Eat Disord. 2009;42(8):687-705. doi: 10.1002/eat.20719.
    """
    
    binge_eating_episodes: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION A: Recurrent episodes of binge eating characterized by eating unusually large amounts of food while experiencing a feeling of loss of control",
        example="yes"
    )
    
    eating_rapidly: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION B1: Eating much more rapidly than normal during binge episodes",
        example="yes"
    )
    
    eating_until_uncomfortably_full: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION B2: Eating until feeling uncomfortably full during binge episodes",
        example="yes"
    )
    
    eating_when_not_hungry: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION B3: Eating large amounts when not feeling physically hungry",
        example="yes"
    )
    
    eating_alone_embarrassment: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION B4: Eating alone due to embarrassment about how much one is eating",
        example="no"
    )
    
    negative_feelings_after: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION B5: Feeling disgusted, depressed, or very guilty afterward",
        example="yes"
    )
    
    marked_distress: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION C: Marked distress regarding binge eating is present",
        example="yes"
    )
    
    frequency_duration: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION D: Binge eating occurs, on average, at least once a week for 3 months",
        example="yes"
    )
    
    no_compensatory_behaviors: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION E1: Binge eating is NOT associated with recurrent use of inappropriate compensatory behavior (e.g., purging, laxatives, excessive exercise)",
        example="yes"
    )
    
    not_during_other_disorders: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION E2: Does NOT occur exclusively during anorexia nervosa, bulimia nervosa, or avoidant/restrictive food intake disorder",
        example="yes"
    )
    
    weekly_frequency: Literal["1_3_per_week", "4_7_per_week", "8_13_per_week", "14_or_more_per_week"] = Field(
        ...,
        description="Average frequency of binge eating episodes per week for severity assessment: 1-3 (Mild), 4-7 (Moderate), 8-13 (Severe), 14+ (Extreme)",
        example="1_3_per_week"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "binge_eating_episodes": "yes",
                "eating_rapidly": "yes",
                "eating_until_uncomfortably_full": "yes",
                "eating_when_not_hungry": "yes",
                "eating_alone_embarrassment": "no",
                "negative_feelings_after": "yes",
                "marked_distress": "yes",
                "frequency_duration": "yes",
                "no_compensatory_behaviors": "yes",
                "not_during_other_disorders": "yes",
                "weekly_frequency": "1_3_per_week"
            }
        }


class Dsm5BingeEatingDisorderResponse(BaseModel):
    """
    Response model for DSM-5 Criteria for Binge Eating Disorder
    
    Diagnostic results based on DSM-5 criteria evaluation:
    - Criteria Not Met: Does not meet diagnostic criteria for BED
    - Criteria Met - Mild: Meets criteria with 1-3 episodes per week
    - Criteria Met - Moderate: Meets criteria with 4-7 episodes per week
    - Criteria Met - Severe: Meets criteria with 8-13 episodes per week
    - Criteria Met - Extreme: Meets criteria with 14+ episodes per week
    
    All core criteria (A-E) must be met for diagnosis:
    - Criterion A: Recurrent binge eating episodes with loss of control
    - Criterion B: At least 3 of 5 associated behavioral/emotional features
    - Criterion C: Marked distress regarding binge eating
    - Criterion D: Frequency ≥1 episode/week for 3 months
    - Criterion E: No compensatory behaviors and not exclusively during other disorders
    
    Important Clinical Considerations:
    - This is a diagnostic aid, not a substitute for clinical evaluation
    - Weight or appearance is not part of BED diagnostic criteria
    - Consider medical complications and psychiatric comorbidities
    - Refer to qualified eating disorder specialists for treatment
    
    Reference: American Psychiatric Association. DSM-5. Washington, DC: APA; 2013.
    """
    
    result: str = Field(
        ...,
        description="Diagnostic result based on DSM-5 criteria evaluation",
        example="Criteria Met - Mild"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the diagnostic result",
        example="diagnosis"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and treatment recommendations based on diagnostic result",
        example="Meets DSM-5 criteria for Binge Eating Disorder, Mild severity (1-3 episodes per week). Treatment recommendations include psychotherapy, nutritional counseling, and consideration of medication if indicated."
    )
    
    stage: str = Field(
        ...,
        description="Diagnostic stage (Criteria Not Met, Criteria Met - Mild/Moderate/Severe/Extreme)",
        example="Criteria Met - Mild"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the diagnostic stage",
        example="Meets DSM-5 criteria - Mild severity"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": "Criteria Met - Mild",
                "unit": "diagnosis",
                "interpretation": "Meets DSM-5 criteria for Binge Eating Disorder, Mild severity (1-3 episodes per week). Treatment recommendations include psychotherapy, nutritional counseling, and consideration of medication if indicated.",
                "stage": "Criteria Met - Mild",
                "stage_description": "Meets DSM-5 criteria - Mild severity"
            }
        }