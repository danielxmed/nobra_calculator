"""
Montgomery-Asberg Depression Rating Scale (MADRS) Models

Request and response models for MADRS calculation.

References (Vancouver style):
1. Montgomery SA, Asberg M. A new depression scale designed to be sensitive to change. 
   Br J Psychiatry. 1979;134:382-9. doi: 10.1192/bjp.134.4.382.
2. Snaith RP, Harrop FM, Newby DA, Teale C. Grade scores of the Montgomery-Asberg 
   Depression and the Clinical Anxiety Scales. Br J Psychiatry. 1986;148:599-601. 
   doi: 10.1192/bjp.148.5.599.
3. Turkoz I, Alphs L, Singh J, Jamieson C, Daly E, Shawi M, et al. Clinically meaningful 
   changes on depressive symptom measures and patient-reported outcomes in patients with 
   treatment-resistant depression. J Affect Disord. 2021;281:267-273. 
   doi: 10.1016/j.jad.2020.12.021.

The MADRS is a 10-item depression rating scale designed to be sensitive to changes 
from antidepressant treatment. Each item is scored from 0-6, with total scores 
ranging from 0-60. It focuses on core mood symptoms rather than somatic symptoms, 
making it more sensitive to treatment-induced changes than the Hamilton Depression 
Rating Scale.
"""

from pydantic import BaseModel, Field
from typing import Literal


class MadrsRequest(BaseModel):
    """
    Request model for Montgomery-Asberg Depression Rating Scale (MADRS)
    
    The MADRS assesses 10 core mood symptoms on a 0-6 scale:
    
    Scoring for each item:
    0 = No symptoms/normal
    1 = These feelings indicated only on questioning
    2 = These feelings spontaneously reported verbally
    3 = Communicated non-verbally (expression, posture, voice, tendency to weep)
    4 = Patient reports virtually only these feeling states in spontaneous verbal and non-verbal communication
    5 = Intensive feelings; non-verbal communication dominates the interview, communication through verbal means is difficult
    6 = Severe/continuous presence of symptoms
    
    Items assess:
    1. Apparent sadness - Observable signs of sadness
    2. Reported sadness - Subjective experience of depressed mood
    3. Inner tension - Feelings of ill-defined discomfort, edginess, turmoil
    4. Reduced sleep - Compared to normal sleep pattern
    5. Reduced appetite - Loss of appetite compared to when well
    6. Concentration difficulties - From mild to incapacitating lack of concentration
    7. Lassitude - Difficulty initiating and performing activities
    8. Inability to feel - Reduced interest and pleasure in activities
    9. Pessimistic thoughts - Thoughts of guilt, inferiority, self-reproach
    10. Suicidal thoughts - From feeling life not worth living to suicide preparations
    
    Total score interpretation:
    - 0-6: Normal/minimal depression
    - 7-19: Mild depression
    - 20-34: Moderate depression  
    - 35-60: Severe depression
    
    Clinical significance:
    - Response to treatment: ≥50% reduction from baseline
    - Remission: typically ≤7-9 points
    - Clinically meaningful change: ≥6 points improvement
    - Clinically substantial change: ≥12 points improvement

    References (Vancouver style):
    1. Montgomery SA, Asberg M. A new depression scale designed to be sensitive to change. 
    Br J Psychiatry. 1979;134:382-9. doi: 10.1192/bjp.134.4.382.
    2. Snaith RP, Harrop FM, Newby DA, Teale C. Grade scores of the Montgomery-Asberg 
    Depression and the Clinical Anxiety Scales. Br J Psychiatry. 1986;148:599-601. 
    doi: 10.1192/bjp.148.5.599.
    3. Turkoz I, Alphs L, Singh J, Jamieson C, Daly E, Shawi M, et al. Clinically meaningful 
    changes on depressive symptom measures and patient-reported outcomes in patients with 
    treatment-resistant depression. J Affect Disord. 2021;281:267-273. 
    doi: 10.1016/j.jad.2020.12.021.
    """
    
    apparent_sadness: int = Field(
        ...,
        ge=0,
        le=6,
        description="Apparent sadness - Observable signs of despondency, gloom and despair reflected in speech, facial expression and posture. Rate by depth and inability to brighten up. 0=No sadness, 6=Looks miserable all the time, extremely despondent",
        example=2
    )
    
    reported_sadness: int = Field(
        ...,
        ge=0,
        le=6,
        description="Reported sadness - Patient's subjective experience of depressed mood, regardless of whether it is reflected in appearance. Includes lowered mood, despondency or feeling of hopelessness. 0=Occasional sadness in keeping with circumstances, 6=Reports virtually only these feelings",
        example=3
    )
    
    inner_tension: int = Field(
        ...,
        ge=0,
        le=6,
        description="Inner tension - Feelings of ill-defined discomfort, edginess, inner turmoil, mental tension mounting to panic, dread, or anguish. Rate according to intensity, frequency, duration and extent of reassurance called for. 0=Placid, only fleeting inner tension, 6=Unrelenting dread or anguish, overwhelming panic",
        example=1
    )
    
    reduced_sleep: int = Field(
        ...,
        ge=0,
        le=6,
        description="Reduced sleep - Experience of reduced duration or depth of sleep compared to the subject's own normal pattern when well. 0=Sleeps as usual, 6=Less than 2-3 hours sleep",
        example=2
    )
    
    reduced_appetite: int = Field(
        ...,
        ge=0,
        le=6,
        description="Reduced appetite - Feeling of loss of appetite compared with when well. Rate by loss of desire for food or the need to force oneself to eat. 0=Normal or increased appetite, 6=Needs persuasion to eat at all",
        example=1
    )
    
    concentration_difficulties: int = Field(
        ...,
        ge=0,
        le=6,
        description="Concentration difficulties - Difficulties in collecting one's thoughts mounting to incapacitating lack of concentration. Rate according to intensity, frequency, and degree of incapacity produced. 0=No difficulties in concentrating, 6=Unable to read or converse without great initiative",
        example=2
    )
    
    lassitude: int = Field(
        ...,
        ge=0,
        le=6,
        description="Lassitude - Difficulty getting started or slowness in initiating and performing everyday activities. 0=Hardly any difficulty in getting started, no sluggishness, 6=Complete lassitude, inability to do anything without help",
        example=3
    )
    
    inability_to_feel: int = Field(
        ...,
        ge=0,
        le=6,
        description="Inability to feel - Subjective experience of reduced interest in the surroundings, or activities that normally give pleasure. The ability to react with adequate emotion to circumstances or people. 0=Normal interest in the surroundings and other people, 6=The experience of being emotionally paralyzed, inability to feel anger, grief or pleasure",
        example=2
    )
    
    pessimistic_thoughts: int = Field(
        ...,
        ge=0,
        le=6,
        description="Pessimistic thoughts - Thoughts of guilt, inferiority, self-reproach, sinfulness, remorse and ruin. 0=No pessimistic thoughts, 6=Delusions of ruin, remorse and unredeemable sin, self-accusations which are absurd and unshakable",
        example=1
    )
    
    suicidal_thoughts: int = Field(
        ...,
        ge=0,
        le=6,
        description="Suicidal thoughts - Feeling that life is not worth living, that a natural death would be welcome, suicidal thoughts, and preparations for suicide. Suicidal attempts should not in themselves influence the rating. 0=Enjoys life or takes it as it comes, 6=Explicit plans for suicide when there is an opportunity, active preparations for suicide",
        example=0
    )
    
    class Config:
        schema_extra = {
            "example": {
                "apparent_sadness": 2,
                "reported_sadness": 3,
                "inner_tension": 1,
                "reduced_sleep": 2,
                "reduced_appetite": 1,
                "concentration_difficulties": 2,
                "lassitude": 3,
                "inability_to_feel": 2,
                "pessimistic_thoughts": 1,
                "suicidal_thoughts": 0
            }
        }


class MadrsResponse(BaseModel):
    """
    Response model for Montgomery-Asberg Depression Rating Scale (MADRS)
    
    The MADRS total score ranges from 0-60 points and is interpreted as:
    - 0-6: Normal mood or minimal depressive symptoms
    - 7-19: Mild depression with some impact on functioning
    - 20-34: Moderate depression with significant impact requiring treatment
    - 35-60: Severe depression with major impairment requiring intensive treatment
    
    Clinical significance:
    - Response to treatment: ≥50% reduction from baseline score
    - Remission: typically defined as score ≤7-9 points
    - Clinically meaningful change: ≥6 points improvement from baseline
    - Clinically substantial change: ≥12 points improvement from baseline
    
    The MADRS is designed to be sensitive to treatment-induced changes and focuses 
    on core mood symptoms rather than somatic symptoms, making it particularly 
    useful for monitoring antidepressant treatment response.
    
    Reference: Montgomery SA, Asberg M. Br J Psychiatry. 1979;134:382-9.
    """
    
    result: int = Field(
        ...,
        description="MADRS total score calculated from all 10 items (range: 0-60 points)",
        example=17
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended next steps based on the MADRS score",
        example="Mild depression with some impact on daily functioning but generally manageable symptoms. The patient experiences mild depressive symptoms that may affect mood and activities but are generally manageable. Symptoms might include occasional sadness, mild sleep disturbances, slight appetite changes, or minor concentration difficulties. While functioning is maintained, the patient may benefit from psychosocial interventions, lifestyle modifications, or close monitoring."
    )
    
    stage: str = Field(
        ...,
        description="Depression severity category (Normal, Mild Depression, Moderate Depression, Severe Depression)",
        example="Mild Depression"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the depression severity level",
        example="Mild depressive symptoms"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 17,
                "unit": "points",
                "interpretation": "Mild depression with some impact on daily functioning but generally manageable symptoms. The patient experiences mild depressive symptoms that may affect mood and activities but are generally manageable. Symptoms might include occasional sadness, mild sleep disturbances, slight appetite changes, or minor concentration difficulties. While functioning is maintained, the patient may benefit from psychosocial interventions, lifestyle modifications, or close monitoring.",
                "stage": "Mild Depression",
                "stage_description": "Mild depressive symptoms"
            }
        }