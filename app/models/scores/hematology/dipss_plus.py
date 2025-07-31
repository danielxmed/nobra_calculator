"""
DIPSS/DIPSS Plus (Dynamic International Prognostic Scoring System) for Myelofibrosis Models

Request and response models for DIPSS/DIPSS Plus calculation.

References (Vancouver style):
1. Passamonti F, Cervantes F, Vannucchi AM, et al. A dynamic prognostic model to predict 
   survival in primary myelofibrosis: a study by the IWG-MRT (International Working Group 
   for Myeloproliferative Neoplasms Research and Treatment). Blood. 2010;115(9):1703-8. 
   doi: 10.1182/blood-2009-09-245837.
2. Gangat N, Caramazza D, Vaidya R, et al. DIPSS plus: a refined Dynamic International 
   Prognostic Scoring System for primary myelofibrosis that incorporates prognostic 
   information from karyotype, platelet count, and transfusion status. J Clin Oncol. 
   2011;29(4):392-7. doi: 10.1200/JCO.2010.32.2446.

The DIPSS and DIPSS Plus are prognostic scoring systems for primary myelofibrosis that 
can be applied at any point during the disease course. DIPSS uses 5 clinical parameters 
while DIPSS Plus adds 3 additional factors including karyotype for more refined risk 
stratification.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal, Optional


class DipssPlusRequest(BaseModel):
    """
    Request model for DIPSS/DIPSS Plus (Dynamic International Prognostic Scoring System) for Myelofibrosis
    
    The DIPSS and DIPSS Plus stratify patients with primary myelofibrosis into risk categories 
    to predict overall survival:
    
    DIPSS Parameters (5 factors):
    - Age >65 years: 1 point
    - WBC >25,000/μL (25 × 10⁹/L): 1 point
    - Hemoglobin <10 g/dL (100 g/L): 2 points
    - Peripheral blood blast ≥1%: 1 point
    - Constitutional symptoms: 1 point
    
    DIPSS Plus Additional Parameters (3 factors):
    - Unfavorable karyotype: 1 point
    - Platelet count <100,000/μL (100 × 10⁹/L): 1 point
    - Red cell transfusion dependency: 1 point
    
    Constitutional symptoms include:
    - Fever >37.5°C (99.5°F) not due to infection
    - Night sweats
    - Unintentional weight loss >10% in 6 months
    
    Unfavorable karyotype includes:
    - Complex karyotype (≥3 abnormalities)
    - Sole or two abnormalities including: +8, -7/7q-, i(17q), -5/5q-, 12p-, inv(3), or 11q23 rearrangement
    
    References (Vancouver style):
    1. Passamonti F, Cervantes F, Vannucchi AM, et al. A dynamic prognostic model to predict 
    survival in primary myelofibrosis: a study by the IWG-MRT (International Working Group 
    for Myeloproliferative Neoplasms Research and Treatment). Blood. 2010;115(9):1703-8.
    2. Gangat N, Caramazza D, Vaidya R, et al. DIPSS plus: a refined Dynamic International 
    Prognostic Scoring System for primary myelofibrosis that incorporates prognostic 
    information from karyotype, platelet count, and transfusion status. J Clin Oncol. 
    2011;29(4):392-7.
    """
    
    scoring_system: Literal["DIPSS", "DIPSS_Plus"] = Field(
        ...,
        description="Choose DIPSS (when karyotype unavailable) or DIPSS Plus (when karyotype available) scoring system",
        example="DIPSS_Plus"
    )
    
    age_over_65: Literal["yes", "no"] = Field(
        ...,
        description="Patient age greater than 65 years. Scores 1 point if yes",
        example="yes"
    )
    
    wbc_over_25: Literal["yes", "no"] = Field(
        ...,
        description="White blood cell count >25,000/μL (25 × 10⁹/L). Scores 1 point if yes",
        example="no"
    )
    
    hemoglobin_under_10: Literal["yes", "no"] = Field(
        ...,
        description="Hemoglobin <10 g/dL (100 g/L). Scores 2 points if yes (note: higher weight than other factors)",
        example="yes"
    )
    
    peripheral_blast_1_or_more: Literal["yes", "no"] = Field(
        ...,
        description="Peripheral blood blast cells ≥1%. Scores 1 point if yes",
        example="no"
    )
    
    constitutional_symptoms: Literal["yes", "no"] = Field(
        ...,
        description="Constitutional symptoms: fever >37.5°C, night sweats, or weight loss >10% in 6 months. Scores 1 point if yes",
        example="no"
    )
    
    unfavorable_karyotype: Optional[Literal["yes", "no"]] = Field(
        None,
        description="Unfavorable karyotype (complex or specific abnormalities). Required for DIPSS Plus. Scores 1 point if yes",
        example="no"
    )
    
    platelets_under_100: Optional[Literal["yes", "no"]] = Field(
        None,
        description="Platelet count <100,000/μL (100 × 10⁹/L). Required for DIPSS Plus. Scores 1 point if yes",
        example="no"
    )
    
    transfusion_dependent: Optional[Literal["yes", "no"]] = Field(
        None,
        description="Red cell transfusion dependency. Required for DIPSS Plus. Scores 1 point if yes",
        example="no"
    )
    
    @field_validator('unfavorable_karyotype', 'platelets_under_100', 'transfusion_dependent')
    def validate_dipss_plus_params(cls, v, values):
        if values.get('scoring_system') == 'DIPSS_Plus' and v is None:
            raise ValueError('This parameter is required when using DIPSS Plus scoring system')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "scoring_system": "DIPSS_Plus",
                "age_over_65": "yes",
                "wbc_over_25": "no",
                "hemoglobin_under_10": "yes",
                "peripheral_blast_1_or_more": "no",
                "constitutional_symptoms": "no",
                "unfavorable_karyotype": "no",
                "platelets_under_100": "no",
                "transfusion_dependent": "no"
            }
        }


class DipssPlusResponse(BaseModel):
    """
    Response model for DIPSS/DIPSS Plus (Dynamic International Prognostic Scoring System) for Myelofibrosis
    
    Risk categories and median survival:
    
    DIPSS:
    - Low risk (0 points): Median survival not reached
    - Intermediate-1 (1-2 points): 14.2 years
    - Intermediate-2 (3-4 points): 4 years
    - High risk (5-6 points): 1.5 years
    
    DIPSS Plus:
    - Low risk (0 points): 185 months (15.4 years)
    - Intermediate-1 (1 point): 78 months (6.5 years)
    - Intermediate-2 (2-3 points): 35 months (2.9 years)
    - High risk (4-6 points): 16 months (1.3 years)
    
    Clinical applications:
    - Helps identify patients who may benefit from allogeneic stem cell transplantation
    - Guides risk-adapted therapy selection
    - Informs prognosis discussions with patients
    - Stratifies patients for clinical trials
    
    Reference: Passamonti F, et al. Blood. 2010;115(9):1703-8.
    """
    
    result: int = Field(
        ...,
        description="Total DIPSS or DIPSS Plus score (range: 0-6 for DIPSS, 0-8 for DIPSS Plus)",
        example=3
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement (points)",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with risk category, median survival, and management recommendations",
        example="DIPSS Plus Intermediate-2 risk: Median survival 35 months (2.9 years). Consider allogeneic stem cell transplantation evaluation in eligible patients."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low risk, Intermediate-1 risk, Intermediate-2 risk, High risk)",
        example="Intermediate-2 risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Intermediate-2 risk category"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 3,
                "unit": "points",
                "interpretation": "DIPSS Plus Intermediate-2 risk: Median survival 35 months (2.9 years). Consider allogeneic stem cell transplantation evaluation in eligible patients.",
                "stage": "Intermediate-2 risk",
                "stage_description": "Intermediate-2 risk category"
            }
        }