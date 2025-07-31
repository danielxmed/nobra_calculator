"""
DSM-5 Criteria for Bipolar Disorder Models

Request and response models for DSM-5 Bipolar Disorder diagnostic evaluation.

References (Vancouver style):
1. American Psychiatric Association. Diagnostic and statistical manual of mental disorders: 
   DSM-5. 5th ed. Washington, DC: American Psychiatric Association; 2013.
2. Youngstrom EA, Birmaher B, Findling RL. Pediatric bipolar disorder: validity, 
   phenomenology, and recommendations for diagnosis. Bipolar Disord. 2008;10(1 Pt 2):194-214. 
   doi: 10.1111/j.1399-5618.2007.00563.x.
3. Angst J, Azorin JM, Bowden CL, et al. Prevalence and characteristics of undiagnosed 
   bipolar disorders in patients with a major depressive episode. Arch Gen Psychiatry. 2011;68(8):791-8. 
   doi: 10.1001/archgenpsychiatry.2011.87.

The DSM-5 diagnostic criteria for Bipolar Disorder includes criteria for manic episodes 
(Bipolar I) and hypomanic episodes (Bipolar II). Key changes in DSM-5 include the addition 
of "increased activity/energy" as a core criterion alongside mood symptoms. Manic episodes 
require ≥7 days duration or hospitalization, while hypomanic episodes require 4-6 days. 
Bipolar I requires only one manic episode; Bipolar II requires both hypomanic and major 
depressive episodes.
"""

from pydantic import BaseModel, Field
from typing import Literal


class Dsm5BipolarDisorderRequest(BaseModel):
    """
    Request model for DSM-5 Criteria for Bipolar Disorder
    
    The DSM-5 diagnostic criteria for Bipolar Disorder evaluates episodes of mania or hypomania:
    
    Core Criteria (both must be present):
    A. Elevated, expansive, or irritable mood
    B. Abnormally and persistently increased goal-directed activity or energy
    
    Additional Symptoms (at least 3 required):
    - Inflated self-esteem or grandiosity
    - Decreased need for sleep (feels rested after only 3 hours)
    - More talkative than usual or pressure to keep talking
    - Flight of ideas or racing thoughts
    - Distractibility (attention easily drawn to unimportant stimuli)
    - Increase in goal-directed activity or psychomotor agitation
    - Excessive involvement in risky activities with high potential for consequences
    
    Duration and Impairment Requirements:
    - Manic Episode: ≥7 days (or hospitalization required) + marked impairment
    - Hypomanic Episode: 4-6 days + observable change but less impairment
    
    Bipolar Disorder Types:
    - Bipolar I: At least one manic episode (may have hypomanic/depressive episodes)
    - Bipolar II: At least one hypomanic episode + at least one major depressive episode
    
    Exclusion Criteria:
    - Episode not better explained by substance use or medical condition
    - Not occurring exclusively during schizophrenia spectrum disorders
    
    Important Clinical Considerations:
    - DSM-5 added "increased activity/energy" as core requirement (48% prevalence reduction)
    - Mixed features specifier can be applied to any mood episode
    - Risk assessment for suicide and psychotic features is essential
    - Comprehensive psychiatric evaluation required for definitive diagnosis

    References (Vancouver style):
    1. American Psychiatric Association. Diagnostic and statistical manual of mental disorders: 
       DSM-5. 5th ed. Washington, DC: American Psychiatric Association; 2013.
    2. Youngstrom EA, Birmaher B, Findling RL. Pediatric bipolar disorder: validity, 
       phenomenology, and recommendations for diagnosis. Bipolar Disord. 2008;10(1 Pt 2):194-214. 
       doi: 10.1111/j.1399-5618.2007.00563.x.
    3. Angst J, Azorin JM, Bowden CL, et al. Prevalence and characteristics of undiagnosed 
       bipolar disorders in patients with a major depressive episode. Arch Gen Psychiatry. 2011;68(8):791-8. 
       doi: 10.1001/archgenpsychiatry.2011.87.
    """
    
    elevated_expansive_irritable_mood: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION A: Elevated, expansive, or irritable mood present most of the day, nearly every day",
        example="yes"
    )
    
    increased_activity_energy: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION B: Abnormally and persistently increased goal-directed activity or energy, present most of the day, nearly every day",
        example="yes"
    )
    
    inflated_self_esteem: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION C1: Inflated self-esteem or grandiosity",
        example="yes"
    )
    
    decreased_need_sleep: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION C2: Decreased need for sleep (feels rested after only 3 hours of sleep)",
        example="yes"
    )
    
    more_talkative: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION C3: More talkative than usual or pressure to keep talking",
        example="yes"
    )
    
    flight_of_ideas: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION C4: Flight of ideas or subjective experience that thoughts are racing",
        example="no"
    )
    
    distractibility: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION C5: Distractibility (attention too easily drawn to unimportant or irrelevant external stimuli)",
        example="yes"
    )
    
    increased_goal_directed_activity: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION C6: Increase in goal-directed activity (socially, at work/school, or sexually) or psychomotor agitation",
        example="yes"
    )
    
    excessive_risky_behavior: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION C7: Excessive involvement in activities with high potential for painful consequences (e.g., spending sprees, sexual indiscretions, foolish business investments)",
        example="no"
    )
    
    episode_duration: Literal["less_than_4_days", "4_to_6_days", "7_days_or_more", "hospitalization_required"] = Field(
        ...,
        description="CRITERION D: Duration of mood episode (manic: ≥7 days or hospitalization; hypomanic: 4-6 days)",
        example="7_days_or_more"
    )
    
    functional_impairment: Literal["none", "mild_noticeable", "marked_impairment", "psychotic_hospitalization"] = Field(
        ...,
        description="CRITERION E: Level of functional impairment (manic: marked impairment/psychotic; hypomanic: noticeable but not marked)",
        example="marked_impairment"
    )
    
    substance_medical_cause: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION F: Episode NOT better explained by physiological effects of substance use or medical condition",
        example="yes"
    )
    
    history_major_depressive_episode: Literal["yes", "no"] = Field(
        ...,
        description="CLINICAL HISTORY: History of at least one major depressive episode (required for Bipolar II diagnosis)",
        example="no"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "elevated_expansive_irritable_mood": "yes",
                "increased_activity_energy": "yes",
                "inflated_self_esteem": "yes",
                "decreased_need_sleep": "yes",
                "more_talkative": "yes",
                "flight_of_ideas": "no",
                "distractibility": "yes",
                "increased_goal_directed_activity": "yes",
                "excessive_risky_behavior": "no",
                "episode_duration": "7_days_or_more",
                "functional_impairment": "marked_impairment",
                "substance_medical_cause": "yes",
                "history_major_depressive_episode": "no"
            }
        }


class Dsm5BipolarDisorderResponse(BaseModel):
    """
    Response model for DSM-5 Criteria for Bipolar Disorder
    
    Diagnostic results based on DSM-5 criteria evaluation:
    - Criteria Not Met: Does not meet diagnostic criteria for bipolar disorder
    - Hypomanic Episode: Meets criteria for hypomanic episode (4-6 days, noticeable change)
    - Manic Episode: Meets criteria for manic episode (≥7 days or hospitalization, marked impairment)
    - Bipolar II Disorder: Hypomanic episode + history of major depressive episode
    
    Key DSM-5 Requirements:
    - Both core criteria (mood + activity/energy) must be present
    - At least 3 additional symptoms from the 7-symptom list
    - Appropriate duration and functional impact for episode type
    - Not better explained by substance use or medical condition
    
    Clinical Implications:
    - Manic Episode → Bipolar I Disorder (requires immediate psychiatric evaluation)
    - Hypomanic Episode + Depression History → Bipolar II Disorder
    - Single Hypomanic Episode → Further evaluation needed for complete diagnosis
    
    Important Considerations:
    - This tool aids clinical assessment but does not replace comprehensive evaluation
    - Consider mixed features, rapid cycling, and other specifiers
    - Assess suicide risk and need for hospitalization in acute episodes
    - Coordinate with psychiatric specialists for treatment planning
    
    Reference: American Psychiatric Association. DSM-5. Washington, DC: APA; 2013.
    """
    
    result: str = Field(
        ...,
        description="Diagnostic result based on DSM-5 criteria evaluation",
        example="Manic Episode"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the diagnostic result",
        example="diagnosis"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and treatment recommendations based on diagnostic result",
        example="Meets criteria for a manic episode, indicating Bipolar I Disorder. Requires immediate psychiatric evaluation and treatment. Consider hospitalization if psychotic features or significant functional impairment present."
    )
    
    stage: str = Field(
        ...,
        description="Diagnostic stage (Criteria Not Met, Hypomanic Episode, Manic Episode, Bipolar II Disorder)",
        example="Manic Episode"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the diagnostic stage",
        example="Meets criteria for manic episode"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": "Manic Episode",
                "unit": "diagnosis",
                "interpretation": "Meets criteria for a manic episode, indicating Bipolar I Disorder. Requires immediate psychiatric evaluation and treatment. Consider hospitalization if psychotic features or significant functional impairment present.",
                "stage": "Manic Episode",
                "stage_description": "Meets criteria for manic episode"
            }
        }