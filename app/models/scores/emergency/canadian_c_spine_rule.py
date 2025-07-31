"""
Canadian C-Spine Rule Models

Request and response models for Canadian C-Spine Rule calculation.

References (Vancouver style):
1. Stiell IG, Wells GA, Vandemheen KL, Clement CM, Lesiuk H, De Maio VJ, et al. 
   The Canadian C-spine rule for radiography in alert and stable trauma patients. 
   JAMA. 2001 Oct 17;286(15):1841-8. doi: 10.1001/jama.286.15.1841.
2. Stiell IG, Clement CM, McKnight RD, Brison R, Schull MJ, Rowe BH, et al. 
   The Canadian C-spine rule versus the NEXUS low-risk criteria in patients with 
   trauma. N Engl J Med. 2003 Dec 25;349(26):2510-8. doi: 10.1056/NEJMoa031375.
3. Stiell IG, Clement CM, Grimshaw J, Brison RJ, Rowe BH, Schull MJ, et al. 
   Implementation of the Canadian C-Spine Rule: prospective 12 centre cluster 
   randomised trial. BMJ. 2009 Oct 29;339:b4146. doi: 10.1136/bmj.b4146.

The Canadian C-Spine Rule is a validated clinical decision tool that safely rules out
cervical spine injury in alert and stable trauma patients. It achieves 100% sensitivity
for clinically significant cervical spine injuries while reducing unnecessary imaging by
approximately 42.5%.
"""

from pydantic import BaseModel, Field
from typing import Literal


class CanadianCSpineRuleRequest(BaseModel):
    """
    Request model for Canadian C-Spine Rule
    
    The Canadian C-Spine Rule applies to alert (GCS 15) and stable trauma patients
    aged ≥16 years with suspected cervical spine injury within 48 hours of trauma.
    
    Exclusions:
    - Non-trauma cases
    - GCS < 15
    - Unstable vital signs
    - Age < 16 years
    - Penetrating trauma
    - Known vertebral disease (ankylosing spondylitis, rheumatoid arthritis, spinal stenosis, previous c-spine surgery)
    - Pregnancy
    
    The rule uses a three-step approach:
    1. Check for high-risk factors (mandate imaging)
    2. Check for low-risk factors (allow ROM testing)
    3. Assess range of motion (if safe to do so)
    
    High-Risk Factors (any present = imaging required):
    - Age ≥65 years
    - Dangerous mechanism of injury
    - Paresthesias in extremities
    
    Low-Risk Factors (allow safe ROM assessment):
    - Simple rear-end MVC
    - Sitting position in ED
    - Ambulatory at any time
    - Delayed onset of neck pain
    - Absence of midline C-spine tenderness
    
    References (Vancouver style):
    1. Stiell IG, Wells GA, Vandemheen KL, Clement CM, Lesiuk H, De Maio VJ, et al. 
    The Canadian C-spine rule for radiography in alert and stable trauma patients. 
    JAMA. 2001 Oct 17;286(15):1841-8. doi: 10.1001/jama.286.15.1841.
    """
    
    age_65_or_over: Literal["yes", "no"] = Field(
        ...,
        description="Is the patient aged 65 years or older? High-risk factor if yes",
        example="no"
    )
    
    dangerous_mechanism: Literal["yes", "no"] = Field(
        ...,
        description="Was there a dangerous mechanism of injury? Includes: fall from elevation >3 feet/5 stairs, axial load to head (e.g., diving), MVC high speed (>100 km/hr)/rollover/ejection, motorized recreational vehicles, bicycle collision. High-risk factor if yes",
        example="no"
    )
    
    paresthesias_in_extremities: Literal["yes", "no"] = Field(
        ...,
        description="Are there paresthesias (numbness/tingling) in the extremities? High-risk factor if yes",
        example="no"
    )
    
    simple_rear_end_mvc: Literal["yes", "no", "not_applicable"] = Field(
        ...,
        description="Was it a simple rear-end motor vehicle collision? Excludes: pushed into oncoming traffic, hit by bus/large truck, rollover, hit by high-speed vehicle. Low-risk factor if yes",
        example="not_applicable"
    )
    
    sitting_position_in_ed: Literal["yes", "no"] = Field(
        ...,
        description="Is the patient sitting upright in the Emergency Department? Low-risk factor if yes",
        example="yes"
    )
    
    ambulatory_at_any_time: Literal["yes", "no"] = Field(
        ...,
        description="Has the patient been ambulatory (able to walk) at any time since the injury? Low-risk factor if yes",
        example="yes"
    )
    
    delayed_onset_neck_pain: Literal["yes", "no"] = Field(
        ...,
        description="Was there delayed (not immediate) onset of neck pain? Low-risk factor if yes",
        example="no"
    )
    
    absence_midline_tenderness: Literal["yes", "no"] = Field(
        ...,
        description="Is there absence of midline cervical spine tenderness on palpation? Low-risk factor if yes",
        example="yes"
    )
    
    able_to_rotate_neck: Literal["yes", "no", "not_assessed"] = Field(
        "not_assessed",
        description="Is the patient able to actively rotate neck 45 degrees left AND right? Only assess if no high-risk factors AND at least one low-risk factor present. NEVER test if high-risk factors present",
        example="yes"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "age_65_or_over": "no",
                "dangerous_mechanism": "no",
                "paresthesias_in_extremities": "no",
                "simple_rear_end_mvc": "not_applicable",
                "sitting_position_in_ed": "yes",
                "ambulatory_at_any_time": "yes",
                "delayed_onset_neck_pain": "no",
                "absence_midline_tenderness": "yes",
                "able_to_rotate_neck": "yes"
            }
        }


class CanadianCSpineRuleResponse(BaseModel):
    """
    Response model for Canadian C-Spine Rule
    
    The rule provides a clear recommendation regarding the need for cervical spine imaging:
    - "Safe to Clear Clinically": No imaging required (100% NPV for CSI)
    - "Imaging Required": Cervical spine radiography or CT indicated
    
    Performance characteristics:
    - Sensitivity: 100% (95% CI 98-100%) for clinically significant CSI
    - Specificity: 42.5% (95% CI 40-44%)
    - Reduces imaging by approximately 42.5% compared to baseline practice
    
    CSI = Clinically Significant Cervical Spine Injury (fracture, dislocation, or 
    ligamentous instability requiring treatment or specialized follow-up)
    
    Reference: Stiell IG, et al. JAMA. 2001;286(15):1841-8.
    """
    
    result: str = Field(
        ...,
        description="Imaging recommendation based on the Canadian C-Spine Rule",
        example="Safe to Clear Clinically"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement (recommendation)",
        example="recommendation"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and detailed explanation of the recommendation",
        example="The patient has low-risk factors allowing safe assessment of range of motion AND can actively rotate neck 45° left and right. The cervical spine can be cleared clinically without imaging."
    )
    
    stage: str = Field(
        ...,
        description="Risk stage or reason for recommendation (High Risk, Clinically Clear, Unable to Rotate, No Low Risk Factors)",
        example="Clinically Clear"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the imaging requirement",
        example="No cervical spine imaging required"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": "Safe to Clear Clinically",
                "unit": "recommendation",
                "interpretation": "The patient has low-risk factors allowing safe assessment of range of motion AND can actively rotate neck 45° left and right. The cervical spine can be cleared clinically without imaging.",
                "stage": "Clinically Clear",
                "stage_description": "No cervical spine imaging required"
            }
        }