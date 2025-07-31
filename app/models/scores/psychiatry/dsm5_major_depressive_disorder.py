"""
DSM-5 Criteria for Major Depressive Disorder Models

Request and response models for DSM-5 Major Depressive Disorder diagnostic evaluation.

References (Vancouver style):
1. American Psychiatric Association. Diagnostic and statistical manual of mental disorders: 
   DSM-5. 5th ed. Washington, DC: American Psychiatric Association; 2013.
2. Uher R, Payne JL, Pavlova B, Perlis RH. Major depressive disorder in DSM-5: 
   implications for clinical practice and research of changes from DSM-IV. 
   Depress Anxiety. 2014;31(6):459-71. doi: 10.1002/da.22217.
3. Fried EI, Nesse RM. Depression sum-scores don't add up: why analyzing specific 
   depression symptoms is essential. BMC Med. 2015;13:72. doi: 10.1186/s12916-015-0325-4.

The DSM-5 criteria for Major Depressive Disorder require at least 5 symptoms from a 
9-symptom list to be present during the same 2-week period, with at least one of the 
symptoms being either depressed mood or anhedonia (loss of interest/pleasure). The 
symptoms must cause clinically significant distress or functional impairment and not 
be attributable to substance use, medical conditions, or better explained by other 
psychiatric disorders. The diagnosis excludes individuals with a history of manic 
or hypomanic episodes (which would suggest bipolar disorder).
"""

from pydantic import BaseModel, Field
from typing import Literal


class Dsm5MajorDepressiveDisorderRequest(BaseModel):
    """
    Request model for DSM-5 Criteria for Major Depressive Disorder
    
    The DSM-5 diagnostic criteria for Major Depressive Disorder requires the following:
    
    Criterion A: Five (or more) of the following symptoms present during the same 2-week 
    period and represent a change from previous functioning; at least one symptom is either 
    (1) depressed mood or (2) loss of interest or pleasure:
    
    Core Symptoms (at least one required):
    1. Depressed mood most of the day, nearly every day
    2. Markedly diminished interest or pleasure in activities (anhedonia)
    
    Additional Symptoms:
    3. Significant weight loss/gain or decrease/increase in appetite
    4. Insomnia or hypersomnia nearly every day
    5. Psychomotor agitation or retardation nearly every day
    6. Fatigue or loss of energy nearly every day
    7. Feelings of worthlessness or excessive/inappropriate guilt
    8. Diminished ability to think/concentrate or indecisiveness
    9. Recurrent thoughts of death, suicidal ideation, or suicide attempt/plan
    
    Criterion B: Symptoms cause clinically significant distress or impairment in functioning
    
    Criterion C: Episode not attributable to substance use or medical condition
    
    Criterion D: Not better explained by schizoaffective, schizophrenia, or delusional disorders
    
    Exclusion: Never had a manic or hypomanic episode (distinguishes from bipolar disorder)
    
    Duration: Symptoms present most of the day, nearly every day for at least 2 weeks
    
    Important Clinical Considerations:
    - Distinguish from normal sadness and grief reactions
    - Assess suicide risk immediately if suicidal ideation present
    - Consider severity specifiers (mild, moderate, severe) and other specifiers
    - Comprehensive psychiatric evaluation required for definitive diagnosis

    References (Vancouver style):
    1. American Psychiatric Association. Diagnostic and statistical manual of mental disorders: 
       DSM-5. 5th ed. Washington, DC: American Psychiatric Association; 2013.
    2. Uher R, Payne JL, Pavlova B, Perlis RH. Major depressive disorder in DSM-5: 
       implications for clinical practice and research of changes from DSM-IV. 
       Depress Anxiety. 2014;31(6):459-71. doi: 10.1002/da.22217.
    3. Fried EI, Nesse RM. Depression sum-scores don't add up: why analyzing specific 
       depression symptoms is essential. BMC Med. 2015;13:72. doi: 10.1186/s12916-015-0325-4.
    """
    
    depressed_mood: Literal["yes", "no"] = Field(
        ...,
        description="CORE SYMPTOM 1: Depressed mood most of the day, nearly every day (as indicated by subjective report or observation)",
        example="yes"
    )
    
    anhedonia: Literal["yes", "no"] = Field(
        ...,
        description="CORE SYMPTOM 2: Markedly diminished interest or pleasure in all, or almost all, activities most of the day, nearly every day",
        example="yes"
    )
    
    weight_appetite_change: Literal["yes", "no"] = Field(
        ...,
        description="SYMPTOM 3: Significant weight loss when not dieting or weight gain (>5% body weight in a month), or decrease/increase in appetite nearly every day",
        example="yes"
    )
    
    sleep_disturbance: Literal["yes", "no"] = Field(
        ...,
        description="SYMPTOM 4: Insomnia or hypersomnia nearly every day",
        example="yes"
    )
    
    psychomotor_changes: Literal["yes", "no"] = Field(
        ...,
        description="SYMPTOM 5: Psychomotor agitation or retardation nearly every day (observable by others, not merely subjective feelings)",
        example="no"
    )
    
    fatigue_energy_loss: Literal["yes", "no"] = Field(
        ...,
        description="SYMPTOM 6: Fatigue or loss of energy nearly every day",
        example="yes"
    )
    
    worthlessness_guilt: Literal["yes", "no"] = Field(
        ...,
        description="SYMPTOM 7: Feelings of worthlessness or excessive or inappropriate guilt (which may be delusional) nearly every day",
        example="yes"
    )
    
    concentration_problems: Literal["yes", "no"] = Field(
        ...,
        description="SYMPTOM 8: Diminished ability to think or concentrate, or indecisiveness, nearly every day",
        example="no"
    )
    
    suicidal_thoughts: Literal["yes", "no"] = Field(
        ...,
        description="SYMPTOM 9: Recurrent thoughts of death (not just fear of dying), recurrent suicidal ideation without specific plan, or suicide attempt or specific plan for committing suicide",
        example="no"
    )
    
    duration_two_weeks: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION B: Symptoms have been present for at least 2 weeks, most of the day, nearly every day",
        example="yes"
    )
    
    functional_impairment: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION C: Symptoms cause clinically significant distress or impairment in social, occupational, or other important areas of functioning",
        example="yes"
    )
    
    not_substance_medical: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION D: Episode is NOT attributable to the physiological effects of a substance or medical condition",
        example="yes"
    )
    
    not_better_explained: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION E: NOT better explained by schizoaffective disorder, schizophrenia, delusional disorder, or other specified/unspecified schizophrenia spectrum disorders",
        example="yes"
    )
    
    no_manic_hypomanic_history: Literal["yes", "no"] = Field(
        ...,
        description="EXCLUSION CRITERION: Has NEVER had a manic episode or hypomanic episode (to distinguish from bipolar disorder)",
        example="yes"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "depressed_mood": "yes",
                "anhedonia": "yes",
                "weight_appetite_change": "yes",
                "sleep_disturbance": "yes",
                "psychomotor_changes": "no",
                "fatigue_energy_loss": "yes",
                "worthlessness_guilt": "yes",
                "concentration_problems": "no",
                "suicidal_thoughts": "no",
                "duration_two_weeks": "yes",
                "functional_impairment": "yes",
                "not_substance_medical": "yes",
                "not_better_explained": "yes",
                "no_manic_hypomanic_history": "yes"
            }
        }


class Dsm5MajorDepressiveDisorderResponse(BaseModel):
    """
    Response model for DSM-5 Criteria for Major Depressive Disorder
    
    Diagnostic results based on DSM-5 criteria evaluation:
    - Criteria Not Met: Does not meet diagnostic criteria for Major Depressive Disorder
    - Major Depressive Episode: Meets all DSM-5 criteria for Major Depressive Disorder
    
    Key DSM-5 Requirements for Diagnosis:
    - At least 5 of 9 symptoms present during same 2-week period
    - At least one core symptom (depressed mood OR anhedonia) must be present
    - Symptoms cause clinically significant distress or functional impairment
    - Not attributable to substance use or medical condition
    - Not better explained by other psychiatric disorders
    - No history of manic or hypomanic episodes (excludes bipolar disorder)
    
    Clinical Implications:
    - Major Depressive Episode → Requires comprehensive psychiatric evaluation
    - Consider severity specifiers (mild, moderate, severe) based on symptom count and impairment
    - Assess for suicide risk, especially if suicidal ideation present
    - Treatment options include psychotherapy, medication, or combination approaches
    
    Important Considerations:
    - This tool aids clinical assessment but does not replace comprehensive evaluation
    - Consider psychosocial stressors, medical history, and family psychiatric history
    - Distinguish from normal grief/bereavement and adjustment disorders
    - Monitor for treatment response and potential emergence of manic/hypomanic episodes
    
    Reference: American Psychiatric Association. DSM-5. Washington, DC: APA; 2013.
    """
    
    result: str = Field(
        ...,
        description="Diagnostic result based on DSM-5 criteria evaluation",
        example="Major Depressive Episode"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the diagnostic result",
        example="diagnosis"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and treatment recommendations based on diagnostic result",
        example="Meets DSM-5 criteria for Major Depressive Disorder. Requires comprehensive psychiatric evaluation and treatment planning. Consider psychotherapy, medication, or combination treatment based on severity and patient preferences."
    )
    
    stage: str = Field(
        ...,
        description="Diagnostic stage (Criteria Not Met or Major Depressive Episode)",
        example="Major Depressive Episode"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the diagnostic stage",
        example="Meets criteria for major depressive episode"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": "Major Depressive Episode",
                "unit": "diagnosis",
                "interpretation": "Meets DSM-5 criteria for Major Depressive Disorder. Requires comprehensive psychiatric evaluation and treatment planning. Consider psychotherapy, medication, or combination treatment based on severity and patient preferences.",
                "stage": "Major Depressive Episode",
                "stage_description": "Meets criteria for major depressive episode"
            }
        }