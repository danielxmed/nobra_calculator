"""
Modified Brain Injury Guideline (mBIG) Models

Request and response models for mBIG traumatic brain injury management classification.

References (Vancouver style):
1. Joseph B, Friese RS, Sadoun M, Aziz H, Kulvatunyou N, Pandit V, et al. The BIG 
   (brain injury guidelines) project: defining the management of traumatic brain injury 
   by acute care surgeons. J Trauma Acute Care Surg. 2014 Oct;77(4):597-605. 
   doi: 10.1097/TA.0000000000000379.
2. Hartwell EA, Fang R, Dzandu JK, Edwards KA, Walsh RM, Colombo CJ, et al. A 
   Multicenter Validation of the Modified Brain Injury Guidelines (mBIG): Are They 
   Safe and Effective? J Trauma Acute Care Surg. 2022 Apr 1;92(4):e92-e98. 
   doi: 10.1097/TA.0000000000003527.

The Modified Brain Injury Guideline (mBIG) is an evidence-based algorithm for 
managing traumatic brain injury patients with intracranial hemorrhage. It stratifies 
patients into three management categories (mBIG 1, 2, 3) based on radiographic and 
clinical findings, optimizing resource utilization while maintaining patient safety. 
The mBIG has been validated to safely reduce unnecessary neurosurgical consultations, 
repeat imaging, and hospital admissions.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal


class ModifiedBrainInjuryGuidelineRequest(BaseModel):
    """
    Request model for Modified Brain Injury Guideline (mBIG)
    
    The mBIG stratifies traumatic brain injury patients with intracranial hemorrhage 
    into three management categories based on hierarchical criteria:
    
    **mBIG 3 Criteria (Highest Severity - triggers standard neurosurgical care):**
    - Anticoagulation/antiplatelet medications
    - Epidural hematoma
    - Intraventricular hemorrhage  
    - Displaced skull fracture
    - Subdural hematoma ≥8 mm
    - Intraparenchymal hemorrhage ≥8 mm or multiple
    - Subarachnoid hemorrhage bihemispheric or >3 mm thick
    
    **mBIG 2 Criteria (Intermediate Severity - requires hospital admission):**
    - Blood alcohol level >80 mg/dL
    - Nondisplaced skull fracture
    - Subdural hematoma >4 to <8 mm
    - Intraparenchymal hemorrhage >4 to <8 mm (single)
    - Subarachnoid hemorrhage 1 hemisphere, >3 sulci, 1-3 mm thick
    
    **mBIG 1 (Lowest Severity - ED observation only):**
    - No mBIG 2 or 3 criteria met
    
    **Key Inclusion Criteria:**
    - Traumatic brain injury with intracranial hemorrhage on CT
    - Glasgow Coma Score 13-15
    - No focal neurologic or pupillary findings
    
    References (Vancouver style):
    1. Joseph B, Friese RS, Sadoun M, Aziz H, Kulvatunyou N, Pandit V, et al. The BIG 
       (brain injury guidelines) project: defining the management of traumatic brain injury 
       by acute care surgeons. J Trauma Acute Care Surg. 2014 Oct;77(4):597-605. 
       doi: 10.1097/TA.0000000000000379.
    2. Hartwell EA, Fang R, Dzandu JK, Edwards KA, Walsh RM, Colombo CJ, et al. A 
       Multicenter Validation of the Modified Brain Injury Guidelines (mBIG): Are They 
       Safe and Effective? J Trauma Acute Care Surg. 2022 Apr 1;92(4):e92-e98. 
       doi: 10.1097/TA.0000000000003527.
    """
    
    anticoagulation_antiplatelet: Literal["yes", "no"] = Field(
        ...,
        description="Patient currently on anticoagulation or antiplatelet medications (warfarin, heparin, clopidogrel, aspirin, etc.). This is a mBIG 3 criterion requiring standard neurosurgical care",
        example="no"
    )
    
    epidural_hematoma: Literal["yes", "no"] = Field(
        ...,
        description="Presence of epidural hematoma on head CT scan. This is a mBIG 3 criterion requiring immediate neurosurgical evaluation",
        example="no"
    )
    
    intraventricular_hemorrhage: Literal["yes", "no"] = Field(
        ...,
        description="Presence of intraventricular hemorrhage on head CT scan. This is a mBIG 3 criterion requiring neurosurgical management",
        example="no"
    )
    
    displaced_skull_fracture: Literal["yes", "no"] = Field(
        ...,
        description="Presence of displaced skull fracture on head CT scan. This is a mBIG 3 criterion requiring neurosurgical evaluation",
        example="no"
    )
    
    subdural_hematoma_size: Literal["none", "4mm_or_less", "4_to_8mm", "8mm_or_more"] = Field(
        ...,
        description="Maximum thickness of subdural hematoma on head CT. ≥8mm triggers mBIG 3, 4-8mm triggers mBIG 2, ≤4mm or none allows mBIG 1",
        example="none"
    )
    
    intraparenchymal_hemorrhage_size: Literal["none", "4mm_or_less_single", "4_to_8mm_single", "8mm_or_more_or_multiple"] = Field(
        ...,
        description="Size and number of intraparenchymal hemorrhages. ≥8mm or multiple triggers mBIG 3, single 4-8mm triggers mBIG 2, single ≤4mm or none allows mBIG 1",
        example="none"
    )
    
    subarachnoid_hemorrhage_extent: Literal["none", "limited_1_3mm", "1_hemisphere_over_3_sulci_1_3mm", "bihemispheric_or_over_3mm"] = Field(
        ...,
        description="Extent and thickness of subarachnoid hemorrhage. Bihemispheric or >3mm triggers mBIG 3, unilateral extensive (>3 sulci) 1-3mm triggers mBIG 2",
        example="none"
    )
    
    blood_alcohol_level: Literal["unknown_or_under_80", "over_80_mg_dl"] = Field(
        ...,
        description="Blood alcohol level status. >80 mg/dL triggers mBIG 2 classification requiring hospital admission",
        example="unknown_or_under_80"
    )
    
    nondisplaced_skull_fracture: Literal["yes", "no"] = Field(
        ...,
        description="Presence of nondisplaced (linear) skull fracture on head CT. This is a mBIG 2 criterion requiring hospital admission",
        example="no"
    )
    
    @field_validator('subdural_hematoma_size', 'intraparenchymal_hemorrhage_size', 'subarachnoid_hemorrhage_extent')
    def validate_hemorrhage_assessment(cls, v, info):
        """Validate that hemorrhage assessments are clinically reasonable"""
        if info.field_name == 'subdural_hematoma_size' and v not in ["none", "4mm_or_less", "4_to_8mm", "8mm_or_more"]:
            raise ValueError("Invalid subdural hematoma size category")
        return v
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "anticoagulation_antiplatelet": "no",
                "epidural_hematoma": "no", 
                "intraventricular_hemorrhage": "no",
                "displaced_skull_fracture": "no",
                "subdural_hematoma_size": "4mm_or_less",
                "intraparenchymal_hemorrhage_size": "4mm_or_less_single",
                "subarachnoid_hemorrhage_extent": "limited_1_3mm",
                "blood_alcohol_level": "unknown_or_under_80",
                "nondisplaced_skull_fracture": "no"
            }
        }
    }


class ModifiedBrainInjuryGuidelineResponse(BaseModel):
    """
    Response model for Modified Brain Injury Guideline (mBIG)
    
    The mBIG classification determines appropriate management strategy:
    
    **mBIG 1 (Lowest Severity):**
    - 6-hour ED observation with Q2 neurological assessments
    - No repeat head CT required
    - No neurosurgery consultation needed
    - Discharge when GCS = 15
    - Validated as safe with significant resource savings
    
    **mBIG 2 (Intermediate Severity):**
    - Hospital admission to general medical floor for 24-48 hours
    - Q2 neurological assessments
    - No repeat head CT required
    - No neurosurgery consultation needed
    - Discharge when GCS = 15
    
    **mBIG 3 (Highest Severity):**
    - Continue with standard of care at institution
    - Neurosurgical consultation required
    - Intensive monitoring and management
    - Full neurosurgical evaluation and treatment
    
    **Clinical Impact:**
    Studies demonstrate that mBIG implementation results in:
    - 57% of patients discharged from ED (vs 4% pre-mBIG)
    - >$250,000 cost savings over 2 years
    - No patient deterioration in mBIG 1 category
    - Safe reduction in unnecessary consultations and imaging
    
    Reference: Hartwell EA, et al. J Trauma Acute Care Surg. 2022;92(4):e92-e98.
    """
    
    result: int = Field(
        ...,
        ge=1,
        le=3,
        description="mBIG classification category (1=lowest severity, 2=intermediate, 3=highest severity)",
        example=1
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement (empty for categorical result)",
        example=""
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with detailed management recommendations based on mBIG category",
        example="mBIG 1 classification indicates lowest severity traumatic brain injury. Management: 6-hour ED observation with Q2 neurological assessments. No repeat head CT required, no neurosurgery consultation needed. Patient can be safely discharged when GCS returns to 15."
    )
    
    stage: str = Field(
        ...,
        description="mBIG category classification (mBIG 1, mBIG 2, mBIG 3)",
        example="mBIG 1"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the severity level and management approach",
        example="Lowest severity - No admission required"
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "result": 1,
                "unit": "",
                "interpretation": "mBIG 1 classification indicates lowest severity traumatic brain injury. Management: 6-hour ED observation with Q2 neurological assessments. No repeat head CT required, no neurosurgery consultation needed. Patient can be safely discharged when GCS returns to 15. This approach has been validated to be safe and significantly reduces resource utilization.",
                "stage": "mBIG 1",
                "stage_description": "Lowest severity - No admission required"
            }
        }
    }