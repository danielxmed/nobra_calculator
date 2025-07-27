"""
2023 Emergency Medicine Coding Guide Models

Request and response models for 2023 Emergency Medicine Coding Guide calculation.
"""

from pydantic import BaseModel, Field
from typing import Optional, Literal


class EmergencyMedicineCodingGuide2023Request(BaseModel):
    """
    Request model for 2023 Emergency Medicine Coding Guide
    
    Based on 2023 AMA CPT Evaluation and Management (E/M) coding changes for Emergency Medicine.
    Determines appropriate ED service level (99281-99285) using Medical Decision Making (MDM) criteria.
    
    References:
    1. American Medical Association. CPT® Evaluation and Management (E/M) Code and Guideline Changes. 2023.
    2. MDCalc. 2023 Emergency Medicine Coding Guide. Available at: https://www.mdcalc.com/calc/10454/2023-emergency-medicine-coding-guide
    """
    number_complexity_problems: Literal[2, 3, 4, 5] = Field(
        ..., 
        description=(
            "Number and complexity of problems addressed during encounter. "
            "2 = 1 minor problem; "
            "3 = 2 minor problems OR 1 stable chronic illness OR acute uncomplicated illness/injury OR stable acute illness OR uncomplicated illness requiring hospitalization; "
            "4 = 2+ stable chronic illnesses OR undiagnosed new problem with uncertain outcome OR acute illness with systemic symptoms OR acute complicated injury; "
            "5 = chronic illness with severe exacerbation OR illness/injury with life or body threat"
        ),
        example=3
    )
    tests_ordered: int = Field(
        ..., 
        ge=0, 
        le=20, 
        description=(
            "Total number of unique tests ordered during encounter. "
            "Each unique test counts once (e.g., CBC, troponin, CT scan, EKG, urinalysis). "
            "Multiple results of the same test count as one. "
            "Laboratory panels count as single tests."
        ),
        example=2
    )
    tests_reviewed: int = Field(
        ..., 
        ge=0, 
        le=20, 
        description=(
            "Number of test results reviewed (excluding routine labs). "
            "Includes imaging studies (X-rays, CT, MRI), EKGs, echocardiograms, etc. "
            "Each unique test result reviewed counts once. "
            "Does not include basic lab values that are results-only."
        ),
        example=1
    )
    prior_notes_reviewed: int = Field(
        ..., 
        ge=0, 
        le=20, 
        description=(
            "Number of prior external notes reviewed from outside sources. "
            "Includes records from other hospitals, specialty clinics, primary care offices, or nursing facilities. "
            "Each unique source counts once regardless of number of notes from that source. "
            "Does not include notes from the same hospital system or department."
        ),
        example=0
    )
    independent_historian: Literal["yes", "no"] = Field(
        ..., 
        description=(
            "Whether assessment required an independent historian. "
            "YES = Additional history obtained from family member, caregiver, witness, or guardian "
            "because patient unable to provide complete/reliable history (due to age, dementia, psychosis, etc.) "
            "or confirmatory history was needed. "
            "NO = Patient provided all necessary history independently. "
            "Does not include translation services."
        ),
        example="no"
    )
    independent_interpretation: Literal["yes", "no"] = Field(
        ..., 
        description=(
            "Whether physician provided independent interpretation of diagnostic tests. "
            "YES = Emergency physician interpreted test (X-ray, EKG, etc.) that will also receive "
            "formal interpretation and report from another specialist (radiologist, cardiologist). "
            "NO = No independent interpretation performed, or test was formally interpreted by ordering physician only. "
            "Must be documented with physician's interpretation notes."
        ),
        example="yes"
    )
    external_discussion: Literal["yes", "no"] = Field(
        ..., 
        description=(
            "Whether management or test interpretation was discussed with external professional. "
            "YES = Interactive exchange (phone call, direct conversation) with physician or qualified healthcare professional "
            "from different specialty/group about patient management or test interpretation. "
            "NO = No external professional consultation occurred. "
            "Must be direct communication, not through intermediaries or written notes."
        ),
        example="no"
    )
    risk_level: Literal["minimal", "low", "moderate", "high"] = Field(
        ..., 
        description=(
            "Risk of morbidity, mortality, or complications from patient management decisions. "
            "MINIMAL = Minimal risk of morbidity from additional diagnostic testing or treatment; "
            "LOW = Low risk of morbidity from additional diagnostic testing or treatment; "
            "MODERATE = Prescription drug management, minor/major surgery decision, or limited by social determinants of health; "
            "HIGH = Parenteral controlled substances, elective/emergency major surgery decision, "
            "hospitalization considered, or DNR/de-escalation considered"
        ),
        example="moderate"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "number_complexity_problems": 3,
                "tests_ordered": 2,
                "tests_reviewed": 1,
                "prior_notes_reviewed": 0,
                "independent_historian": "no",
                "independent_interpretation": "yes",
                "external_discussion": "no",
                "risk_level": "moderate"
            }
        }


class EmergencyMedicineCodingGuide2023Response(BaseModel):
    """
    Response model for 2023 Emergency Medicine Coding Guide
    
    Returns the appropriate CPT code for Emergency Department services based on 
    Medical Decision Making (MDM) complexity according to 2023 AMA guidelines.
    
    CPT Code Levels:
    - 99281: Level 1 - No MDM required (may not require physician presence)
    - 99282: Level 2 - Straightforward MDM
    - 99283: Level 3 - Low level MDM  
    - 99284: Level 4 - Moderate level MDM
    - 99285: Level 5 - High level MDM
    
    References:
    1. American Medical Association. CPT® Evaluation and Management (E/M) Code and Guideline Changes. 2023.
    2. MDCalc. 2023 Emergency Medicine Coding Guide. Available at: https://www.mdcalc.com/calc/10454/2023-emergency-medicine-coding-guide
    """
    result: str = Field(
        ..., 
        description=(
            "Emergency Department CPT code (99281-99285) based on Medical Decision Making complexity. "
            "Higher numbers indicate more complex cases requiring higher level of physician service."
        ),
        example="99283"
    )
    unit: str = Field(
        ..., 
        description="Unit of measurement for the result",
        example="CPT code"
    )
    interpretation: str = Field(
        ..., 
        description=(
            "Clinical interpretation explaining the assigned service level, "
            "MDM complexity, and what this means for documentation and billing purposes."
        ),
        example="Emergency department visit requiring low level of medical decision making. Limited complexity with some data review or minimal risk."
    )
    stage: Optional[str] = Field(
        None,
        description=(
            "Emergency Department service level CPT code. "
            "Same as result field - provided for consistency with other medical calculators."
        ),
        example="99283"
    )
    stage_description: Optional[str] = Field(
        None,
        description=(
            "Human-readable description of the ED service level. "
            "Indicates the complexity tier (Level 1-5) for quick reference."
        ),
        example="Level 3 ED Visit"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "99283",
                "unit": "CPT code",
                "interpretation": "Emergency department visit requiring low level of medical decision making. Limited complexity with some data review or minimal risk.",
                "stage": "99283",
                "stage_description": "Level 3 ED Visit"
            }
        }