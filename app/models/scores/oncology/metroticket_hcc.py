"""
Metroticket Calculator for HCC Models

Request and response models for Metroticket HCC survival prediction calculation.

References (Vancouver style):
1. Mazzaferro V, Llovet JM, Miceli R, Bozzetti F, Burroughs AK, Andreola S, et al. 
   Predicting survival after liver transplantation in patients with hepatocellular 
   carcinoma beyond the Milan criteria: a retrospective, exploratory analysis. 
   Lancet Oncol. 2009 Jan;10(1):35-43. doi: 10.1016/S1470-2045(08)70284-5.
2. Mazzaferro V, Sposito C, Zhou J, Pinna AD, De Carlis L, Fan J, et al. 
   Metroticket 2.0 Model for Analysis of Competing Risks of Death After Liver 
   Transplantation for Hepatocellular Carcinoma. Gastroenterology. 2018 
   Jan;154(1):128-139. doi: 10.1053/j.gastro.2017.09.025.
3. Lei JY, Wang WT, Yan LN. "Metroticket" predictor for assessing liver 
   transplantation to treat hepatocellular carcinoma: a single-center analysis 
   in mainland China. World J Gastroenterol. 2013 Nov 28;19(44):8093-8. 
   doi: 10.3748/wjg.v19.i44.8093.

The Metroticket calculator provides individualized survival predictions for patients 
with hepatocellular carcinoma (HCC) undergoing liver transplantation, particularly 
those beyond Milan criteria. It introduced the "up-to-seven" criteria where the sum 
of tumor size (cm) and number should not exceed seven in absence of vascular invasion.
"""

from pydantic import BaseModel, Field, validator
from typing import Literal, Dict, Any


class MetroticketHccRequest(BaseModel):
    """
    Request model for Metroticket Calculator for HCC survival prediction
    
    The Metroticket calculator uses tumor characteristics to predict post-transplant 
    survival in HCC patients. Key innovations include:
    
    1. Up-to-Seven Criteria: Sum of largest tumor size (cm) + number of tumors ≤7
    2. Continuous survival prediction vs. dichotomous in/out criteria
    3. Incorporation of vascular invasion status
    
    Clinical Context:
    Developed from 1,556 patients across 36 European centers, this model expanded 
    transplant eligibility beyond restrictive Milan criteria (single tumor ≤5cm or 
    up to 3 tumors ≤3cm each). The up-to-seven criteria achieved 71.2% 5-year 
    survival, comparable to Milan criteria outcomes.
    
    Important Considerations:
    - Tumor measurements should be based on pre-transplant imaging
    - Only vital tumors ≥1cm should be counted
    - Vascular invasion significantly worsens prognosis
    - Metroticket 2.0 also incorporates AFP levels (not included in this version)
    
    References (Vancouver style):
    1. Mazzaferro V, Llovet JM, Miceli R, Bozzetti F, Burroughs AK, Andreola S, et al. 
       Predicting survival after liver transplantation in patients with hepatocellular 
       carcinoma beyond the Milan criteria: a retrospective, exploratory analysis. 
       Lancet Oncol. 2009 Jan;10(1):35-43. doi: 10.1016/S1470-2045(08)70284-5.
    """
    
    largest_nodule_size: int = Field(
        ...,
        description="Size of the largest vital tumor nodule in millimeters based on "
                    "pre-transplant imaging (CT or MRI). Only tumors showing enhancement "
                    "in arterial phase with washout should be measured. Maximum 99mm.",
        ge=0,
        le=99,
        example=45
    )
    
    number_of_nodules: int = Field(
        ...,
        description="Total number of vital tumor nodules ≥1cm in diameter. Count all "
                    "nodules meeting HCC imaging criteria. The model supports up to 10 "
                    "nodules; patients with more than 10 have very poor prognosis.",
        ge=0,
        le=10,
        example=2
    )
    
    vascular_invasion: Literal["unknown", "absent", "present"] = Field(
        ...,
        description="Presence of macrovascular invasion (portal vein or hepatic vein). "
                    "'unknown' if not definitively assessed on imaging, 'absent' if "
                    "specifically evaluated and not present, 'present' if radiologically "
                    "evident. Microvascular invasion cannot be determined pre-transplant.",
        example="absent"
    )
    
    @validator('largest_nodule_size')
    def validate_nodule_size(cls, v):
        """Ensure nodule size is within valid range"""
        if v < 0:
            raise ValueError("Nodule size cannot be negative")
        if v > 99:
            raise ValueError("Model validated for tumors up to 99mm")
        return v
    
    @validator('number_of_nodules')
    def validate_nodule_count(cls, v):
        """Ensure nodule count is reasonable"""
        if v < 0:
            raise ValueError("Number of nodules cannot be negative")
        if v > 10:
            raise ValueError("Model supports up to 10 nodules")
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "largest_nodule_size": 45,
                "number_of_nodules": 2,
                "vascular_invasion": "absent"
            }
        }


class MetroticketHccResponse(BaseModel):
    """
    Response model for Metroticket Calculator for HCC survival prediction
    
    Provides individualized survival predictions for liver transplant candidates with HCC.
    Key outputs include:
    - Sum score (size in cm + number)
    - Up-to-seven criteria status
    - 3-year and 5-year survival predictions
    
    Clinical Applications:
    - Patient counseling regarding transplant outcomes
    - Transplant listing decisions for borderline candidates
    - Comparison with other expanded criteria (UCSF, etc.)
    - Risk stratification for post-transplant surveillance
    
    Limitations:
    - Less validated than Milan criteria
    - Does not include tumor markers (AFP) - see Metroticket 2.0
    - Assumes complete tumor staging information
    - Outcomes may vary by center expertise and patient selection
    
    Reference: Mazzaferro V, et al. Lancet Oncol. 2009;10(1):35-43.
    """
    
    result: Dict[str, Any] = Field(
        ...,
        description="Dictionary containing sum score, up-to-seven status, and survival predictions",
        example={
            "sum_score": 6.5,
            "within_up_to_seven": True,
            "survival_3_year": 77,
            "survival_5_year": 68
        }
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement (empty for this composite score)",
        example=""
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation including prognosis and transplant recommendations",
        example="Excellent prognosis with predicted 3-year survival of 77% and 5-year "
                "survival of 68%. These patients have outcomes comparable to those within "
                "Milan criteria and are good candidates for liver transplantation."
    )
    
    stage: str = Field(
        ...,
        description="Classification based on up-to-seven criteria and vascular invasion",
        example="Within Up-to-Seven Criteria"
    )
    
    stage_description: str = Field(
        ...,
        description="Description of the patient's tumor burden and criteria status",
        example="Sum = 6.5 (≤7), no vascular invasion"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": {
                    "sum_score": 6.5,
                    "within_up_to_seven": True,
                    "survival_3_year": 77,
                    "survival_5_year": 68
                },
                "unit": "",
                "interpretation": "Excellent prognosis with predicted 3-year survival of 77% "
                                "and 5-year survival of 68%. These patients have outcomes "
                                "comparable to those within Milan criteria and are good "
                                "candidates for liver transplantation.",
                "stage": "Within Up-to-Seven Criteria",
                "stage_description": "Sum = 6.5 (≤7), no vascular invasion"
            }
        }