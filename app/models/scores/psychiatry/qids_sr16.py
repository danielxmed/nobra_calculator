"""
Quick Inventory of Depressive Symptomatology (QIDS-SR-16) Models

Request and response models for QIDS-SR-16 calculation.

References (Vancouver style):
1. Rush AJ, Trivedi MH, Ibrahim HM, Carmody TJ, Arnow B, Klein DN, et al. 
   The 16-Item Quick Inventory of Depressive Symptomatology (QIDS), clinician rating 
   (QIDS-C), and self-report (QIDS-SR): a psychometric evaluation in patients with 
   chronic major depression. Biol Psychiatry. 2003 Sep 1;54(5):573-83. 
   doi: 10.1016/s0006-3223(02)01866-8.
2. Trivedi MH, Rush AJ, Ibrahim HM, Carmody TJ, Biggs MM, Suppes T, et al. 
   The Inventory of Depressive Symptomatology, Clinician Rating (IDS-C) and Self-Report 
   (IDS-SR), and the Quick Inventory of Depressive Symptomatology, Clinician Rating 
   (QIDS-C) and Self-Report (QIDS-SR) in public sector patients with mood disorders: 
   a psychometric evaluation. Psychol Med. 2004 Jan;34(1):73-82. doi: 10.1017/s0033291703001107.
3. Reilly TJ, MacGillivray SA, Reid IC, Cameron IM. Psychometric properties of the 16-item 
   Quick Inventory of Depressive Symptomatology: a systematic review and meta-analysis. 
   J Psychiatr Res. 2015 Jan;60:132-40. doi: 10.1016/j.jpsychires.2014.09.008.

The Quick Inventory of Depressive Symptomatology (QIDS-SR-16) is a validated 16-item 
self-report instrument designed to assess the severity of depressive symptoms over the 
past 7 days. Developed by Rush and colleagues in 2003, the QIDS-SR-16 provides a brief 
yet comprehensive evaluation of the nine DSM-IV depression criterion symptom domains, 
making it an essential tool for clinical assessment, treatment monitoring, and research 
applications in mental health settings.

Clinical Background and Development:
The QIDS-SR-16 was derived from the 30-item Inventory of Depressive Symptomatology (IDS) 
to create a more efficient assessment tool while maintaining comprehensive coverage of 
depression symptoms. The instrument was designed to parallel the clinician-rated version 
(QIDS-C-16) and incorporates items that evaluate all nine DSM-IV depression criterion 
symptom domains including sad mood, concentration difficulties, self-criticism, suicidal 
ideation, loss of interest, energy/fatigue, sleep disturbances, appetite/weight changes, 
and psychomotor symptoms.

Clinical Applications:
- Screening for depression in primary care and specialty mental health settings
- Monitoring treatment response and symptom changes over time
- Clinical trial outcome measurement and research applications
- Treatment planning and adjustment based on specific symptom patterns
- Quality improvement initiatives in mental health care
- Training and educational purposes for depression assessment
- Telehealth and remote monitoring applications
- Integrated care and collaborative treatment models

QIDS-SR-16 Scoring Structure:
The QIDS-SR-16 employs a sophisticated scoring system that accounts for the heterogeneous 
nature of depression presentation:

Sleep Domain (Items 1-4):
- Falling asleep difficulty (sleep onset insomnia)
- Sleep maintenance problems (frequent nighttime awakenings)
- Early morning awakening (terminal insomnia)
- Hypersomnia (excessive sleep)
- Scoring: Only the highest score among these four items is counted

Appetite/Weight Domain (Items 6-9):
- Decreased appetite and food intake
- Increased appetite and overeating
- Weight loss (≥2 pounds or ≥5 pounds)
- Weight gain (≥2 pounds or ≥5 pounds)
- Scoring: Only the highest score among these four items is counted

Core Depression Symptoms (Items 5, 10-14):
- Sad mood (feelings of sadness and dysphoria)
- Concentration/decision making difficulties
- Self-view and feelings of guilt/worthlessness
- Suicidal ideation and thoughts of death
- General interest and anhedonia
- Energy level and fatigue

Psychomotor Symptoms (Items 15-16):
- Psychomotor retardation (feeling slowed down)
- Psychomotor agitation (feeling restless)
- Scoring: Only the highest score between these two items is counted

Severity Classification and Clinical Interpretation:
The QIDS-SR-16 total score ranges from 0-27 points with established severity thresholds:

No Depression (0-5 points):
- Absence of clinically significant depressive symptoms
- Normal mood and functioning within expected range
- Routine monitoring and wellness maintenance appropriate
- Focus on prevention and positive mental health strategies

Mild Depression (6-10 points):
- Subclinical or emerging depressive symptoms
- May benefit from psychosocial interventions and lifestyle modifications
- Consider supportive counseling and stress management techniques
- Monitor for progression and reassess within 2-4 weeks

Moderate Depression (11-15 points):
- Clinically significant depression requiring active treatment
- Evidence-based psychotherapy and/or medication evaluation indicated
- Monitor functional impairment and treatment response
- Consider combination treatments for optimal outcomes

Severe Depression (16-20 points):
- Significant depressive episode requiring intensive treatment
- Combination therapy (psychotherapy + medication) typically recommended
- Close monitoring for safety concerns and suicidal ideation
- May require psychiatric consultation and specialized care

Very Severe Depression (21-27 points):
- Severe depression with high risk for complications
- Immediate psychiatric evaluation and intensive treatment required
- High-risk monitoring with safety assessment protocols
- Consider hospitalization if safety concerns present

Psychometric Properties and Validation:
The QIDS-SR-16 demonstrates excellent psychometric characteristics:
- Internal consistency: Cronbach's α = 0.86-0.87 across diverse populations
- Concurrent validity: Strong correlations with IDS-SR-30 (r = 0.96-0.97) and HAM-D (r = 0.85-0.86)
- Sensitivity to change: Comparable to longer instruments for detecting treatment response
- Test-retest reliability: Stable over short periods in clinically stable patients
- Cross-cultural validity: Validated across multiple languages and cultural contexts

Clinical Implementation Guidelines:
- Administer as self-report questionnaire with clear instructions
- Ensure patient understands the 7-day assessment timeframe
- Review responses for consistency and completeness
- Pay special attention to suicidal ideation responses (Item 12)
- Use as part of comprehensive clinical assessment, not in isolation
- Consider cultural factors and language barriers in interpretation
- Document scores and track changes over time for treatment monitoring

Important Clinical Considerations:
- Suicidal ideation assessment: Item 12 scores ≥2 require immediate safety evaluation
- Sleep and appetite domains: Special scoring rules prevent double-counting symptoms
- Medical comorbidities: Consider physical health conditions affecting symptoms
- Medication effects: Some symptoms may be medication-related rather than depression
- Seasonal variations: Consider seasonal patterns in mood and sleep symptoms
- Substance use: Evaluate for comorbid substance use disorders affecting presentation

Treatment Planning and Monitoring:
- Baseline assessment before treatment initiation
- Regular monitoring every 2-4 weeks during active treatment
- Target remission defined as QIDS-SR-16 score <5
- Assess specific symptom clusters for targeted interventions
- Consider treatment modifications based on persistent symptom patterns
- Use for shared decision-making with patients about treatment options

The QIDS-SR-16 represents a highly efficient and clinically valuable tool for depression 
assessment, combining brevity with comprehensive symptom coverage to support evidence-based 
mental health care and improved patient outcomes through accurate assessment and monitoring.
"""

from pydantic import BaseModel, Field
from typing import Literal


class QidsSr16Request(BaseModel):
    """
    Request model for Quick Inventory of Depressive Symptomatology (QIDS-SR-16)
    
    The QIDS-SR-16 is a validated self-report instrument that assesses depressive symptom 
    severity over the past 7 days using 16 items covering all nine DSM-IV depression 
    criterion symptom domains. This comprehensive yet efficient tool provides reliable 
    assessment for screening, treatment monitoring, and research applications.
    
    Assessment Instructions:
    
    1. Timeframe: All items assess symptoms during the PAST 7 DAYS
    2. Scoring: Each item is rated from 0 (no symptoms) to 3 (severe symptoms)
    3. Self-Report: Patients complete independently with clear instructions
    4. Comprehensive: Covers all major depression symptom domains
    
    Special Scoring Rules:
    
    Sleep Domain (Items 1-4):
    - Only the HIGHEST score among sleep items is counted in total
    - Assesses different types of sleep disturbance common in depression
    - Prevents over-weighting of sleep symptoms in total score
    
    Appetite/Weight Domain (Items 6-9):
    - Only the HIGHEST score among appetite/weight items is counted
    - Accounts for both increased and decreased appetite/weight patterns
    - Reflects individual variation in depression presentation
    
    Psychomotor Domain (Items 15-16):
    - Only the HIGHEST score between agitation and retardation is counted
    - Recognizes that patients typically experience one predominant pattern
    
    Clinical Assessment Guidelines:
    
    Sleep Assessment (Items 1-4):
    - Consider typical sleep patterns before current episode
    - Account for environmental factors affecting sleep
    - Note any medications or substances affecting sleep
    - Distinguish depression-related from primary sleep disorders
    
    Mood and Cognitive Assessment (Items 5, 10-14):
    - Assess subjective mood states and emotional experience
    - Evaluate concentration and decision-making abilities
    - Monitor interest and pleasure in activities (anhedonia)
    - Assess energy levels and fatigue patterns
    
    Critical Safety Assessment (Item 12 - Suicidal Ideation):
    - Scores ≥2 require immediate safety evaluation
    - Document specific thoughts, plans, or intent
    - Implement appropriate safety protocols
    - Consider immediate psychiatric consultation if indicated
    
    Quality Assurance:
    - Ensure patient understands 7-day timeframe for all items
    - Review completed assessment for missing or unclear responses
    - Verify understanding of rating scale (0-3 for each item)
    - Consider cultural and linguistic factors in interpretation
    
    References: See module docstring for complete citation list.
    """
    
    sleep_onset: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Falling asleep difficulty over the past 7 days. 0=Never takes longer than 30 minutes, 1=Takes at least 30 minutes less than half the time, 2=Takes at least 30 minutes more than half the time, 3=Takes more than 60 minutes more than half the time.",
        example=1
    )
    
    sleep_maintenance: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Sleep during the night over the past 7 days. 0=Does not wake up at night, 1=Restless light sleep with few awakenings, 2=Wakes up at least once but goes back to sleep easily, 3=Awakens more than once and stays awake for 20+ minutes.",
        example=2
    )
    
    early_awakening: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Waking up too early over the past 7 days. 0=Less than half the time awakens ≤30 minutes before necessary, 1=More than half the time awakens >30 minutes before necessary, 2=Awakens ≥1 hour before necessary more than half the time, 3=Awakens ≥2 hours before necessary more than half the time.",
        example=0
    )
    
    hypersomnia: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Sleeping too much over the past 7 days. 0=Sleeps no longer than 7-8 hours/night without naps, 1=Sleeps no longer than 10 hours in 24-hour period, 2=Sleeps no longer than 12 hours in 24-hour period, 3=Sleeps longer than 12 hours in 24-hour period.",
        example=0
    )
    
    sad_mood: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Feeling sad over the past 7 days. 0=Does not feel sad, 1=Feels sad less than half the time, 2=Feels sad more than half the time, 3=Feels sad nearly all of the time.",
        example=2
    )
    
    appetite_decrease: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Decreased appetite over the past 7 days. 0=No change in usual appetite, 1=Eats somewhat less often or lesser amounts, 2=Eats much less than usual and only with personal effort, 3=Rarely eats within 24-hour period and only with extreme effort or persuasion.",
        example=1
    )
    
    appetite_increase: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Increased appetite over the past 7 days. 0=No change in usual appetite, 1=More frequently feels need to eat than usual, 2=Regularly eats more often and/or greater amounts than usual, 3=Feels driven to overeat both at mealtime and between meals.",
        example=0
    )
    
    weight_decrease: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Decreased weight over the past 7 days. 0=No change in weight, 1=Feels as if some slight weight loss, 2=Has lost 2 pounds or more, 3=Has lost 5 pounds or more.",
        example=0
    )
    
    weight_increase: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Increased weight over the past 7 days. 0=No change in weight, 1=Feels as if some slight weight gain, 2=Has gained 2 pounds or more, 3=Has gained 5 pounds or more.",
        example=0
    )
    
    concentration: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Concentration/decision making over the past 7 days. 0=No change in usual capacity to concentrate or make decisions, 1=Occasionally feels indecisive or notices attention wanders, 2=Most of the time struggles to focus attention or make decisions, 3=Cannot concentrate well enough to read or make even minor decisions.",
        example=2
    )
    
    self_view: Literal[0, 1, 2, 3] = Field(
        ...,
        description="View of myself over the past 7 days. 0=Sees self as equally worthwhile and deserving as others, 1=Is more self-blaming than usual, 2=Largely believes that he/she causes problems for others, 3=Thinks almost constantly about major and minor defects in self.",
        example=1
    )
    
    suicidal_ideation: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Thoughts of death or suicide over the past 7 days. 0=Does not think of suicide or death, 1=Feels that life is empty or wonders if it's worth living, 2=Thinks of suicide or death several times a week for several minutes, 3=Thinks of suicide or death several times a day in detail or has made specific plans or attempted suicide.",
        example=0
    )
    
    general_interest: Literal[0, 1, 2, 3] = Field(
        ...,
        description="General interest over the past 7 days. 0=No change from usual level of interest in people and activities, 1=Notices a reduction in former interests/activities, 2=Finds only one or two former interests remain, 3=Has virtually no interest in formerly pursued activities.",
        example=2
    )
    
    energy_level: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Energy level over the past 7 days. 0=No change in usual level of energy, 1=Tires more easily than usual, 2=Makes significant personal effort to initiate or maintain usual daily activities, 3=Unable to carry out most usual daily activities due to lack of energy.",
        example=2
    )
    
    psychomotor_slowing: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Feeling slowed down over the past 7 days. 0=Normal speed of thinking, gesturing, speaking, and moving, 1=Patient notes slowed thinking and voice tone or speech is slightly retarded, 2=Takes several seconds to respond to questions; reports slowed thinking, 3=Often does not respond to questions without repeated prompting.",
        example=1
    )
    
    psychomotor_agitation: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Feeling restless over the past 7 days. 0=No increased speed or disorganization in thinking or gesturing, 1=Fidgets, wrings hands, and shifts positions, 2=Describes impulse to move about and displays motor restlessness, 3=Unable to stay seated and paces about, or hands shake or tremble.",
        example=0
    )
    
    class Config:
        schema_extra = {
            "example": {
                "sleep_onset": 1,
                "sleep_maintenance": 2,
                "early_awakening": 0,
                "hypersomnia": 0,
                "sad_mood": 2,
                "appetite_decrease": 1,
                "appetite_increase": 0,
                "weight_decrease": 0,
                "weight_increase": 0,
                "concentration": 2,
                "self_view": 1,
                "suicidal_ideation": 0,
                "general_interest": 2,
                "energy_level": 2,
                "psychomotor_slowing": 1,
                "psychomotor_agitation": 0
            }
        }


class QidsSr16Response(BaseModel):
    """
    Response model for Quick Inventory of Depressive Symptomatology (QIDS-SR-16)
    
    The QIDS-SR-16 score provides evidence-based assessment of depression severity and 
    guides clinical decision-making for treatment planning, monitoring, and outcome 
    evaluation. Understanding score interpretation is essential for appropriate mental 
    health care and optimal patient outcomes.
    
    Score Interpretation and Clinical Management:
    
    No Depression (0-5 points):
    - Absence of clinically significant depressive symptoms
    - Normal mood state within expected variations
    - Routine wellness monitoring and prevention strategies appropriate
    - Focus on maintaining positive mental health and resilience factors
    - Continue healthy lifestyle practices and stress management
    - Regular check-ins at routine healthcare visits
    
    Mild Depression (6-10 points):
    - Subclinical or emerging depressive symptoms present
    - May benefit from early intervention and supportive approaches
    - Consider lifestyle modifications: exercise, sleep hygiene, stress reduction
    - Psychoeducation about depression and symptom monitoring
    - Brief supportive counseling or guided self-help interventions
    - Reassess in 2-4 weeks to monitor progression or improvement
    
    Moderate Depression (11-15 points):
    - Clinically significant depression requiring active treatment
    - Evidence-based psychotherapy recommended (CBT, IPT, behavioral activation)
    - Consider antidepressant medication evaluation, especially if psychotherapy alone insufficient
    - Monitor functional impairment and safety concerns regularly
    - Combination therapy may be optimal for many patients
    - Regular follow-up every 2-4 weeks initially to assess treatment response
    
    Severe Depression (16-20 points):
    - Significant major depressive episode requiring intensive treatment
    - Combination therapy (psychotherapy + medication) typically recommended
    - Close monitoring for safety concerns and suicidal ideation essential
    - Consider psychiatric consultation for complex cases or treatment resistance
    - Assess functional impairment and need for work/disability accommodations
    - May require more frequent appointments and intensive case management
    
    Very Severe Depression (21-27 points):
    - Severe depression with high risk for complications and safety concerns
    - Immediate psychiatric evaluation and intensive treatment required
    - Comprehensive safety assessment with suicide risk protocols
    - Consider hospitalization if imminent safety risk or severe impairment
    - Intensive case management with frequent monitoring and family involvement
    - May require specialty mental health services and coordinated care approach
    
    Treatment Planning and Monitoring:
    
    Psychotherapy Considerations:
    - Mild-Moderate: Consider CBT, IPT, behavioral activation, problem-solving therapy
    - Severe-Very Severe: Combination therapy typically superior to monotherapy
    - Consider therapy modality based on patient preferences and availability
    - Monitor therapy engagement and therapeutic alliance development
    
    Medication Considerations:
    - Moderate depression: Consider if psychotherapy insufficient or patient preference
    - Severe-Very Severe: Typically indicated as part of combination treatment
    - Consider patient factors: medical comorbidities, prior response, side effect profile
    - Monitor for treatment response, side effects, and adherence
    
    Safety Assessment and Monitoring:
    - Suicidal ideation (Item 12): Scores ≥2 require immediate comprehensive risk assessment
    - Develop safety planning for high-risk patients
    - Involve family/supports when appropriate and with patient consent
    - Consider environmental modifications to reduce access to lethal means
    
    Functional Assessment:
    - Evaluate impact on work, relationships, self-care, and daily activities
    - Consider need for workplace accommodations or disability support
    - Assess social support systems and strengthen as needed
    - Monitor improvement in functional domains as treatment progresses
    
    Follow-up and Monitoring Guidelines:
    - Baseline QIDS-SR-16 before treatment initiation
    - Regular monitoring every 2-4 weeks during active treatment phase
    - Target remission defined as QIDS-SR-16 score <5
    - Maintenance monitoring monthly to quarterly after achieving remission
    - Consider treatment modifications if inadequate response by 6-8 weeks
    
    Quality Assurance and Documentation:
    - Document QIDS-SR-16 scores and clinical interpretation in medical record
    - Track changes over time to assess treatment response and guide decisions
    - Consider patient-reported outcome measures for comprehensive assessment
    - Use standardized assessment to improve care quality and outcomes
    
    Limitations and Clinical Judgment:
    - QIDS-SR-16 is a screening and monitoring tool, not a diagnostic instrument
    - Clinical interview and comprehensive assessment required for diagnosis
    - Consider cultural factors, language barriers, and health literacy in interpretation
    - Integrate with other clinical information and patient-specific factors
    - Reassess if significant clinical changes or concerns arise between scheduled evaluations
    
    The QIDS-SR-16 enables evidence-based depression assessment that supports optimal 
    treatment planning, monitoring, and outcomes through systematic evaluation of symptom 
    severity and treatment response over time.
    
    Reference: See module docstring for complete citation list.
    """
    
    result: int = Field(
        ...,
        description="QIDS-SR-16 total score calculated using special scoring rules for sleep, appetite/weight, and psychomotor domains. Score ranges from 0 to 27 points, with higher scores indicating greater depression severity.",
        example=12
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the QIDS-SR-16 score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including depression severity level, treatment recommendations, monitoring guidelines, and safety considerations based on the calculated QIDS-SR-16 score.",
        example="Moderate depression. Clinically significant depressive symptoms requiring active treatment. Consider evidence-based psychotherapy (CBT, IPT, behavioral activation), medication evaluation with antidepressants, or combination treatment. Monitor for functional impairment, safety concerns, and treatment response. Reassess every 2-4 weeks initially."
    )
    
    stage: str = Field(
        ...,
        description="QIDS-SR-16 depression severity category (No Depression, Mild Depression, Moderate Depression, Severe Depression, or Very Severe Depression)",
        example="Moderate Depression"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the depression severity level associated with the calculated QIDS-SR-16 score",
        example="Moderate depression"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 12,
                "unit": "points",
                "interpretation": "Moderate depression. Clinically significant depressive symptoms requiring active treatment. Consider evidence-based psychotherapy (CBT, IPT, behavioral activation), medication evaluation with antidepressants, or combination treatment. Monitor for functional impairment, safety concerns, and treatment response. Reassess every 2-4 weeks initially.",
                "stage": "Moderate Depression",
                "stage_description": "Moderate depression"
            }
        }