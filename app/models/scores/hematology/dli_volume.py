"""
Donor Lymphocyte Infusion (DLI) Volume Models

Request and response models for DLI Volume calculation.

References (Vancouver style):
1. Wingard JR, Hsu J, Hiemenz JW. Hematopoietic Stem Cell Transplantation: A Handbook 
   for Clinicians. 2nd ed. Bethesda, MD: AABB Press; 2010.
2. Schmitz N, Dreger P, Suttorp M, Löffler H, Schmitz B, Pfistner B, et al. Primary 
   transplantation of allogeneic peripheral blood progenitor cells mobilized by 
   filgrastim (granulocyte colony-stimulating factor). Blood. 1995 Mar 1;85(5):1666-72.
3. Kolb HJ, Schattenberg A, Goldman JM, Hertenstein B, Jacobsen N, Arcese W, et al. 
   European Group for Blood and Marrow Transplantation Working Party Chronic Leukemia. 
   Graft-versus-leukemia effect of donor lymphocyte transfusions in marrow grafted patients. 
   Blood. 1995 Nov 1;86(5):2041-50.

The Donor Lymphocyte Infusion (DLI) Volume calculator estimates the total blood volume 
that needs to be processed by apheresis to collect sufficient CD3+ T-lymphocytes for 
therapeutic infusion. DLI is used primarily in allogeneic stem cell transplant recipients 
to treat disease relapse by harnessing the graft-versus-leukemia effect. The calculator 
considers recipient weight, desired CD3+ cell dose, number of planned infusions, collection 
efficiency, and donor lymphocyte parameters to determine the optimal apheresis volume 
while ensuring donor safety.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Union
import math


class DliVolumeRequest(BaseModel):
    """
    Request model for Donor Lymphocyte Infusion (DLI) Volume calculation
    
    The DLI Volume calculator determines apheresis blood volume requirements using:
    
    Clinical Parameters:
    - Recipient weight: Patient weight receiving the DLI (1-300 kg)
    - CD3+ infusion dose: Target dose per kg recipient weight (0.1-1000 × 10⁶ cells/kg)
    - Number of infusions: Planned treatment cycles (1-10)
    - Collection efficiency: Expected lymphocyte recovery percentage (10-90%, typical 50%)
    
    Donor Laboratory Parameters:
    - Donor WBC count: Total white blood cell count (1-50 × 10³/μL)
    - Donor total lymphocytes: Percentage of WBC that are lymphocytes (5-80%)
    - Donor CD3+ lymphocytes: Percentage of lymphocytes that are CD3+ T-cells (30-90%)
    
    Calculation Process:
    1. Calculate absolute CD3+ count in donor blood
    2. Determine total CD3+ cells needed for all infusions
    3. Calculate blood volume required accounting for collection efficiency
    
    Clinical Context:
    - Typical DLI goal: 5×10⁷ CD3+ T-cells/kg recipient body weight
    - Used for treating relapsed hematologic malignancies post-transplant
    - Harnesses graft-versus-leukemia effect for disease control

    References (Vancouver style):
    1. Wingard JR, Hsu J, Hiemenz JW. Hematopoietic Stem Cell Transplantation: A Handbook 
       for Clinicians. 2nd ed. Bethesda, MD: AABB Press; 2010.
    2. Kolb HJ, Schattenberg A, Goldman JM, Hertenstein B, Jacobsen N, Arcese W, et al. 
       European Group for Blood and Marrow Transplantation Working Party Chronic Leukemia. 
       Graft-versus-leukemia effect of donor lymphocyte transfusions in marrow grafted patients. 
       Blood. 1995 Nov 1;86(5):2041-50.
    """
    
    recipient_weight: Union[int, float] = Field(
        ...,
        description="Recipient weight in kg (patient receiving the DLI)",
        ge=1,
        le=300,
        example=70.0
    )
    
    cd3_infusion_dose: Union[int, float] = Field(
        ...,
        description="CD3+ infusion dose target (× 10⁶ cells/kg recipient weight). Typical goal: 50 × 10⁶ cells/kg",
        ge=0.1,
        le=1000,
        example=50.0
    )
    
    number_of_infusions: int = Field(
        ...,
        description="Number of planned DLI treatment cycles",
        ge=1,
        le=10,
        example=1
    )
    
    collection_efficiency: Union[int, float] = Field(
        ...,
        description="Expected lymphocyte collection efficiency as percentage (typical: 50%)",
        ge=10,
        le=90,
        example=50.0
    )
    
    donor_wbc_count: Union[int, float] = Field(
        ...,
        description="Donor white blood cell count (× 10³/μL). Normal range: 4-11 × 10³/μL",
        ge=1,
        le=50,
        example=6.5
    )
    
    donor_total_lymphocytes: Union[int, float] = Field(
        ...,
        description="Donor total lymphocytes as percentage of WBC. Normal range: 20-40%",
        ge=5,
        le=80,
        example=30.0
    )
    
    donor_cd3_lymphocytes: Union[int, float] = Field(
        ...,
        description="Donor CD3+ lymphocytes as percentage of total lymphocytes. Normal range: 60-80%",
        ge=30,
        le=90,
        example=70.0
    )
    
    @field_validator('recipient_weight', 'cd3_infusion_dose', 'collection_efficiency', 
              'donor_wbc_count', 'donor_total_lymphocytes', 'donor_cd3_lymphocytes')
    def validate_numeric_fields(cls, v):
        if not isinstance(v, (int, float)):
            raise ValueError("Value must be a number")
        if math.isnan(v) or math.isinf(v):
            raise ValueError("Value must be a finite number")
        return v
    
    @field_validator('number_of_infusions')
    def validate_infusions(cls, v):
        if not isinstance(v, int):
            raise ValueError("Number of infusions must be an integer")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "recipient_weight": 70.0,
                "cd3_infusion_dose": 50.0,
                "number_of_infusions": 1,
                "collection_efficiency": 50.0,
                "donor_wbc_count": 6.5,
                "donor_total_lymphocytes": 30.0,
                "donor_cd3_lymphocytes": 70.0
            }
        }


class DliVolumeResponse(BaseModel):
    """
    Response model for Donor Lymphocyte Infusion (DLI) Volume calculation
    
    The DLI Volume result provides the total blood volume (in mL) that needs to be 
    processed by apheresis to collect the required CD3+ T-lymphocytes for therapeutic 
    infusion. The result is categorized into volume ranges:
    
    Volume Categories:
    - Low volume (<2,000 mL): Short apheresis procedure, minimal donor impact
    - Moderate volume (2,000-5,000 mL): Standard apheresis procedure
    - High volume (5,000-10,000 mL): Extended procedure, consider donor monitoring
    - Very high volume (>10,000 mL): Multiple sessions recommended for donor safety
    
    Clinical Considerations:
    - Maximum recommended single session: 12,000 mL processed blood volume
    - Higher volumes may require splitting into multiple apheresis sessions
    - Donor safety limits should always be observed
    - Collection efficiency may vary based on donor factors and equipment
    - Linear correlation exists between CD3+ cells collected and processed volume
    
    Safety Guidelines:
    - Ensure donor meets standard apheresis eligibility criteria
    - Monitor donor vital signs and comfort throughout procedure
    - Maintain adequate donor hydration and electrolyte balance
    - Consider pre-medication for longer procedures
    
    Reference: Wingard JR, et al. Hematopoietic Stem Cell Transplantation: A Handbook 
    for Clinicians. 2010.
    """
    
    result: float = Field(
        ...,
        description="Total blood volume needed to process by apheresis (in mL)",
        example=3500.0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the volume",
        example="mL"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and procedure recommendations based on volume requirements",
        example="Moderate blood volume requirement. Standard apheresis procedure. Ensure adequate donor hydration and monitor vital signs."
    )
    
    stage: str = Field(
        ...,
        description="Volume category (Low volume, Moderate volume, High volume, Very high volume)",
        example="Moderate volume"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the volume category",
        example="Standard apheresis procedure"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 3500.0,
                "unit": "mL",
                "interpretation": "Moderate blood volume requirement. Standard apheresis procedure. Ensure adequate donor hydration and monitor vital signs.",
                "stage": "Moderate volume",
                "stage_description": "Standard apheresis procedure"
            }
        }