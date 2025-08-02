"""
Modified Minnesota Detoxification Scale (mMINDS) Models

Request and response models for Modified Minnesota Detoxification Scale assessment 
of alcohol withdrawal syndrome in critically ill patients.

References (Vancouver style):
1. Hack JB, Hoffmann RS, Nelson LS. Resistant alcohol withdrawal: does an unexpectedly 
   large sedative requirement identify these patients early? J Med Toxicol. 2006 Jun;2(2):55-60. 
   doi: 10.1007/BF03161175.
2. Awissi DK, Lebrun G, Fagnan M, Skrobik Y. Alcohol, nicotine, and iatrogenic withdrawals 
   in the ICU. Crit Care Med. 2013 Sep;41(9 Suppl 1):S57-68. doi: 10.1097/CCM.0b013e3182a168d5.
3. DeCarolis DD, Rice KL, Ho L, Willenbring ML, Cassaro S. Symptom-driven lorazepam protocol 
   for treatment of severe alcohol withdrawal delirium in the intensive care unit. 
   Pharmacotherapy. 2007 Apr;27(4):510-8. doi: 10.1592/phco.27.4.510.
4. Foy A, March S, Drinkwater V. Use of an objective clinical scale in the assessment and 
   management of alcohol withdrawal in a large general hospital. Alcohol Clin Exp Res. 
   1988 Jun;12(3):360-4. doi: 10.1111/j.1530-0277.1988.tb00208.x.

The Modified Minnesota Detoxification Scale (mMINDS) is an objective assessment tool 
for alcohol withdrawal syndrome, particularly valuable in critically ill patients 
where subjective scales like CIWA-Ar may be inappropriate. The scale evaluates 9 
clinical parameters and provides guidance for benzodiazepine therapy protocols.
"""

from pydantic import BaseModel, Field
from typing import Literal


class ModifiedMinnesotaDetoxificationScaleRequest(BaseModel):
    """
    Request model for Modified Minnesota Detoxification Scale (mMINDS)
    
    The mMINDS assesses alcohol withdrawal severity through 9 objective clinical parameters:
    
    **Vital Signs Assessment:**
    
    **Pulse Rate (0-2 points):**
    - <90 bpm: 0 points (normal cardiac response)
    - 90-110 bpm: 1 point (mild tachycardia)
    - >110 bpm: 2 points (significant tachycardia)
    
    **Diastolic Blood Pressure (0-2 points):**
    - <90 mmHg: 0 points (normal blood pressure)
    - 90-110 mmHg: 1 point (mild hypertension)
    - >110 mmHg: 2 points (significant hypertension)
    
    **Physical Signs Assessment:**
    
    **Tremor (0-6 points):**
    - Absent: 0 points (no visible tremor)
    - Slightly visible: 2 points (subtle tremor when observed)
    - Moderate with arms extended: 4 points (visible when arms outstretched)
    - Severe without extending arms: 6 points (obvious tremor at rest)
    
    **Diaphoresis/Sweat (0-6 points):**
    - Absent: 0 points (no visible sweating)
    - Barely moist palms: 2 points (minimal perspiration)
    - Beads visible: 4 points (obvious sweating on forehead/face)
    - Drenching: 6 points (profuse sweating requiring frequent changes)
    
    **Neuropsychiatric Assessment:**
    
    **Hallucinations (0-3 points):**
    - Absent: 0 points (no hallucinations reported or observed)
    - Mild/sporadic: 1 point (occasional, not distressing)
    - Moderate/intermittent: 2 points (frequent, somewhat distressing)
    - Severe/continuous: 3 points (persistent, highly distressing)
    
    **Agitation (0-9 points) - Based on Richmond Agitation-Sedation Scale:**
    - Normal/sedated: 0 points (calm, cooperative behavior)
    - Somewhat increased: 3 points (restless, easily startled)
    - Moderately fidgety: 6 points (frequent non-purposeful movements)
    - Pacing/thrashing: 9 points (violent, requiring restraints)
    
    **Orientation (0-6 points):**
    - Oriented x3: 0 points (person, place, time correct)
    - Oriented x2: 2 points (two of three correct)
    - Oriented x1: 4 points (only one of three correct)
    - Disoriented: 6 points (none correct or unable to assess)
    
    **Delusions (0-6 points):**
    - Absent/Unable to assess: 0 points (no delusions or over-sedated)
    - Present: 6 points (fixed false beliefs identified)
    
    **Seizures (0-6 points):**
    - Not actively seizing: 0 points (no seizure activity)
    - Actively seizing: 6 points (seizure activity at time of assessment)
    
    **Clinical Advantages over CIWA-Ar:**
    - Entirely objective assessment (no subjective patient responses required)
    - Validated for use in critically ill and mechanically ventilated patients
    - More accurate assessment when CIWA-Ar scores exceed 10
    - Associated with shorter ICU stays and reduced benzodiazepine use
    - Preferred by nursing staff for ease of use and reliability
    - Can be used in patients with altered mental status or communication barriers
    
    **Assessment Guidelines:**
    - If unable to assess a parameter due to over-sedation or mechanical ventilation, score = 0
    - Perform assessment at regular intervals (typically every 4-8 hours or per protocol)
    - Document specific findings that contribute to each score
    - Consider trending scores over time rather than single point assessments
    
    **Clinical Context:**
    - Primarily validated in medical and surgical ICU populations
    - Useful for guiding symptom-triggered benzodiazepine protocols
    - Helps identify patients at risk for severe withdrawal complications
    - Can be used in emergency department, medical floor, and ICU settings
    
    References (Vancouver style):
    1. Hack JB, Hoffmann RS, Nelson LS. Resistant alcohol withdrawal: does an unexpectedly 
       large sedative requirement identify these patients early? J Med Toxicol. 2006;2(2):55-60.
    2. Awissi DK, Lebrun G, Fagnan M, Skrobik Y. Alcohol, nicotine, and iatrogenic withdrawals 
       in the ICU. Crit Care Med. 2013;41(9 Suppl 1):S57-68.
    """
    
    pulse: int = Field(
        ...,
        ge=40,
        le=200,
        description="Pulse rate in beats per minute. <90 bpm = 0 points, 90-110 bpm = 1 point, >110 bpm = 2 points",
        example=95
    )
    
    diastolic_bp: int = Field(
        ...,
        ge=40,
        le=150,
        description="Diastolic blood pressure in mmHg. <90 mmHg = 0 points, 90-110 mmHg = 1 point, >110 mmHg = 2 points",
        example=85
    )
    
    tremor: Literal["absent", "slightly_visible", "moderate_with_arms_extended", "severe_without_extending_arms"] = Field(
        ...,
        description="Tremor severity. Absent (0 pts), slightly visible (2 pts), moderate with arms extended (4 pts), severe without extending arms (6 pts)",
        example="slightly_visible"
    )
    
    sweat: Literal["absent", "barely_moist_palms", "beads_visible", "drenching"] = Field(
        ...,
        description="Diaphoresis severity. Absent (0 pts), barely moist palms (2 pts), beads visible (4 pts), drenching (6 pts)",
        example="barely_moist_palms"
    )
    
    hallucinations: Literal["absent", "mild_sporadic", "moderate_intermittent", "severe_continuous"] = Field(
        ...,
        description="Hallucination presence and severity. Absent (0 pts), mild/sporadic (1 pt), moderate/intermittent (2 pts), severe/continuous (3 pts)",
        example="absent"
    )
    
    agitation: Literal["normal_sedated", "somewhat_increased", "moderately_fidgety", "pacing_thrashing"] = Field(
        ...,
        description="Agitation level based on RASS principles. Normal/sedated (0 pts), somewhat increased (3 pts), moderately fidgety (6 pts), pacing/thrashing (9 pts)",
        example="somewhat_increased"
    )
    
    orientation: Literal["oriented_x3", "oriented_x2", "oriented_x1", "disoriented"] = Field(
        ...,
        description="Orientation to person, place, and time. Oriented x3 (0 pts), x2 (2 pts), x1 (4 pts), disoriented (6 pts)",
        example="oriented_x3"
    )
    
    delusions: Literal["absent_unable_to_assess", "present"] = Field(
        ...,
        description="Presence of delusions. Absent or unable to assess due to sedation (0 pts), present (6 pts)",
        example="absent_unable_to_assess"
    )
    
    seizures: Literal["not_actively_seizing", "actively_seizing"] = Field(
        ...,
        description="Active seizure activity. Not actively seizing (0 pts), actively seizing (6 pts)",
        example="not_actively_seizing"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "pulse": 95,
                "diastolic_bp": 85,
                "tremor": "slightly_visible",
                "sweat": "barely_moist_palms",
                "hallucinations": "absent",
                "agitation": "somewhat_increased",
                "orientation": "oriented_x3",
                "delusions": "absent_unable_to_assess",
                "seizures": "not_actively_seizing"
            }
        }


class ModifiedMinnesotaDetoxificationScaleResponse(BaseModel):
    """
    Response model for Modified Minnesota Detoxification Scale (mMINDS)
    
    The mMINDS score ranges from 0-46 points and stratifies alcohol withdrawal severity:
    
    **Score Interpretation and Management:**
    
    **Minimal Withdrawal (0-10 points):**
    - Minimal to no withdrawal symptoms present
    - Clinical observation may be sufficient
    - Consider symptom-triggered therapy protocols
    - Frequent reassessment recommended as symptoms can progress
    - May not require immediate benzodiazepine therapy
    
    **Mild Withdrawal (11-20 points):**
    - Mild alcohol withdrawal syndrome
    - Consider initiating benzodiazepine therapy
    - Implement symptom-triggered dosing protocols
    - Monitor closely for symptom progression
    - Reassess frequently during first 24-72 hours
    
    **Moderate Withdrawal (21-30 points):**
    - Moderate alcohol withdrawal syndrome requiring active treatment
    - Benzodiazepine therapy indicated with higher doses
    - Consider ICU-level monitoring if score increasing
    - Monitor for progression to delirium tremens
    - Ensure thiamine supplementation and electrolyte management
    
    **Severe Withdrawal (31-46 points):**
    - Severe withdrawal with high risk for delirium tremens
    - Aggressive benzodiazepine therapy required
    - ICU monitoring strongly recommended
    - Consider high-dose or continuous infusion protocols
    - May require additional medications (phenobarbital, propofol)
    - Comprehensive supportive care essential
    
    **Treatment Protocols by Score:**
    
    **Low Risk (≤20 points):**
    - Symptom-triggered benzodiazepine therapy
    - Standard monitoring with vital signs q4-6h
    - Oral medications typically sufficient
    - Consider outpatient management if appropriate
    
    **Moderate Risk (21-30 points):**
    - Scheduled + PRN benzodiazepine therapy
    - Enhanced monitoring with vital signs q2-4h
    - Consider IV access for medication administration
    - Inpatient monitoring recommended
    
    **High Risk (≥31 points):**
    - Intensive benzodiazepine protocols
    - Continuous monitoring in ICU setting
    - IV medication administration
    - Multidisciplinary team involvement
    - Prepare for potential intubation/mechanical ventilation
    
    **Comparison with CIWA-Ar:**
    - mMINDS preferred in ICU and critically ill patients
    - More objective assessment without patient cooperation required
    - Better inter-rater reliability in sedated patients
    - Associated with improved clinical outcomes
    - Can be used in mechanically ventilated patients
    
    **Quality Metrics and Outcomes:**
    - Shorter ICU length of stay compared to CIWA-Ar
    - Reduced total benzodiazepine consumption
    - Decreased incidence of delirium tremens
    - Improved nursing satisfaction and ease of use
    - Better identification of patients needing intensive monitoring
    
    Reference: Hack JB, et al. J Med Toxicol. 2006;2(2):55-60.
    """
    
    result: int = Field(
        ...,
        ge=0,
        le=46,
        description="Modified Minnesota Detoxification Scale score indicating alcohol withdrawal severity (0-46 points)",
        example=7
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the scale",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with withdrawal severity assessment and treatment recommendations based on mMINDS score",
        example="mMINDS Score 7: Minimal alcohol withdrawal symptoms present. Clinical observation may be sufficient with close monitoring for symptom progression. Consider implementing symptom-triggered therapy protocols. Patient may not require benzodiazepine therapy at this time, but frequent reassessment is recommended as withdrawal can progress rapidly."
    )
    
    stage: str = Field(
        ...,
        description="Withdrawal severity category (Minimal, Mild, Moderate, Severe)",
        example="Minimal Withdrawal"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of withdrawal severity level",
        example="Minimal to no withdrawal symptoms"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 7,
                "unit": "points",
                "interpretation": "mMINDS Score 7: Minimal alcohol withdrawal symptoms present. Clinical observation may be sufficient with close monitoring for symptom progression. Consider implementing symptom-triggered therapy protocols. Patient may not require benzodiazepine therapy at this time, but frequent reassessment is recommended as withdrawal can progress rapidly.",
                "stage": "Minimal Withdrawal",
                "stage_description": "Minimal to no withdrawal symptoms"
            }
        }