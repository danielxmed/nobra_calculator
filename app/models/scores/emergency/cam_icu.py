"""
Confusion Assessment Method for the ICU (CAM-ICU) Models

Request and response models for CAM-ICU delirium assessment calculation.

References (Vancouver style):
1. Ely EW, Inouye SK, Bernard GR, Gordon S, Francis J, May L, et al. Delirium in mechanically 
   ventilated patients: validity and reliability of the confusion assessment method for the 
   intensive care unit (CAM-ICU). JAMA. 2001 Dec 5;286(21):2703-10. doi: 10.1001/jama.286.21.2703.
2. Ely EW, Margolin R, Francis J, May L, Truman B, Dittus R, et al. Evaluation of delirium in 
   critically ill patients: validation of the Confusion Assessment Method for the Intensive Care 
   Unit (CAM-ICU). Crit Care Med. 2001 Jul;29(7):1370-9. doi: 10.1097/00003246-200107000-00012.
3. Devlin JW, Skrobik Y, Gélinas C, Needham DM, Slooter AJ, Pandharipande PP, et al. Clinical 
   Practice Guidelines for the Prevention and Management of Pain, Agitation/Sedation, Delirium, 
   Immobility, and Sleep Disruption in Adult Patients in the ICU. Crit Care Med. 2018 Sep;46(9):e825-e873. 
   doi: 10.1097/CCM.0000000000003299.
4. Sessler CN, Gosnell MS, Grap MJ, Brophy GM, O'Neal PV, Keane KA, et al. The Richmond 
   Agitation-Sedation Scale: validity and reliability in adult intensive care unit patients. 
   Am J Respir Crit Care Med. 2002 Nov 15;166(10):1338-44. doi: 10.1164/rccm.2107138.

The CAM-ICU is a validated bedside tool for detecting delirium in critically ill patients, 
including those receiving mechanical ventilation. This systematic assessment evaluates four 
key features of delirium: acute onset/fluctuating course, inattention, altered level of 
consciousness, and disorganized thinking.

Clinical Background:

Delirium Epidemiology in ICU:
- Affects 40-87% of ICU patients, with highest rates in mechanically ventilated patients
- More common in elderly patients, those with cognitive impairment, and severe illness
- Associated with increased mortality, longer ICU stays, and long-term cognitive dysfunction
- Often under-recognized without systematic screening tools

CAM-ICU Assessment Process:

Prerequisites:
- Patient must have RASS (Richmond Agitation-Sedation Scale) ≥ -3 for assessment
- Requires trained healthcare provider familiar with the assessment technique
- Should be performed at least once per nursing shift in ICU patients

Feature Assessment:
1. Acute Onset or Fluctuating Course: Mental status change from baseline or fluctuation in past 24 hours
2. Inattention: Letters attention test (CASABLANCA) - patient squeezes hand for letter "A"
3. Altered Level of Consciousness: RASS score ≠ 0 (not alert and calm)
4. Disorganized Thinking: Yes/no questions and simple commands to assess cognitive organization

Diagnostic Criteria:
CAM-ICU positive (delirium present) requires:
- Feature 1 (Acute onset/fluctuating course) AND
- Feature 2 (Inattention) AND  
- Either Feature 3 (Altered consciousness) OR Feature 4 (Disorganized thinking)

Clinical Performance:
- Sensitivity: 95-100% for delirium detection
- Specificity: 89-93% with low false positive rate
- Can be completed in 1-2 minutes by experienced assessors
- Excellent inter-rater reliability when proper training provided

Clinical Applications:
- ICU delirium screening and monitoring
- Research studies investigating delirium interventions
- Quality improvement initiatives for delirium prevention
- Part of PADIS (Pain, Agitation, Delirium, Immobility, Sleep) bundle assessment

Management Implications:
- Positive results trigger delirium management protocols
- Guides medication review and optimization
- Informs family discussions and discharge planning
- Enables early intervention to prevent complications

Test Limitations:
- Requires adequate level of consciousness (RASS ≥ -3)
- May be challenging in patients with hearing impairment or language barriers
- Requires training for reliable implementation
- Cannot be performed in deeply sedated or comatose patients
- May have reduced accuracy in patients with severe cognitive impairment
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any


class CamIcuRequest(BaseModel):
    """
    Request model for Confusion Assessment Method for the ICU (CAM-ICU)
    
    The CAM-ICU is a validated bedside instrument for detecting delirium in critically ill 
    patients. It systematically evaluates four key features that define delirium: acute 
    onset or fluctuating course, inattention, altered level of consciousness, and 
    disorganized thinking.
    
    Assessment Prerequisites:
    
    RASS Requirement:
    - Patient must have Richmond Agitation-Sedation Scale (RASS) score ≥ -3
    - RASS < -3 indicates patient too sedated for meaningful assessment
    - Assessment should be delayed until adequate level of consciousness achieved
    
    RASS Scale Reference:
    +4: Combative (overtly combative, violent, immediate danger to staff)
    +3: Very agitated (pulls/removes tubes or catheters, aggressive)
    +2: Agitated (frequent non-purposeful movement, fights ventilator)
    +1: Restless (anxious, apprehensive, movements not aggressive)
     0: Alert and calm (spontaneously pays attention to caregiver)
    -1: Drowsy (not fully alert, sustained awakening to voice, >10 seconds)
    -2: Light sedation (briefly awakens to voice, <10 seconds)
    -3: Moderate sedation (movement/eye opening to voice, no eye contact)
    -4: Deep sedation (no response to voice, movement/eye opening to touch)
    -5: Unarousable (no response to voice or physical stimulation)
    
    Feature 1 - Acute Onset or Fluctuating Course:
    Assess whether there has been an acute change in mental status from baseline or if 
    the patient's mental status has fluctuated during the past 24 hours. Consider:
    - Comparison to patient's baseline mental status
    - Input from family members about baseline cognitive function
    - Documentation of mental status changes by nursing staff
    - Fluctuation between normal and abnormal states
    
    Feature 2 - Inattention (Letters Attention Test):
    Perform the standardized attention test using the letters in "CASABLANCA":
    - Say each letter clearly at 1-second intervals
    - Patient should squeeze your hand (or nod) when they hear the letter "A"
    - There are 4 "A"s in CASABLANCA (positions 2, 4, 6, and 8)
    - Count total number of errors (missed "A"s plus squeezes for non-"A" letters)
    - >2 errors indicates significant inattention
    
    Alternative attention tests if letters test not feasible:
    - Picture recognition test (if available)
    - Vigilance A test with different words
    
    Feature 3 - Altered Level of Consciousness:
    Determined by RASS score assessment:
    - RASS = 0 (Alert and calm): Feature 3 absent
    - RASS ≠ 0 (Any other score): Feature 3 present
    - This feature captures both hypoactive and hyperactive presentations
    
    Feature 4 - Disorganized Thinking:
    Assess cognitive organization using standardized questions and commands:
    
    Yes/No Questions (choose 2 from set A or set B):
    Set A:
    - "Will a stone float on water?"
    - "Are there fish in the sea?"
    - "Does one pound weigh more than two pounds?"
    - "Can you use a hammer to pound a nail?"
    
    Set B:
    - "Will a leaf float on water?"
    - "Are there elephants in the sea?"
    - "Do two pounds weigh more than one pound?"
    - "Can you use a hammer to cut wood?"
    
    Command: "Hold up this many fingers" (hold up 2 fingers)
    Then: "Now do the same thing with the other hand" (do not repeat number)
    
    Scoring: >1 error indicates disorganized thinking
    
    Clinical Considerations:
    
    Training Requirements:
    - Healthcare providers should receive formal CAM-ICU training
    - Practice with standardized cases recommended
    - Inter-rater reliability assessment beneficial
    
    Timing and Frequency:
    - Perform at least once per nursing shift
    - Additional assessments with significant clinical changes
    - Document time of assessment and clinical context
    
    Special Populations:
    - May be less reliable in patients with baseline cognitive impairment
    - Consider hearing aids or visual aids if sensory impairments present
    - Language barriers may affect assessment accuracy
    - Pediatric versions available for younger patients
    
    Documentation Standards:
    - Record exact responses to attention and thinking tests
    - Note any factors that may have influenced assessment
    - Document clinical context and concurrent medications
    - Include assessment validity indicators
    
    References (Vancouver style):
    1. Ely EW, Inouye SK, Bernard GR, Gordon S, Francis J, May L, et al. Delirium in mechanically 
    ventilated patients: validity and reliability of the confusion assessment method for the 
    intensive care unit (CAM-ICU). JAMA. 2001 Dec 5;286(21):2703-10. doi: 10.1001/jama.286.21.2703.
    2. Ely EW, Margolin R, Francis J, May L, Truman B, Dittus R, et al. Evaluation of delirium in 
    critically ill patients: validation of the Confusion Assessment Method for the Intensive Care 
    Unit (CAM-ICU). Crit Care Med. 2001 Jul;29(7):1370-9. doi: 10.1097/00003246-200107000-00012.
    3. Devlin JW, Skrobik Y, Gélinas C, Needham DM, Slooter AJ, Pandharipande PP, et al. Clinical 
    Practice Guidelines for the Prevention and Management of Pain, Agitation/Sedation, Delirium, 
    Immobility, and Sleep Disruption in Adult Patients in the ICU. Crit Care Med. 2018 Sep;46(9):e825-e873. 
    doi: 10.1097/CCM.0000000000003299.
    """
    
    rass_score: int = Field(
        ...,
        ge=-5,
        le=4,
        description="Richmond Agitation-Sedation Scale (RASS) score. Must be ≥-3 for valid CAM-ICU assessment. -5=Unarousable, -4=Deep sedation, -3=Moderate sedation, -2=Light sedation, -1=Drowsy, 0=Alert and calm, +1=Restless, +2=Agitated, +3=Very agitated, +4=Combative",
        example=0
    )
    
    acute_onset_fluctuating: Literal["yes", "no"] = Field(
        ...,
        description="Is there acute onset of mental status changes from baseline OR fluctuating course in the past 24 hours? Consider baseline cognitive function, family input, and nursing documentation of mental status changes",
        example="yes"
    )
    
    attention_errors: int = Field(
        ...,
        ge=0,
        le=10,
        description="Number of errors in letters attention test (CASABLANCA test). Patient should squeeze hand for letter 'A' (appears 4 times). Count missed A's plus incorrect squeezes for non-A letters. >2 errors indicates inattention",
        example=1
    )
    
    thinking_errors: int = Field(
        ...,
        ge=0,
        le=4,
        description="Number of errors in organized thinking test. Includes 2 yes/no questions plus 2-step command ('Hold up this many fingers', then 'Do the same with other hand'). >1 error indicates disorganized thinking",
        example=0
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "rass_score": 0,
                "acute_onset_fluctuating": "yes",
                "attention_errors": 1,
                "thinking_errors": 0
            }
        }


class CamIcuResponse(BaseModel):
    """
    Response model for Confusion Assessment Method for the ICU (CAM-ICU)
    
    Provides comprehensive delirium assessment results with detailed feature analysis, 
    clinical interpretation, and evidence-based management recommendations for ICU patients.
    
    CAM-ICU Diagnostic Algorithm:
    
    Positive Result (Delirium Present):
    Requires ALL of the following:
    - Feature 1: Acute onset or fluctuating course (present)
    - Feature 2: Inattention (>2 errors in attention test)
    - Feature 3 OR 4: Either altered consciousness (RASS ≠ 0) OR disorganized thinking (>1 error)
    
    Negative Result (No Delirium):
    Patient does not meet all required criteria above
    
    Clinical Significance by Result:
    
    CAM-ICU Positive (Delirium Present):
    - Immediate risk: Increased mortality, self-injury, treatment interference
    - Short-term complications: Prolonged ICU stay, delayed extubation, falls
    - Long-term consequences: Persistent cognitive dysfunction, functional decline
    - Management priority: Identify and treat underlying causes, optimize environment
    
    CAM-ICU Negative (No Delirium Detected):
    - Continue preventive measures to reduce delirium risk
    - Maintain regular monitoring as delirium can develop or fluctuate
    - Address modifiable risk factors proactively
    - Document baseline for future comparisons
    
    Feature-Specific Clinical Insights:
    
    Feature 1 - Acute Onset/Fluctuating Course:
    - Essential feature that must be present for delirium diagnosis
    - Reflects underlying pathophysiology of acute brain dysfunction
    - May indicate infectious, metabolic, or medication-related causes
    - Family input crucial for baseline mental status assessment
    
    Feature 2 - Inattention:
    - Core cognitive domain affected in delirium
    - Often earliest sign of developing delirium
    - Measured objectively through standardized attention testing
    - High sensitivity for detecting delirium across all subtypes
    
    Feature 3 - Altered Level of Consciousness:
    - Captures both hypoactive and hyperactive delirium presentations
    - RASS score provides objective measurement of consciousness level
    - Important for identifying hypoactive delirium (often missed)
    - Guides sedation management and liberation protocols
    
    Feature 4 - Disorganized Thinking:
    - Reflects higher-order cognitive dysfunction
    - May manifest as illogical flow of ideas or conversation
    - Can impact decision-making capacity and safety awareness
    - Important for communication with family and care planning
    
    Management Framework by Assessment Outcome:
    
    Immediate Actions for Positive Results:
    - Implement delirium management bundle (environmental modifications, medication review)
    - Evaluate and treat underlying precipitating factors (infection, hypoxia, metabolic disturbances)
    - Review and minimize deliriogenic medications (benzodiazepines, anticholinergics)
    - Optimize sleep-wake cycle and reduce noise/stimulation at night
    - Consider antipsychotic therapy for severe agitation if non-pharmacological measures inadequate
    
    Ongoing Monitoring Requirements:
    - Continue CAM-ICU assessments every nursing shift
    - Monitor for delirium-related complications (falls, self-extubation, aggressive behavior)
    - Track functional status and cognitive recovery progress
    - Engage family in reorientation and familiar environmental cues
    
    Prevention Strategies (All Patients):
    - Early mobilization and physical therapy when medically appropriate
    - Sleep hygiene protocols (noise reduction, natural light exposure)
    - Cognitive stimulation and reorientation activities
    - Family involvement in care and communication
    - Adequate pain management without oversedation
    
    Quality Improvement Applications:
    
    Clinical Metrics:
    - Delirium incidence rates by unit and patient population
    - Time to delirium recognition and intervention
    - CAM-ICU compliance rates and assessment frequency
    - Delirium duration and associated outcomes
    
    Performance Indicators:
    - Healthcare provider training completion rates
    - Inter-rater reliability scores for CAM-ICU assessments
    - Protocol adherence for delirium prevention and management
    - Patient and family satisfaction with delirium care
    
    Research and Evidence Applications:
    - Clinical trials evaluating delirium prevention interventions
    - Quality improvement studies on delirium reduction strategies
    - Pharmacological studies on delirium treatment approaches
    - Health economic analyses of delirium prevention programs
    
    Special Considerations:
    
    Assessment Limitations:
    - Cannot be performed in deeply sedated patients (RASS < -3)
    - May be less accurate in patients with baseline cognitive impairment
    - Requires training for reliable implementation and interpretation
    - May be affected by sensory impairments (hearing, vision)
    
    Clinical Context Factors:
    - Consider medication effects on assessment performance
    - Account for metabolic disturbances affecting cognition
    - Evaluate impact of sleep deprivation on test results
    - Document environmental factors that may influence assessment
    
    Documentation Requirements:
    - Record specific responses to attention and thinking tests
    - Note assessment timing relative to medications and procedures
    - Document factors that may affect assessment validity
    - Include clinical context and concurrent interventions
    
    Reference: Ely EW, et al. JAMA. 2001;286(21):2703-10. doi: 10.1001/jama.286.21.2703.
    """
    
    result: Dict[str, Any] = Field(
        ...,
        description="Comprehensive CAM-ICU assessment including feature analysis, clinical interpretation, and management recommendations",
        example={
            "cam_icu_positive": False,
            "features": {
                "feature_1": {
                    "name": "Acute Onset or Fluctuating Course",
                    "positive": True,
                    "description": "Acute change in mental status or fluctuating course in past 24 hours",
                    "assessment": "Present"
                },
                "feature_2": {
                    "name": "Inattention",
                    "positive": False,
                    "description": "Attention test errors: 1 (>2 errors indicates inattention)",
                    "assessment": "Absent"
                },
                "feature_3": {
                    "name": "Altered Level of Consciousness",
                    "positive": False,
                    "description": "RASS score: 0 (Alert and calm)",
                    "assessment": "Absent"
                },
                "feature_4": {
                    "name": "Disorganized Thinking", 
                    "positive": False,
                    "description": "Thinking test errors: 0 (>1 error indicates disorganized thinking)",
                    "assessment": "Absent"
                }
            },
            "clinical_interpretation": {
                "stage": "CAM-ICU Negative",
                "description": "No delirium detected",
                "interpretation": "Patient does not meet CAM-ICU criteria for delirium at this time. Continue routine monitoring and reassess regularly as delirium can fluctuate throughout the day."
            },
            "management_recommendations": {
                "immediate_actions": ["Continue current care plan", "Maintain delirium prevention strategies"],
                "ongoing_monitoring": ["Continue routine CAM-ICU screening", "Monitor for risk factors that could precipitate delirium"],
                "prevention_strategies": ["Maintain normal sleep-wake cycles", "Early mobilization", "Minimize sedating medications", "Frequent reorientation", "Family involvement in care"],
                "reassessment_timing": "Every nursing shift as per ICU protocol"
            },
            "assessment_validity": {
                "valid": True,
                "reason": "RASS score 0 adequate for assessment", 
                "recommendation": "Assessment results are valid"
            }
        }
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the assessment",
        example="assessment"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with assessment results and evidence-based recommendations",
        example="Patient does not meet CAM-ICU criteria for delirium at this time. Continue routine monitoring and reassess regularly as delirium can fluctuate throughout the day."
    )
    
    stage: str = Field(
        ...,
        description="Overall delirium status classification (CAM-ICU Positive, CAM-ICU Negative)",
        example="CAM-ICU Negative"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the delirium assessment result",
        example="No delirium detected"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": {
                    "cam_icu_positive": False,
                    "features": {
                        "feature_1": {
                            "name": "Acute Onset or Fluctuating Course",
                            "positive": True,
                            "description": "Acute change in mental status or fluctuating course in past 24 hours",
                            "assessment": "Present"
                        },
                        "feature_2": {
                            "name": "Inattention",
                            "positive": False,
                            "description": "Attention test errors: 1 (>2 errors indicates inattention)",
                            "assessment": "Absent"
                        },
                        "feature_3": {
                            "name": "Altered Level of Consciousness",
                            "positive": False,
                            "description": "RASS score: 0 (Alert and calm)",
                            "assessment": "Absent"
                        },
                        "feature_4": {
                            "name": "Disorganized Thinking",
                            "positive": False,
                            "description": "Thinking test errors: 0 (>1 error indicates disorganized thinking)",
                            "assessment": "Absent"
                        }
                    },
                    "clinical_interpretation": {
                        "stage": "CAM-ICU Negative",
                        "description": "No delirium detected",
                        "interpretation": "Patient does not meet CAM-ICU criteria for delirium at this time. Continue routine monitoring and reassess regularly as delirium can fluctuate throughout the day."
                    },
                    "management_recommendations": {
                        "immediate_actions": ["Continue current care plan", "Maintain delirium prevention strategies"],
                        "ongoing_monitoring": ["Continue routine CAM-ICU screening", "Monitor for risk factors that could precipitate delirium"],
                        "prevention_strategies": ["Maintain normal sleep-wake cycles", "Early mobilization", "Minimize sedating medications", "Frequent reorientation", "Family involvement in care"],
                        "reassessment_timing": "Every nursing shift as per ICU protocol"
                    },
                    "assessment_validity": {
                        "valid": True,
                        "reason": "RASS score 0 adequate for assessment",
                        "recommendation": "Assessment results are valid"
                    }
                },
                "unit": "assessment",
                "interpretation": "Patient does not meet CAM-ICU criteria for delirium at this time. Continue routine monitoring and reassess regularly as delirium can fluctuate throughout the day.",
                "stage": "CAM-ICU Negative",
                "stage_description": "No delirium detected"
            }
        }