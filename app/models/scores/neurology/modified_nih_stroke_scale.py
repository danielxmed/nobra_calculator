"""
Modified NIH Stroke Scale (mNIHSS) Models

Request and response models for Modified NIH Stroke Scale assessment of stroke severity.

References (Vancouver style):
1. Meyer BC, Hemmen TM, Jackson CM, Lyden PD. Modified National Institutes of Health 
   Stroke Scale for use in stroke clinical trials: preliminary reliability and validity. 
   Stroke. 2002 Feb;33(2):328-33. doi: 10.1161/hs0202.102318.
2. Meyer BC, Lyden PD. The modified National Institutes of Health Stroke Scale: its time 
   has come. Int J Stroke. 2009 Aug;4(4):267-73. doi: 10.1111/j.1747-4949.2009.00294.x.
3. Lyden P, Brott T, Tilley B, Welch KM, Mascha EJ, Levine S, Haley EC, Grotta J, Marler J. 
   Improved reliability of the NIH Stroke Scale using video training. NINDS TPA Stroke Study Group. 
   Stroke. 1994 Nov;25(11):2220-6. doi: 10.1161/01.str.25.11.2220.
4. Bruno A, Shah N, Lin C, Close B, Hess DC, Davis K, Baute V, Switzer JA, Waller JL, 
   Nichols FT. Improving modified Rankin Scale assessment with a simplified questionnaire. 
   Stroke. 2010 May;41(5):1048-50. doi: 10.1161/STROKEAHA.109.571562.

The Modified NIH Stroke Scale (mNIHSS) is a shortened, validated version of the original 
NIHSS that removes redundant and poorly reliable items while maintaining validity for 
stroke severity assessment. It provides improved interrater reliability and takes less 
time to complete while predicting outcomes equally well.
"""

from pydantic import BaseModel, Field
from typing import Literal


class ModifiedNihStrokeScaleRequest(BaseModel):
    """
    Request model for Modified NIH Stroke Scale (mNIHSS)
    
    The mNIHSS assesses stroke severity through 11 neurological parameters, removing 
    redundant and poorly reliable items from the original NIHSS:
    
    **Level of Consciousness Assessments:**
    
    **1B. Orientation Questions (0-2 points):**
    Ask patient the month and their age:
    - Both questions correct: 0 points (normal orientation)
    - 1 question correct: 1 point (mild disorientation) 
    - 0 questions correct: 2 points (significant disorientation)
    
    **1C. Commands (0-2 points):**
    Ask patient to open/close eyes and grip/release non-paretic hand:
    - Both tasks correct: 0 points (normal response to commands)
    - 1 task correct: 1 point (partial response)
    - 0 tasks correct: 2 points (no response to commands)
    
    **Neurological Function Assessments:**
    
    **2. Horizontal Extraocular Movements (0-2 points):**
    - Normal: 0 points (conjugate gaze normal)
    - Partial gaze palsy: 1 point (gaze abnormal in one or both eyes, but not total)
    - Total gaze palsy: 2 points (forced deviation or total gaze paresis)
    
    **3. Visual Fields (0-3 points):**
    Test visual fields by confrontation:
    - No visual loss: 0 points (no visual field defect)
    - Partial hemianopia: 1 point (quadrantanopia or partial field defect)
    - Complete hemianopia: 2 points (dense hemianopia)
    - Bilateral hemianopia: 3 points (bilateral hemianopia including cortical blindness)
    
    **Motor Function Assessments (0-4 points each):**
    
    **5a-5d. Motor Drift - Arms and Legs:**
    Test each limb for 10 seconds (arms) or 5 seconds (legs):
    - No drift: 0 points (limb holds position for full time)
    - Drift before 10 seconds: 1 point (limb drifts down before full time, some effort against gravity)
    - Falls before 10 seconds: 2 points (limb cannot maintain position, falls immediately)  
    - No effort against gravity: 3 points (limb falls, no effort against gravity)
    - No movement: 4 points (no movement)
    
    **8. Sensation (0-1 points):**
    Test sensation using pin prick on face, arms, legs, and trunk:
    - Normal; no sensory loss: 0 points (normal sensation)
    - Abnormal; sensory loss: 1 point (mild to moderate sensory loss or patient reports numbness)
    
    **9. Language/Aphasia (0-3 points):**
    Assess comprehension, expression, and repetition:
    - Normal; no aphasia: 0 points (normal language function)
    - Mild aphasia: 1 point (mild loss of fluency, comprehension, but can communicate)
    - Severe aphasia: 2 points (severe aphasia, fragmentary expression, inference needed)
    - Mute/global aphasia: 3 points (mute, global aphasia, no usable speech or comprehension)
    
    **11. Extinction/Inattention/Neglect (0-2 points):**
    Test for simultaneous bilateral stimulation:
    - Normal: 0 points (no abnormality)
    - Mild: 1 point (extinction to bilateral simultaneous stimulation)
    - Severe: 2 points (profound hemi-inattention or extinction to more than one modality)
    
    **Key Differences from Original NIHSS:**
    - Removes Item 1A (level of consciousness alertness) - found to be redundant
    - Removes Item 7 (ataxia) - poor interrater reliability
    - Removes Item 10 (dysarthria) - poor interrater reliability  
    - Combines facial weakness assessment with other motor evaluations
    - Simplifies sensory assessment to binary normal/abnormal
    - Maximum score 31 points (vs 42 for original NIHSS)
    
    **Clinical Advantages:**
    - Improved interrater reliability (71% vs 55% excellent reliability items)
    - Faster administration (6 minutes vs 7-10 minutes)
    - Better performance in telemedicine applications
    - More reliable when abstracted from medical records
    - Validated for clinical trials and research applications
    - Maintains equal validity for outcome prediction
    
    **Assessment Guidelines:**
    - Perform assessment in systematic order
    - Use standardized techniques for each test
    - Score based on actual performance, not patient effort
    - Consider best performance if multiple attempts needed
    - Document specific findings that contribute to scoring
    - Reassess periodically to monitor changes
    
    References (Vancouver style):
    1. Meyer BC, Hemmen TM, Jackson CM, Lyden PD. Modified National Institutes of Health 
       Stroke Scale for use in stroke clinical trials: preliminary reliability and validity. 
       Stroke. 2002;33(2):328-33.
    2. Meyer BC, Lyden PD. The modified National Institutes of Health Stroke Scale: its time 
       has come. Int J Stroke. 2009;4(4):267-73.
    """
    
    orientation_questions: Literal["both_correct", "one_correct", "zero_correct"] = Field(
        ...,
        description="Level of consciousness - orientation questions (month and age). Both correct (0 pts), one correct (1 pt), zero correct (2 pts)",
        example="both_correct"
    )
    
    commands: Literal["both_correct", "one_correct", "zero_correct"] = Field(
        ...,
        description="Level of consciousness - commands (open/close eyes, grip/release hand). Both correct (0 pts), one correct (1 pt), zero correct (2 pts)",
        example="both_correct"
    )
    
    horizontal_eye_movements: Literal["normal", "partial_gaze_palsy", "total_gaze_palsy"] = Field(
        ...,
        description="Horizontal extraocular movements. Normal (0 pts), partial gaze palsy (1 pt), total gaze palsy (2 pts)",
        example="normal"
    )
    
    visual_fields: Literal["no_visual_loss", "partial_hemianopia", "complete_hemianopia", "bilateral_hemianopia"] = Field(
        ...,
        description="Visual field testing by confrontation. No visual loss (0 pts), partial hemianopia (1 pt), complete hemianopia (2 pts), bilateral hemianopia (3 pts)",
        example="no_visual_loss"
    )
    
    left_arm_motor: Literal["no_drift", "drift_before_10_seconds", "falls_before_10_seconds", "no_effort_against_gravity", "no_movement"] = Field(
        ...,
        description="Left arm motor drift test for 10 seconds. No drift (0 pts), drift before 10s (1 pt), falls before 10s (2 pts), no effort against gravity (3 pts), no movement (4 pts)",
        example="no_drift"
    )
    
    right_arm_motor: Literal["no_drift", "drift_before_10_seconds", "falls_before_10_seconds", "no_effort_against_gravity", "no_movement"] = Field(
        ...,
        description="Right arm motor drift test for 10 seconds. No drift (0 pts), drift before 10s (1 pt), falls before 10s (2 pts), no effort against gravity (3 pts), no movement (4 pts)",
        example="no_drift"
    )
    
    left_leg_motor: Literal["no_drift", "drift_before_10_seconds", "falls_before_10_seconds", "no_effort_against_gravity", "no_movement"] = Field(
        ...,
        description="Left leg motor drift test for 5 seconds. No drift (0 pts), drift before 5s (1 pt), falls before 5s (2 pts), no effort against gravity (3 pts), no movement (4 pts)",
        example="no_drift"
    )
    
    right_leg_motor: Literal["no_drift", "drift_before_10_seconds", "falls_before_10_seconds", "no_effort_against_gravity", "no_movement"] = Field(
        ...,
        description="Right leg motor drift test for 5 seconds. No drift (0 pts), drift before 5s (1 pt), falls before 5s (2 pts), no effort against gravity (3 pts), no movement (4 pts)",
        example="no_drift"
    )
    
    sensation: Literal["normal_no_sensory_loss", "abnormal_sensory_loss"] = Field(
        ...,
        description="Sensory function test with pin prick. Normal/no sensory loss (0 pts), abnormal/sensory loss present (1 pt)",
        example="normal_no_sensory_loss"
    )
    
    language_aphasia: Literal["normal_no_aphasia", "mild_aphasia", "severe_aphasia", "mute_global_aphasia"] = Field(
        ...,
        description="Language and aphasia assessment. Normal/no aphasia (0 pts), mild aphasia (1 pt), severe aphasia (2 pts), mute/global aphasia (3 pts)",
        example="normal_no_aphasia"
    )
    
    extinction_neglect: Literal["normal", "mild", "severe"] = Field(
        ...,
        description="Extinction, inattention, or neglect assessment. Normal (0 pts), mild extinction (1 pt), severe neglect (2 pts)",
        example="normal"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "orientation_questions": "both_correct",
                "commands": "both_correct", 
                "horizontal_eye_movements": "normal",
                "visual_fields": "no_visual_loss",
                "left_arm_motor": "no_drift",
                "right_arm_motor": "no_drift",
                "left_leg_motor": "no_drift",
                "right_leg_motor": "no_drift",
                "sensation": "normal_no_sensory_loss",
                "language_aphasia": "normal_no_aphasia",
                "extinction_neglect": "normal"
            }
        }


class ModifiedNihStrokeScaleResponse(BaseModel):
    """
    Response model for Modified NIH Stroke Scale (mNIHSS)
    
    The mNIHSS score ranges from 0-31 points and stratifies stroke severity:
    
    **Score Interpretation and Prognosis:**
    
    **Minor Stroke (0-4 points):**
    - Minimal neurological deficit with good functional prognosis
    - Patients typically have minimal impact on activities of daily living
    - High likelihood of functional independence
    - Early mobilization and standard stroke protocols appropriate
    - Consider outpatient rehabilitation if needed
    
    **Moderate Stroke (5-15 points):**
    - Moderate neurological deficits with variable functional outcomes
    - Outcomes depend on specific deficit patterns and rehabilitation quality
    - Most patients benefit from comprehensive stroke unit care
    - Multidisciplinary rehabilitation planning essential
    - Consider thrombolytic therapy if within time window
    
    **Moderate-Severe Stroke (16-20 points):**
    - Significant neurological impairment affecting multiple domains
    - Substantial rehabilitation typically required
    - Functional independence may be achieved with intensive therapy
    - Higher risk of complications requiring close monitoring
    - Early palliative care consultation may be beneficial
    
    **Severe Stroke (21-31 points):**
    - Major neurological deficits with poor functional prognosis
    - High likelihood of long-term disability or death
    - Intensive monitoring and comprehensive care required
    - Consider advanced stroke interventions if appropriate
    - Goals of care discussions important for treatment planning
    
    **Clinical Applications:**
    
    **Treatment Decisions:**
    - Guides thrombolytic therapy eligibility assessment
    - Helps determine appropriate level of care (ICU vs stroke unit)
    - Assists in rehabilitation planning and resource allocation
    - Supports prognosis discussions with families
    
    **Monitoring and Assessment:**
    - Serial assessments track neurological improvement or deterioration
    - Objective measure for clinical trial endpoints
    - Quality metric for stroke care programs
    - Communication tool between healthcare providers
    
    **Outcome Prediction:**
    - Correlates with functional independence at discharge
    - Predicts need for long-term care services
    - Associated with mortality risk stratification
    - Helps estimate rehabilitation potential and duration
    
    **Advantages over Original NIHSS:**
    - 29% reduction in items with less than excellent reliability
    - Faster administration (6 vs 7-10 minutes)
    - Better performance in telemedicine applications
    - More reliable when abstracted from medical records
    - Equal validity for outcome prediction with improved efficiency
    
    **Quality Metrics:**
    - Interrater reliability improved from 55% to 71% excellent items
    - Maintains correlation with functional outcomes (r=0.84)
    - Validated across multiple clinical settings and populations
    - Suitable for both clinical care and research applications
    
    Reference: Meyer BC, et al. Stroke. 2002;33(2):328-33.
    """
    
    result: int = Field(
        ...,
        ge=0,
        le=31,
        description="Modified NIH Stroke Scale score indicating stroke severity (0-31 points)",
        example=3
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the scale",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with stroke severity assessment and management recommendations based on mNIHSS score",
        example="mNIHSS Score 3: Minor stroke with minimal neurological impairment. The patient demonstrates minor deficits that are unlikely to significantly impact daily activities. Good functional outcome is likely with appropriate medical management. Consider standard stroke protocols and monitor for potential improvement. Early mobilization and rehabilitation may accelerate recovery."
    )
    
    stage: str = Field(
        ...,
        description="Stroke severity category (Minor, Moderate, Moderate-Severe, Severe)",
        example="Minor Stroke"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of stroke severity level",
        example="Minimal neurological deficit"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 3,
                "unit": "points",
                "interpretation": "mNIHSS Score 3: Minor stroke with minimal neurological impairment. The patient demonstrates minor deficits that are unlikely to significantly impact daily activities. Good functional outcome is likely with appropriate medical management. Consider standard stroke protocols and monitor for potential improvement. Early mobilization and rehabilitation may accelerate recovery.",
                "stage": "Minor Stroke",
                "stage_description": "Minimal neurological deficit"
            }
        }