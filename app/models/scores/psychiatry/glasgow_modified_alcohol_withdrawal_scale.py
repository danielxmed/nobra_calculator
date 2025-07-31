"""
Glasgow Modified Alcohol Withdrawal Scale (GMAWS) Models

Request and response models for Glasgow Modified Alcohol Withdrawal Scale calculation.

References (Vancouver style):
1. Sullivan JT, Sykora K, Schneiderman J, Naranjo CA, Sellers EM. Assessment of 
   alcohol withdrawal: the revised clinical institute withdrawal assessment for 
   alcohol scale (CIWA-Ar). Br J Addict. 1989;84(11):1353-1357.
2. Macleod AD, Peden NR, Pryde EA, Proctor SJ. Glasgow assessment and management 
   of alcohol guideline: an evidence-based guideline for the assessment and 
   management of patients with harmful alcohol use in acute medical units. 
   QJM. 2012;105(7):649-666. doi: 10.1093/qjmed/hcs070.
3. Ferguson C, O'Neill A, Hameed A, Kenny RA, O'Neill D. FAST alcohol screening 
   and the modified Glasgow alcoholic hepatitis score in the general hospital. 
   QJM. 2009;102(4):269-273. doi: 10.1093/qjmed/hcp004.

The Glasgow Modified Alcohol Withdrawal Scale (GMAWS) is a clinical assessment tool 
designed to evaluate and monitor the severity of alcohol withdrawal symptoms in 
hospitalized patients. It is a modified version of the Clinical Institute Withdrawal 
Assessment for Alcohol-Revised (CIWA-Ar) scale, adapted specifically for use in 
general hospital settings as part of the Glasgow Assessment and Management of 
Alcohol (GAMA) protocol.

Key Clinical Applications:
- Assessment of alcohol withdrawal syndrome severity
- Guide benzodiazepine dosing and administration frequency
- Monitor patient response to treatment interventions
- Identify patients at risk for severe complications (delirium tremens)
- Standardize alcohol withdrawal management across healthcare providers

The GMAWS evaluates five key clinical domains that are commonly affected in alcohol 
withdrawal syndrome. Each component is scored from 0-2 points, providing a total 
score range of 0-10 points. The scale is designed to be administered by trained 
healthcare professionals and should not be used in intoxicated patients (must be 
at least 8 hours since last alcohol consumption).

Clinical Context and Validation:
The GMAWS has been validated for use in general hospital settings and provides a 
systematic approach to alcohol withdrawal assessment that enables consistent evaluation 
across different healthcare providers. The scale helps standardize treatment protocols 
and ensures appropriate monitoring frequency based on symptom severity.
"""

from pydantic import BaseModel, Field
from typing import Literal


class GlasgowModifiedAlcoholWithdrawalScaleRequest(BaseModel):
    """
    Request model for Glasgow Modified Alcohol Withdrawal Scale (GMAWS)
    
    The GMAWS provides systematic assessment of alcohol withdrawal syndrome using 
    five clinical domains, each scored from 0-2 points. This standardized approach 
    enables consistent evaluation and appropriate treatment guidance across healthcare 
    settings and providers.
    
    **CLINICAL ASSESSMENT FRAMEWORK**:
    
    **Assessment Prerequisites**:
    - Patient must not be currently intoxicated
    - Minimum 8 hours since last alcohol consumption
    - Patient may need to be awakened for assessment
    - Consider co-existing medical conditions that may affect scoring
    
    **Component Assessment Methodology**:
    
    **Tremor Assessment (0-2 points)**:
    
    **Clinical Significance**: Objective measure of neurological hyperexcitability
    - **Neurophysiology**: Reflects enhanced sympathetic nervous system activity
    - **Assessment Method**: Observe tremor at rest and with arms extended
    - **Prognostic Value**: Severity correlates with withdrawal complications risk
    - **Clinical Context**: Most objective component of withdrawal assessment
    
    **Scoring Criteria**:
    
    **0 - None**:
    - **Assessment**: No visible tremor at rest or with arms extended
    - **Clinical Significance**: Normal neurological state, minimal withdrawal
    - **Monitoring Implications**: Lower risk of seizure or severe complications
    
    **1 - Present with arms extended**:
    - **Assessment**: Tremor visible only when patient extends arms forward
    - **Clinical Significance**: Mild neurological hyperexcitability
    - **Monitoring Implications**: Moderate withdrawal symptoms developing
    
    **2 - Present with arms at rest**:
    - **Assessment**: Tremor visible even when arms are at rest
    - **Clinical Significance**: Significant neurological hyperexcitability
    - **Monitoring Implications**: High risk for seizure activity and severe withdrawal
    
    **Sweating Assessment (0-2 points)**:
    
    **Clinical Significance**: Indicator of autonomic nervous system hyperactivity
    - **Pathophysiology**: Reflects sympathetic nervous system overactivity
    - **Assessment Method**: Visual inspection of skin moisture and diaphoresis
    - **Clinical Context**: Early sign of withdrawal progression
    - **Monitoring Value**: Correlates with cardiovascular instability risk
    
    **Scoring Criteria**:
    
    **0 - None**:
    - **Assessment**: Normal skin moisture, no diaphoresis
    - **Clinical Significance**: Minimal autonomic dysfunction
    - **Monitoring Implications**: Lower risk of hemodynamic instability
    
    **1 - Moist skin**:
    - **Assessment**: Skin feels moist to touch but no visible sweating
    - **Clinical Significance**: Mild autonomic hyperactivity
    - **Monitoring Implications**: Early withdrawal symptom development
    
    **2 - Drenching sweat**:
    - **Assessment**: Profuse sweating, visible diaphoresis
    - **Clinical Significance**: Severe autonomic hyperactivity
    - **Monitoring Implications**: High risk for cardiovascular complications
    
    **Hallucinations Assessment (0-2 points)**:
    
    **Clinical Significance**: Indicator of severe withdrawal and delirium tremens risk
    - **Pathophysiology**: Reflects CNS hyperexcitability and cortical dysfunction
    - **Assessment Method**: Direct questioning and behavioral observation
    - **Types**: Visual, auditory, tactile hallucinations may occur
    - **Clinical Context**: Most concerning symptom predicting severe complications
    
    **Scoring Criteria**:
    
    **0 - None**:
    - **Assessment**: No reported or observed hallucinations
    - **Clinical Significance**: No evidence of severe CNS dysfunction
    - **Risk Stratification**: Lower risk for delirium tremens
    
    **1 - Uncertain, or patient reports but not distressed**:
    - **Assessment**: Patient reports mild perceptual disturbances without distress
    - **Clinical Significance**: Early sign of CNS hyperexcitability
    - **Risk Stratification**: Moderate risk for progression to severe withdrawal
    
    **2 - Present and distressed**:
    - **Assessment**: Clear evidence of hallucinations causing patient distress
    - **Clinical Significance**: Severe CNS dysfunction, high delirium tremens risk
    - **Risk Stratification**: Immediate intervention required, ICU consideration
    
    **Orientation Assessment (0-2 points)**:
    
    **Clinical Significance**: Measure of cognitive function and delirium assessment
    - **Cognitive Domains**: Person, place, time orientation
    - **Assessment Method**: Direct questioning about identity, location, date/time
    - **Clinical Context**: Reflects severity of brain dysfunction
    - **Prognostic Value**: Disorientation predicts complicated withdrawal course
    
    **Scoring Criteria**:
    
    **0 - Oriented**:
    - **Assessment**: Correctly identifies person, place, and time
    - **Clinical Significance**: Preserved cognitive function
    - **Risk Stratification**: Lower risk for delirium development
    
    **1 - Uncertain or disoriented in one domain**:
    - **Assessment**: Confusion in one of three orientation domains
    - **Clinical Significance**: Mild cognitive impairment
    - **Risk Stratification**: Moderate risk for delirium progression
    
    **2 - Disoriented in ≥2 domains**:
    - **Assessment**: Confused about two or more orientation domains
    - **Clinical Significance**: Significant cognitive dysfunction, possible delirium
    - **Risk Stratification**: High risk for delirium tremens and complications
    
    **Agitation Assessment (0-2 points)**:
    
    **Clinical Significance**: Behavioral manifestation of withdrawal severity
    - **Pathophysiology**: Reflects CNS hyperexcitability and anxiety
    - **Assessment Method**: Observation of behavior and patient movement
    - **Clinical Context**: Correlates with treatment response and monitoring needs
    - **Safety Implications**: Severe agitation may require physical restraints
    
    **Scoring Criteria**:
    
    **0 - None**:
    - **Assessment**: Calm, cooperative, no restlessness
    - **Clinical Significance**: Minimal behavioral manifestation of withdrawal
    - **Management Implications**: Standard monitoring sufficient
    
    **1 - Anxious/restless**:
    - **Assessment**: Patient appears anxious, mild restlessness
    - **Clinical Significance**: Early behavioral signs of withdrawal
    - **Management Implications**: Increased monitoring, environmental modification
    
    **2 - Distressed or pacing**:
    - **Assessment**: Patient unable to sit still, pacing, highly agitated
    - **Clinical Significance**: Severe behavioral manifestation of withdrawal
    - **Management Implications**: Immediate intervention, possible restraints needed
    
    **CLINICAL ASSESSMENT GUIDELINES**:
    
    **Assessment Environment**:
    - **Setting**: Quiet, well-lit room with minimal external stimulation
    - **Timing**: Avoid assessment during medical procedures or medication effects
    - **Safety**: Ensure patient and staff safety during assessment
    - **Documentation**: Record exact time and circumstances of assessment
    
    **Assessment Limitations**:
    - **Medical Conditions**: Underlying neurological conditions may confound scoring
    - **Medication Effects**: Sedatives or other medications may mask symptoms
    - **Comorbidities**: Psychiatric conditions may overlap with withdrawal symptoms
    - **Physical Limitations**: Inability to follow commands may affect assessment
    
    References (Vancouver style):
    1. Sullivan JT, Sykora K, Schneiderman J, Naranjo CA, Sellers EM. Assessment of 
       alcohol withdrawal: the revised clinical institute withdrawal assessment for 
       alcohol scale (CIWA-Ar). Br J Addict. 1989;84(11):1353-1357.
    2. Macleod AD, Peden NR, Pryde EA, Proctor SJ. Glasgow assessment and management 
       of alcohol guideline: an evidence-based guideline for the assessment and 
       management of patients with harmful alcohol use in acute medical units. 
       QJM. 2012;105(7):649-666.
    3. Ferguson C, O'Neill A, Hameed A, Kenny RA, O'Neill D. FAST alcohol screening 
       and the modified Glasgow alcoholic hepatitis score in the general hospital. 
       QJM. 2009;102(4):269-273.
    """
    
    tremor: Literal[0, 1, 2] = Field(
        ...,
        description="Tremor assessment. 0=None, 1=Present with arms extended, 2=Present with arms at rest",
        example=0
    )
    
    sweating: Literal[0, 1, 2] = Field(
        ...,
        description="Sweating/diaphoresis assessment. 0=None, 1=Moist skin, 2=Drenching sweat",
        example=1
    )
    
    hallucinations: Literal[0, 1, 2] = Field(
        ...,
        description="Hallucinations assessment. 0=None, 1=Uncertain or patient reports but not distressed, 2=Present and distressed",
        example=0
    )
    
    orientation: Literal[0, 1, 2] = Field(
        ...,
        description="Orientation assessment. 0=Oriented, 1=Uncertain or disoriented in one domain, 2=Disoriented in ≥2 domains",
        example=0
    )
    
    agitation: Literal[0, 1, 2] = Field(
        ...,
        description="Agitation assessment. 0=None, 1=Anxious/restless, 2=Distressed or pacing",
        example=1
    )
    
    class Config:
        schema_extra = {
            "example": {
                "tremor": 0,
                "sweating": 1,
                "hallucinations": 0,
                "orientation": 0,
                "agitation": 1
            }
        }


class GlasgowModifiedAlcoholWithdrawalScaleResponse(BaseModel):
    """
    Response model for Glasgow Modified Alcohol Withdrawal Scale (GMAWS)
    
    The response provides the calculated GMAWS total score with comprehensive clinical 
    interpretation and evidence-based treatment recommendations based on validated 
    severity categories from clinical research and hospital implementation studies.
    
    **CLINICAL INTERPRETATION FRAMEWORK**:
    
    **GMAWS Score Validation and Clinical Significance**:
    - **Scoring Range**: 0-10 points combining five clinical domains
    - **Clinical Validation**: Validated in general hospital settings
    - **Treatment Guidance**: Directly linked to benzodiazepine dosing protocols
    - **Monitoring Frequency**: Score-based reassessment intervals
    
    **Severity Categories and Treatment Protocols**:
    
    **No Withdrawal (Score 0)**:
    - **Clinical Significance**: No active withdrawal symptoms present
    - **Treatment Protocol**: No benzodiazepines required
    - **Monitoring**: Reassess in 2 hours, continue supportive care
    - **Management Focus**: Prevention measures and vitamin supplementation
    
    **Mild Withdrawal (Scores 1-3)**:
    - **Clinical Significance**: Early withdrawal symptoms with low complication risk
    - **Treatment Protocol**: Diazepam 10mg PO or Lorazepam 2mg PO
    - **Monitoring**: Reassess in 2 hours, vital signs monitoring
    - **Management Focus**: Symptom control and progression prevention
    
    **Moderate to Severe Withdrawal (Scores 4-8)**:
    - **Clinical Significance**: Significant symptoms requiring immediate intervention
    - **Treatment Protocol**: Diazepam 20mg PO or Lorazepam 4mg PO
    - **Monitoring**: Reassess in 1 hour, close monitoring required
    - **Management Focus**: Aggressive symptom control, complication prevention
    
    **Severe Withdrawal (Scores 9-10)**:
    - **Clinical Significance**: Life-threatening withdrawal with high complication risk
    - **Treatment Protocol**: Diazepam 20mg PO/IV or Lorazepam 4mg PO/IV
    - **Monitoring**: Reassess in 1 hour, consider ICU-level care
    - **Management Focus**: Intensive monitoring, prevention of delirium tremens
    
    **EVIDENCE-BASED TREATMENT PROTOCOLS**:
    
    **Pharmacological Management by Severity**:
    
    **First-Line Medications**:
    - **Diazepam**: Long half-life, preferred for most patients
    - **Lorazepam**: Preferred for hepatic impairment or elderly patients
    - **Route Selection**: Oral preferred, IV for severe cases or inability to take PO
    
    **Monitoring and Assessment Protocols**:
    - **Vital Signs**: Blood pressure, heart rate, temperature, respiratory rate
    - **Neurological Assessment**: Level of consciousness, seizure monitoring
    - **Fluid Balance**: Hydration status, electrolyte monitoring
    - **Safety Measures**: Fall risk assessment, restraint considerations
    
    **Supportive Care Interventions**:
    
    **Nutritional Support**:
    - **Thiamine**: 100mg IV/PO daily for Wernicke's encephalopathy prevention
    - **Multivitamins**: IV formulation for severe cases
    - **Hydration**: Adequate fluid replacement, electrolyte correction
    - **Nutrition**: Nutritional assessment and supplementation as needed
    
    **Environmental Management**:
    - **Quiet Environment**: Minimize external stimulation
    - **Lighting**: Adequate lighting to prevent disorientation
    - **Safety**: Remove potentially harmful objects
    - **Comfort Measures**: Temperature control, positioning
    
    **COMPLICATION PREVENTION AND MANAGEMENT**:
    
    **High-Risk Indicators**:
    - **GMAWS ≥8 persisting >1 hour**: Urgent medical evaluation required
    - **Seizure Activity**: Immediate intervention and neurological consultation
    - **Cardiovascular Instability**: Hemodynamic monitoring and support
    - **Hyperthermia**: Aggressive cooling measures and close monitoring
    
    **Escalation Criteria**:
    - **ICU Transfer**: Severe withdrawal, hemodynamic instability, seizures
    - **Specialist Consultation**: Psychiatry, addiction medicine, neurology
    - **Additional Interventions**: Mechanical ventilation, invasive monitoring
    
    **QUALITY IMPROVEMENT AND DOCUMENTATION**:
    
    **Documentation Requirements**:
    - **Component Scores**: Record individual domain scores
    - **Time Stamps**: Exact assessment times for trend analysis
    - **Interventions**: Medications given, doses, routes, timing
    - **Response**: Patient response to treatment interventions
    
    **Performance Metrics**:
    - **Assessment Frequency**: Adherence to reassessment intervals
    - **Treatment Response**: Time to symptom improvement
    - **Complication Rates**: Seizures, delirium tremens, ICU admissions
    - **Length of Stay**: Treatment duration and discharge planning
    
    Reference: Macleod AD, et al. QJM. 2012;105(7):649-666.
    """
    
    result: int = Field(
        ...,
        description="Total GMAWS score calculated from five clinical components (0-10 points)",
        ge=0,
        le=10,
        example=2
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for GMAWS score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation with severity assessment and evidence-based treatment recommendations",
        example="GMAWS Score: 2/10. [Tremor: None, Sweating: Moist skin, Hallucinations: None, Orientation: Oriented, Agitation: Anxious/restless]. Mild alcohol withdrawal symptoms present. Administer Diazepam 10mg PO or Lorazepam 2mg PO as first-line treatment. Reassess with GMAWS in 2 hours. Monitor vital signs and provide supportive care. Ensure thiamine supplementation (100mg IV/PO daily). Maintain adequate hydration and electrolyte balance. Consider environmental modifications (quiet room, minimal stimulation)."
    )
    
    stage: str = Field(
        ...,
        description="Severity category based on GMAWS score (No Withdrawal, Mild Withdrawal, Moderate to Severe Withdrawal, Severe Withdrawal)",
        example="Mild Withdrawal"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of withdrawal severity level",
        example="Mild alcohol withdrawal symptoms"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 2,
                "unit": "points",
                "interpretation": "GMAWS Score: 2/10. [Tremor: None, Sweating: Moist skin, Hallucinations: None, Orientation: Oriented, Agitation: Anxious/restless]. Mild alcohol withdrawal symptoms present. Administer Diazepam 10mg PO or Lorazepam 2mg PO as first-line treatment. Reassess with GMAWS in 2 hours. Monitor vital signs and provide supportive care. Ensure thiamine supplementation (100mg IV/PO daily). Maintain adequate hydration and electrolyte balance. Consider environmental modifications (quiet room, minimal stimulation).",
                "stage": "Mild Withdrawal",
                "stage_description": "Mild alcohol withdrawal symptoms"
            }
        }