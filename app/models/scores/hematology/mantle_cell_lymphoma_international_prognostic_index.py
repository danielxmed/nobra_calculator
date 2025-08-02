"""
Mantle Cell Lymphoma International Prognostic Index (MIPI) Models

Request and response models for MIPI calculation.

References (Vancouver style):
1. Hoster E, Dreyling M, Klapper W, Gisselbrecht C, van Hoof A, Kluin-Nelemans HC, et al. 
   A new prognostic index (MIPI) for patients with advanced-stage mantle cell lymphoma. 
   Blood. 2008 Jan 15;111(2):558-65. doi: 10.1182/blood-2007-06-095331.
2. Hoster E, Klapper W, Hermine O, Kluin-Nelemans HC, Walewski J, Trneny M, et al. 
   Confirmation of the mantle-cell lymphoma International Prognostic Index in randomized 
   trials of the European Mantle-Cell Lymphoma Network. J Clin Oncol. 2014 May 1;32(13):1338-46. 
   doi: 10.1200/JCO.2013.52.2466.
3. Geisler CH, Kolstad A, Laurell A, Andersen NS, Pedersen LB, Jerkeman M, et al. 
   Long-term progression-free survival of mantle cell lymphoma after intensive front-line 
   immunochemotherapy with in vivo-purged stem cell rescue: a nonrandomized phase 2 
   multicenter study by the Nordic Lymphoma Group. Blood. 2008 Oct 1;112(7):2687-93. 
   doi: 10.1182/blood-2008-03-147025.

The MIPI is the first prognostic index specifically developed for mantle cell lymphoma (MCL) 
patients. It combines four independent prognostic factors (age, ECOG performance status, 
LDH level, and WBC count) to stratify patients into low, intermediate, and high risk groups. 
The biological MIPI (MIPIb) incorporates Ki-67 proliferation index for enhanced prognostic 
accuracy. This index is more specific to MCL than the International Prognostic Index (IPI) 
and helps guide treatment decisions and clinical trial stratification.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Optional, Any


class MantleCellLymphomaInternationalPrognosticIndexRequest(BaseModel):
    """
    Request model for Mantle Cell Lymphoma International Prognostic Index (MIPI)
    
    The MIPI calculator uses four independent prognostic factors to predict survival 
    in patients with advanced-stage mantle cell lymphoma:
    
    **Four Prognostic Factors:**
    1. **Age**: Continuous variable with significant prognostic impact
    2. **ECOG Performance Status**: Functional status assessment (0-1 vs 2-4)
    3. **Serum LDH**: Reflects tumor burden and tissue damage
    4. **WBC Count**: Indicates disease burden and bone marrow involvement
    
    **Optional Enhancement:**
    - **Ki-67 Index**: Cell proliferation marker for biological MIPI (MIPIb)
    
    **Calculation Formulas:**
    - **MIPI**: (0.03535 × age) + 0.6978 (if ECOG 2-4) + [1.367 × log10(LDH/ULN)] + [0.9393 × log10(WBC)]
    - **MIPIb**: MIPI + (0.02142 × Ki-67 %) when Ki-67 available
    
    **Risk Stratification:**
    - **MIPI < 5.7**: Low risk (5-year OS ~60%)
    - **MIPI 5.7-6.2**: Intermediate risk (median OS ~51 months)
    - **MIPI ≥ 6.2**: High risk (median OS ~29 months)
    
    **MIPIb Risk Stratification (when Ki-67 available):**
    - **MIPIb < 5.7**: Low risk (median OS not reached)
    - **MIPIb 5.7-6.5**: Intermediate risk (median OS ~58 months)
    - **MIPIb ≥ 6.5**: High risk (median OS ~37 months)
    
    **Clinical Applications:**
    - Treatment intensity stratification
    - Clinical trial eligibility assessment
    - Prognostic counseling
    - Stem cell transplantation consideration
    - Risk-adapted therapy selection
    
    **Validation and Performance:**
    - Developed from 455 advanced MCL patients in European trials
    - More specific to MCL than International Prognostic Index (IPI)
    - Validated in multiple independent cohorts
    - Applicable across different treatment eras
    
    References (Vancouver style):
    1. Hoster E, Dreyling M, Klapper W, Gisselbrecht C, van Hoof A, Kluin-Nelemans HC, et al. 
       A new prognostic index (MIPI) for patients with advanced-stage mantle cell lymphoma. 
       Blood. 2008 Jan 15;111(2):558-65. doi: 10.1182/blood-2007-06-095331.
    2. Hoster E, Klapper W, Hermine O, Kluin-Nelemans HC, Walewski J, Trneny M, et al. 
       Confirmation of the mantle-cell lymphoma International Prognostic Index in randomized 
       trials of the European Mantle-Cell Lymphoma Network. J Clin Oncol. 2014 May 1;32(13):1338-46. 
       doi: 10.1200/JCO.2013.52.2466.
    """
    
    age: int = Field(
        ...,
        ge=18,
        le=100,
        description="Patient age in years. Age is a continuous variable in the MIPI formula and significantly impacts prognosis in MCL patients",
        example=65
    )
    
    ecog_performance_status: Literal["0_to_1", "2_to_4"] = Field(
        ...,
        description="ECOG Performance Status scale measuring functional status. 0-1 indicates good performance status, 2-4 indicates poor performance status with significant functional limitations",
        example="0_to_1"
    )
    
    serum_ldh: float = Field(
        ...,
        ge=50,
        le=10000,
        description="Serum lactate dehydrogenase level in U/L. Elevated LDH indicates tissue damage, cellular turnover, or disease burden. Normal values typically range 140-280 U/L",
        example=245.0
    )
    
    ldh_upper_limit_normal: float = Field(
        ...,
        ge=150,
        le=400,
        description="Laboratory's upper limit of normal for serum LDH in U/L. This varies by laboratory and methodology, typically 200-250 U/L. Required for calculating LDH ratio",
        example=240.0
    )
    
    white_blood_cell_count: float = Field(
        ...,
        ge=1.0,
        le=500.0,
        description="White blood cell count in ×10³/μL. Elevated WBC may indicate disease burden, bone marrow involvement, or leukemic phase of MCL. Normal range typically 4-11 ×10³/μL",
        example=8.5
    )
    
    ki67_index: Optional[float] = Field(
        None,
        ge=0,
        le=100,
        description="Ki-67 proliferation index as percentage (0-100%). Optional parameter for calculating biological MIPI (MIPIb). Higher Ki-67 indicates more aggressive disease with increased cell proliferation",
        example=30.0
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": 65,
                "ecog_performance_status": "0_to_1",
                "serum_ldh": 245.0,
                "ldh_upper_limit_normal": 240.0,
                "white_blood_cell_count": 8.5,
                "ki67_index": 30.0
            }
        }


class MantleCellLymphomaInternationalPrognosticIndexResponse(BaseModel):
    """
    Response model for Mantle Cell Lymphoma International Prognostic Index (MIPI)
    
    The MIPI provides prognostic stratification for mantle cell lymphoma patients:
    
    **Low Risk (MIPI <5.7):**
    - 5-year overall survival ~60%
    - Median survival not reached in original studies
    - May consider standard chemotherapy (R-CHOP, R-bendamustine)
    - Less intensive treatment approaches may be appropriate
    
    **Intermediate Risk (MIPI 5.7-6.2):**
    - Median survival ~51 months (58 months for MIPIb)
    - Typically requires systemic treatment at diagnosis
    - Consider intensive chemotherapy or clinical trials
    - May benefit from autologous stem cell transplantation
    
    **High Risk (MIPI ≥6.2):**
    - Median survival ~29 months (37 months for MIPIb)
    - Requires immediate intensive treatment
    - Consider aggressive chemotherapy, clinical trials, or novel therapies
    - Strong consideration for stem cell transplantation
    - May benefit from maintenance therapy
    
    **Clinical Considerations:**
    - Most MCL patients require treatment at diagnosis regardless of risk group
    - MIPI helps guide treatment intensity and transplant consideration
    - Should be used with other clinical factors and patient preferences
    - Ki-67 when available provides additional prognostic information (MIPIb)
    - Regular reassessment during treatment important for modifications
    
    **Treatment Implications:**
    - Risk stratification influences clinical trial eligibility
    - Guides discussion about prognosis and treatment goals
    - Helps inform decisions about experimental vs standard therapy
    - Assists in stem cell transplantation timing and candidacy
    
    Reference: Hoster E, et al. Blood. 2008;111(2):558-65.
    """
    
    result: Dict[str, Any] = Field(
        ...,
        description="Comprehensive MIPI assessment results including score calculation, risk stratification, and clinical parameters analysis",
        example={
            "mipi_score": 5.892,
            "mipib_score": 6.532,
            "score_type": "MIPIb",
            "score_components": {
                "age_component": 2.298,
                "ecog_component": 0,
                "ldh_component": 0.059,
                "wbc_component": 0.895,
                "ki67_component": 0.640
            },
            "ldh_ratio": 1.02,
            "clinical_parameters": {
                "age_years": 65,
                "ecog_status": "0-1",
                "ldh_level": "245.0 U/L",
                "ldh_uln": "240.0 U/L",
                "wbc_count": "8.5 ×10³/μL",
                "ki67_index": "30.0%"
            }
        }
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation with risk stratification, survival estimates, and treatment recommendations based on MIPI or MIPIb score",
        example="MIPIb score of 6.532 indicates high risk group. These patients have a median survival of approximately 37 months. Immediate intensive treatment is required."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, Intermediate Risk, High Risk)",
        example="High Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category and its prognostic implications",
        example="High risk for poor prognosis"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": {
                    "mipi_score": 5.892,
                    "mipib_score": 6.532,
                    "score_type": "MIPIb",
                    "score_components": {
                        "age_component": 2.298,
                        "ecog_component": 0,
                        "ldh_component": 0.059,
                        "wbc_component": 0.895,
                        "ki67_component": 0.640
                    },
                    "ldh_ratio": 1.02,
                    "clinical_parameters": {
                        "age_years": 65,
                        "ecog_status": "0-1",
                        "ldh_level": "245.0 U/L",
                        "ldh_uln": "240.0 U/L",
                        "wbc_count": "8.5 ×10³/μL",
                        "ki67_index": "30.0%"
                    }
                },
                "unit": "points",
                "interpretation": "MIPIb score of 6.532 indicates high risk group. These patients have a median survival of approximately 37 months. Immediate intensive treatment is required. Consider aggressive chemotherapy regimens, clinical trial participation, or novel targeted therapies.",
                "stage": "High Risk",
                "stage_description": "High risk for poor prognosis"
            }
        }