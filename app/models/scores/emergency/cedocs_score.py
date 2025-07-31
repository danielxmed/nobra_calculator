"""
CEDOCS Score for Emergency Department Overcrowding Models

Request and response models for CEDOCS Score calculation.

References (Vancouver style):
1. Weiss SJ, Rogers DB, Maas F, Ernst AA, Nick TG. Evaluating community ED crowding: 
   the Community ED Overcrowding Scale study. Am J Emerg Med. 2014 Nov;32(11):1357-63. 
   doi: 10.1016/j.ajem.2014.08.035.
2. Weiss SJ, Ernst AA, Derlet R, King R, Bair A, Nick TG. Relationship between the 
   National ED Overcrowding Scale and the number of patients who leave without being 
   seen in an academic ED. Am J Emerg Med. 2005 Jul;23(4):456-61.

The Community Emergency Department Overcrowding Scale (CEDOCS) estimates the severity 
of overcrowding in community emergency departments. Developed specifically for community 
EDs with varying patient volumes, making it more broadly applicable than other scales 
like NEDOCS which were designed for academic centers.

The CEDOCS formula incorporates:
- Critical care patients in ED (number requiring critical care)
- Waiting time of longest admitted patient (minutes)
- Number of patients in waiting room
- Total ED patients to ED beds ratio
- Annual ED visit volume (for volume-based adjustments)
- Optional scaling factor (default 2.0)

CEDOCS Score Levels:
- Level 1 (1-20): Not busy - Normal operations
- Level 2 (21-60): Busy - Increased activity
- Level 3 (61-100): Extremely busy but not overcrowded
- Level 4 (101-140): Overcrowded - Threshold exceeded  
- Level 5 (141-180): Severely overcrowded
- Level 6 (181-200): Dangerously overcrowded

Overcrowding is defined as CEDOCS score > 100.
"""

from pydantic import BaseModel, Field
from typing import Dict, Any, Optional


class CedocsScoreRequest(BaseModel):
    """
    Request model for CEDOCS Score for Emergency Department Overcrowding
    
    The CEDOCS Score uses 6 main parameters to assess ED overcrowding levels:
    
    Core ED Status Parameters:
    - critical_care_patients: Number of patients requiring critical care (ICU-level care)
    - longest_wait_time_minutes: Waiting time of longest admitted patient (boarding time)
    - waiting_room_patients: Number of patients waiting to be seen
    - total_ed_patients: Total current ED census (all patients in department)
    - ed_beds: Licensed ED bed capacity
    
    Volume Context:
    - annual_ed_visits: Annual visit volume (for volume-based adjustments)
    - scaling_factor: Optional multiplier for institutional calibration (default 2.0)
    
    The formula includes complex cubic spline adjustments based on annual visit 
    thresholds to account for different ED sizes and patient mix patterns.
    
    Clinical Applications:
    - Real-time overcrowding assessment for resource allocation
    - Objective measurement for quality improvement initiatives
    - Decision support for diversion protocols and emergency staffing
    - Research tool for studying ED operations and patient flow
    
    Validation: Appropriate for community EDs with ≥18,000 annual visits.
    
    References (Vancouver style):
    1. Weiss SJ, Rogers DB, Maas F, Ernst AA, Nick TG. Evaluating community ED crowding: 
    the Community ED Overcrowding Scale study. Am J Emerg Med. 2014 Nov;32(11):1357-63. 
    doi: 10.1016/j.ajem.2014.08.035.
    2. Weiss SJ, Ernst AA, Derlet R, King R, Bair A, Nick TG. Relationship between the 
    National ED Overcrowding Scale and the number of patients who leave without being 
    seen in an academic ED. Am J Emerg Med. 2005 Jul;23(4):456-61.
    """
    
    critical_care_patients: int = Field(
        ...,
        ge=0,
        le=100,
        description="Number of patients currently requiring critical care in the ED (ICU-level interventions, continuous monitoring, etc.)",
        example=3
    )
    
    longest_wait_time_minutes: int = Field(
        ...,
        ge=0,
        le=2880,
        description="Waiting time in minutes of the longest admitted patient currently boarding in the ED (48 hours = 2880 minutes maximum)",
        example=240
    )
    
    waiting_room_patients: int = Field(
        ...,
        ge=0,
        le=500,
        description="Number of patients currently in the waiting room awaiting initial assessment or triage",
        example=12
    )
    
    total_ed_patients: int = Field(
        ...,
        ge=0,
        le=1000,
        description="Total number of patients currently in the ED including those being treated, boarding, and waiting",
        example=45
    )
    
    ed_beds: int = Field(
        ...,
        ge=1,
        le=500,
        description="Total number of licensed beds in the emergency department (treatment spaces, observation beds, etc.)",
        example=25
    )
    
    annual_ed_visits: int = Field(
        ...,
        ge=1000,
        le=500000,
        description="Annual volume of ED visits for this department (total visits per year, used for volume-based score adjustments)",
        example=35000
    )
    
    scaling_factor: Optional[float] = Field(
        None,
        ge=0.1,
        le=10.0,
        description="Optional scaling factor for institutional calibration (default 2.0 if not specified). Allows adjustment for local validation",
        example=2.0
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "critical_care_patients": 3,
                "longest_wait_time_minutes": 240,
                "waiting_room_patients": 12,
                "total_ed_patients": 45,
                "ed_beds": 25,
                "annual_ed_visits": 35000,
                "scaling_factor": 2.0
            }
        }


class CedocsScoreResponse(BaseModel):
    """
    Response model for CEDOCS Score for Emergency Department Overcrowding
    
    The CEDOCS Score provides a quantitative assessment of ED overcrowding with:
    - Numerical score (typically 1-200+ points)
    - Overcrowding level classification (Level 1-6)
    - Overcrowding status and recommendations
    - Detailed calculation breakdown for transparency
    
    Score Interpretation:
    - Level 1 (1-20): Not busy - Normal operations
    - Level 2 (21-60): Busy - Monitor patient flow
    - Level 3 (61-100): Extremely busy but not overcrowded
    - Level 4 (101-140): Overcrowded - Implement protocols
    - Level 5 (141-180): Severely overcrowded - Emergency measures
    - Level 6 (181-200): Dangerously overcrowded - Crisis intervention
    
    Clinical Impact:
    - Enables objective resource allocation decisions
    - Standardizes overcrowding assessment across institutions
    - Supports research and quality improvement initiatives
    - Provides evidence for staffing and operational decisions
    
    The calculation includes volume-based adjustments using cubic splines
    to account for different ED sizes and patient complexity patterns.
    
    Reference: Weiss SJ, et al. Am J Emerg Med. 2014;32(11):1357-63.
    """
    
    result: Dict[str, Any] = Field(
        ...,
        description="Detailed CEDOCS assessment including score, overcrowding level, and calculation breakdown",
        example={
            "total_score": 89.5,
            "overcrowding_level": "Level 3",
            "overcrowding_status": "High activity",
            "is_overcrowded": False,
            "patient_bed_ratio": 1.8,
            "calculation_breakdown": {
                "input_parameters": {
                    "critical_care_patients": 3,
                    "longest_wait_time_minutes": 240,
                    "waiting_room_patients": 12,
                    "total_ed_patients": 45,
                    "ed_beds": 25,
                    "annual_ed_visits": 35000,
                    "patient_bed_ratio": 1.8
                },
                "calculation_components": {
                    "base_constant": -29.53,
                    "critical_care_contribution": 9.42,
                    "wait_time_contribution": 124.8,
                    "waiting_room_contribution": 13.68,
                    "patient_bed_ratio_contribution": 36.99,
                    "annual_visits_contribution": 43.4,
                    "raw_score": 198.36,
                    "conditional_adjustments": -153.61,
                    "scaling_factor": 2.0
                },
                "volume_adjustments": {
                    "annual_visits": 35000,
                    "adjustments_applied": ["Adjustment A applied (visits >= 18,811)"]
                }
            }
        }
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with overcrowding assessment and management recommendations",
        example="CEDOCS Score 89.5: Extremely busy but not overcrowded. High activity level approaching capacity. Consider proactive measures to prevent overcrowding including expedited discharge planning."
    )
    
    stage: str = Field(
        ...,
        description="Overcrowding level classification (Level 1-6 or Level 6+ for extreme cases)",
        example="Level 3"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the overcrowding level",
        example="Extremely busy but not overcrowded"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": {
                    "total_score": 89.5,
                    "overcrowding_level": "Level 3",
                    "overcrowding_status": "High activity",
                    "is_overcrowded": False,
                    "patient_bed_ratio": 1.8,
                    "calculation_breakdown": {
                        "input_parameters": {
                            "critical_care_patients": 3,
                            "longest_wait_time_minutes": 240,
                            "waiting_room_patients": 12,
                            "total_ed_patients": 45,
                            "ed_beds": 25,
                            "annual_ed_visits": 35000,
                            "patient_bed_ratio": 1.8
                        },
                        "calculation_components": {
                            "base_constant": -29.53,
                            "critical_care_contribution": 9.42,
                            "wait_time_contribution": 124.8,
                            "waiting_room_contribution": 13.68,
                            "patient_bed_ratio_contribution": 36.99,
                            "annual_visits_contribution": 43.4,
                            "raw_score": 198.36,
                            "conditional_adjustments": -153.61,
                            "scaling_factor": 2.0
                        },
                        "volume_adjustments": {
                            "annual_visits": 35000,
                            "adjustments_applied": ["Adjustment A applied (visits >= 18,811)"]
                        }
                    }
                },
                "unit": "points",
                "interpretation": "CEDOCS Score 89.5: Extremely busy but not overcrowded. High activity level approaching capacity. Consider proactive measures to prevent overcrowding including expedited discharge planning.",
                "stage": "Level 3",
                "stage_description": "Extremely busy but not overcrowded"
            }
        }