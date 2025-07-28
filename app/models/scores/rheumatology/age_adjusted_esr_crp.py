"""
Age-Adjusted ESR/CRP for Rheumatoid Arthritis Models

Request and response models for Age-Adjusted ESR/CRP calculation.

References (Vancouver style):
1. Ranganath VK, Elashoff DA, Khanna D, Park G, Peter JB, Paulus HE, et al. 
   Age adjustment corrects for apparent differences in erythrocyte sedimentation 
   rate and C-reactive protein values at the onset of seropositive rheumatoid 
   arthritis in younger and older patients. J Rheumatol. 2005;32(6):1040-2. 
   doi: 10.3899/jrheum.041167.
2. Miller A, Green M, Robinson D. Simple rule for calculating normal erythrocyte 
   sedimentation rate. BMJ. 1983;286(6361):266. doi: 10.1136/bmj.286.6361.266.
3. Wener MH, Daum PR, McQuillan GM. The influence of age, sex, and race on the 
   upper reference limit of serum C-reactive protein concentration. J Rheumatol. 
   2000;27(10):2351-9. PMID: 11036832.
4. Siemons L, ten Klooster PM, Vonkeman HE, van Riel PL, Glas CA, van de Laar MA. 
   How age and sex affect the erythrocyte sedimentation rate and C-reactive protein 
   in early rheumatoid arthritis. BMC Musculoskelet Disord. 2014;15:368. 
   doi: 10.1186/1471-2474-15-368.

The Age-Adjusted ESR/CRP calculator helps clinicians interpret inflammatory markers 
in the context of patient age and sex. Both ESR and CRP naturally increase with age, 
and sex-specific differences exist. Age-adjusted upper limits help distinguish true 
disease activity from age-related increases, particularly important in elderly patients 
with rheumatoid arthritis.

Formulas:
ESR: Male = Age ÷ 2 mm/hr, Female = (Age + 10) ÷ 2 mm/hr
CRP: Male = Age ÷ 50 mg/dL, Female = (Age ÷ 50) + 0.6 mg/dL

This approach has been validated in rheumatoid arthritis patients and helps improve 
the accuracy of disease activity assessment across different age groups.
"""

from pydantic import BaseModel, Field
from typing import Literal, Optional, Dict, Any


class AgeAdjustedEsrCrpRequest(BaseModel):
    """
    Request model for Age-Adjusted ESR/CRP for Rheumatoid Arthritis
    
    The Age-Adjusted ESR/CRP calculator helps clinicians interpret inflammatory 
    markers in the context of patient age and sex, accounting for the natural 
    increase in ESR and CRP with aging.
    
    Parameters:
    - Age: Patient age in years (≥18 years)
    - Sex: Patient sex (affects both ESR and CRP formulas)
      * Male: ESR = Age ÷ 2, CRP = Age ÷ 50
      * Female: ESR = (Age + 10) ÷ 2, CRP = (Age ÷ 50) + 0.6
    - Measured ESR: Optional measured ESR value for comparison
    - Measured CRP: Optional measured CRP value for comparison
    
    Clinical Application:
    - Helps distinguish true disease activity from age-related increases
    - Particularly useful in elderly patients with rheumatoid arthritis
    - Improves accuracy of disease activity assessment
    - Should be used with clinical judgment and other disease measures
    
    Benefits:
    - Age-specific interpretation of inflammatory markers
    - Reduces overestimation of disease activity in elderly patients
    - Evidence-based approach validated in RA patients
    - Accounts for sex-specific differences in inflammatory markers

    References (Vancouver style):
    1. Ranganath VK, Elashoff DA, Khanna D, Park G, Peter JB, Paulus HE, et al. 
    Age adjustment corrects for apparent differences in erythrocyte sedimentation 
    rate and C-reactive protein values at the onset of seropositive rheumatoid 
    arthritis in younger and older patients. J Rheumatol. 2005;32(6):1040-2. 
    doi: 10.3899/jrheum.041167.
    2. Miller A, Green M, Robinson D. Simple rule for calculating normal erythrocyte 
    sedimentation rate. BMJ. 1983;286(6361):266. doi: 10.1136/bmj.286.6361.266.
    3. Wener MH, Daum PR, McQuillan GM. The influence of age, sex, and race on the 
    upper reference limit of serum C-reactive protein concentration. J Rheumatol. 
    2000;27(10):2351-9. PMID: 11036832.
    4. Siemons L, ten Klooster PM, Vonkeman HE, van Riel PL, Glas CA, van de Laar MA. 
    How age and sex affect the erythrocyte sedimentation rate and C-reactive protein 
    in early rheumatoid arthritis. BMC Musculoskelet Disord. 2014;15:368. 
    doi: 10.1186/1471-2474-15-368.
    """
    
    age: int = Field(
        ...,
        description="Patient age in years (must be ≥18 years for adult formulas)",
        ge=18,
        le=120,
        example=65
    )
    
    sex: Literal["male", "female"] = Field(
        ...,
        description="Patient sex (affects both ESR and CRP age-adjustment formulas). Male: ESR = Age ÷ 2, CRP = Age ÷ 50. Female: ESR = (Age + 10) ÷ 2, CRP = (Age ÷ 50) + 0.6",
        example="female"
    )
    
    measured_esr: Optional[float] = Field(
        None,
        description="Measured ESR value in mm/hr (optional, for comparison with age-adjusted upper limit)",
        ge=0,
        le=200,
        example=35.0
    )
    
    measured_crp: Optional[float] = Field(
        None,
        description="Measured CRP value in mg/dL (optional, for comparison with age-adjusted upper limit)",
        ge=0,
        le=50,
        example=1.8
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": 65,
                "sex": "female",
                "measured_esr": 35.0,
                "measured_crp": 1.8
            }
        }


class AgeAdjustedEsrCrpResponse(BaseModel):
    """
    Response model for Age-Adjusted ESR/CRP for Rheumatoid Arthritis
    
    The response provides age-adjusted upper limits for ESR and CRP, along with 
    clinical interpretation. Age-adjusted limits help distinguish true disease 
    activity from age-related increases in inflammatory markers.
    
    Key Benefits:
    - Age-specific interpretation of inflammatory markers
    - Improved accuracy in elderly patients
    - Evidence-based approach for RA assessment
    - Reduces overestimation of disease activity
    
    Clinical Decision Making:
    - Values ≤ age-adjusted limits: Normal for age, no significant inflammation
    - Values > age-adjusted limits: May indicate active disease beyond age-related increases
    - Should be interpreted with clinical context and other disease measures
    
    Important Notes:
    - Age-adjusted limits are higher than conventional limits in elderly patients
    - Formulas validated in rheumatoid arthritis populations
    - Sex-specific differences are accounted for in the calculations
    - Should be used as part of comprehensive disease activity assessment
    
    Reference: Ranganath VK, et al. J Rheumatol. 2005;32(6):1040-2.
    """
    
    result: Dict[str, Any] = Field(
        ...,
        description="Age-adjusted upper limits for ESR and CRP, plus conventional limits for comparison",
        example={
            "esr_age_adjusted_limit": 37.5,
            "crp_age_adjusted_limit": 1.9,
            "esr_conventional_limit": 22,
            "crp_conventional_limit": 0.5
        }
    )
    
    unit: str = Field(
        ...,
        description="Units of measurement (various for different parameters)",
        example="various"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of the age-adjusted limits and measured values (if provided)",
        example="Age-adjusted upper limits for 65-year-old female: ESR ≤37.5 mm/hr, CRP ≤1.9 mg/dL. Conventional limits: ESR ≤22 mm/hr, CRP ≤0.5 mg/dL. Normal (within age-adjusted limits): ESR (35.0 mm/hr), CRP (1.8 mg/dL). No evidence of significant inflammation for this age group. Age-adjustment helps distinguish true disease activity from age-related increases in inflammatory markers, particularly important in elderly patients."
    )
    
    stage: str = Field(
        ...,
        description="Clinical decision category (Normal for Age, Elevated Markers, Age-Adjusted Limits)",
        example="Normal for Age"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the clinical decision category",
        example="All markers within age-adjusted limits"
    )
    
    measured_values: Dict[str, Optional[float]] = Field(
        ...,
        description="Measured ESR and CRP values provided for comparison (if any)",
        example={"esr": 35.0, "crp": 1.8}
    )
    
    elevated_markers: Dict[str, bool] = Field(
        ...,
        description="Indicates which markers (if any) are elevated above age-adjusted limits",
        example={"esr_elevated": False, "crp_elevated": False}
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": {
                    "esr_age_adjusted_limit": 37.5,
                    "crp_age_adjusted_limit": 1.9,
                    "esr_conventional_limit": 22,
                    "crp_conventional_limit": 0.5
                },
                "unit": "various",
                "interpretation": "Age-adjusted upper limits for 65-year-old female: ESR ≤37.5 mm/hr, CRP ≤1.9 mg/dL. Conventional limits: ESR ≤22 mm/hr, CRP ≤0.5 mg/dL. Normal (within age-adjusted limits): ESR (35.0 mm/hr), CRP (1.8 mg/dL). No evidence of significant inflammation for this age group. Age-adjustment helps distinguish true disease activity from age-related increases in inflammatory markers, particularly important in elderly patients.",
                "stage": "Normal for Age",
                "stage_description": "All markers within age-adjusted limits",
                "measured_values": {"esr": 35.0, "crp": 1.8},
                "elevated_markers": {"esr_elevated": False, "crp_elevated": False}
            }
        }