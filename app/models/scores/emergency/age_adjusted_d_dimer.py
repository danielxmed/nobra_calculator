"""
Age-Adjusted D-dimer for Venous Thromboembolism (VTE) Models

Request and response models for Age-Adjusted D-dimer calculation.

References (Vancouver style):
1. Schouten HJ, Geersing GJ, Koek HL, Zuithoff NP, Janssen KJ, Douma RA, et al. 
   Diagnostic accuracy of conventional or age adjusted D-dimer cut-off values in 
   older patients with suspected venous thromboembolism: systematic review and 
   meta-analysis. BMJ. 2013;346:f2492. doi: 10.1136/bmj.f2492.
2. Righini M, Van Es J, Den Exter PL, Roy PM, Verschuren F, Ghuysen A, et al. 
   Age-adjusted D-dimer cutoff levels to rule out pulmonary embolism: the ADJUST-PE 
   study. JAMA. 2014;311(11):1117-24. doi: 10.1001/jama.2014.2135.
3. Sharp AL, Vinson DR, Alamshaw F, Handler J, Gould MK. An Age-Adjusted D-dimer 
   Threshold for Emergency Department Patients With Suspected Pulmonary Embolus: 
   Accuracy and Clinical Implications. Ann Emerg Med. 2016;67(2):249-257. 
   doi: 10.1016/j.annemergmed.2015.06.024.

The Age-Adjusted D-dimer calculator adjusts D-dimer cutoff values based on patient 
age to improve specificity in patients ≥50 years old while maintaining sensitivity. 
This helps reduce unnecessary imaging studies in elderly patients with suspected VTE.

The formula varies by D-dimer unit type:
- FEU (Fibrinogen Equivalent Units): Age × 10 µg/L
- DDU (D-dimer Units): Age × 5 µg/L

This approach has been validated in multiple studies and is recommended by various 
clinical guidelines for VTE diagnosis in elderly patients.
"""

from pydantic import BaseModel, Field
from typing import Literal, Optional


class AgeAdjustedDDimerRequest(BaseModel):
    """
    Request model for Age-Adjusted D-dimer for VTE
    
    The Age-Adjusted D-dimer calculator helps clinicians determine appropriate 
    D-dimer cutoff values for patients ≥50 years old with suspected VTE.
    
    Parameters:
    - Age: Patient age in years (must be ≥50)
    - D-dimer unit type: Laboratory D-dimer unit type
      * FEU (Fibrinogen Equivalent Units): More common, conventional cutoff ~500 µg/L
      * DDU (D-dimer Units): Less common, conventional cutoff ~250 µg/L
    - D-dimer level: Optional measured D-dimer level for interpretation
    
    Calculation:
    - FEU: Age × 10 µg/L
    - DDU: Age × 5 µg/L
    
    Clinical Use:
    - If measured D-dimer ≤ age-adjusted cutoff: VTE unlikely, no imaging needed
    - If measured D-dimer > age-adjusted cutoff: Cannot rule out VTE, proceed with imaging
    
    Benefits:
    - Improved specificity in elderly patients
    - Reduced unnecessary imaging studies
    - Maintained sensitivity for VTE detection
    - Cost-effective approach to VTE diagnosis

    References (Vancouver style):
    1. Schouten HJ, Geersing GJ, Koek HL, Zuithoff NP, Janssen KJ, Douma RA, et al. 
    Diagnostic accuracy of conventional or age adjusted D-dimer cut-off values in 
    older patients with suspected venous thromboembolism: systematic review and 
    meta-analysis. BMJ. 2013;346:f2492. doi: 10.1136/bmj.f2492.
    2. Righini M, Van Es J, Den Exter PL, Roy PM, Verschuren F, Ghuysen A, et al. 
    Age-adjusted D-dimer cutoff levels to rule out pulmonary embolism: the ADJUST-PE 
    study. JAMA. 2014;311(11):1117-24. doi: 10.1001/jama.2014.2135.
    3. Sharp AL, Vinson DR, Alamshaw F, Handler J, Gould MK. An Age-Adjusted D-dimer 
    Threshold for Emergency Department Patients With Suspected Pulmonary Embolus: 
    Accuracy and Clinical Implications. Ann Emerg Med. 2016;67(2):249-257. 
    doi: 10.1016/j.annemergmed.2015.06.024.
    """
    
    age: int = Field(
        ...,
        description="Patient age in years (must be ≥50 years old for age-adjusted D-dimer)",
        ge=50,
        le=120,
        example=65
    )
    
    d_dimer_unit_type: Literal["FEU", "DDU"] = Field(
        ...,
        description="Type of D-dimer units used by the laboratory. FEU (Fibrinogen Equivalent Units) is more common with conventional cutoff ~500 µg/L. DDU (D-dimer Units) is less common with conventional cutoff ~250 µg/L.",
        example="FEU"
    )
    
    d_dimer_level: Optional[float] = Field(
        None,
        description="Measured D-dimer level in µg/L (optional, for comparison with age-adjusted cutoff)",
        ge=0,
        le=10000,
        example=450.0
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": 65,
                "d_dimer_unit_type": "FEU",
                "d_dimer_level": 450.0
            }
        }


class AgeAdjustedDDimerResponse(BaseModel):
    """
    Response model for Age-Adjusted D-dimer for VTE
    
    The response provides the calculated age-adjusted D-dimer cutoff and clinical 
    interpretation. The age-adjusted approach improves specificity in elderly 
    patients while maintaining sensitivity for VTE detection.
    
    Key Benefits:
    - Reduces false positives in elderly patients
    - Prevents unnecessary imaging studies
    - Maintains diagnostic accuracy
    - Cost-effective VTE evaluation
    
    Clinical Decision Making:
    - Measured D-dimer ≤ age-adjusted cutoff: VTE ruled out, no imaging needed
    - Measured D-dimer > age-adjusted cutoff: VTE cannot be excluded, proceed with imaging
    
    Important Notes:
    - Only applicable to patients ≥50 years old
    - Should be used with clinical probability assessment
    - Not appropriate for high-risk patients who should proceed directly to imaging
    - D-dimer elevation can have many causes besides VTE
    
    Reference: Righini M, et al. JAMA. 2014;311(11):1117-24.
    """
    
    result: float = Field(
        ...,
        description="Age-adjusted D-dimer cutoff value in µg/L",
        example=650.0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the cutoff value",
        example="µg/L"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended next steps based on the cutoff and measured level",
        example="VTE diagnosis UNLIKELY. Measured D-dimer (450.0 µg/L) is ≤ age-adjusted cutoff (650.0 µg/L). No further testing needed. Note: Age-adjusted cutoff (650.0 µg/L) is higher than conventional cutoff (500 µg/L), allowing safe rule-out in elderly patients."
    )
    
    stage: str = Field(
        ...,
        description="Clinical decision category (VTE Ruled Out, Further Testing Required, Age-Adjusted Cutoff)",
        example="VTE Ruled Out"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the clinical decision category",
        example="D-dimer below age-adjusted cutoff"
    )
    
    conventional_cutoff: int = Field(
        ...,
        description="Conventional D-dimer cutoff for the unit type (for comparison)",
        example=500
    )
    
    measured_d_dimer: Optional[float] = Field(
        None,
        description="Measured D-dimer level provided for comparison (if any)",
        example=450.0
    )
    
    vte_ruled_out: Optional[bool] = Field(
        None,
        description="Whether VTE is ruled out based on measured D-dimer vs age-adjusted cutoff (if measured level provided)",
        example=True
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 650.0,
                "unit": "µg/L",
                "interpretation": "VTE diagnosis UNLIKELY. Measured D-dimer (450.0 µg/L) is ≤ age-adjusted cutoff (650.0 µg/L). No further testing needed. Note: Age-adjusted cutoff (650.0 µg/L) is higher than conventional cutoff (500 µg/L), allowing safe rule-out in elderly patients.",
                "stage": "VTE Ruled Out",
                "stage_description": "D-dimer below age-adjusted cutoff",
                "conventional_cutoff": 500,
                "measured_d_dimer": 450.0,
                "vte_ruled_out": True
            }
        }