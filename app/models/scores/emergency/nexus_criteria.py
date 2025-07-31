"""
NEXUS Criteria for C-Spine Imaging Models

Request and response models for NEXUS Criteria calculation.

References (Vancouver style):
1. Hoffman JR, Mower WR, Wolfson AB, Todd KH, Zucker MI. Validity of a set of clinical 
   criteria to rule out injury to the cervical spine in patients with blunt trauma. 
   N Engl J Med. 2000 Jul 13;343(2):94-99. doi: 10.1056/NEJM200007133430203.
2. Stiell IG, Wells GA, Vandemheen KL, Clement CM, Lesiuk H, De Maio VJ, et al. 
   The Canadian C-spine rule versus the NEXUS low-risk criteria in patients with trauma. 
   N Engl J Med. 2003 Dec 25;349(26):2510-8. doi: 10.1056/NEJMoa031375.
3. Paykin G, O'Reilly G, Ackland HM, Mitra B. The NEXUS criteria are insufficient 
   to exclude cervical spine fractures in older blunt trauma patients. Injury. 
   2017 May;48(5):1020-1024. doi: 10.1016/j.injury.2017.02.013.

The NEXUS (National Emergency X-Radiography Utilization Study) criteria are a set of 
validated clinical decision rules used to determine which blunt trauma patients do not 
require cervical spine imaging. The criteria help reduce unnecessary radiation exposure 
while maintaining high sensitivity (99.6%) for detecting clinically significant cervical 
spine injuries.

All five criteria must be met for the patient to be classified as low risk:
1. No midline cervical spine tenderness
2. No focal neurologic deficit  
3. Normal alertness/level of consciousness
4. No evidence of intoxication
5. No painful distracting injury

Mnemonic: NSAID (Neurologic deficit absent, Spinal tenderness absent, Alertness normal, 
Intoxication absent, Distracting injury absent)
"""

from pydantic import BaseModel, Field
from typing import Literal


class NexusCriteriaRequest(BaseModel):
    """
    Request model for NEXUS Criteria for C-Spine Imaging
    
    The NEXUS criteria help determine which blunt trauma patients do not require 
    cervical spine imaging. All five criteria must be met for low risk classification:
    
    1. Midline Cervical Tenderness: Midline posterior bony cervical spine tenderness 
       on palpation from nuchal ridge to first thoracic vertebra prominence. Pain on 
       palpation of posterior midline neck or any cervical spinous process.
    
    2. Focal Neurologic Deficit: Any focal neurologic deficit including weakness, 
       numbness, sensory changes, or motor dysfunction.
    
    3. Altered Alertness: Normal level of consciousness - alert, oriented, and 
       cooperative. Altered includes confusion, disorientation, or decreased consciousness.
    
    4. Intoxication: Evidence of intoxication from alcohol, drugs, or other substances 
       that may impair clinical assessment.
    
    5. Distracting Injury: Painful injury that may impair the reliability of the 
       physical examination or distract from cervical spine pain.
    
    References (Vancouver style):
    1. Hoffman JR, Mower WR, Wolfson AB, Todd KH, Zucker MI. Validity of a set of clinical 
       criteria to rule out injury to the cervical spine in patients with blunt trauma. 
       N Engl J Med. 2000 Jul 13;343(2):94-99. doi: 10.1056/NEJM200007133430203.
    2. Stiell IG, Wells GA, Vandemheen KL, Clement CM, Lesiuk H, De Maio VJ, et al. 
       The Canadian C-spine rule versus the NEXUS low-risk criteria in patients with trauma. 
       N Engl J Med. 2003 Dec 25;349(26):2510-8. doi: 10.1056/NEJMoa031375.
    """
    
    midline_cervical_tenderness: Literal["absent", "present"] = Field(
        ...,
        description="Midline posterior bony cervical spine tenderness on palpation from nuchal ridge to first thoracic vertebra. 'absent' = no tenderness, 'present' = tenderness on palpation",
        example="absent"
    )
    
    focal_neurologic_deficit: Literal["absent", "present"] = Field(
        ...,
        description="Any focal neurologic deficit including weakness, numbness, sensory changes, or motor dysfunction. 'absent' = no deficits, 'present' = neurologic deficits present",
        example="absent"
    )
    
    altered_alertness: Literal["normal", "altered"] = Field(
        ...,
        description="Level of consciousness and alertness. 'normal' = alert, oriented, cooperative; 'altered' = confusion, disorientation, or decreased consciousness",
        example="normal"
    )
    
    intoxication: Literal["absent", "present"] = Field(
        ...,
        description="Evidence of intoxication from alcohol, drugs, or other substances that may impair clinical assessment. 'absent' = no intoxication, 'present' = evidence of intoxication",
        example="absent"
    )
    
    distracting_injury: Literal["absent", "present"] = Field(
        ...,
        description="Painful injury that may impair the reliability of the physical examination or distract from cervical spine pain. 'absent' = no distracting injuries, 'present' = distracting painful injuries present",
        example="absent"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "midline_cervical_tenderness": "absent",
                "focal_neurologic_deficit": "absent",
                "altered_alertness": "normal",
                "intoxication": "absent",
                "distracting_injury": "absent"
            }
        }


class NexusCriteriaResponse(BaseModel):
    """
    Response model for NEXUS Criteria for C-Spine Imaging
    
    The NEXUS criteria classify patients as either low risk (no imaging required) or 
    high risk (imaging recommended) based on five clinical criteria. All criteria 
    must be met for low risk classification.
    
    Performance characteristics:
    - Sensitivity: 99.6% (95% CI: 98.6-100%)
    - Specificity: 12.9%
    - Negative predictive value: 99.8%
    - Validated in over 34,000 patients
    
    Important limitations:
    - Less reliable in patients >65 years of age
    - Use caution in pediatric patients (<18 years)
    - Canadian C-Spine Rule may be more sensitive
    - Validated in blunt trauma patients only
    
    Reference: Hoffman JR, et al. N Engl J Med. 2000;343(2):94-99.
    """
    
    result: str = Field(
        ...,
        description="Risk assessment and imaging recommendation based on NEXUS criteria",
        example="Low Risk - No Imaging Required"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement (empty for this score)",
        example=""
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended management based on risk assessment",
        example="Patient meets all five NEXUS criteria and is at low risk for cervical spine injury. Cervical spine imaging can be safely avoided. Sensitivity 99.6% for detecting clinically significant cervical spine injuries."
    )
    
    stage: str = Field(
        ...,
        description="Risk classification (Low Risk or High Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk classification",
        example="No cervical spine imaging required"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": "Low Risk - No Imaging Required",
                "unit": "",
                "interpretation": "Patient meets all five NEXUS criteria and is at low risk for cervical spine injury. Cervical spine imaging can be safely avoided. Sensitivity 99.6% for detecting clinically significant cervical spine injuries.",
                "stage": "Low Risk",
                "stage_description": "No cervical spine imaging required"
            }
        }