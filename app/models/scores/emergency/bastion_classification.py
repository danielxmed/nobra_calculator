"""
Bastion Classification of Lower Limb Blast Injuries Models

Request and response models for Bastion Classification.

References (Vancouver style):
1. Jacobs N, Rourke K, Rutherford J, Hicks A, Smith SR, Templeton P, et al. Lower limb injuries 
   caused by improvised explosive devices: Proposed 'Bastion Classification' and prospective 
   validation. Injury. 2014 Sep;45(9):1422-8.
2. Lundy JB, Hobbs CM. 'Bastion Classification': evolution of experience mandates caution when 
   considering using class as predictor for method of temporary vascular control. Injury. 2013 
   Nov;44(11):1671-2.
3. Scerbo MH, Mumm JP, Gates K, Love JD, Wade CE, Holcomb JB, et al. Safety and Appropriateness 
   of Tourniquets in 105 Civilians. Prehosp Emerg Care. 2016 Nov-Dec;20(6):712-722.

The Bastion Classification was developed by military surgeons at Camp Bastion, Afghanistan, 
to provide a comprehensive classification system for lower limb blast injuries that correlates 
with treatment needs and facilitates communication between clinicians.
"""

from pydantic import BaseModel, Field
from typing import Literal


class BastionClassificationRequest(BaseModel):
    """
    Request model for Bastion Classification of Lower Limb Blast Injuries
    
    The classification system stratifies explosion-related lower extremity injuries into 
    five anatomical classes, with additional suffixes denoting associated injuries that 
    are important for treatment and operative planning.
    
    Classes (1-5):
    1. Injury confined to foot
    2. Injury involving lower leg permitting effective below-knee tourniquet application
    3. Injury involving proximal lower leg or thigh, permitting effective above-knee tourniquet application
    4. Proximal thigh injury, preventing effective tourniquet application  
    5. Any injury with buttock involvement
    
    Suffixes:
    - S: Segmental injury (potentially viable tissue distal to the most proximal injury)
    - A: Associated intraperitoneal abdominal injury
    - B: Associated genitalia and perineal injury
    - C: Associated pelvic ring injury
    - D: Associated upper limb injury
    
    In the validation study:
    - 69% of injuries were traumatic amputations
    - 49% of casualties suffered bilateral lower limb amputation
    - Class 3 was most common (49%), but Classes 4-5 accounted for 18% of injuries
    - 98 of 179 injuries (55%) required pneumatic tourniquets
    """
    
    injury_class: Literal[1, 2, 3, 4, 5] = Field(
        ...,
        description="Anatomical level of injury. Class 1: Foot only. Class 2: Lower leg with effective below-knee tourniquet. Class 3: Proximal lower leg/thigh with effective above-knee tourniquet. Class 4: Proximal thigh preventing tourniquet. Class 5: Any injury with buttock involvement",
        example=3
    )
    
    segmental_injury: Literal["yes", "no"] = Field(
        ...,
        description="Presence of potentially viable tissue distal to the most proximal injury. Suffix 'S' is added if present",
        example="no"
    )
    
    abdominal_injury: Literal["yes", "no"] = Field(
        ...,
        description="Associated intraperitoneal abdominal injury. Suffix 'A' is added if present. Found in 11% of validation cohort",
        example="no"
    )
    
    genital_perineal_injury: Literal["yes", "no"] = Field(
        ...,
        description="Associated genitalia and perineal injury. Suffix 'B' is added if present. Found in 40% of validation cohort",
        example="no"
    )
    
    pelvic_ring_injury: Literal["yes", "no"] = Field(
        ...,
        description="Associated pelvic ring injury/fracture. Suffix 'C' is added if present. Found in 9% of validation cohort",
        example="no"
    )
    
    upper_limb_injury: Literal["yes", "no"] = Field(
        ...,
        description="Associated upper limb injury. Suffix 'D' is added if present. Found in 64% of validation cohort",
        example="yes"
    )
    
    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "title": "Class 3 injury with upper limb involvement",
                    "value": {
                        "injury_class": 3,
                        "segmental_injury": "no",
                        "abdominal_injury": "no",
                        "genital_perineal_injury": "no",
                        "pelvic_ring_injury": "no",
                        "upper_limb_injury": "yes"
                    }
                },
                {
                    "title": "Class 5 injury with multiple associated injuries",
                    "value": {
                        "injury_class": 5,
                        "segmental_injury": "yes",
                        "abdominal_injury": "yes",
                        "genital_perineal_injury": "yes",
                        "pelvic_ring_injury": "yes",
                        "upper_limb_injury": "no"
                    }
                }
            ]
        }


class BastionClassificationResponse(BaseModel):
    """
    Response model for Bastion Classification of Lower Limb Blast Injuries
    
    Returns the classification with applicable suffixes and detailed interpretation 
    including management recommendations. The classification correlates with treatment 
    needs such as requirement for operative proximal vascular control or amputation level.
    
    Important: This classification was not designed to correlate with mortality, 
    transfusion requirements, or definitive amputation level.
    
    Reference: Jacobs N, et al. Injury. 2014;45(9):1422-8.
    """
    
    result: str = Field(
        ...,
        description="Bastion Classification with applicable suffixes (e.g., '3-D' for Class 3 with upper limb injury)",
        example="3-D"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the classification",
        example="classification"
    )
    
    interpretation: str = Field(
        ...,
        description="Detailed interpretation including injury description, management recommendations, tourniquet effectiveness, and considerations for associated injuries",
        example="Bastion Class 3: Injury involving proximal lower leg or thigh, permitting effective above-knee tourniquet application. Management: Above-knee tourniquet effective for hemorrhage control (most common pattern: 49%) Tourniquet application is effective for hemorrhage control. Associated injuries: Associated upper limb injury."
    )
    
    stage: str = Field(
        ...,
        description="Primary anatomical classification level",
        example="Class 3"
    )
    
    stage_description: str = Field(
        ...,
        description="Description of the anatomical injury level",
        example="Injury involving proximal lower leg or thigh, permitting effective above-knee tourniquet application"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": "3-D",
                "unit": "classification",
                "interpretation": "Bastion Class 3: Injury involving proximal lower leg or thigh, permitting effective above-knee tourniquet application. Management: Above-knee tourniquet effective for hemorrhage control (most common pattern: 49%) Tourniquet application is effective for hemorrhage control. Associated injuries: Associated upper limb injury.",
                "stage": "Class 3",
                "stage_description": "Injury involving proximal lower leg or thigh, permitting effective above-knee tourniquet application"
            }
        }