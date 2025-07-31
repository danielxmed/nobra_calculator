"""
CIWA-Ar for Alcohol Withdrawal Models

Request and response models for CIWA-Ar alcohol withdrawal assessment calculation.

References (Vancouver style):
1. Sullivan JT, Sykora K, Schneiderman J, Naranjo CA, Sellers EM. Assessment of alcohol 
   withdrawal: the revised clinical institute withdrawal assessment for alcohol scale 
   (CIWA-Ar). Br J Addict. 1989 Nov;84(11):1353-7.
2. Mayo-Smith MF, Beecher LH, Fischer TL, Gorelick DA, Guillaume JL, Hill A, et al. 
   Management of alcohol withdrawal delirium. An evidence-based practice guideline. 
   Arch Intern Med. 2004 Jul 12;164(13):1405-12.
3. Holbrook AM, Crowther R, Lotter A, Cheng C, King D. Meta-analysis of benzodiazepine 
   use in the treatment of acute alcohol withdrawal. CMAJ. 1999 Mar 23;160(6):649-55.

The Clinical Institute Withdrawal Assessment for Alcohol, Revised (CIWA-Ar) is a 
validated 10-item assessment tool designed to quantify the severity of alcohol 
withdrawal symptoms and guide evidence-based treatment decisions. This scale 
provides objective measurement of withdrawal severity, enabling healthcare providers 
to implement appropriate interventions and prevent potentially life-threatening 
complications such as delirium tremens and withdrawal seizures.

Clinical Background and Development:

The CIWA-Ar was developed as a revision of the original 15-item Clinical Institute 
Withdrawal Assessment (CIWA), reducing the number of assessment items to 10 while 
maintaining clinical validity and reliability. This streamlined version can be 
completed in less than 5 minutes, making it practical for frequent monitoring 
during acute withdrawal management.

Development and Validation:
The CIWA-Ar has been extensively validated in multiple clinical settings and has 
become the gold standard for alcohol withdrawal assessment. The scale demonstrates 
high inter-rater reliability and correlates well with clinical outcomes, including 
the need for medication intervention and risk of complications.

Ten-Component Assessment Framework:

1. Nausea and Vomiting (0-7 points):
This component assesses gastrointestinal symptoms commonly associated with alcohol 
withdrawal, ranging from no symptoms to constant nausea with frequent vomiting.

Clinical Assessment:
- 0: No nausea or vomiting
- 1: Mild nausea with no vomiting
- 4: Intermittent nausea with dry heaves
- 7: Constant nausea, frequent dry heaves and vomiting

Clinical Significance:
Gastrointestinal symptoms are often among the earliest signs of alcohol withdrawal 
and can contribute to dehydration and electrolyte imbalances if severe.

2. Tremor (0-7 points):
Tremor assessment evaluates both resting and postural tremor, which is one of the 
most characteristic signs of alcohol withdrawal.

Clinical Assessment:
- 0: No tremor
- 1: Not visible, but can be felt fingertip to fingertip
- 4: Moderate tremor with patient's arms extended
- 7: Severe tremor even with arms not extended

Clinical Significance:
Tremor intensity often correlates with overall withdrawal severity and responds well 
to benzodiazepine treatment.

3. Paroxysmal Sweats (0-7 points):
This component evaluates autonomic nervous system hyperactivity through assessment 
of diaphoresis and sweating patterns.

Clinical Assessment:
- 0: No sweat visible
- 1: Barely perceptible sweating, palms moist
- 4: Beads of sweat obvious on forehead
- 7: Drenching sweats

Clinical Significance:
Sweating reflects autonomic instability and may indicate increased risk for 
cardiovascular complications during withdrawal.

4. Anxiety (0-7 points):
Anxiety assessment evaluates the psychological distress associated with alcohol 
withdrawal, ranging from calm to panic-level anxiety.

Clinical Assessment:
- 0: None, at ease
- 1: Mildly anxious
- 4: Moderately anxious or guarded
- 7: Equivalent to acute panic states

Clinical Significance:
Anxiety is a central component of withdrawal and may persist longer than physical 
symptoms, requiring continued monitoring and treatment.

5. Agitation (0-7 points):
This component assesses motor restlessness and behavioral agitation that commonly 
accompanies alcohol withdrawal.

Clinical Assessment:
- 0: Normal activity
- 1: Somewhat more than normal activity
- 4: Moderately fidgety and restless
- 7: Paces or constantly thrashes about

Clinical Significance:
Agitation increases risk for injury and may interfere with medical care. High 
scores indicate need for closer monitoring and environmental modifications.

6. Tactile Disturbances (0-7 points):
This component evaluates abnormal tactile sensations that may progress to tactile 
hallucinations in severe withdrawal.

Clinical Assessment:
- 0: None
- 1-3: Mild to moderate itching, pins and needles, burning, or numbness
- 4-6: Hallucinations of increasing severity
- 7: Continuous hallucinations

Clinical Significance:
Tactile disturbances may be early indicators of progression toward delirium tremens 
and require careful monitoring.

7. Auditory Disturbances (0-7 points):
Assessment of auditory hypersensitivity and potential auditory hallucinations, 
which can be distressing and indicate severe withdrawal.

Clinical Assessment:
- 0: Not present
- 1-3: Mild to moderate harshness or sounds that frighten
- 4-6: Hallucinations of increasing severity
- 7: Continuous hallucinations

Clinical Significance:
Auditory disturbances, particularly hallucinations, are associated with increased 
risk for delirium tremens and require immediate attention.

8. Visual Disturbances (0-7 points):
This component evaluates visual hypersensitivity and potential visual hallucinations, 
which are particularly concerning withdrawal symptoms.

Clinical Assessment:
- 0: Not present
- 1-3: Mild to moderate light sensitivity
- 4-6: Hallucinations of increasing severity
- 7: Continuous hallucinations

Clinical Significance:
Visual hallucinations are strongly associated with delirium tremens and indicate 
the need for aggressive treatment and intensive monitoring.

9. Headache and Fullness in Head (0-7 points):
Assessment of cephalic symptoms commonly associated with alcohol withdrawal, ranging 
from absent to extremely severe.

Clinical Assessment:
- 0: Not present
- 1: Very mild
- 4: Moderately severe
- 7: Extremely severe

Clinical Significance:
Headache often accompanies other withdrawal symptoms and may indicate increased 
intracranial pressure or vascular changes associated with withdrawal.

10. Orientation and Clouding of Sensorium (0-4 points):
This component assesses cognitive function and level of consciousness, which are 
critical indicators of withdrawal severity and delirium risk.

Clinical Assessment:
- 0: Oriented and can do serial additions
- 1: Cannot do serial additions or uncertain about date
- 2: Disoriented for date by no more than 2 calendar days
- 3: Disoriented for date by more than 2 calendar days
- 4: Disoriented for place and/or person

Clinical Significance:
Cognitive impairment and disorientation are key features of delirium tremens and 
require immediate intensive treatment.

Scoring and Clinical Decision Making:

Score Interpretation and Risk Stratification:

Minimal Withdrawal (0-8 points):
- Clinical significance: Absent or minimal withdrawal symptoms
- Treatment approach: Usually no pharmacological intervention required
- Monitoring: Every 4-8 hours
- Risk level: Low risk for complications
- Management: Supportive care, hydration, thiamine supplementation

Mild to Moderate Withdrawal (9-19 points):
- Clinical significance: Mild to moderate withdrawal symptoms
- Treatment approach: Consider symptom-triggered benzodiazepine therapy
- Monitoring: Every 1-2 hours
- Risk level: Moderate risk requiring close monitoring
- Management: Lorazepam 1-2mg PO/IV q1-2h PRN based on symptoms

Severe Withdrawal (≥20 points):
- Clinical significance: Severe withdrawal with high risk for complications
- Treatment approach: Aggressive benzodiazepine treatment required
- Monitoring: Continuous monitoring, consider ICU placement
- Risk level: High risk for delirium tremens and seizures
- Management: Lorazepam 2-4mg IV q15-30min PRN, intensive monitoring

Clinical Implementation and Best Practices:

Assessment Frequency:
- Initial assessment upon admission or recognition of withdrawal risk
- Repeat every 1-2 hours during active withdrawal
- Continue until scores consistently <8-10 for 24 hours
- More frequent assessment (every 15-30 minutes) for severe cases

Treatment Protocols:
The CIWA-Ar is most effective when used with symptom-triggered treatment protocols 
rather than fixed-schedule dosing. This approach has been shown to:
- Reduce total benzodiazepine requirements
- Decrease length of stay
- Minimize oversedation in mild cases
- Provide more appropriate treatment for severe cases

Quality Assurance:
- Ensure staff training on proper assessment techniques
- Regular inter-rater reliability checks
- Documentation of all scores and corresponding interventions
- Correlation of scores with clinical outcomes

Limitations and Considerations:

Patient Population Limitations:
- Not suitable for intubated or heavily sedated patients
- Requires patient cooperation and communication ability
- May be less reliable in patients with cognitive impairment
- Not validated in pediatric populations

Clinical Judgment Integration:
- CIWA-Ar scores should supplement, not replace, clinical judgment
- Consider patient's medical history, comorbidities, and social factors
- Account for medications that may mask or exacerbate symptoms
- Recognize that some patients may require treatment at lower scores

Comorbidity Considerations:
- Patients with liver disease may have altered drug metabolism
- Cardiac conditions may affect choice of sedating medications
- Psychiatric comorbidities may complicate assessment and treatment
- Concurrent substance use may modify withdrawal presentation

The CIWA-Ar for Alcohol Withdrawal represents an essential tool for evidence-based 
alcohol withdrawal management, providing objective assessment criteria that guide 
appropriate treatment while minimizing both under-treatment and over-sedation risks. 
When properly implemented with trained staff and appropriate protocols, the CIWA-Ar 
significantly improves patient safety and clinical outcomes in alcohol withdrawal 
management.
"""

from pydantic import BaseModel, Field
from typing import Dict, Any


class CiwaArAlcoholWithdrawalRequest(BaseModel):
    """
    Request model for CIWA-Ar Alcohol Withdrawal Assessment
    
    The Clinical Institute Withdrawal Assessment for Alcohol, Revised (CIWA-Ar) is a 
    validated 10-component assessment tool designed to quantify alcohol withdrawal 
    severity and guide evidence-based treatment decisions. This assessment takes less 
    than 5 minutes to complete and should be performed every 1-2 hours during active 
    withdrawal management.
    
    Assessment Component Scoring Guidelines:
    
    Nausea and Vomiting (0-7 points):
    Assess gastrointestinal symptoms associated with withdrawal:
    - 0: No nausea or vomiting present
    - 1: Mild nausea with no vomiting episodes
    - 4: Intermittent nausea with dry heaves
    - 7: Constant nausea with frequent dry heaves and vomiting
    
    Tremor (0-7 points):
    Evaluate both resting and postural tremor severity:
    - 0: No tremor observable or palpable
    - 1: Not visible but can be felt fingertip to fingertip
    - 4: Moderate tremor with patient's arms extended
    - 7: Severe tremor even with arms not extended
    
    Paroxysmal Sweats (0-7 points):
    Assess autonomic hyperactivity through sweating patterns:
    - 0: No sweat visible on examination
    - 1: Barely perceptible sweating, palms moist
    - 4: Beads of sweat obvious on forehead
    - 7: Drenching sweats requiring clothing changes
    
    Anxiety (0-7 points):
    Evaluate psychological distress and anxiety level:
    - 0: No anxiety, patient appears at ease
    - 1: Mildly anxious but manageable
    - 4: Moderately anxious or guarded behavior
    - 7: Equivalent to acute panic states or severe agitation
    
    Agitation (0-7 points):
    Assess motor restlessness and behavioral agitation:
    - 0: Normal activity level and behavior
    - 1: Somewhat more active than normal
    - 4: Moderately fidgety and restless
    - 7: Paces back and forth or constantly thrashes about
    
    Tactile Disturbances (0-7 points):
    Evaluate abnormal tactile sensations and potential hallucinations:
    - 0: No abnormal tactile sensations
    - 1-3: Mild to moderate itching, pins and needles, burning, or numbness
    - 4-6: Tactile hallucinations of increasing severity
    - 7: Continuous tactile hallucinations
    
    Auditory Disturbances (0-7 points):
    Assess auditory hypersensitivity and potential hallucinations:
    - 0: No auditory disturbances present
    - 1-3: Mild to moderate harshness or sounds that disturb or frighten
    - 4-6: Auditory hallucinations of increasing severity
    - 7: Continuous auditory hallucinations
    
    Visual Disturbances (0-7 points):
    Evaluate visual hypersensitivity and potential hallucinations:
    - 0: No visual disturbances present
    - 1-3: Mild to moderate light sensitivity
    - 4-6: Visual hallucinations of increasing severity
    - 7: Continuous visual hallucinations
    
    Headache and Fullness in Head (0-7 points):
    Assess cephalic symptoms associated with withdrawal:
    - 0: No headache or head discomfort
    - 1: Very mild headache or head discomfort
    - 4: Moderately severe headache
    - 7: Extremely severe headache
    
    Orientation and Clouding of Sensorium (0-4 points):
    Evaluate cognitive function and level of consciousness:
    - 0: Oriented to person, place, time; can do serial additions
    - 1: Cannot do serial additions or uncertain about date
    - 2: Disoriented for date by no more than 2 calendar days
    - 3: Disoriented for date by more than 2 calendar days
    - 4: Disoriented for place and/or person
    
    Clinical Assessment Guidelines:
    
    Timing and Frequency:
    - Perform initial assessment upon recognition of withdrawal risk
    - Repeat every 1-2 hours during active withdrawal
    - Continue until scores consistently <8-10 for 24 hours
    - More frequent assessment (q15-30 minutes) for severe cases
    
    Patient Requirements:
    - Patient must be alert enough to participate in assessment
    - Not suitable for intubated or heavily sedated patients
    - Requires verbal communication and cooperation
    - Should be performed in quiet, well-lit environment
    
    Assessment Technique:
    - Observe patient behavior during routine interactions
    - Ask specific questions about symptoms patient is experiencing
    - Perform brief cognitive assessment for orientation component
    - Document exact score for each component with time stamp
    
    References (Vancouver style):
    1. Sullivan JT, Sykora K, Schneiderman J, Naranjo CA, Sellers EM. Assessment of alcohol 
    withdrawal: the revised clinical institute withdrawal assessment for alcohol scale 
    (CIWA-Ar). Br J Addict. 1989 Nov;84(11):1353-7.
    2. Mayo-Smith MF, Beecher LH, Fischer TL, Gorelick DA, Guillaume JL, Hill A, et al. 
    Management of alcohol withdrawal delirium. An evidence-based practice guideline. 
    Arch Intern Med. 2004 Jul 12;164(13):1405-12.
    """
    
    nausea_vomiting: int = Field(
        ...,
        ge=0,
        le=7,
        description="Nausea and vomiting severity. 0=None, 1=Mild nausea no vomiting, 4=Intermittent nausea with dry heaves, 7=Constant nausea frequent vomiting",
        example=2
    )
    
    tremor: int = Field(
        ...,
        ge=0,
        le=7,
        description="Tremor severity. 0=No tremor, 1=Not visible but felt fingertip to fingertip, 4=Moderate with arms extended, 7=Severe even arms not extended",
        example=3
    )
    
    paroxysmal_sweats: int = Field(
        ...,
        ge=0,
        le=7,
        description="Sweating severity. 0=No sweat visible, 1=Barely perceptible palms moist, 4=Beads of sweat on forehead, 7=Drenching sweats",
        example=2
    )
    
    anxiety: int = Field(
        ...,
        ge=0,
        le=7,
        description="Anxiety level. 0=None at ease, 1=Mildly anxious, 4=Moderately anxious or guarded, 7=Equivalent to acute panic states",
        example=4
    )
    
    agitation: int = Field(
        ...,
        ge=0,
        le=7,
        description="Agitation level. 0=Normal activity, 1=Somewhat more than normal, 4=Moderately fidgety restless, 7=Paces constantly thrashes about",
        example=3
    )
    
    tactile_disturbances: int = Field(
        ...,
        ge=0,
        le=7,
        description="Tactile disturbances. 0=None, 1-3=Mild to moderate itching/tingling, 4-6=Tactile hallucinations increasing severity, 7=Continuous hallucinations",
        example=1
    )
    
    auditory_disturbances: int = Field(
        ...,
        ge=0,
        le=7,
        description="Auditory disturbances. 0=Not present, 1-3=Mild to moderate sounds that frighten, 4-6=Auditory hallucinations increasing, 7=Continuous hallucinations",
        example=0
    )
    
    visual_disturbances: int = Field(
        ...,
        ge=0,
        le=7,
        description="Visual disturbances. 0=Not present, 1-3=Mild to moderate light sensitivity, 4-6=Visual hallucinations increasing, 7=Continuous hallucinations",
        example=1
    )
    
    headache: int = Field(
        ...,
        ge=0,
        le=7,
        description="Headache fullness in head. 0=Not present, 1=Very mild, 4=Moderately severe, 7=Extremely severe",
        example=3
    )
    
    orientation: int = Field(
        ...,
        ge=0,
        le=4,
        description="Orientation clouding of sensorium. 0=Oriented can do serial additions, 1=Cannot do serial additions, 2=Disoriented date ≤2 days, 3=Disoriented date >2 days, 4=Disoriented place/person",
        example=0
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "nausea_vomiting": 2,
                "tremor": 3,
                "paroxysmal_sweats": 2,
                "anxiety": 4,
                "agitation": 3,
                "tactile_disturbances": 1,
                "auditory_disturbances": 0,
                "visual_disturbances": 1,
                "headache": 3,
                "orientation": 0
            }
        }


class CiwaArAlcoholWithdrawalResponse(BaseModel):
    """
    Response model for CIWA-Ar Alcohol Withdrawal Assessment
    
    The CIWA-Ar response provides comprehensive withdrawal severity assessment with 
    evidence-based treatment recommendations to guide clinical decision-making. The 
    total score ranges from 0-67 points and is categorized into three severity levels 
    that correspond to specific treatment protocols and monitoring requirements.
    
    Scoring Interpretation and Clinical Management:
    
    Minimal Withdrawal (0-8 points): Absent or Minimal Symptoms
    
    Clinical Characteristics:
    - No significant withdrawal symptoms present
    - Patient appears comfortable and stable
    - Vital signs typically within normal limits
    - No evidence of autonomic instability
    - Cognitive function intact
    
    Treatment Approach:
    - Usually no pharmacological intervention required
    - Focus on supportive care and comfort measures
    - Ensure adequate hydration and nutrition
    - Thiamine 100mg daily for all patients
    - Folate supplementation as indicated
    
    Monitoring Requirements:
    - Assess CIWA-Ar score every 4-8 hours
    - Monitor vital signs per routine protocols
    - Continue assessment until patient stable for 24 hours
    - Watch for symptom progression
    
    Mild to Moderate Withdrawal (9-19 points): Symptomatic Requiring Treatment
    
    Clinical Characteristics:
    - Moderate withdrawal symptoms present
    - Patient experiences discomfort but remains stable
    - May have mild autonomic symptoms
    - Anxiety and agitation manageable
    - Cognitive function may be mildly impaired
    
    Treatment Approach:
    - Symptom-triggered benzodiazepine therapy preferred
    - Typical initial dose: Lorazepam 1-2mg PO/IV q1-2h PRN
    - Titrate based on symptom response and CIWA-Ar scores
    - Target score reduction to <8-10 consistently
    - Consider standing doses if frequent PRN dosing required
    
    Monitoring Requirements:
    - Assess CIWA-Ar score every 1-2 hours
    - Monitor vital signs every 2-4 hours
    - Watch for symptom progression or improvement
    - Assess response to medication interventions
    - Document all medication administration and effects
    
    Severe Withdrawal (≥20 points): High Risk for Complications
    
    Clinical Characteristics:
    - Severe withdrawal symptoms with high complication risk
    - Significant autonomic instability present
    - High risk for delirium tremens and seizures
    - May have hallucinations or severe agitation
    - Cognitive impairment likely present
    
    Treatment Approach:
    - Aggressive benzodiazepine treatment required immediately
    - Typical dose: Lorazepam 2-4mg IV q15-30min PRN
    - May require continuous IV infusion for refractory cases
    - Consider adjunctive medications (phenobarbital, propofol)
    - ICU-level monitoring often required
    
    Monitoring Requirements:
    - Continuous monitoring with frequent vital signs
    - CIWA-Ar assessment every 15-30 minutes initially
    - Neurological checks for seizure activity
    - Cardiovascular monitoring for arrhythmias
    - Strict input/output monitoring
    
    Evidence-Based Treatment Benefits:
    
    Symptom-Triggered Therapy Advantages:
    - Reduces total benzodiazepine requirements compared to fixed dosing
    - Decreases length of hospital stay
    - Minimizes oversedation in patients with milder symptoms
    - Provides more appropriate treatment for severe cases
    - Improves patient comfort and satisfaction scores
    
    CIWA-Ar Protocol Outcomes:
    - Decreased incidence of delirium tremens when properly implemented
    - Reduced mortality rates compared to clinical judgment alone
    - Lower rates of oversedation and associated complications
    - More efficient use of healthcare resources
    - Improved nursing confidence in withdrawal management
    
    Clinical Decision Support Features:
    
    Risk Stratification:
    - Objective assessment eliminates subjective variations
    - Standardized criteria for medication administration
    - Clear thresholds for escalation of care
    - Documented rationale for treatment decisions
    
    Quality Assurance:
    - Reproducible assessments between providers
    - Audit trail for quality improvement initiatives
    - Standardized documentation for regulatory compliance
    - Training tool for new staff members
    
    Implementation Considerations:
    
    Staff Training Requirements:
    - Proper assessment technique education
    - Inter-rater reliability verification
    - Understanding of scoring criteria and thresholds
    - Knowledge of treatment protocols and medication management
    
    Protocol Integration:
    - Integration with existing alcohol withdrawal order sets
    - Clear medication administration protocols
    - Escalation criteria for physician notification
    - Documentation requirements and legal considerations
    
    Special Populations and Modifications:
    
    Elderly Patients:
    - May require lower medication doses
    - Increased fall risk with sedating medications
    - Higher risk for delirium and cognitive impairment
    - Consider comorbid medical conditions
    
    Patients with Liver Disease:
    - Altered drug metabolism may prolong effects
    - Increased risk for hepatic encephalopathy
    - May require dose adjustments or alternative medications
    - Monitor liver function tests regularly
    
    Pregnant Patients:
    - Specialized protocols required for maternal-fetal safety
    - Consultation with maternal-fetal medicine recommended
    - Modified medication choices and dosing
    - Enhanced monitoring requirements
    
    Limitations and Clinical Judgment:
    
    Assessment Limitations:
    - Not suitable for intubated or heavily sedated patients
    - Requires patient cooperation and communication ability
    - May be less reliable in cognitive impairment
    - Cultural and language barriers may affect accuracy
    
    Clinical Integration:
    - CIWA-Ar should supplement, not replace, clinical judgment
    - Consider patient medical history and comorbidities
    - Account for concurrent medications and substances
    - Individualize treatment based on patient response
    
    The CIWA-Ar for Alcohol Withdrawal provides essential objective assessment criteria 
    that enable evidence-based treatment decisions while minimizing both under-treatment 
    and over-sedation risks. When properly implemented with appropriate training and 
    protocols, the CIWA-Ar significantly improves patient safety and clinical outcomes 
    in alcohol withdrawal management.
    
    Reference: Sullivan JT, et al. Br J Addict. 1989;84(11):1353-7.
    """
    
    result: int = Field(
        ...,
        ge=0,
        le=67,
        description="Total CIWA-Ar score calculated from all 10 components (0-67 points)",
        example=19
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with severity assessment and treatment recommendations",
        example="CIWA-Ar Score 19: Mild to moderate withdrawal symptoms. Consider symptom-triggered benzodiazepine therapy. Monitor every 1-2 hours. Typical dose: lorazepam 1-2mg PO/IV q1-2h PRN."
    )
    
    stage: str = Field(
        ...,
        description="Withdrawal severity category (Minimal, Mild to Moderate, Severe)",
        example="Mild to Moderate"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the withdrawal severity stage",
        example="Mild to moderate withdrawal"
    )
    
    scoring_breakdown: Dict[str, Any] = Field(
        ...,
        description="Detailed breakdown of component scores, treatment recommendations, and clinical context",
        example={
            "component_scores": {
                "nausea_vomiting": {
                    "name": "Nausea and Vomiting",
                    "score": 2,
                    "max_score": 7,
                    "description": "",
                    "clinical_significance": "GI symptoms often early sign of withdrawal - Mild symptoms present"
                },
                "tremor": {
                    "name": "Tremor",
                    "score": 3,
                    "max_score": 7,
                    "description": "",
                    "clinical_significance": "Classic withdrawal sign, often most noticeable - Mild symptoms present"
                }
            },
            "score_summary": {
                "total_score": 19,
                "max_possible_score": 67,
                "severity_category": "Mild to moderate withdrawal",
                "risk_level": "Moderate risk, requires monitoring"
            },
            "treatment_recommendations": {
                "score_range": "9-19",
                "medication": "Consider benzodiazepines (lorazepam 1-2mg PO/IV q1-2h PRN)",
                "monitoring": "Monitor every 1-2 hours",
                "considerations": "Symptom-triggered therapy preferred"
            }
        }
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 19,
                "unit": "points",
                "interpretation": "CIWA-Ar Score 19: Mild to moderate withdrawal symptoms. Consider symptom-triggered benzodiazepine therapy. Monitor every 1-2 hours. Typical dose: lorazepam 1-2mg PO/IV q1-2h PRN.",
                "stage": "Mild to Moderate",
                "stage_description": "Mild to moderate withdrawal",
                "scoring_breakdown": {
                    "component_scores": {
                        "nausea_vomiting": {
                            "name": "Nausea and Vomiting",
                            "score": 2,
                            "max_score": 7,
                            "clinical_significance": "GI symptoms often early sign of withdrawal - Mild symptoms present"
                        }
                    },
                    "score_summary": {
                        "total_score": 19,
                        "max_possible_score": 67,
                        "severity_category": "Mild to moderate withdrawal"
                    }
                }
            }
        }