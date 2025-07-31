"""
Fisher Grading Scale for Subarachnoid Hemorrhage (SAH) Models

Request and response models for Fisher Grading Scale calculation.

References (Vancouver style):
1. Fisher CM, Kistler JP, Davis JM. Relation of cerebral vasospasm to subarachnoid 
   hemorrhage visualized by computerized tomographic scanning. Neurosurgery. 
   1980;6(1):1-9. doi: 10.1227/00006123-198001000-00001.
2. Kistler JP, Crowell RM, Davis KR, Heros R, Ojemann RG, Zervas T, et al. The 
   relation of cerebral vasospasm to the extent and location of subarachnoid blood 
   visualized by CT scan: a prospective study. Neurology. 1983 Apr;33(4):424-36. 
   doi: 10.1212/wnl.33.4.424.

The Fisher Grading Scale is a radiological grading system for subarachnoid hemorrhage 
(SAH) that predicts the risk of cerebral vasospasm based on the amount and distribution 
of blood seen on the initial non-contrast head CT. It remains widely used despite the 
introduction of the Modified Fisher Scale, which some consider more accurate for 
vasospasm prediction.
"""

from pydantic import BaseModel, Field
from typing import Literal


class FisherGradingScaleRequest(BaseModel):
    """
    Request model for Fisher Grading Scale for Subarachnoid Hemorrhage (SAH)
    
    The Fisher Scale grades SAH based on CT findings:
    
    CT Findings Categories:
    - no_sah: No subarachnoid hemorrhage detected (Grade I)
    - diffuse_thin: Diffuse deposition or vertical layer <1mm thick (Grade II)
    - localized_thick: Localized clot and/or vertical layer ≥1mm thick (Grade III)
    - ich_ivh: Intracerebral or intraventricular hemorrhage with diffuse or no SAH (Grade IV)
    
    Vasospasm Risk by Grade:
    - Grade I: Low risk (0-21%)
    - Grade II: Low risk (0-25%)
    - Grade III: Low to high risk (23-96%)
    - Grade IV: Low to moderate risk (0-35%)
    
    Note: The paradoxically lower vasospasm risk in Grade IV compared to Grade III 
    is a known limitation of the original Fisher scale.

    References (Vancouver style):
    1. Fisher CM, Kistler JP, Davis JM. Relation of cerebral vasospasm to subarachnoid 
    hemorrhage visualized by computerized tomographic scanning. Neurosurgery. 
    1980;6(1):1-9. doi: 10.1227/00006123-198001000-00001.
    2. Kistler JP, Crowell RM, Davis KR, Heros R, Ojemann RG, Zervas T, et al. The 
    relation of cerebral vasospasm to the extent and location of subarachnoid blood 
    visualized by CT scan: a prospective study. Neurology. 1983 Apr;33(4):424-36. 
    doi: 10.1212/wnl.33.4.424.
    """
    
    ct_findings: Literal["no_sah", "diffuse_thin", "localized_thick", "ich_ivh"] = Field(
        ...,
        description=(
            "CT scan findings for subarachnoid hemorrhage. "
            "no_sah: No subarachnoid hemorrhage detected (Grade I). "
            "diffuse_thin: Diffuse deposition of subarachnoid blood or vertical layers less than 1mm thick (Grade II). "
            "localized_thick: Localized clots and/or vertical layers of blood 1mm or greater in thickness (Grade III). "
            "ich_ivh: Intracerebral hemorrhage (ICH) or intraventricular hemorrhage (IVH) with diffuse or no subarachnoid blood (Grade IV)"
        ),
        example="localized_thick"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "ct_findings": "localized_thick"
            }
        }


class FisherGradingScaleResponse(BaseModel):
    """
    Response model for Fisher Grading Scale for Subarachnoid Hemorrhage (SAH)
    
    The Fisher scale provides a grade from I to IV based on the initial CT findings,
    which correlates with the risk of developing cerebral vasospasm. Grade III has
    the highest risk of vasospasm (23-96%), while Grade IV paradoxically has a
    lower risk (0-35%).
    
    Reference: Fisher CM, et al. Neurosurgery. 1980;6(1):1-9.
    """
    
    result: int = Field(
        ...,
        description="Fisher grade (1-4) indicating severity of SAH",
        example=3
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement (empty for grade)",
        example=""
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation including vasospasm risk range and CT findings description",
        example="Low to high risk of vasospasm (23-96%). Localized clots and/or vertical layers of blood 1mm or greater in thickness"
    )
    
    stage: str = Field(
        ...,
        description="Fisher grade (Grade I, II, III, or IV)",
        example="Grade III"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the CT findings for this grade",
        example="Localized clot or layer >1mm thick"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 3,
                "unit": "",
                "interpretation": "Low to high risk of vasospasm (23-96%). Localized clots and/or vertical layers of blood 1mm or greater in thickness",
                "stage": "Grade III",
                "stage_description": "Localized clot or layer >1mm thick"
            }
        }