"""
Geriatric Depression Scale (GDS-15) Models

Request and response models for GDS-15 calculation.

References (Vancouver style):
1. Yesavage JA, Brink TL, Rose TL, et al. Development and validation of a geriatric depression 
   screening scale: a preliminary report. J Psychiatr Res. 1982-1983;17(1):37-49. 
   doi: 10.1016/0022-3956(82)90033-4.
2. Sheikh JI, Yesavage JA. Geriatric Depression Scale (GDS): recent evidence and development 
   of a shorter version. Clin Gerontol. 1986;5(1-2):165-173. doi: 10.1300/J018v05n01_09.
3. D'Ath P, Katona P, Mullan E, Evans S, Katona C. Screening, detection and management of 
   depression in elderly primary care attenders. I: The acceptability and performance of the 
   15 item Geriatric Depression Scale (GDS15) and the development of short versions. 
   Fam Pract. 1994;11(3):260-266. doi: 10.1093/fampra/11.3.260.

The Geriatric Depression Scale (GDS-15) is a validated screening instrument specifically 
designed for identifying possible depression in adults aged 55 and older. The 15-item 
version, developed in 1986, provides a brief and reliable assessment using simple yes/no 
questions that focus on psychological rather than somatic symptoms, making it particularly 
suitable for the geriatric population where medical illness may confound other depression 
screening tools.

Key Clinical Applications:
- Depression screening in primary care settings for older adults
- Routine mental health assessment in geriatric clinics
- Pre-treatment evaluation in psychiatric and psychological services
- Monitoring depression symptoms over time in treatment settings
- Population health screening in community and residential care settings

The GDS-15 demonstrates strong psychometric properties with sensitivity of 81% and specificity 
of 78% for identifying late-life depression in primary care settings. It avoids questions 
about somatic symptoms that may be related to medical conditions common in older adults, 
focusing instead on mood, cognition, and social aspects of depression. The scale covers 
the past week and uses a straightforward yes/no response format that is well-tolerated 
by elderly patients and can be self-administered or clinician-administered.

Clinical validation studies have consistently shown that scores of 0-4 indicate absence 
of clinically significant depression, scores of 5-7 suggest mild depression, scores of 
8-9 suggest moderate depression, and scores of 10-15 suggest severe depression requiring 
urgent evaluation and treatment. The tool serves as an effective screening instrument 
that helps identify patients who would benefit from more comprehensive diagnostic evaluation 
and appropriate mental health interventions.
"""

from pydantic import BaseModel, Field
from typing import Literal


class Gds15Request(BaseModel):
    """
    Request model for Geriatric Depression Scale (GDS-15)
    
    The GDS-15 provides screening for depression in adults aged 55 and older using 15 
    carefully selected questions that assess psychological symptoms of depression over 
    the past week. The scale uses simple yes/no responses and avoids somatic symptoms 
    that may be confounded by medical illness in older adults.
    
    **CLINICAL CONTEXT AND INDICATIONS**:
    
    **Primary Clinical Application**:
    - **Target Population**: Adults aged 55 and older in various healthcare settings
    - **Clinical Settings**: Primary care, geriatric clinics, psychiatric services, long-term care
    - **Assessment Period**: Symptoms and feelings over the past week
    - **Administration**: Can be self-administered or clinician-administered
    
    **Key Advantages for Geriatric Population**:
    - **Age-Appropriate**: Specifically designed and validated for older adults
    - **Simplified Format**: Yes/no responses suitable for patients with cognitive changes
    - **Medical Illness Friendly**: Avoids somatic symptoms that may be due to medical conditions
    - **Brief Administration**: 15 questions can be completed in 5-10 minutes
    - **Multi-Setting Use**: Effective in outpatient, inpatient, and residential care settings
    
    **QUESTION INTERPRETATION FRAMEWORK**:
    
    **DEPRESSION-INDICATING "YES" RESPONSES (10 questions)**:
    
    These questions identify depression when the patient answers "YES":
    
    **Q2: "Have you dropped many of your activities and interests?"**:
    - **Clinical Significance**: Assesses anhedonia and behavioral withdrawal
    - **Depression Indicator**: Loss of interest in previously enjoyed activities
    - **Geriatric Context**: Important to distinguish from activity limitations due to physical health
    - **Scoring**: YES = 1 point (indicates depression)
    
    **Q3: "Do you feel that your life is empty?"**:
    - **Clinical Significance**: Evaluates existential emptiness and life satisfaction
    - **Depression Indicator**: Sense of meaninglessness and lack of purpose
    - **Geriatric Context**: May relate to role changes, losses, and life transitions
    - **Scoring**: YES = 1 point (indicates depression)
    
    **Q4: "Do you often get bored?"**:
    - **Clinical Significance**: Assesses lack of engagement and motivation
    - **Depression Indicator**: Difficulty finding interest or pleasure in daily activities
    - **Geriatric Context**: May reflect reduced cognitive stimulation or social isolation
    - **Scoring**: YES = 1 point (indicates depression)
    
    **Q6: "Are you afraid that something bad is going to happen to you?"**:
    - **Clinical Significance**: Evaluates anxiety and pessimistic thinking
    - **Depression Indicator**: Anxious anticipation and negative expectation
    - **Geriatric Context**: May relate to health concerns, safety fears, or mortality anxiety
    - **Scoring**: YES = 1 point (indicates depression)
    
    **Q8: "Do you often feel helpless?"**:
    - **Clinical Significance**: Assesses feelings of powerlessness and lack of control
    - **Depression Indicator**: Learned helplessness and reduced self-efficacy
    - **Geriatric Context**: May relate to physical limitations, dependency, or cognitive changes
    - **Scoring**: YES = 1 point (indicates depression)
    
    **Q9: "Do you prefer to stay at home, rather than going out and doing new things?"**:
    - **Clinical Significance**: Evaluates social withdrawal and avoidance behaviors
    - **Depression Indicator**: Isolation and reduced engagement with environment
    - **Geriatric Context**: Important to distinguish from mobility limitations or transportation issues
    - **Scoring**: YES = 1 point (indicates depression)
    
    **Q10: "Do you feel you have more problems with memory than most?"**:
    - **Clinical Significance**: Assesses cognitive concerns and self-perceived impairment
    - **Depression Indicator**: Concentration difficulties and memory complaints in depression
    - **Geriatric Context**: May reflect depression-related cognitive symptoms vs. dementia
    - **Scoring**: YES = 1 point (indicates depression)
    
    **Q12: "Do you feel pretty worthless the way you are now?"**:
    - **Clinical Significance**: Evaluates self-esteem and self-worth
    - **Depression Indicator**: Negative self-evaluation and feelings of inadequacy
    - **Geriatric Context**: May relate to role loss, physical changes, or perceived burden
    - **Scoring**: YES = 1 point (indicates depression)
    
    **Q14: "Do you feel that your situation is hopeless?"**:
    - **Clinical Significance**: Assesses hopelessness and future orientation
    - **Depression Indicator**: Negative expectations and despair about the future
    - **Geriatric Context**: Critical indicator requiring suicide risk assessment
    - **Scoring**: YES = 1 point (indicates depression)
    
    **Q15: "Do you think that most people are better off than you are?"**:
    - **Clinical Significance**: Evaluates social comparison and self-perception
    - **Depression Indicator**: Negative social comparison and relative deprivation
    - **Geriatric Context**: May reflect realistic assessment of health/function vs. depressive thinking
    - **Scoring**: YES = 1 point (indicates depression)
    
    **DEPRESSION-INDICATING "NO" RESPONSES (5 questions)**:
    
    These questions identify depression when the patient answers "NO":
    
    **Q1: "Are you basically satisfied with your life?"**:
    - **Clinical Significance**: Assesses overall life satisfaction and contentment
    - **Depression Indicator**: Dissatisfaction and negative life evaluation
    - **Geriatric Context**: Considers adaptation to aging and life circumstances
    - **Scoring**: NO = 1 point (indicates depression)
    
    **Q5: "Are you in good spirits most of the time?"**:
    - **Clinical Significance**: Evaluates general mood state and emotional well-being
    - **Depression Indicator**: Persistent low mood and reduced positive affect
    - **Geriatric Context**: Distinguishes from temporary mood changes due to circumstances
    - **Scoring**: NO = 1 point (indicates depression)
    
    **Q7: "Do you feel happy most of the time?"**:
    - **Clinical Significance**: Assesses subjective happiness and positive emotions
    - **Depression Indicator**: Absence of joy and positive mood states
    - **Geriatric Context**: Important measure of emotional well-being in later life
    - **Scoring**: NO = 1 point (indicates depression)
    
    **Q11: "Do you think it is wonderful to be alive now?"**:
    - **Clinical Significance**: Evaluates life appreciation and existential well-being
    - **Depression Indicator**: Loss of life appreciation and possible suicidal ideation
    - **Geriatric Context**: Critical question requiring careful follow-up if answered "NO"
    - **Scoring**: NO = 1 point (indicates depression)
    
    **Q13: "Do you feel full of energy?"**:
    - **Clinical Significance**: Assesses energy level and vitality
    - **Depression Indicator**: Fatigue and lack of energy (psychological, not just physical)
    - **Geriatric Context**: Distinguishes depression-related fatigue from medical causes
    - **Scoring**: NO = 1 point (indicates depression)
    
    **CLINICAL ADMINISTRATION GUIDELINES**:
    
    **Assessment Environment**:
    - Quiet, private setting conducive to honest self-reflection
    - Adequate time without rushing (5-10 minutes typically)
    - Clear instructions emphasizing focus on the past week
    - Supportive, non-judgmental approach by administrator
    
    **Response Collection**:
    - Simple yes/no format reduces cognitive burden
    - Clarify that responses should reflect the past week specifically
    - Allow for brief clarification but avoid leading responses
    - Document any qualifications or additional context provided
    
    **Special Considerations**:
    
    **Cognitive Impairment**:
    - May still be useful in mild cognitive impairment
    - Consider informant input for validation
    - May require simplified administration or repetition
    - Results should be interpreted cautiously with significant cognitive impairment
    
    **Cultural and Language Factors**:
    - Available in multiple languages with validated translations
    - Consider cultural concepts of depression and emotional expression
    - May require adaptation for different cultural contexts
    - Use qualified interpreters when needed
    
    **Medical Illness Context**:
    - Particularly valuable because it avoids somatic symptoms
    - Consider interaction between depression and medical conditions
    - May be useful in hospitalized patients and those with chronic illness
    - Results should be integrated with comprehensive medical evaluation
    
    **Suicide Risk Assessment**:
    - Questions 11 and 14 are particularly important for suicide risk
    - Any concerning responses should trigger immediate suicide risk assessment
    - Have safety protocols and resources readily available
    - Consider immediate referral for high-risk patients
    
    References (Vancouver style):
    1. Yesavage JA, Brink TL, Rose TL, et al. Development and validation of a geriatric depression 
       screening scale: a preliminary report. J Psychiatr Res. 1982-1983;17(1):37-49.
    2. Sheikh JI, Yesavage JA. Geriatric Depression Scale (GDS): recent evidence and development 
       of a shorter version. Clin Gerontol. 1986;5(1-2):165-173.
    3. D'Ath P, Katona P, Mullan E, Evans S, Katona C. Screening, detection and management of 
       depression in elderly primary care attenders. Fam Pract. 1994;11(3):260-266.
    """
    
    q1_satisfied_with_life: Literal["yes", "no"] = Field(
        ...,
        description="Are you basically satisfied with your life? (Depression indicated if NO)",
        example="yes"
    )
    
    q2_dropped_activities: Literal["yes", "no"] = Field(
        ...,
        description="Have you dropped many of your activities and interests? (Depression indicated if YES)",
        example="no"
    )
    
    q3_life_empty: Literal["yes", "no"] = Field(
        ...,
        description="Do you feel that your life is empty? (Depression indicated if YES)",
        example="no"
    )
    
    q4_often_bored: Literal["yes", "no"] = Field(
        ...,
        description="Do you often get bored? (Depression indicated if YES)",
        example="no"
    )
    
    q5_good_spirits: Literal["yes", "no"] = Field(
        ...,
        description="Are you in good spirits most of the time? (Depression indicated if NO)",
        example="yes"
    )
    
    q6_afraid_bad_happen: Literal["yes", "no"] = Field(
        ...,
        description="Are you afraid that something bad is going to happen to you? (Depression indicated if YES)",
        example="no"
    )
    
    q7_happy_most_time: Literal["yes", "no"] = Field(
        ...,
        description="Do you feel happy most of the time? (Depression indicated if NO)",
        example="yes"
    )
    
    q8_feel_helpless: Literal["yes", "no"] = Field(
        ...,
        description="Do you often feel helpless? (Depression indicated if YES)",
        example="no"
    )
    
    q9_prefer_stay_home: Literal["yes", "no"] = Field(
        ...,
        description="Do you prefer to stay at home, rather than going out and doing new things? (Depression indicated if YES)",
        example="no"
    )
    
    q10_memory_problems: Literal["yes", "no"] = Field(
        ...,
        description="Do you feel you have more problems with memory than most? (Depression indicated if YES)",
        example="no"
    )
    
    q11_wonderful_to_be_alive: Literal["yes", "no"] = Field(
        ...,
        description="Do you think it is wonderful to be alive now? (Depression indicated if NO)",
        example="yes"
    )
    
    q12_feel_worthless: Literal["yes", "no"] = Field(
        ...,
        description="Do you feel pretty worthless the way you are now? (Depression indicated if YES)",
        example="no"
    )
    
    q13_full_of_energy: Literal["yes", "no"] = Field(
        ...,
        description="Do you feel full of energy? (Depression indicated if NO)",
        example="yes"
    )
    
    q14_situation_hopeless: Literal["yes", "no"] = Field(
        ...,
        description="Do you feel that your situation is hopeless? (Depression indicated if YES)",
        example="no"
    )
    
    q15_others_better_off: Literal["yes", "no"] = Field(
        ...,
        description="Do you think that most people are better off than you are? (Depression indicated if YES)",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "q1_satisfied_with_life": "no",
                "q2_dropped_activities": "yes",
                "q3_life_empty": "yes",
                "q4_often_bored": "no",
                "q5_good_spirits": "no",
                "q6_afraid_bad_happen": "yes",
                "q7_happy_most_time": "no",
                "q8_feel_helpless": "yes",
                "q9_prefer_stay_home": "no",
                "q10_memory_problems": "no",
                "q11_wonderful_to_be_alive": "yes",
                "q12_feel_worthless": "no",
                "q13_full_of_energy": "no",
                "q14_situation_hopeless": "no",
                "q15_others_better_off": "no"
            }
        }


class Gds15Response(BaseModel):
    """
    Response model for Geriatric Depression Scale (GDS-15)
    
    The response provides the calculated GDS-15 score with detailed clinical interpretation 
    and evidence-based recommendations for further evaluation and treatment based on 
    validated severity thresholds from geriatric psychiatry research.
    
    **CLINICAL INTERPRETATION FRAMEWORK**:
    
    **GDS-15 Score Components and Validation**:
    - **Total Score Range**: 0-15 points with four distinct severity categories
    - **Psychometric Properties**: Sensitivity 81%, specificity 78% for late-life depression
    - **Validation Population**: Extensively validated in community-dwelling and clinical older adults
    - **Scoring Method**: Sum of depression-indicating responses across 15 carefully selected items
    
    **Severity Category Definitions and Clinical Implications**:
    
    **Normal Range (0-4 points)**:
    - **Clinical Interpretation**: Absence of clinically significant depressive symptoms
    - **Population Prevalence**: Approximately 60-70% of community-dwelling older adults
    - **Clinical Significance**: Scores within normal range for age, education, and life circumstances
    - **Management Approach**: Routine screening, health promotion, and preventive interventions
    - **Risk Factors**: Monitor for changes due to life stressors, medical illness, or functional decline
    
    **Mild Depression (5-7 points)**:
    - **Clinical Interpretation**: Mild depressive symptoms requiring attention and monitoring
    - **Population Prevalence**: Approximately 15-20% of older adults in primary care settings
    - **Clinical Significance**: Subthreshold depression that may progress without intervention
    - **Management Approach**: Formal diagnostic evaluation, counseling, supportive interventions
    - **Treatment Options**: Psychotherapy, behavioral activation, social support, lifestyle interventions
    
    **Moderate Depression (8-9 points)**:
    - **Clinical Interpretation**: Moderate depression requiring active treatment intervention
    - **Population Prevalence**: Approximately 8-12% of older adults in clinical settings
    - **Clinical Significance**: Significant functional impairment and reduced quality of life
    - **Management Approach**: Psychiatric evaluation, combination treatment approaches
    - **Treatment Options**: Antidepressant medication, psychotherapy, collaborative care models
    
    **Severe Depression (10-15 points)**:
    - **Clinical Interpretation**: Severe depression requiring urgent comprehensive evaluation
    - **Population Prevalence**: Approximately 3-5% of community-dwelling older adults
    - **Clinical Significance**: Major functional impairment, high suicide risk, potential hospitalization needs
    - **Management Approach**: Immediate psychiatric consultation, intensive treatment, safety assessment
    - **Treatment Options**: Combination medication and psychotherapy, intensive outpatient programs, hospitalization
    
    **CLINICAL MANAGEMENT BY SEVERITY CATEGORY**:
    
    **Normal Range Management (0-4 points)**:
    
    **Routine Care Approach**:
    - **Screening Frequency**: Annual screening or with significant life changes
    - **Health Promotion**: Encourage physical activity, social engagement, cognitive stimulation
    - **Preventive Strategies**: Address modifiable risk factors (social isolation, medical comorbidities)
    - **Patient Education**: Information about normal aging vs. depression, when to seek help
    
    **Monitoring Strategy**:
    - **Risk Assessment**: Identify patients at higher risk (chronic illness, functional decline, bereavement)
    - **Proactive Support**: Connect with community resources, senior centers, support groups
    - **Follow-up Planning**: Establish regular check-ins for patients with risk factors
    - **Family Involvement**: Educate family members about depression warning signs
    
    **Mild Depression Management (5-7 points)**:
    
    **Assessment and Evaluation**:
    - **Comprehensive Evaluation**: Formal diagnostic interview to rule out major depression
    - **Functional Assessment**: Evaluate impact on activities of daily living and social functioning
    - **Medical Review**: Assess for medical conditions or medications contributing to symptoms
    - **Psychosocial Assessment**: Identify stressors, losses, and support system adequacy
    
    **Intervention Strategies**:
    - **Psychosocial Interventions**: Counseling, behavioral activation, problem-solving therapy
    - **Community Resources**: Senior centers, support groups, volunteer opportunities
    - **Lifestyle Modifications**: Exercise programs, sleep hygiene, nutrition counseling
    - **Social Support**: Family involvement, peer support programs, social service coordination
    
    **Monitoring and Follow-up**:
    - **Follow-up Schedule**: 2-4 week intervals initially, then monthly until improvement
    - **Symptom Tracking**: Regular administration of GDS-15 to monitor progress
    - **Functional Monitoring**: Assess changes in daily activities, social engagement, self-care
    - **Treatment Response**: Adjust interventions based on symptom trajectory and functional improvement
    
    **Moderate Depression Management (8-9 points)**:
    
    **Comprehensive Psychiatric Assessment**:
    - **Diagnostic Evaluation**: Structured clinical interview for major depressive disorder
    - **Suicide Risk Assessment**: Comprehensive evaluation using validated tools and clinical interview
    - **Cognitive Assessment**: Screen for cognitive impairment that may complicate treatment
    - **Medical Evaluation**: Thorough review of medical conditions, medications, and substance use
    
    **Treatment Planning**:
    - **Pharmacological Intervention**: Consider antidepressant medication with geriatric dosing principles
    - **Psychotherapy**: Evidence-based approaches (cognitive-behavioral therapy, interpersonal therapy)
    - **Collaborative Care**: Coordinate between primary care, mental health, and social services
    - **Family Involvement**: Engage family members in treatment planning and support
    
    **Intensive Monitoring**:
    - **Frequent Visits**: Weekly to bi-weekly appointments initially
    - **Safety Assessment**: Regular suicide risk evaluation and safety planning
    - **Medication Management**: Monitor for side effects, drug interactions, and treatment response
    - **Functional Assessment**: Track improvement in daily activities and quality of life
    
    **Severe Depression Management (10-15 points)**:
    
    **Urgent Psychiatric Evaluation**:
    - **Same-day Assessment**: Urgent referral to mental health services
    - **Comprehensive Safety Assessment**: Immediate evaluation for suicide risk and safety planning
    - **Crisis Intervention**: Consider emergency department evaluation if imminent safety concerns
    - **Hospitalization Assessment**: Evaluate need for inpatient psychiatric treatment
    
    **Intensive Treatment Approach**:
    - **Medication Management**: Prompt initiation of antidepressant therapy with close monitoring
    - **Intensive Psychotherapy**: Frequent sessions with experienced geriatric mental health providers
    - **Care Coordination**: Multidisciplinary team approach with psychiatry, psychology, social work
    - **Family Crisis Support**: Immediate family involvement and crisis support resources
    
    **Safety and Support Systems**:
    - **24/7 Crisis Resources**: Ensure access to crisis hotlines and emergency services
    - **Social Support Activation**: Mobilize family, friends, and community resources
    - **Environmental Safety**: Address home safety concerns and access to means of self-harm
    - **Intensive Case Management**: Coordinate complex care needs and ensure treatment adherence
    
    **SPECIAL CLINICAL CONSIDERATIONS**:
    
    **Suicide Risk Assessment**:
    - **High-Risk Indicators**: Scores ≥10, responses to questions 11 or 14, history of attempts
    - **Protective Factors**: Social support, religious beliefs, responsibility to others
    - **Risk Mitigation**: Safety planning, means restriction, increased monitoring
    - **Crisis Resources**: National Suicide Prevention Lifeline: 988, local crisis services
    
    **Medical Comorbidity Considerations**:
    - **Depression-Medical Illness Interaction**: Assess bidirectional relationship
    - **Medication Interactions**: Review for drug-drug interactions and contraindications
    - **Functional Impact**: Consider combined impact on mobility, cognition, and self-care
    - **Integrated Care**: Coordinate mental health and medical treatment approaches
    
    **Cognitive Impairment Interface**:
    - **Depression vs. Dementia**: Differentiate cognitive symptoms of depression from dementia
    - **Treatment Modifications**: Adapt interventions for patients with cognitive limitations
    - **Family Education**: Help families understand interaction between mood and cognition
    - **Monitoring Complexity**: Track both mood and cognitive symptoms over time
    
    **Quality Improvement Applications**:
    - **Population Health**: Track depression prevalence and treatment outcomes in older adults
    - **Care Quality Metrics**: Monitor screening rates, treatment initiation, and response
    - **Provider Education**: Train healthcare teams in geriatric depression assessment and treatment
    - **Resource Allocation**: Guide allocation of mental health resources for older adults
    
    Reference: Sheikh JI, Yesavage JA. Clin Gerontol. 1986;5(1-2):165-173.
    """
    
    result: int = Field(
        ...,
        description="GDS-15 total score calculated from depression-indicating responses (0-15 points)",
        ge=0,
        le=15,
        example=6
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for GDS-15 score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation with severity assessment and evidence-based management recommendations",
        example="GDS-15 Score: 6/15 points. Concerning responses: not satisfied with life, dropped activities/interests, not in good spirits, afraid something bad will happen, not happy most of the time, not full of energy. Mild depression indicated. Consider formal diagnostic evaluation by qualified mental health professional. Monitor symptoms closely and consider counseling, supportive interventions, or community resources. Assess functional impact and provide patient education about depression in older adults. Follow up in 2-4 weeks."
    )
    
    stage: str = Field(
        ...,
        description="Depression severity category (Normal, Mild Depression, Moderate Depression, Severe Depression)",
        example="Mild Depression"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of depression severity level",
        example="Suggests mild depression"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 6,
                "unit": "points",
                "interpretation": "GDS-15 Score: 6/15 points. Concerning responses: not satisfied with life, dropped activities/interests, not in good spirits, afraid something bad will happen, not happy most of the time, not full of energy. Mild depression indicated. Consider formal diagnostic evaluation by qualified mental health professional. Monitor symptoms closely and consider counseling, supportive interventions, or community resources. Assess functional impact and provide patient education about depression in older adults. Follow up in 2-4 weeks.",
                "stage": "Mild Depression",
                "stage_description": "Suggests mild depression"
            }
        }