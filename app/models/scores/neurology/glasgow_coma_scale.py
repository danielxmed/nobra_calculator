"""
Glasgow Coma Scale (GCS) Models

Request and response models for Glasgow Coma Scale calculation.

References (Vancouver style):
1. Teasdale G, Jennett B. Assessment of coma and impaired consciousness. A practical scale. 
   Lancet. 1974;2(7872):81-84. doi: 10.1016/s0140-6736(74)91639-0.
2. Teasdale G, Maas A, Lecky F, Manley G, Stocchetti N, Murray G. The Glasgow Coma Scale 
   at 40 years: standing the test of time. Lancet Neurol. 2014;13(8):844-854. 
   doi: 10.1016/S1474-4422(14)70120-6.
3. Brennan PM, Murray GD, Teasdale GM. Simplifying the use of prognostic information in 
   traumatic brain injury. Part 1: The GCS-Pupils score: an extended index of clinical 
   severity. J Neurosurg. 2018;128(6):1612-1620. doi: 10.3171/2017.12.JNS172780.

The Glasgow Coma Scale (GCS) is a clinical scale used to reliably measure a person's 
level of consciousness after a brain injury. Developed by Graham Teasdale and Bryan 
Jennett in 1974, it has become the most widely used neurological assessment tool 
internationally, translated into over 30 languages and used across diverse healthcare 
settings worldwide.

Key Clinical Applications:
- Assessment of consciousness level in acute brain injury
- Monitoring neurological status and detecting deterioration
- Prognostic indicator for traumatic brain injury outcomes
- Communication tool between healthcare providers
- Clinical trial stratification and research applications

The GCS evaluates three fundamental aspects of neurological function that together 
provide a comprehensive picture of consciousness level. The motor component has been 
shown to be the most predictive of outcome, while the combined score provides reliable 
assessment of overall neurological status. Serial assessments are more valuable than 
single measurements for tracking patient progress and detecting changes in neurological 
condition.
"""

from pydantic import BaseModel, Field
from typing import Literal


class GlasgowComaScaleRequest(BaseModel):
    """
    Request model for Glasgow Coma Scale (GCS)
    
    The Glasgow Coma Scale provides standardized assessment of consciousness level 
    using three components that evaluate different aspects of neurological function. 
    This assessment tool enables consistent evaluation across healthcare providers 
    and settings, facilitating communication and clinical decision-making.
    
    **CLINICAL CONTEXT AND INDICATIONS**:
    
    **Primary Clinical Application**:
    - **Target Population**: Patients with suspected or confirmed brain injury, altered consciousness
    - **Clinical Settings**: Emergency departments, intensive care units, neurology services, trauma centers
    - **Assessment Timing**: Initial evaluation, serial monitoring, pre/post-intervention assessment
    - **Diagnostic Context**: Traumatic brain injury, stroke, intoxication, metabolic encephalopathy
    
    **Key Advantages for Neurological Assessment**:
    - **Standardized Evaluation**: Consistent methodology across different healthcare providers
    - **Objective Measurement**: Reduces subjective interpretation in consciousness assessment
    - **Prognostic Value**: Correlates with functional outcomes and mortality in brain injury
    - **Communication Tool**: Provides common language for healthcare team collaboration
    - **Serial Monitoring**: Enables tracking of neurological changes over time
    
    **COMPONENT ASSESSMENT FRAMEWORK**:
    
    **Eye Opening Response (E1-E4)**:
    
    **Clinical Significance**: Assesses level of arousal and brainstem function
    - **Neuroanatomical Basis**: Reflects ascending reticular activating system integrity
    - **Assessment Method**: Observe spontaneous eye opening or response to stimuli
    - **Scoring Range**: 1-4 points with higher scores indicating better function
    - **Clinical Context**: Most basic indicator of consciousness level
    
    **Detailed Scoring Criteria**:
    
    **E4 - Spontaneous Eye Opening**:
    - **Clinical Significance**: Normal arousal level, intact brainstem function
    - **Assessment**: Eyes open spontaneously without external stimulation
    - **Neurological Implication**: Preserved sleep-wake cycle and arousal mechanisms
    - **Clinical Context**: Indicates normal or near-normal consciousness level
    
    **E3 - Eye Opening to Verbal Command**:
    - **Clinical Significance**: Responsive to auditory stimuli, partial arousal
    - **Assessment**: Eyes open in response to normal speaking voice or calling name
    - **Neurological Implication**: Intact auditory pathways and arousal response
    - **Clinical Context**: Mild to moderate impairment of consciousness
    
    **E2 - Eye Opening to Pain**:
    - **Clinical Significance**: Requires noxious stimuli for arousal response
    - **Assessment**: Eyes open only in response to physical painful stimulus
    - **Neurological Implication**: Significant impairment of arousal mechanisms
    - **Clinical Context**: Moderate to severe brain injury or altered consciousness
    
    **E1 - No Eye Opening**:
    - **Clinical Significance**: Absent arousal response, severe brainstem dysfunction
    - **Assessment**: No eye opening despite maximal stimulation attempts
    - **Neurological Implication**: Severe impairment of arousal systems
    - **Clinical Context**: Comatose state, severe brain injury
    
    **Verbal Response (V1-V5)**:
    
    **Clinical Significance**: Assesses cognitive function, orientation, and language abilities
    - **Neuroanatomical Basis**: Reflects cerebral cortex function, particularly language areas
    - **Assessment Method**: Evaluate speech content, orientation, and comprehension
    - **Scoring Range**: 1-5 points with higher scores indicating better cognitive function
    - **Clinical Context**: Most sensitive indicator of cognitive impairment
    
    **Detailed Scoring Criteria**:
    
    **V5 - Oriented and Conversing**:
    - **Clinical Significance**: Normal cognitive function and orientation
    - **Assessment**: Knows person, place, time; appropriate conversation
    - **Neurological Implication**: Intact higher cognitive functions
    - **Clinical Context**: Normal consciousness or minimal cognitive impairment
    
    **V4 - Confused Conversation**:
    - **Clinical Significance**: Impaired orientation with preserved language
    - **Assessment**: Can converse but disoriented to person, place, or time
    - **Neurological Implication**: Selective cognitive impairment
    - **Clinical Context**: Mild to moderate brain injury or delirium
    
    **V3 - Inappropriate Words**:
    - **Clinical Significance**: Severe cognitive impairment with some language preservation
    - **Assessment**: Random words unrelated to questions or context
    - **Neurological Implication**: Significant cortical dysfunction
    - **Clinical Context**: Moderate to severe brain injury
    
    **V2 - Incomprehensible Sounds**:
    - **Clinical Significance**: Loss of language function with preserved vocalization
    - **Assessment**: Moaning, groaning, or unintelligible vocalizations
    - **Neurological Implication**: Severe language area dysfunction
    - **Clinical Context**: Severe brain injury or deep altered consciousness
    
    **V1 - No Verbal Response**:
    - **Clinical Significance**: Complete loss of verbal communication
    - **Assessment**: No vocalization despite stimulation
    - **Neurological Implication**: Severe cerebral dysfunction or mechanical inability
    - **Clinical Context**: Comatose state, intubation, or severe brain injury
    
    **Motor Response (M1-M6)**:
    
    **Clinical Significance**: Assesses motor function and ability to follow commands
    - **Neuroanatomical Basis**: Reflects motor cortex, corticospinal tracts, and brainstem function
    - **Assessment Method**: Evaluate purposeful movement and response to commands
    - **Scoring Range**: 1-6 points with higher scores indicating better motor function
    - **Clinical Context**: Most predictive component for outcome assessment
    
    **Detailed Scoring Criteria**:
    
    **M6 - Obeys Commands**:
    - **Clinical Significance**: Normal motor function and command comprehension
    - **Assessment**: Follows simple two-step commands appropriately
    - **Neurological Implication**: Intact motor cortex and comprehension
    - **Clinical Context**: Normal or minimal neurological impairment
    
    **M5 - Localizes to Pain**:
    - **Clinical Significance**: Purposeful response to noxious stimuli
    - **Assessment**: Brings hand across midline to remove painful stimulus
    - **Neurological Implication**: Preserved higher motor functions
    - **Clinical Context**: Mild to moderate brain injury
    
    **M4 - Normal Flexion (Withdrawal)**:
    - **Clinical Significance**: Appropriate withdrawal response to pain
    - **Assessment**: Flexes arm away from painful stimulus
    - **Neurological Implication**: Intact spinal reflex pathways
    - **Clinical Context**: Moderate brain injury with preserved reflexes
    
    **M3 - Abnormal Flexion (Decorticate)**:
    - **Clinical Significance**: Pathological posturing indicating severe brain injury
    - **Assessment**: Slow flexion of arms toward body with painful stimulus
    - **Neurological Implication**: Damage above red nucleus, preserved rubrospinal tract
    - **Clinical Context**: Severe brain injury with cortical dysfunction
    
    **M2 - Extension (Decerebrate)**:
    - **Clinical Significance**: More severe pathological posturing
    - **Assessment**: Abnormal extension of arms and legs with stimulation
    - **Neurological Implication**: Damage to brainstem at midbrain level
    - **Clinical Context**: Very severe brain injury with brainstem involvement
    
    **M1 - No Motor Response**:
    - **Clinical Significance**: Complete absence of motor response
    - **Assessment**: No movement despite maximal painful stimulation
    - **Neurological Implication**: Severe brain or spinal cord dysfunction
    - **Clinical Context**: Comatose state or complete motor system failure
    
    **CLINICAL ASSESSMENT GUIDELINES**:
    
    **Assessment Environment**:
    - **Optimal Conditions**: Quiet environment, adequate lighting, patient comfort
    - **Timing Considerations**: Avoid assessment during sedation or immediately post-procedure
    - **Safety Measures**: Ensure patient safety during stimulus application
    - **Documentation**: Record best response observed during assessment period
    
    **Stimulus Application**:
    - **Verbal Stimuli**: Use normal speaking voice, progress to loud voice if needed
    - **Painful Stimuli**: Use appropriate noxious stimuli (trapezius squeeze, supraorbital pressure)
    - **Safety Protocols**: Avoid harmful or excessive force during assessment
    - **Technique Consistency**: Standardize stimulus application across assessments
    
    **Special Considerations**:
    
    **Modifying Factors**:
    - **Intubation**: Use "T" modifier for intubated patients (unable to assess verbal response)
    - **Facial Swelling**: Use "C" modifier when eyes cannot open due to swelling
    - **Language Barriers**: Consider cultural and linguistic factors in assessment
    - **Medications**: Account for sedating medications or neuromuscular blocking agents
    
    **Clinical Limitations**:
    - **Sensory Impairments**: Visual or hearing deficits may affect component assessment
    - **Pharmacological Effects**: Sedatives, analgesics, or paralytics may alter scores
    - **Medical Conditions**: Pre-existing neurological conditions may confound interpretation
    - **Age Factors**: Consider age-appropriate modifications for pediatric patients
    
    References (Vancouver style):
    1. Teasdale G, Jennett B. Assessment of coma and impaired consciousness. A practical scale. 
       Lancet. 1974;2(7872):81-84.
    2. Teasdale G, Maas A, Lecky F, Manley G, Stocchetti N, Murray G. The Glasgow Coma Scale 
       at 40 years: standing the test of time. Lancet Neurol. 2014;13(8):844-854.
    3. Brennan PM, Murray GD, Teasdale GM. Simplifying the use of prognostic information in 
       traumatic brain injury. J Neurosurg. 2018;128(6):1612-1620.
    """
    
    eye_opening: Literal[1, 2, 3, 4] = Field(
        ...,
        description="Eye opening response. 4=Spontaneous, 3=To verbal command, 2=To pain, 1=None",
        example=4
    )
    
    verbal_response: Literal[1, 2, 3, 4, 5] = Field(
        ...,
        description="Verbal response. 5=Oriented, 4=Confused, 3=Inappropriate words, 2=Incomprehensible sounds, 1=None",
        example=5
    )
    
    motor_response: Literal[1, 2, 3, 4, 5, 6] = Field(
        ...,
        description="Motor response. 6=Obeys commands, 5=Localizes to pain, 4=Normal flexion, 3=Abnormal flexion, 2=Extension, 1=None",
        example=6
    )
    
    class Config:
        schema_extra = {
            "example": {
                "eye_opening": 4,
                "verbal_response": 5,
                "motor_response": 6
            }
        }


class GlasgowComaScaleResponse(BaseModel):
    """
    Response model for Glasgow Coma Scale (GCS)
    
    The response provides the calculated GCS total score with comprehensive clinical 
    interpretation and evidence-based management recommendations based on validated 
    severity categories from extensive clinical research and validation studies.
    
    **CLINICAL INTERPRETATION FRAMEWORK**:
    
    **GCS Components and Validation**:
    - **Scoring Range**: 3-15 points combining three neurological domains
    - **Clinical Validation**: Extensively validated across diverse patient populations
    - **Prognostic Accuracy**: Strong correlation with functional outcomes and mortality
    - **International Standards**: Most widely used consciousness assessment tool globally
    
    **Severity Categories and Clinical Implications**:
    
    **Severe Brain Injury (GCS 3-8)**:
    - **Clinical Significance**: Comatose state with significant consciousness impairment
    - **Neurological Status**: Unable to follow commands, severe brainstem or cortical dysfunction
    - **Mortality Risk**: High mortality risk requiring intensive medical management
    - **Management Approach**: Intensive care monitoring, airway protection, neurological intervention
    
    **Moderate Brain Injury (GCS 9-12)**:
    - **Clinical Significance**: Altered consciousness with preserved some neurological functions  
    - **Neurological Status**: May be stuporous or obtunded but retains some responsiveness
    - **Recovery Potential**: Variable outcomes with potential for significant recovery
    - **Management Approach**: Close monitoring, frequent reassessment, targeted interventions
    
    **Mild Brain Injury (GCS 13-15)**:
    - **Clinical Significance**: Normal or near-normal consciousness with minimal impairment
    - **Neurological Status**: Alert and responsive with possible mild confusion
    - **Prognosis**: Generally good outcomes with appropriate management
    - **Management Approach**: Observation, symptom management, gradual return to activities
    
    **CLINICAL MANAGEMENT BY SEVERITY CATEGORY**:
    
    **Severe Brain Injury Management (GCS 3-8)**:
    
    **Immediate Interventions**:
    - **Airway Management**: Immediate assessment for intubation (typically required for GCS ≤8)
    - **Neurological Monitoring**: Continuous neurological assessment and ICP monitoring
    - **Imaging Studies**: Urgent CT scan, consider MRI for detailed assessment
    - **Specialist Consultation**: Immediate neurosurgical evaluation and intervention
    
    **Intensive Care Management**:
    - **Monitoring**: Continuous cardiac, respiratory, and neurological monitoring
    - **ICP Management**: Intracranial pressure monitoring and targeted therapy
    - **Supportive Care**: Mechanical ventilation, hemodynamic support, nutritional support
    - **Complication Prevention**: DVT prophylaxis, skin care, infection prevention
    
    **Moderate Brain Injury Management (GCS 9-12)**:
    
    **Assessment and Monitoring**:
    - **Serial GCS**: Frequent neurological assessments (every 1-2 hours initially)
    - **Imaging**: CT scan if not performed, consider repeat imaging if deterioration
    - **Specialist Input**: Neurology or neurosurgery consultation based on clinical context
    - **Monitoring Setting**: Admission to monitored unit or intensive care as appropriate
    
    **Treatment Approach**:
    - **Symptom Management**: Address pain, nausea, agitation as appropriate
    - **Activity Restrictions**: Bed rest initially with gradual mobilization as tolerated
    - **Complication Prevention**: Monitor for seizures, infection, other complications
    - **Family Education**: Provide information about expected course and warning signs
    
    **Mild Brain Injury Management (GCS 13-15)**:
    
    **Clinical Assessment**:
    - **Comprehensive Evaluation**: Detailed neurological examination and history
    - **Imaging Decisions**: CT scan based on clinical criteria and risk factors
    - **Cognitive Assessment**: Evaluate orientation, memory, and cognitive function
    - **Symptom Inventory**: Assess for headache, dizziness, nausea, cognitive complaints
    
    **Management Strategy**:
    - **Observation Period**: Monitor for deterioration during initial hours
    - **Discharge Planning**: Home discharge with reliable caregiver if stable
    - **Return Instructions**: Clear guidelines for when to seek immediate medical attention
    - **Follow-up Care**: Arrange appropriate outpatient follow-up and monitoring
    
    **SPECIAL CLINICAL CONSIDERATIONS**:
    
    **Serial Assessment Importance**:
    - **Trend Analysis**: Changes in GCS more significant than single measurements
    - **Deterioration Detection**: Declining scores indicate worsening neurological status
    - **Treatment Response**: Monitor improvement following interventions
    - **Prognostic Value**: Serial trends inform long-term outcome predictions
    
    **Documentation and Communication**:
    - **Component Scoring**: Document individual component scores (E4, V5, M6)
    - **Modifiers**: Use appropriate modifiers (T for intubated, C for eye closure)
    - **Trend Reporting**: Communicate changes and trends to healthcare team
    - **Standardization**: Ensure consistent assessment techniques across providers
    
    **Prognostic Counseling Guidelines**:
    - **Outcome Prediction**: Discuss expected outcomes based on GCS category
    - **Recovery Timeline**: Provide realistic expectations for recovery process
    - **Functional Outcomes**: Address potential long-term functional implications
    - **Family Support**: Offer resources and support for patients and families
    
    **Quality Improvement Applications**:
    - **Clinical Protocols**: Standardized assessment and management pathways
    - **Performance Metrics**: Track assessment accuracy and clinical outcomes
    - **Provider Training**: Ensure consistent GCS assessment across healthcare teams
    - **Research Applications**: Use for clinical trials and outcome studies
    
    Reference: Teasdale G, Jennett B. Lancet. 1974;2(7872):81-84.
    """
    
    result: int = Field(
        ...,
        description="Total Glasgow Coma Scale score calculated from three components (3-15 points)",
        ge=3,
        le=15,
        example=15
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for GCS score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation with severity assessment and evidence-based management recommendations",
        example="Glasgow Coma Scale: 15/15 [E4 (Spontaneous eye opening), V5 (Oriented and conversing), M6 (Obeys commands)]. Mild brain injury or normal consciousness. Patient is awake and can follow directions and communicate appropriately. May have mild confusion but maintains cognitive function. Continue routine neurological monitoring. Consider discharge planning if clinically stable and no other concerning features. Provide head injury precautions and return instructions. Follow-up as clinically indicated."
    )
    
    stage: str = Field(
        ...,
        description="Severity category based on GCS score (Severe Brain Injury, Moderate Brain Injury, Mild Brain Injury)",
        example="Mild Brain Injury"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of consciousness level",
        example="Alert to mildly confused"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 15,
                "unit": "points",
                "interpretation": "Glasgow Coma Scale: 15/15 [E4 (Spontaneous eye opening), V5 (Oriented and conversing), M6 (Obeys commands)]. Mild brain injury or normal consciousness. Patient is awake and can follow directions and communicate appropriately. May have mild confusion but maintains cognitive function. Continue routine neurological monitoring. Consider discharge planning if clinically stable and no other concerning features. Provide head injury precautions and return instructions. Follow-up as clinically indicated.",
                "stage": "Mild Brain Injury",
                "stage_description": "Alert to mildly confused"
            }
        }