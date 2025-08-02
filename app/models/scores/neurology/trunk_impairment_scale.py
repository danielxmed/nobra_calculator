"""
Trunk Impairment Scale Models

Request and response models for Trunk Impairment Scale calculation.

References (Vancouver style):
1. Verheyden G, Nieuwboer A, Mertin J, Preger R, Kiekens C, De weerdt W. 
   The Trunk Impairment Scale: a new tool to measure motor impairment of the trunk after stroke. 
   Clin Rehabil. 2004;18(3):326-34.
2. Verheyden G, Willems AM, Ooms L, Nieuwboer A. Validity of the trunk impairment scale 
   as a measure of trunk performance in people with Parkinson's disease. 
   Arch Phys Med Rehabil. 2007;88(10):1304-8.

The Trunk Impairment Scale (TIS) quantifies disability after stroke and has been validated 
in Parkinson's disease. It assesses three domains of trunk function: static sitting balance 
(3 items, 0-7 points), dynamic sitting balance (10 items, 0-10 points), and coordination 
(4 items, 0-6 points) for a total possible score of 23 points.

The assessment requires the patient to sit on the edge of a bed/table without back or arm 
support, with thighs fully in contact with the surface, knees bent at 90°, feet hip-width 
apart and flat on the floor, arms resting on legs, and head and trunk in midline position.

A special rule applies: if the patient cannot maintain the basic sitting position without 
support for 10 seconds (static_item_1 = "no"), the total score is 0 and no further 
assessment is performed.

Various dependency rules apply where failing certain items automatically scores 0 for 
related follow-up items (e.g., if dynamic elbow movement fails, the associated shortening 
and compensation assessments score 0).
"""

from pydantic import BaseModel, Field
from typing import Literal


class TrunkImpairmentScaleRequest(BaseModel):
    """
    Request model for Trunk Impairment Scale
    
    The TIS assesses trunk function through 17 items across 3 categories:
    
    Static Sitting Balance (3 items, 0-7 points):
    - Item 1: Basic sitting position maintenance (2 points if yes, 0 if no)
    - Item 2: Therapist crosses patient's legs (2 points if maintains position)
    - Item 3: Patient crosses own legs (0-3 points based on ability)
    
    Dynamic Sitting Balance (10 items, 0-10 points):
    - Items 1-3: Hemiplegic elbow movement with shortening and compensation assessment
    - Items 4-6: Unaffected elbow movement with shortening and compensation assessment
    - Items 7-8: Hemiplegic pelvis lift with compensation assessment
    - Items 9-10: Unaffected pelvis lift with compensation assessment
    
    Coordination (4 items, 0-6 points):
    - Items 1-2: Upper trunk rotation (6x) with speed assessment
    - Items 3-4: Lower trunk rotation (6x) with speed assessment
    
    Starting Position Requirements:
    Patient sits on edge of bed/table without back or arm support, thighs fully in contact 
    with surface, knees bent at 90°, feet hip-width apart and flat on floor, arms resting 
    on legs, head and trunk in midline position.
    
    Special Rules:
    - If static_item_1 = "no", total score is 0 (cannot maintain starting position)
    - Dependency rules apply for dynamic and coordination items
    - Each item can be performed 3 times; highest score is recorded
    
    References:
    1. Verheyden G, Nieuwboer A, Mertin J, Preger R, Kiekens C, De weerdt W. 
       The Trunk Impairment Scale: a new tool to measure motor impairment of the trunk after stroke. 
       Clin Rehabil. 2004;18(3):326-34.
    2. Verheyden G, Willems AM, Ooms L, Nieuwboer A. Validity of the trunk impairment scale 
       as a measure of trunk performance in people with Parkinson's disease. 
       Arch Phys Med Rehabil. 2007;88(10):1304-8.
    """
    
    # Static Sitting Balance Items (3 items, 0-7 points)
    
    static_item_1: Literal["no", "yes"] = Field(
        ...,
        description="Patient maintains starting position without support for 10 seconds. If 'no', total score is 0.",
        example="yes"
    )
    
    static_item_2: Literal["falls_or_cannot_maintain", "maintains_position"] = Field(
        ...,
        description="Therapist crosses unaffected leg over hemiplegic leg - patient maintains sitting position (2 points if maintains position, 0 if falls or cannot maintain)",
        example="maintains_position"
    )
    
    static_item_3: Literal["falls", "cannot_cross_without_arm_support", "crosses_with_displacement_or_assistance", "crosses_without_displacement"] = Field(
        ...,
        description="Patient crosses unaffected leg over the hemiplegic leg (0=falls, 1=cannot cross without arm support, 2=crosses with displacement or assistance, 3=crosses without displacement)",
        example="crosses_without_displacement"
    )
    
    # Dynamic Sitting Balance Items (10 items, 0-10 points)
    
    dynamic_item_1: Literal["falls_needs_support_or_no_touch", "moves_actively_and_touches"] = Field(
        ...,
        description="Patient touches bed/table with hemiplegic elbow and returns to starting position (1 point if moves actively and touches, 0 if falls/needs support/no touch)",
        example="moves_actively_and_touches"
    )
    
    dynamic_item_2: Literal["no_or_opposite_shortening", "appropriate_shortening"] = Field(
        ...,
        description="Repeat item 1 - shortening/lengthening assessment of trunk muscles (1 point if appropriate shortening, 0 if no or opposite shortening). Only assessed if dynamic_item_1 scores 1.",
        example="appropriate_shortening"
    )
    
    dynamic_item_3: Literal["compensation_present", "moves_without_compensation"] = Field(
        ...,
        description="Repeat item 1 - compensation assessment (1 point if moves without compensation, 0 if compensation present). Only assessed if dynamic_item_2 scores 1.",
        example="moves_without_compensation"
    )
    
    dynamic_item_4: Literal["falls_needs_support_or_no_touch", "moves_actively_and_touches"] = Field(
        ...,
        description="Patient touches bed/table with unaffected elbow and returns to starting position (1 point if moves actively and touches, 0 if falls/needs support/no touch)",
        example="moves_actively_and_touches"
    )
    
    dynamic_item_5: Literal["no_or_opposite_shortening", "appropriate_shortening"] = Field(
        ...,
        description="Repeat item 4 - shortening/lengthening assessment of trunk muscles (1 point if appropriate shortening, 0 if no or opposite shortening). Only assessed if dynamic_item_4 scores 1.",
        example="appropriate_shortening"
    )
    
    dynamic_item_6: Literal["compensation_present", "moves_without_compensation"] = Field(
        ...,
        description="Repeat item 4 - compensation assessment (1 point if moves without compensation, 0 if compensation present). Only assessed if dynamic_item_5 scores 1.",
        example="moves_without_compensation"
    )
    
    dynamic_item_7: Literal["no_or_opposite_shortening", "appropriate_shortening"] = Field(
        ...,
        description="Lifts pelvis at hemiplegic side and returns to starting position - shortening/lengthening assessment (1 point if appropriate shortening, 0 if no or opposite shortening)",
        example="appropriate_shortening"
    )
    
    dynamic_item_8: Literal["compensation_present", "moves_without_compensation"] = Field(
        ...,
        description="Repeat item 7 - compensation assessment (1 point if moves without compensation, 0 if compensation present). Only assessed if dynamic_item_7 scores 1.",
        example="moves_without_compensation"
    )
    
    dynamic_item_9: Literal["no_or_opposite_shortening", "appropriate_shortening"] = Field(
        ...,
        description="Lifts pelvis at unaffected side and returns to starting position - shortening/lengthening assessment (1 point if appropriate shortening, 0 if no or opposite shortening)",
        example="appropriate_shortening"
    )
    
    dynamic_item_10: Literal["compensation_present", "moves_without_compensation"] = Field(
        ...,
        description="Repeat item 9 - compensation assessment (1 point if moves without compensation, 0 if compensation present). Only assessed if dynamic_item_9 scores 1.",
        example="moves_without_compensation"
    )
    
    # Coordination Items (4 items, 0-6 points)
    
    coordination_item_1: Literal["hemiplegic_not_moved_3x", "asymmetrical_rotation", "symmetrical_rotation"] = Field(
        ...,
        description="Rotates upper trunk 6x (each shoulder moved forward 3x), hemiplegic side must move first (0=hemiplegic side not moved 3x, 1=asymmetrical rotation, 2=symmetrical rotation)",
        example="symmetrical_rotation"
    )
    
    coordination_item_2: Literal["asymmetrical_rotation", "symmetrical_rotation"] = Field(
        ...,
        description="Repeat item 1 within 6 seconds (0=asymmetrical rotation, 1=symmetrical rotation). Only assessed if coordination_item_1 does not score 0.",
        example="symmetrical_rotation"
    )
    
    coordination_item_3: Literal["hemiplegic_not_moved_3x", "asymmetrical_rotation", "symmetrical_rotation"] = Field(
        ...,
        description="Rotate lower trunk 6x (each knee moved forward 3x), hemiplegic side must move first (0=hemiplegic side not moved 3x, 1=asymmetrical rotation, 2=symmetrical rotation)",
        example="symmetrical_rotation"
    )
    
    coordination_item_4: Literal["asymmetrical_rotation", "symmetrical_rotation"] = Field(
        ...,
        description="Repeat item 3 within 6 seconds (0=asymmetrical rotation, 1=symmetrical rotation). Only assessed if coordination_item_3 does not score 0.",
        example="symmetrical_rotation"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "static_item_1": "yes",
                "static_item_2": "maintains_position",
                "static_item_3": "crosses_without_displacement",
                "dynamic_item_1": "moves_actively_and_touches",
                "dynamic_item_2": "appropriate_shortening",
                "dynamic_item_3": "moves_without_compensation",
                "dynamic_item_4": "moves_actively_and_touches",
                "dynamic_item_5": "appropriate_shortening",
                "dynamic_item_6": "moves_without_compensation",
                "dynamic_item_7": "appropriate_shortening",
                "dynamic_item_8": "moves_without_compensation",
                "dynamic_item_9": "appropriate_shortening",
                "dynamic_item_10": "moves_without_compensation",
                "coordination_item_1": "symmetrical_rotation",
                "coordination_item_2": "symmetrical_rotation",
                "coordination_item_3": "symmetrical_rotation",
                "coordination_item_4": "symmetrical_rotation"
            }
        }


class TrunkImpairmentScaleResponse(BaseModel):
    """
    Response model for Trunk Impairment Scale
    
    The TIS score ranges from 0-23 points and classifies trunk function into 5 categories:
    - 0 points: Severe Impairment (Unable to maintain starting position)
    - 1-7 points: Severe Impairment (Severe trunk motor impairment)
    - 8-15 points: Moderate Impairment (Moderate trunk motor impairment)
    - 16-19 points: Mild Impairment (Mild trunk motor impairment)
    - 20-23 points: Normal/Near Normal (Normal or near-normal trunk function)
    
    Lower scores indicate greater trunk impairment and higher rehabilitation needs.
    The assessment is particularly useful for stroke and Parkinson's disease patients.
    
    Reference: Verheyden G, et al. Clin Rehabil. 2004;18(3):326-34.
    """
    
    result: int = Field(
        ...,
        description="Total Trunk Impairment Scale score calculated from all 17 items (range: 0-23 points)",
        example=18
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and rehabilitation recommendations based on the total score",
        example="Mild trunk impairment with generally good sitting balance but some deficits in coordination or dynamic movements. Rehabilitation should focus on fine-tuning trunk control and coordination."
    )
    
    stage: str = Field(
        ...,
        description="Trunk function category (Severe Impairment, Moderate Impairment, Mild Impairment, Normal/Near Normal)",
        example="Mild Impairment"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the impairment level",
        example="Mild trunk motor impairment"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 18,
                "unit": "points",
                "interpretation": "Mild trunk impairment with generally good sitting balance but some deficits in coordination or dynamic movements. Rehabilitation should focus on fine-tuning trunk control and coordination.",
                "stage": "Mild Impairment",
                "stage_description": "Mild trunk motor impairment"
            }
        }