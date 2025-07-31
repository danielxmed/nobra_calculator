"""
GAD-7 (General Anxiety Disorder-7) Models

Request and response models for GAD-7 anxiety assessment.

References (Vancouver style):
1. Spitzer RL, Kroenke K, Williams JB, Löwe B. A brief measure for assessing generalized 
   anxiety disorder: the GAD-7. Arch Intern Med. 2006;166(10):1092-7. 
   doi: 10.1001/archinte.166.10.1092.
2. Löwe B, Decker O, Müller S, et al. Validation and standardization of the Generalized 
   Anxiety Disorder Screener (GAD-7) in the general population. Med Care. 2008;46(3):266-74. 
   doi: 10.1097/MLR.0b013e318160d093.
3. Plummer F, Manea L, Trepel D, McMillan D. Screening for anxiety disorders with the GAD-7 
   and GAD-2: a systematic review and diagnostic metaanalysis. Gen Hosp Psychiatry. 
   2016;39:24-31. doi: 10.1016/j.genhosppsych.2015.11.005.

The GAD-7 (General Anxiety Disorder-7) is a validated, reliable screening tool for generalized 
anxiety disorder and a measure of anxiety severity. Originally developed by Spitzer et al. in 2006, 
it has become one of the most widely used anxiety screening instruments in primary care and 
mental health settings.

Key Features:
- 7-item self-report questionnaire assessing anxiety symptoms over past 2 weeks
- 4-point Likert scale (0-3) for each item: "not at all" to "nearly every day"
- Total score range: 0-21 points with higher scores indicating greater anxiety severity
- Quick administration (2-3 minutes) making it ideal for busy clinical settings
- Validated across diverse populations and clinical settings

Clinical Applications:
- Primary care screening for anxiety disorders
- Mental health assessment and treatment monitoring
- Research studies measuring anxiety severity
- Population health screening programs
- Treatment response evaluation over time

Diagnostic Performance:
- Sensitivity 89%, specificity 82% for GAD using cutoff score ≥10
- Score ≥8 optimal for screening probable GAD (sensitivity 92%, specificity 76%)
- Also screens effectively for panic disorder, social anxiety disorder, and PTSD
- Excellent internal consistency (Cronbach's α = 0.92)
- Good test-retest reliability and construct validity

Score Interpretation:
- 0-4: Minimal anxiety (no intervention needed)
- 5-9: Mild anxiety (monitor, provide reassurance, stress management)
- 10-14: Moderate anxiety (further assessment, possible mental health referral)
- 15-21: Severe anxiety (active treatment warranted, mental health referral recommended)

Clinical Considerations:
- Assesses symptoms over past 2 weeks (not diagnostic period for GAD)
- Does not replace comprehensive psychiatric evaluation
- Consider cultural and linguistic factors in interpretation
- Monitor changes over time to assess treatment response
- Evaluate functional impairment and quality of life impact
- Screen for comorbid conditions (depression, substance use)
- Assess suicide risk in high-scoring patients

Limitations:
- Self-report measure subject to response bias
- Does not provide specific anxiety disorder diagnosis
- May be influenced by transient stressors or medical conditions
- Limited validation in certain populations (children, elderly, specific ethnicities)
- Should be combined with clinical judgment and additional assessment tools
"""

from pydantic import BaseModel, Field
from typing import Literal


class Gad7Request(BaseModel):
    """
    Request model for GAD-7 (General Anxiety Disorder-7) Scale
    
    The GAD-7 is a 7-item questionnaire that assesses anxiety symptoms experienced over 
    the past 2 weeks. Each item is rated on a 4-point scale from 0 (not at all) to 3 
    (nearly every day), providing a comprehensive assessment of generalized anxiety severity.
    
    **INSTRUCTIONS FOR ADMINISTRATION**:
    
    Ask the patient: "Over the last 2 weeks, how often have you been bothered by the following problems?"
    
    For each item, select the response that best describes how often the patient has experienced 
    the symptom over the past 2 weeks:
    - **0 = Not at all**: The symptom has not occurred or bothered the patient
    - **1 = Several days**: The symptom occurred on some days but not most days
    - **2 = More than half the days**: The symptom occurred on more than 7 out of 14 days
    - **3 = Nearly every day**: The symptom occurred almost daily (11+ out of 14 days)
    
    **GAD-7 QUESTIONNAIRE ITEMS**:
    
    1. **Feeling nervous, anxious, or on edge**
       - Assesses core anxiety symptoms and physiological arousal
       - Includes restlessness, tension, feeling keyed up or wound up
    
    2. **Not being able to stop or control worrying**
       - Evaluates uncontrollable worry, a hallmark of generalized anxiety disorder
       - Includes excessive, persistent worry that is difficult to manage
    
    3. **Worrying too much about different things**
       - Assesses excessive worry across multiple life domains
       - Includes concern about work, health, family, finances, or other areas
    
    4. **Trouble relaxing**
       - Evaluates difficulty achieving relaxation or calm states
       - Includes feeling unable to rest, unwind, or feel at ease
    
    5. **Being so restless that it's hard to sit still**
       - Assesses motor restlessness and psychomotor agitation
       - Includes fidgeting, pacing, inability to remain seated
    
    6. **Becoming easily annoyed or irritable**
       - Evaluates irritability as a manifestation of anxiety
       - Includes short temper, feeling on edge, snapping at others
    
    7. **Feeling afraid as if something awful might happen**
       - Assesses catastrophic thinking and anticipatory anxiety
       - Includes fear of disaster, sense of impending doom, worry about future threats
    
    **CLINICAL INTERPRETATION GUIDELINES**:
    
    **Total Score Calculation**: Sum all 7 item scores (range 0-21)
    
    **Severity Categories**:
    - **0-4 points**: Minimal anxiety (no clinical intervention needed)
    - **5-9 points**: Mild anxiety (monitor, provide reassurance, stress management)
    - **10-14 points**: Moderate anxiety (further assessment, possible referral)
    - **15-21 points**: Severe anxiety (active treatment, mental health referral)
    
    **Screening Thresholds**:
    - **Score ≥8**: Optimal cutoff for probable GAD (sensitivity 92%, specificity 76%)
    - **Score ≥10**: Recommended cutoff for further mental health evaluation
    - **Score ≥15**: Strong indication for immediate mental health intervention
    
    **CLINICAL APPLICATIONS**:
    - Primary care anxiety screening
    - Mental health assessment and diagnosis
    - Treatment monitoring and response evaluation
    - Research studies measuring anxiety severity
    - Population health surveillance
    
    **IMPORTANT CONSIDERATIONS**:
    - Assess symptoms over past 2 weeks specifically
    - Consider cultural factors in symptom expression and interpretation
    - Evaluate functional impairment and quality of life impact
    - Screen for comorbid conditions (depression, substance use, medical conditions)
    - Assess suicide risk in patients with high scores
    - Use clinical judgment in conjunction with GAD-7 results
    - Consider additional assessment tools for comprehensive evaluation
    
    References (Vancouver style):
    1. Spitzer RL, Kroenke K, Williams JB, Löwe B. A brief measure for assessing generalized 
       anxiety disorder: the GAD-7. Arch Intern Med. 2006;166(10):1092-7.
    2. Löwe B, Decker O, Müller S, et al. Validation and standardization of the Generalized 
       Anxiety Disorder Screener (GAD-7) in the general population. Med Care. 2008;46(3):266-74.
    3. Plummer F, Manea L, Trepel D, McMillan D. Screening for anxiety disorders with the GAD-7 
       and GAD-2: a systematic review and diagnostic metaanalysis. Gen Hosp Psychiatry. 2016;39:24-31.
    """
    
    nervous_anxious_on_edge: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Feeling nervous, anxious, or on edge (over the past 2 weeks). 0=Not at all, 1=Several days, 2=More than half the days, 3=Nearly every day",
        example=1
    )
    
    not_able_stop_control_worrying: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Not being able to stop or control worrying (over the past 2 weeks). 0=Not at all, 1=Several days, 2=More than half the days, 3=Nearly every day",
        example=2
    )
    
    worrying_too_much_different_things: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Worrying too much about different things (over the past 2 weeks). 0=Not at all, 1=Several days, 2=More than half the days, 3=Nearly every day",
        example=1
    )
    
    trouble_relaxing: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Trouble relaxing (over the past 2 weeks). 0=Not at all, 1=Several days, 2=More than half the days, 3=Nearly every day",
        example=1
    )
    
    being_so_restless: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Being so restless that it's hard to sit still (over the past 2 weeks). 0=Not at all, 1=Several days, 2=More than half the days, 3=Nearly every day",
        example=0
    )
    
    becoming_easily_annoyed_irritable: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Becoming easily annoyed or irritable (over the past 2 weeks). 0=Not at all, 1=Several days, 2=More than half the days, 3=Nearly every day",
        example=1
    )
    
    feeling_afraid_something_awful: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Feeling afraid as if something awful might happen (over the past 2 weeks). 0=Not at all, 1=Several days, 2=More than half the days, 3=Nearly every day",
        example=2
    )
    
    class Config:
        schema_extra = {
            "example": {
                "nervous_anxious_on_edge": 1,
                "not_able_stop_control_worrying": 2,
                "worrying_too_much_different_things": 1,
                "trouble_relaxing": 1,
                "being_so_restless": 0,
                "becoming_easily_annoyed_irritable": 1,
                "feeling_afraid_something_awful": 2
            }
        }


class Gad7Response(BaseModel):
    """
    Response model for GAD-7 (General Anxiety Disorder-7) Scale
    
    The response provides the calculated GAD-7 total score along with severity classification 
    and evidence-based clinical recommendations for anxiety assessment and management.
    
    **SCORE INTERPRETATION AND CLINICAL MANAGEMENT**:
    
    **Minimal Anxiety (0-4 points)**:
    - **Clinical Significance**: No significant anxiety symptoms present
    - **Management**: No specific intervention required at this time
    - **Follow-up**: Routine monitoring during regular healthcare visits
    - **Patient Education**: General wellness counseling, stress management techniques
    - **Documentation**: Note baseline anxiety level for future comparison
    
    **Mild Anxiety (5-9 points)**:
    - **Clinical Significance**: Mild anxiety symptoms that may benefit from support
    - **Management**: Monitor symptoms, provide reassurance and psychoeducation
    - **Interventions**: Stress management techniques, relaxation training, mindfulness
    - **Follow-up**: Reassess in 2-4 weeks to monitor symptom progression
    - **Referral**: Generally managed in primary care setting
    - **Patient Education**: Anxiety psychoeducation, lifestyle modifications, coping strategies
    
    **Moderate Anxiety (10-14 points)**:
    - **Clinical Significance**: Possible clinically significant anxiety disorder
    - **Assessment**: Further evaluation recommended to determine specific diagnosis
    - **Management**: Consider structured clinical interview (MINI, SCID-5)
    - **Treatment Options**: 
      - Psychotherapy: Cognitive Behavioral Therapy (CBT), Acceptance and Commitment Therapy
      - Pharmacotherapy: Consider if psychotherapy insufficient or patient preference
      - Combination: Often most effective for moderate anxiety
    - **Referral**: Mental health professional referral appropriate
    - **Monitoring**: Regular follow-up every 2-4 weeks initially
    
    **Severe Anxiety (15-21 points)**:
    - **Clinical Significance**: Significant anxiety symptoms requiring active treatment
    - **Immediate Actions**: Strong recommendation for mental health referral
    - **Assessment Priorities**:
      - Comprehensive psychiatric evaluation
      - Screen for comorbid conditions (depression, substance use)
      - Assess functional impairment and quality of life
      - Evaluate suicide risk and safety planning if needed
    - **Treatment Recommendations**:
      - **Psychotherapy**: CBT, exposure therapy, or other evidence-based approaches
      - **Pharmacotherapy**: SSRIs, SNRIs, or other appropriate anxiolytics
      - **Combination Therapy**: Often recommended for severe symptoms
    - **Crisis Resources**: Provide if immediate risk concerns
    - **Monitoring**: Close follow-up, potentially weekly initially
    
    **TREATMENT CONSIDERATIONS**:
    
    **Psychotherapy Options** (Evidence-Based):
    - **Cognitive Behavioral Therapy (CBT)**: First-line treatment for anxiety disorders
    - **Exposure and Response Prevention**: Particularly effective for specific phobias
    - **Acceptance and Commitment Therapy (ACT)**: Helpful for anxiety with avoidance
    - **Mindfulness-Based Stress Reduction (MBSR)**: Adjunctive treatment option
    
    **Pharmacotherapy Considerations**:
    - **First-Line**: SSRIs (sertraline, escitalopram, paroxetine)
    - **Alternative**: SNRIs (venlafaxine, duloxetine)
    - **Short-term**: Benzodiazepines only for acute symptoms (limited duration)
    - **Adjunctive**: Buspirone, pregabalin, or other agents based on clinical picture
    
    **Monitoring and Follow-up**:
    - **Frequency**: Based on severity and treatment response
    - **Tools**: Repeat GAD-7 to monitor treatment response
    - **Target**: 50% reduction in GAD-7 score or score <10 for remission
    - **Duration**: Minimum 6-12 months of treatment for sustained remission
    
    **Special Populations**:
    - **Elderly**: Start low, go slow with medications; consider medical comorbidities
    - **Pregnancy**: Psychotherapy preferred; medication decisions require risk-benefit analysis
    - **Adolescents**: Family involvement important; school-based interventions may help
    - **Medical Comorbidity**: Consider anxiety secondary to medical conditions
    
    **Quality Measures**:
    - Validated across diverse populations and clinical settings
    - Excellent psychometric properties (sensitivity 89%, specificity 82%)
    - Widely used in clinical practice and research
    - Incorporated into major clinical practice guidelines
    - Suitable for treatment monitoring and outcome measurement
    
    Reference: Spitzer RL, et al. Arch Intern Med. 2006;166(10):1092-7.
    """
    
    result: int = Field(
        ...,
        description="Total GAD-7 score calculated by summing all 7 item scores (range: 0-21 points)",
        ge=0,
        le=21,
        example=8
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the GAD-7 score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including severity level, clinical significance, and evidence-based management recommendations",
        example="GAD-7 score of 8 indicates mild anxiety symptoms. Monitor symptoms and provide reassurance and support. Consider stress management techniques such as relaxation training, mindfulness exercises, or cognitive behavioral strategies. Evaluate for psychosocial stressors and provide appropriate counseling. Reassess in 2-4 weeks to monitor symptom progression."
    )
    
    stage: str = Field(
        ...,
        description="Anxiety severity category (Minimal Anxiety, Mild Anxiety, Moderate Anxiety, Severe Anxiety)",
        example="Mild Anxiety"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the anxiety severity level",
        example="Mild anxiety symptoms"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 8,
                "unit": "points",
                "interpretation": "GAD-7 score of 8 indicates mild anxiety symptoms. Monitor symptoms and provide reassurance and support. Consider stress management techniques such as relaxation training, mindfulness exercises, or cognitive behavioral strategies. Evaluate for psychosocial stressors and provide appropriate counseling. Reassess in 2-4 weeks to monitor symptom progression.",
                "stage": "Mild Anxiety",
                "stage_description": "Mild anxiety symptoms"
            }
        }