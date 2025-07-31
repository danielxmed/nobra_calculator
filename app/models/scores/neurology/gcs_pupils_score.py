"""
GCS-Pupils Score Models

Request and response models for GCS-Pupils Score calculation in traumatic brain injury.

References (Vancouver style):
1. Brennan PM, Murray GD, Teasdale GM. Simplifying the use of prognostic information in traumatic 
   brain injury. Part 1: The GCS-Pupils score: an extended index of clinical severity. 
   J Neurosurg. 2018;128(6):1612-1620. doi: 10.3171/2017.12.JNS172780.
2. Teasdale G, Maas A, Lecky F, et al. The Glasgow Coma Scale at 40 years: standing the test of time. 
   Lancet Neurol. 2014;13(8):844-54. doi: 10.1016/S1474-4422(14)70120-6.
3. Steyerberg EW, Mushkudiani N, Perel P, et al. Predicting outcome after traumatic brain injury: 
   development and international validation of prognostic scores based on admission characteristics. 
   PLoS Med. 2008;5(8):e165. doi: 10.1371/journal.pmed.0050165.

The GCS-Pupils Score (GCS-P) represents a significant advancement in traumatic brain injury assessment 
by combining the well-established Glasgow Coma Scale (GCS) with pupillary reactivity evaluation. 
This integrated approach provides enhanced prognostic accuracy, particularly valuable in severe TBI 
where traditional GCS scores may cluster at low values (3-4) with limited discriminatory power.

Developed by Brennan, Murray, and Teasdale in 2018, the GCS-P score extends the prognostic range 
from 1-17 points (compared to GCS 3-15), offering improved prediction of 6-month mortality and 
functional outcomes. The score addresses a critical limitation of GCS alone, where pupillary 
non-reactivity indicates brainstem dysfunction and significantly worsens prognosis even within 
the same GCS category.

Clinical Applications:
- Enhanced prognostic assessment in traumatic brain injury
- Improved clinical decision-making in severe TBI (GCS 3-8)
- Risk stratification for family counseling and goals of care discussions
- Research tool for TBI outcome studies and clinical trial stratification
- Quality improvement metric for trauma center outcomes
- Support for resource allocation and intensive care decision-making

Key Advantages over GCS Alone:
- Extended prognostic range providing better discrimination across severity spectrum
- Incorporation of brainstem function assessment through pupillary reactivity
- Validated prediction models for 6-month mortality and unfavorable outcomes
- Simple arithmetic combination of readily available clinical assessments
- Particularly valuable in severe TBI where GCS clustering limits discrimination
- Continuous relationship between score and outcomes rather than categorical thresholds

The score demonstrates that pupillary non-reactivity consistently worsens prognosis across all 
GCS levels, with the effect being most pronounced in severe injuries. This reflects the importance 
of brainstem integrity for neurological recovery and survival.

Pupillary Assessment Components:
- Both pupils reactive to light: 0 points (normal response)
- One pupil unreactive to light: 1 point (unilateral brainstem dysfunction)
- Both pupils unreactive to light: 2 points (bilateral brainstem dysfunction)

Glasgow Coma Scale Components:
- Eye Opening Response (1-4 points): Arousal and brainstem function
- Verbal Response (1-5 points): Cognitive function and language processing
- Motor Response (1-6 points): Motor pathway integrity and consciousness level

Clinical Interpretation Framework:
The GCS-P score provides evidence-based outcome predictions derived from large international 
databases (IMPACT and CRASH), enabling clinicians to move beyond subjective assessments to 
quantitative risk stratification. This supports more informed decision-making regarding 
treatment intensity, family counseling, and resource allocation while maintaining hope 
for recovery in appropriate cases.
"""

from pydantic import BaseModel, Field
from typing import Literal


class GcsPupilsScoreRequest(BaseModel):
    """
    Request model for GCS-Pupils Score calculation
    
    The GCS-Pupils Score combines the Glasgow Coma Scale with pupillary reactivity assessment 
    to provide enhanced prognostic accuracy in traumatic brain injury patients. This score 
    is particularly valuable in severe TBI where standard GCS scores may cluster at low values 
    with limited discriminatory power.
    
    **CLINICAL CONTEXT AND INDICATIONS**:
    
    **Primary Indications**:
    - Traumatic brain injury assessment and prognosis
    - Severe TBI where enhanced prognostic discrimination is needed
    - Clinical decision-making regarding treatment intensity and goals of care
    - Family counseling and prognostic discussions
    - Research applications and clinical trial stratification
    
    **Clinical Advantages**:
    - **Enhanced Discrimination**: Extends prognostic range from GCS 3-15 to GCS-P 1-17
    - **Brainstem Assessment**: Incorporates pupillary reactivity as marker of brainstem function
    - **Evidence-Based Predictions**: Provides quantitative 6-month mortality and outcome risks
    - **Clinical Practicality**: Uses readily available bedside assessments
    - **Validated Accuracy**: Derived from large international TBI databases (IMPACT, CRASH)
    
    **PARAMETER INTERPRETATION GUIDE**:
    
    **GLASGOW COMA SCALE COMPONENTS**:
    
    **1. Eye Opening Response (1-4 points)**:
    
    **4 - Eyes open spontaneously**:
    - **Clinical Context**: Normal arousal and brainstem function
    - **Assessment**: Patient opens eyes without external stimulation
    - **Implications**: Indicates preserved sleep-wake cycle and brainstem reflexes
    
    **3 - Eye opening to voice**:
    - **Clinical Context**: Mild impairment of arousal requiring verbal stimulation
    - **Assessment**: Eyes open in response to normal or loud verbal commands
    - **Implications**: Suggests intact auditory pathways and partial arousal mechanisms
    
    **2 - Eye opening to pain**:
    - **Clinical Context**: Significant arousal impairment requiring painful stimulation
    - **Assessment**: Eyes open only with physical painful stimulus (nail bed pressure, supraorbital pressure)
    - **Implications**: Indicates severe brainstem dysfunction but preserved minimal reflexes
    
    **1 - No eye opening**:
    - **Clinical Context**: Severe brainstem dysfunction or anatomical obstruction
    - **Assessment**: No eye opening despite maximal stimulation
    - **Considerations**: Rule out mechanical factors (orbital swelling, facial fractures)
    
    **2. Verbal Response (1-5 points)**:
    
    **5 - Oriented**:
    - **Clinical Context**: Normal cognitive function and language processing
    - **Assessment**: Correctly answers questions about person, place, time, and situation
    - **Implications**: Indicates preserved higher cortical functions and consciousness
    
    **4 - Confused**:
    - **Clinical Context**: Mild cognitive impairment with preserved language
    - **Assessment**: Responds appropriately but with disorientation or confusion
    - **Implications**: Suggests cortical dysfunction but intact language centers
    
    **3 - Inappropriate words**:
    - **Clinical Context**: Moderate language dysfunction with word production
    - **Assessment**: Speaks words but inappropriately or out of context
    - **Implications**: Indicates significant cortical or language area dysfunction
    
    **2 - Incomprehensible sounds**:
    - **Clinical Context**: Severe language impairment with only vocalization
    - **Assessment**: Makes sounds (moaning, groaning) but no recognizable words
    - **Implications**: Suggests preserved brainstem function but severe cortical damage
    
    **1 - No verbal response**:
    - **Clinical Context**: Complete absence of vocalization
    - **Assessment**: No sounds despite stimulation
    - **Considerations**: Rule out intubation, tracheostomy, or anatomical barriers
    
    **3. Motor Response (1-6 points)**:
    
    **6 - Obeys commands**:
    - **Clinical Context**: Normal motor pathway integrity and comprehension
    - **Assessment**: Follows simple motor commands (move fingers, stick out tongue)
    - **Implications**: Indicates preserved cortical-motor connections and understanding
    
    **5 - Localizes pain**:
    - **Clinical Context**: Purposeful motor response to painful stimuli
    - **Assessment**: Moves hand toward or crosses midline to remove painful stimulus
    - **Implications**: Suggests intact sensory-motor integration and cortical processing
    
    **4 - Withdrawal from pain**:
    - **Clinical Context**: Appropriate but non-purposeful response to pain
    - **Assessment**: Flexion withdrawal of limb from painful stimulus
    - **Implications**: Indicates preserved spinal reflexes and some cortical function
    
    **3 - Flexion to pain (decorticate posturing)**:
    - **Clinical Context**: Abnormal flexor response indicating cortical damage
    - **Assessment**: Arms flex at elbow and wrist, legs extend
    - **Implications**: Suggests damage above brainstem with preserved some brainstem function
    
    **2 - Extension to pain (decerebrate posturing)**:
    - **Clinical Context**: Abnormal extensor response indicating brainstem damage
    - **Assessment**: Arms and legs extend with internal rotation
    - **Implications**: Indicates severe brainstem dysfunction at midbrain level
    
    **1 - No motor response**:
    - **Clinical Context**: Complete absence of motor response
    - **Assessment**: No movement despite maximal painful stimulation
    - **Considerations**: Rule out spinal cord injury, neuromuscular blockade, or anatomical factors
    
    **PUPILLARY REACTIVITY ASSESSMENT**:
    
    **Both Pupils Reactive (0 points)**:
    - **Clinical Context**: Normal brainstem function and third cranial nerve integrity
    - **Assessment**: Both pupils constrict briskly to bright light
    - **Technique**: Use bright penlight, observe direct and consensual responses
    - **Implications**: Indicates preserved midbrain function and autonomic pathways
    
    **One Pupil Unreactive (1 point)**:
    - **Clinical Context**: Unilateral brainstem dysfunction or focal pathology
    - **Assessment**: One pupil fails to constrict to light, other responds normally
    - **Differential**: Consider unilateral herniation, direct ocular trauma, medications
    - **Implications**: Suggests asymmetric intracranial pathology or focal nerve injury
    
    **Both Pupils Unreactive (2 points)**:
    - **Clinical Context**: Bilateral brainstem dysfunction or severe intracranial pressure
    - **Assessment**: Neither pupil constricts to bright light stimulation
    - **Critical Sign**: Often indicates impending or actual brainstem herniation
    - **Implications**: Associated with very poor prognosis and need for urgent intervention
    
    **CLINICAL DECISION SUPPORT FRAMEWORK**:
    
    **Assessment Timing and Frequency**:
    - **Initial Assessment**: Within first hour of hospital presentation
    - **Serial Monitoring**: Every 15-30 minutes in unstable patients, hourly when stable
    - **Critical Changes**: Immediate reassessment with any neurological deterioration
    - **Documentation**: Record time, examiner, and any confounding factors
    
    **Confounding Factors to Consider**:
    
    **Eye Opening**:
    - Orbital swelling, facial fractures, sedating medications
    - Consider alternative assessment methods if mechanical obstruction present
    
    **Verbal Response**:
    - Intubation, tracheostomy, language barriers, hearing impairment
    - May use alternative communication methods or defer until extubation possible
    
    **Motor Response**:
    - Spinal cord injury, peripheral nerve damage, neuromuscular blockade
    - Assess bilateral responses and consider best motor response
    
    **Pupillary Response**:
    - Direct ocular trauma, cataracts, medications (opioids, anticholinergics)
    - Pre-existing pupil abnormalities, contact lenses, chemical exposure
    
    **SCORE INTERPRETATION AND CLINICAL IMPLICATIONS**:
    
    **GCS-P Score 1-3 (Extremely Severe)**:
    - **Mortality Risk**: 40-75% at 6 months
    - **Clinical Actions**: Intensive monitoring, family meetings, goals of care discussions
    - **Prognosis**: Very poor, consider comfort measures if appropriate
    
    **GCS-P Score 4-6 (Severe)**:
    - **Mortality Risk**: 25-40% at 6 months
    - **Clinical Actions**: Aggressive supportive care, early rehabilitation planning
    - **Prognosis**: Guarded but potential for meaningful recovery
    
    **GCS-P Score 7-9 (Moderate)**:
    - **Mortality Risk**: 17-20% at 6 months
    - **Clinical Actions**: Close monitoring, early rehabilitation intervention
    - **Prognosis**: Fair with good potential for functional recovery
    
    **GCS-P Score 10-12 (Mild-Moderate)**:
    - **Mortality Risk**: 9-17% at 6 months
    - **Clinical Actions**: Regular monitoring, comprehensive rehabilitation
    - **Prognosis**: Generally good with appropriate support
    
    **GCS-P Score 13-17 (Mild)**:
    - **Mortality Risk**: 3-7% at 6 months
    - **Clinical Actions**: Symptom monitoring, outpatient follow-up
    - **Prognosis**: Excellent with focus on post-concussive syndrome prevention
    
    **FAMILY COMMUNICATION AND COUNSELING**:
    
    **Prognostic Discussions**:
    - Use GCS-P score to provide evidence-based outcome estimates
    - Emphasize that predictions are population-based, individual variation exists
    - Discuss timeline for neurological recovery and when reassessment may occur
    - Address questions about quality of life and functional outcomes
    
    **Decision-Making Support**:
    - Facilitate informed decisions about treatment intensity and goals of care
    - Provide context for rehabilitation potential and resource needs
    - Support families through uncertainty while maintaining appropriate hope
    - Connect with social work, chaplaincy, and other support services
    
    References (Vancouver style):
    1. Brennan PM, Murray GD, Teasdale GM. Simplifying the use of prognostic information in traumatic 
       brain injury. Part 1: The GCS-Pupils score: an extended index of clinical severity. 
       J Neurosurg. 2018;128(6):1612-1620. doi: 10.3171/2017.12.JNS172780.
    2. Teasdale G, Maas A, Lecky F, et al. The Glasgow Coma Scale at 40 years: standing the test of time. 
       Lancet Neurol. 2014;13(8):844-54. doi: 10.1016/S1474-4422(14)70120-6.
    3. Steyerberg EW, Mushkudiani N, Perel P, et al. Predicting outcome after traumatic brain injury: 
       development and international validation of prognostic scores based on admission characteristics. 
       PLoS Med. 2008;5(8):e165. doi: 10.1371/journal.pmed.0050165.
    """
    
    eye_response: Literal[1, 2, 3, 4] = Field(
        ...,
        description="Eye opening response: 1=No eye opening, 2=Eye opening to pain, 3=Eye opening to voice, 4=Eyes open spontaneously",
        example=3
    )
    
    verbal_response: Literal[1, 2, 3, 4, 5] = Field(
        ...,
        description="Verbal response: 1=No verbal response, 2=Incomprehensible sounds, 3=Inappropriate words, 4=Confused, 5=Oriented",
        example=4
    )
    
    motor_response: Literal[1, 2, 3, 4, 5, 6] = Field(
        ...,
        description="Motor response: 1=No motor response, 2=Extension to pain, 3=Flexion to pain, 4=Withdrawal from pain, 5=Localizes pain, 6=Obeys commands",
        example=5
    )
    
    pupil_reactivity: Literal["both_reactive", "one_unreactive", "both_unreactive"] = Field(
        ...,
        description="Pupillary light reflex assessment: both_reactive=0 points, one_unreactive=1 point, both_unreactive=2 points",
        example="both_reactive"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "eye_response": 3,
                "verbal_response": 4,
                "motor_response": 5,
                "pupil_reactivity": "both_reactive"
            }
        }


class GcsPupilsScoreResponse(BaseModel):
    """
    Response model for GCS-Pupils Score calculation
    
    The response provides the calculated GCS-Pupils score along with component scores, 
    evidence-based outcome predictions, and comprehensive clinical interpretation with 
    management recommendations based on validated prognostic data.
    
    **CLINICAL INTERPRETATION FRAMEWORK**:
    
    **GCS-Pupils Score Components**:
    - **GCS Total Score**: Sum of eye, verbal, and motor responses (3-15 points)
    - **Pupil Score**: Pupillary reactivity assessment (0-2 points)
    - **GCS-P Score**: Combined score extending prognostic range (1-17 points)
    
    **Evidence-Based Outcome Predictions**:
    
    **6-Month Mortality Rates** (derived from IMPACT and CRASH databases):
    - **GCS-P 1**: 74.5% mortality - Extremely poor prognosis
    - **GCS-P 2**: 64.6% mortality - Very poor prognosis
    - **GCS-P 3**: 40.9% mortality - Poor prognosis with some recovery potential
    - **GCS-P 4-6**: 25-40% mortality - Guarded prognosis, aggressive care warranted
    - **GCS-P 7-9**: 17-20% mortality - Fair prognosis with good recovery potential
    - **GCS-P 10-12**: 9-17% mortality - Good prognosis with comprehensive rehabilitation
    - **GCS-P 13-17**: 3-7% mortality - Excellent prognosis, focus on symptom management
    
    **6-Month Unfavorable Outcome Rates** (death, vegetative state, severe disability):
    - **GCS-P 1**: 89.6% unfavorable - Very high disability risk
    - **GCS-P 2**: 85.2% unfavorable - High disability risk
    - **GCS-P 3**: 65.5% unfavorable - Moderate to high disability risk
    - **GCS-P 4-6**: 46-69% unfavorable - Variable outcomes, individualized approach
    - **GCS-P 7-9**: 30-37% unfavorable - Good potential for functional recovery
    - **GCS-P 10-12**: 20-29% unfavorable - Generally favorable outcomes
    - **GCS-P 13-17**: 12-16% unfavorable - Excellent functional prognosis
    
    **CLINICAL DECISION SUPPORT BY SCORE RANGE**:
    
    **Extremely Severe (GCS-P 1-3)**:
    
    **Immediate Actions**:
    - Intensive neurological monitoring with ICP measurement if indicated
    - Aggressive management of secondary brain injury prevention
    - Urgent neurosurgical consultation for potential interventions
    - Family meeting to discuss prognosis and goals of care
    
    **Monitoring Parameters**:
    - Continuous ICP monitoring if GCS ≤8 and abnormal CT
    - Maintain CPP 60-70 mmHg, avoid hypotension (SBP <90 mmHg)
    - Temperature management, normoglycemia, seizure prophylaxis
    - Serial neurological assessments every 15-30 minutes initially
    
    **Family Communication**:
    - Honest discussion of poor prognosis with quantitative risk estimates
    - Exploration of patient's previously expressed wishes and values
    - Discussion of treatment goals: curative vs. comfort-focused care
    - Connection with chaplaincy, social work, and palliative care services
    
    **Severe (GCS-P 4-6)**:
    
    **Management Approach**:
    - Intensive monitoring with frequent neurological assessments
    - Comprehensive supportive care with secondary injury prevention
    - Early involvement of rehabilitation team for outcome optimization
    - Regular family updates with prognostic information and support
    
    **Treatment Protocols**:
    - ICP monitoring and management per Brain Trauma Foundation guidelines
    - Multimodal monitoring including brain tissue oxygenation if available
    - Early nutrition support and DVT prophylaxis
    - Seizure monitoring and prophylaxis consideration
    
    **Recovery Planning**:
    - Early rehabilitation assessment and intervention
    - Multidisciplinary team involvement (PT, OT, speech therapy)
    - Family education about expected recovery trajectory
    - Planning for long-term care needs and support services
    
    **Moderate (GCS-P 7-9)**:
    
    **Clinical Management**:
    - Close neurological monitoring with serial assessments
    - Prevention of secondary complications and medical management
    - Early mobilization and rehabilitation intervention
    - Patient and family education about recovery expectations
    
    **Rehabilitation Focus**:
    - Comprehensive assessment of cognitive and functional deficits
    - Individualized therapy programs addressing specific impairments
    - Return-to-work and return-to-drive evaluations when appropriate
    - Long-term follow-up for cognitive and behavioral sequelae
    
    **Mild-Moderate (GCS-P 10-12)**:
    
    **Care Coordination**:
    - Regular monitoring for delayed complications or deterioration
    - Early rehabilitation services to optimize functional outcomes
    - Screening for post-concussive symptoms and mood disorders
    - Education about gradual return to activities and work
    
    **Follow-up Planning**:
    - Outpatient neurology or rehabilitation medicine follow-up
    - Neuropsychological testing if cognitive concerns present
    - Return-to-activity protocols for work, driving, and recreation
    - Long-term monitoring for late complications or symptoms
    
    **Mild (GCS-P 13-17)**:
    
    **Management Approach**:
    - Monitoring for post-concussive symptoms and complications
    - Patient education about expected recovery and symptom management
    - Gradual return to normal activities with symptom-guided progression
    - Follow-up care coordination with primary care or neurology
    
    **Symptom Management**:
    - Education about common post-concussive symptoms (headache, dizziness, fatigue)
    - Cognitive rest recommendations and gradual return to mental activities
    - Sleep hygiene and stress management strategies
    - When to seek urgent medical attention for concerning symptoms
    
    **LONGITUDINAL CARE CONSIDERATIONS**:
    
    **Recovery Timeline**:
    - **Acute Phase (0-7 days)**: Primary injury stabilization and secondary prevention
    - **Subacute Phase (1-4 weeks)**: Medical stabilization and early rehabilitation
    - **Rehabilitation Phase (1-6 months)**: Intensive therapy and functional improvement
    - **Long-term Phase (6+ months)**: Community reintegration and chronic symptom management
    
    **Reassessment Points**:
    - **72 hours**: Neurological stability and withdrawal of life support if appropriate
    - **1 week**: Medical complications and rehabilitation potential assessment
    - **1 month**: Functional status and discharge planning evaluation
    - **3 months**: Recovery trajectory and long-term prognosis determination
    - **6 months**: Final outcome assessment and ongoing care needs
    
    **Quality of Life Factors**:
    - Functional independence in activities of daily living
    - Cognitive function including memory, attention, and executive skills
    - Social relationships and community participation
    - Employment status and financial independence
    - Mood and psychological well-being
    
    **Family and Caregiver Support**:
    - Education about TBI effects and recovery expectations
    - Training in care techniques and safety considerations
    - Connection with support groups and community resources
    - Respite care and caregiver well-being support
    - Long-term care planning and resource coordination
    
    Reference: Brennan PM, et al. J Neurosurg. 2018;128(6):1612-1620.
    """
    
    result: int = Field(
        ...,
        description="GCS-Pupils score calculated from GCS components plus pupil reactivity (range 1-17 points)",
        ge=1,
        le=17,
        example=12
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for GCS-Pupils score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation with evidence-based outcome predictions and management recommendations",
        example="GCS-Pupils score of 12 (GCS 12 + pupil score 0) with both pupils reactive to light. Predicted 6-month mortality: 9.4%. Predicted unfavorable outcome: 19.9%. Mild to moderate brain injury with lower mortality risk. Regular neurological monitoring to detect any complications or deterioration. Initiate appropriate rehabilitation services including physical, occupational, and speech therapy as indicated. Screen for post-concussive symptoms, cognitive impairment, and mood changes. Educate patient and family about recovery expectations and available support resources."
    )
    
    stage: str = Field(
        ...,
        description="Severity category based on GCS-Pupils score range",
        example="Mild-Moderate"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of prognosis category",
        example="Fair prognosis"
    )
    
    gcs_total: int = Field(
        ...,
        description="Standard Glasgow Coma Scale total score (3-15 points)",
        ge=3,
        le=15,
        example=12
    )
    
    pupil_score: int = Field(
        ...,
        description="Pupillary reactivity score component (0-2 points)",
        ge=0,
        le=2,
        example=0
    )
    
    mortality_6_month: float = Field(
        ...,
        description="Predicted 6-month mortality percentage based on GCS-P score",
        example=9.4
    )
    
    unfavorable_outcome_6_month: float = Field(
        ...,
        description="Predicted 6-month unfavorable outcome percentage (death, vegetative state, severe disability)",
        example=19.9
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 12,
                "unit": "points",
                "interpretation": "GCS-Pupils score of 12 (GCS 12 + pupil score 0) with both pupils reactive to light. Predicted 6-month mortality: 9.4%. Predicted unfavorable outcome: 19.9%. Mild to moderate brain injury with lower mortality risk. Regular neurological monitoring to detect any complications or deterioration. Initiate appropriate rehabilitation services including physical, occupational, and speech therapy as indicated. Screen for post-concussive symptoms, cognitive impairment, and mood changes. Educate patient and family about recovery expectations and available support resources.",
                "stage": "Mild-Moderate",
                "stage_description": "Fair prognosis",
                "gcs_total": 12,
                "pupil_score": 0,
                "mortality_6_month": 9.4,
                "unfavorable_outcome_6_month": 19.9
            }
        }