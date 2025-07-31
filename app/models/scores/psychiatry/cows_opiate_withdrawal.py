"""
Clinical Opiate Withdrawal Scale (COWS) for Opiate Withdrawal Models

Request and response models for COWS calculation.

References (Vancouver style):
1. Wesson DR, Ling W. The Clinical Opiate Withdrawal Scale (COWS). 
   Journal of Psychoactive Drugs. 2003;35(2):253-259. 
   doi:10.1080/02791072.2003.10400007
2. Tompkins DA, Bigelow GE, Harrison JA, Johnson RE, Fudala PJ, Strain EC. 
   Concurrent validation of the Clinical Opiate Withdrawal Scale (COWS) and 
   single-item indices against the Clinical Institute Withdrawal Assessment 
   for Alcohol-revised (CIWA-Ar). Drug Alcohol Depend. 2009;105(1-2):154-159.

The Clinical Opiate Withdrawal Scale (COWS) is a clinician-administered assessment 
tool that quantifies the severity of opiate withdrawal symptoms using 11 clinical 
criteria. Developed in 2003 by Wesson and Ling and validated in 2009, COWS provides 
a standardized method for evaluating withdrawal severity to guide treatment decisions, 
particularly for medication-assisted treatment (MAT) and buprenorphine induction.

The scale assesses physiological symptoms (pulse, sweating, pupil size, tremor), 
behavioral symptoms (restlessness, anxiety), and physical manifestations 
(bone/joint aches, GI upset, runny nose, gooseflesh, yawning) with scores 
ranging from 0 to 48 points total.
"""

from pydantic import BaseModel, Field
from typing import Literal


class CowsOpiateWithdrawalRequest(BaseModel):
    """
    Request model for Clinical Opiate Withdrawal Scale (COWS) for Opiate Withdrawal
    
    The COWS score uses 11 clinical symptoms to assess opiate withdrawal severity:
    
    Physiological Symptoms:
    - resting_pulse_rate: Heart rate assessment (≤80, 81-100, 101-120, >120 BPM)
    - sweating: Perspiration and thermal regulation (0-4 points)
    - pupil_size: Pupillary dilation assessment (0-5 points)
    - tremor: Motor tremor severity (0-4 points)
    
    Behavioral/Psychological Symptoms:
    - restlessness: Motor activity and agitation (0-5 points)
    - anxiety_irritability: Mood and anxiety symptoms (0-4 points)
    
    Physical Manifestations:
    - bone_joint_aches: Musculoskeletal discomfort (0-4 points)
    - runny_nose_tearing: Rhinorrhea and lacrimation (0-4 points)
    - gi_upset: Gastrointestinal symptoms including nausea, vomiting, diarrhea (0-5 points)
    - gooseflesh_skin: Piloerection assessment (0-3 points)
    - yawning: Excessive yawning during assessment (0-3 points)
    
    Scoring Ranges:
    - 0-4 points: None to minimal withdrawal
    - 5-12 points: Mild withdrawal symptoms
    - 13-24 points: Moderate withdrawal symptoms
    - 25-36 points: Moderately severe withdrawal symptoms
    - 37-48 points: Severe withdrawal symptoms
    
    Clinical Applications:
    - Guides medication-assisted treatment (MAT) decisions
    - Determines appropriate buprenorphine induction timing
    - Monitors withdrawal progression during treatment
    - Assesses need for intensive monitoring or inpatient care
    
    References (Vancouver style):
    1. Wesson DR, Ling W. The Clinical Opiate Withdrawal Scale (COWS). 
    Journal of Psychoactive Drugs. 2003;35(2):253-259. 
    doi:10.1080/02791072.2003.10400007
    2. Tompkins DA, Bigelow GE, Harrison JA, Johnson RE, Fudala PJ, Strain EC. 
    Concurrent validation of the Clinical Opiate Withdrawal Scale (COWS) and 
    single-item indices against the Clinical Institute Withdrawal Assessment 
    for Alcohol-revised (CIWA-Ar). Drug Alcohol Depend. 2009;105(1-2):154-159.
    """
    
    resting_pulse_rate: Literal["<=80", "81-100", "101-120", ">120"] = Field(
        ...,
        description="Resting pulse rate in beats per minute. ≤80 BPM = 0 points, 81-100 BPM = 1 point, 101-120 BPM = 2 points, >120 BPM = 4 points",
        example="81-100"
    )
    
    sweating: Literal["no_chills_flushing", "subjective_chills", "flushed_moist_face", "beads_on_brow", "streaming_sweat"] = Field(
        ...,
        description="Sweating severity. No chills/flushing = 0 points, subjective chills = 1 point, flushed/moist face = 2 points, beads on brow = 3 points, streaming sweat = 4 points",
        example="subjective_chills"
    )
    
    restlessness: Literal["sits_still", "difficulty_sitting", "frequent_shifting", "unable_to_sit"] = Field(
        ...,
        description="Motor restlessness. Sits still = 0 points, difficulty sitting = 1 point, frequent shifting = 3 points, unable to sit still = 5 points",
        example="difficulty_sitting"
    )
    
    pupil_size: Literal["normal_pinned", "possibly_larger", "moderately_dilated", "extremely_dilated"] = Field(
        ...,
        description="Pupillary assessment. Normal/pinned = 0 points, possibly larger = 1 point, moderately dilated = 2 points, extremely dilated = 5 points",
        example="moderately_dilated"
    )
    
    bone_joint_aches: Literal["not_present", "mild_diffuse", "severe_diffuse", "unable_to_sit_discomfort"] = Field(
        ...,
        description="Bone or joint aches. Not present = 0 points, mild diffuse discomfort = 1 point, severe diffuse aching = 2 points, unable to sit due to discomfort = 4 points",
        example="mild_diffuse"
    )
    
    runny_nose_tearing: Literal["not_present", "nasal_stuffiness", "runny_nose_tearing", "constant_streaming"] = Field(
        ...,
        description="Rhinorrhea or tearing. Not present = 0 points, nasal stuffiness/moist eyes = 1 point, runny nose/tearing = 2 points, constant streaming = 4 points",
        example="nasal_stuffiness"
    )
    
    gi_upset: Literal["no_symptoms", "stomach_cramps", "nausea_loose_stool", "vomiting_diarrhea", "multiple_episodes"] = Field(
        ...,
        description="GI upset including nausea, vomiting, diarrhea. No symptoms = 0 points, stomach cramps = 1 point, nausea/loose stool = 2 points, vomiting/diarrhea = 3 points, multiple episodes = 5 points",
        example="stomach_cramps"
    )
    
    tremor: Literal["no_tremor", "barely_perceptible", "moderate_arms_extended", "severe_rest_tremor"] = Field(
        ...,
        description="Tremor assessment. No tremor = 0 points, barely perceptible = 1 point, moderate with arms extended = 2 points, severe tremor at rest = 4 points",
        example="barely_perceptible"
    )
    
    anxiety_irritability: Literal["none", "occasionally_anxious", "moderately_anxious", "extremely_anxious"] = Field(
        ...,
        description="Anxiety or irritability. None = 0 points, occasionally anxious = 1 point, moderately anxious = 2 points, extremely anxious = 4 points",
        example="moderately_anxious"
    )
    
    gooseflesh_skin: Literal["no_piloerection", "barely_perceptible", "prominent_arms", "extensive_body"] = Field(
        ...,
        description="Gooseflesh skin (piloerection). No piloerection = 0 points, barely perceptible = 1 point, prominent on arms = 2 points, extensive over body = 3 points",
        example="barely_perceptible"
    )
    
    yawning: Literal["no_yawning", "yawning_once_twice", "yawning_three_times", "unable_to_conduct"] = Field(
        ...,
        description="Yawning frequency during assessment. No yawning = 0 points, yawning 1-2 times = 1 point, yawning ≥3 times = 2 points, unable to conduct assessment = 3 points",
        example="yawning_once_twice"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "resting_pulse_rate": "81-100",
                "sweating": "subjective_chills",
                "restlessness": "difficulty_sitting",
                "pupil_size": "moderately_dilated",
                "bone_joint_aches": "mild_diffuse",
                "runny_nose_tearing": "nasal_stuffiness",
                "gi_upset": "stomach_cramps",
                "tremor": "barely_perceptible",
                "anxiety_irritability": "moderately_anxious",
                "gooseflesh_skin": "barely_perceptible",
                "yawning": "yawning_once_twice"
            }
        }


class CowsOpiateWithdrawalResponse(BaseModel):
    """
    Response model for Clinical Opiate Withdrawal Scale (COWS) for Opiate Withdrawal
    
    The COWS score provides a standardized assessment of opiate withdrawal severity 
    to guide clinical decision-making, particularly for medication-assisted treatment 
    and buprenorphine induction timing.
    
    Score Interpretation:
    - 0-4 points: None to minimal withdrawal - No treatment necessary
    - 5-12 points: Mild withdrawal - Supportive care and comfort medications
    - 13-24 points: Moderate withdrawal - Pharmacologic treatment indicated, consider buprenorphine
    - 25-36 points: Moderately severe withdrawal - MAT strongly recommended
    - 37-48 points: Severe withdrawal - Immediate medical intervention required
    
    Clinical Applications:
    - Medication-assisted treatment (MAT) decision-making
    - Buprenorphine induction timing to prevent precipitated withdrawal
    - Monitoring withdrawal progression during treatment
    - Resource allocation and level of care determination
    
    Reference: Wesson DR, Ling W. J Psychoactive Drugs. 2003;35(2):253-259.
    """
    
    result: int = Field(
        ...,
        ge=0,
        le=48,
        description="Total COWS score indicating withdrawal severity (0-48 points)",
        example=15
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the COWS score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with treatment recommendations based on the COWS score",
        example="COWS score of 15 indicates moderate withdrawal symptoms. Pharmacologic treatment is indicated. Consider buprenorphine induction if appropriate. Provide supportive care and frequent monitoring."
    )
    
    stage: str = Field(
        ...,
        description="Withdrawal severity category (None to Minimal, Mild, Moderate, Moderately Severe, Severe)",
        example="Moderate"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the withdrawal severity stage",
        example="Moderate withdrawal symptoms"
    )
    
    calculation_details: dict = Field(
        ...,
        description="Detailed breakdown of symptom scores and clinical recommendations",
        example={
            "symptom_scores": {
                "resting_pulse": 1,
                "sweating": 1,
                "restlessness": 1,
                "pupil_size": 2,
                "bone_joint_aches": 1,
                "runny_nose_tearing": 1,
                "gi_upset": 1,
                "tremor": 1,
                "anxiety_irritability": 2,
                "gooseflesh_skin": 1,
                "yawning": 1
            },
            "treatment_recommendations": "Pharmacologic treatment indicated, consider buprenorphine induction",
            "monitoring_recommendations": "Frequent assessments and symptom management"
        }
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 15,
                "unit": "points",
                "interpretation": "COWS score of 15 indicates moderate withdrawal symptoms. Pharmacologic treatment is indicated. Consider buprenorphine induction if appropriate. Provide supportive care and frequent monitoring.",
                "stage": "Moderate",
                "stage_description": "Moderate withdrawal symptoms",
                "calculation_details": {
                    "symptom_scores": {
                        "resting_pulse": 1,
                        "sweating": 1,
                        "restlessness": 1,
                        "pupil_size": 2,
                        "bone_joint_aches": 1,
                        "runny_nose_tearing": 1,
                        "gi_upset": 1,
                        "tremor": 1,
                        "anxiety_irritability": 2,
                        "gooseflesh_skin": 1,
                        "yawning": 1
                    },
                    "treatment_recommendations": "Pharmacologic treatment indicated, consider buprenorphine induction",
                    "monitoring_recommendations": "Frequent assessments and symptom management"
                }
            }
        }