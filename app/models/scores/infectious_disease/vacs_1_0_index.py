"""
Veterans Aging Cohort Study (VACS) 1.0 Index Models

Request and response models for VACS 1.0 Index calculation.

References (Vancouver style):
1. Justice AC, McGinnis KA, Skanderson M, et al. Towards a combined prognostic index for 
   survival in HIV infection: the role of 'non-HIV' biomarkers. HIV Med. 2010;11(2):143-151.
2. Tate JP, Justice AC, Hughes MD, et al. An internationally generalizable risk index for 
   mortality prediction in HIV-infected adults. AIDS. 2013;27(4):563-572.
3. Justice AC, Dombrowski E, Conigliaro J, et al. Veterans Aging Cohort Study (VACS): 
   Overview and description. Med Care. 2006;44(8 Suppl 2):S13-24.

The Veterans Aging Cohort Study (VACS) 1.0 Index estimates 5-year all-cause mortality risk 
in patients with HIV and/or HCV by integrating HIV-specific biomarkers (CD4 count, HIV-1 RNA) 
with general health indicators including hemoglobin, liver function (FIB-4), kidney function 
(eGFR), and hepatitis C co-infection status.

Scoring Components:
Age: <50y=0, 50-64y=12, ≥65y=27 points
CD4 count: ≥500=0, 350-499=6, 200-349=6, 100-199=10, 50-99=28, <50=29 points
HIV-1 RNA: <500=0, 500-99,999=7, ≥100,000=14 points
Hemoglobin: ≥14=0, 12-13.9=10, 10-11.9=22, <10=38 points
FIB-4 Index: <1.45=0, 1.45-3.25=6, >3.25=25 points
eGFR: ≥60=0, 45-59.9=6, 30-44.9=8, <30=26 points
Hepatitis C: No=0, Yes=5 points

Clinical significance:
- Higher scores indicate increased 5-year mortality risk
- Validated in diverse HIV+ populations including veterans and non-veterans
- Better discrimination than HIV markers alone (C-statistic 0.77 vs 0.74)
- Most accurate in patients with ≥1 year of antiretroviral therapy exposure
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict


class Vacs10IndexRequest(BaseModel):
    """
    Request model for Veterans Aging Cohort Study (VACS) 1.0 Index calculation
    
    The VACS 1.0 Index combines HIV-specific and general health biomarkers to estimate 
    5-year all-cause mortality risk in HIV and/or HCV patients.
    
    Required parameters:
    1. Age (years) - Component of mortality risk assessment
    2. CD4 count (cells/mm³) - Primary HIV immune marker  
    3. HIV-1 RNA (copies/mL) - HIV viral load measurement
    4. Hemoglobin (g/dL) - Anemia assessment
    5. FIB-4 Index - Liver fibrosis marker calculated as (Age × AST)/(Platelet count × √ALT)
    6. eGFR (mL/min/1.73m²) - Kidney function assessment
    7. Hepatitis C co-infection - Present or absent
    
    Point assignment by ranges:
    - Age: <50 (0pts), 50-64 (12pts), ≥65 (27pts)
    - CD4: ≥500 (0pts), 350-499 (6pts), 200-349 (6pts), 100-199 (10pts), 50-99 (28pts), <50 (29pts)
    - HIV RNA: <500 (0pts), 500-99,999 (7pts), ≥100,000 (14pts)
    - Hemoglobin: ≥14 (0pts), 12-13.9 (10pts), 10-11.9 (22pts), <10 (38pts)
    - FIB-4: <1.45 (0pts), 1.45-3.25 (6pts), >3.25 (25pts)
    - eGFR: ≥60 (0pts), 45-59.9 (6pts), 30-44.9 (8pts), <30 (26pts)
    - HCV: No (0pts), Yes (5pts)
    
    Clinical applications:
    - Risk stratification in HIV care
    - Treatment prioritization decisions
    - Monitoring response to interventions
    - Research and quality improvement initiatives
    
    References (Vancouver style):
    1. Justice AC, McGinnis KA, Skanderson M, et al. Towards a combined prognostic index for 
    survival in HIV infection: the role of 'non-HIV' biomarkers. HIV Med. 2010;11(2):143-151.
    2. Tate JP, Justice AC, Hughes MD, et al. An internationally generalizable risk index for 
    mortality prediction in HIV-infected adults. AIDS. 2013;27(4):563-572.
    """
    
    age: int = Field(
        ...,
        ge=18,
        le=120,
        description="Patient's age in years. Used for age-specific mortality risk component",
        example=52
    )
    
    cd4_count: int = Field(
        ...,
        ge=0,
        le=5000,
        description="CD4+ T cell count in cells/mm³. Primary marker of HIV immune function and disease progression",
        example=350
    )
    
    hiv_rna_copies_ml: int = Field(
        ...,
        ge=0,
        le=10000000,
        description="HIV-1 RNA viral load in copies/mL. Undetectable is typically <20-50 copies/mL depending on assay",
        example=10000
    )
    
    hemoglobin_g_dl: float = Field(
        ...,
        ge=3.0,
        le=25.0,
        description="Hemoglobin level in g/dL. Marker of anemia which is associated with increased mortality in HIV",
        example=11.5
    )
    
    fib4_index: float = Field(
        ...,
        ge=0.0,
        le=50.0,
        description="FIB-4 Index for liver fibrosis assessment. Calculated as (Age × AST)/(Platelet count × √ALT). Values >3.25 suggest advanced fibrosis",
        example=2.8
    )
    
    egfr_ml_min: float = Field(
        ...,
        ge=0.0,
        le=200.0,
        description="Estimated glomerular filtration rate in mL/min/1.73m². Marker of kidney function. Normal is typically >90",
        example=75.0
    )
    
    hepatitis_c_coinfection: Literal["yes", "no"] = Field(
        ...,
        description="Hepatitis C virus co-infection status. HCV co-infection is associated with increased liver-related mortality in HIV patients",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": 52,
                "cd4_count": 350,
                "hiv_rna_copies_ml": 10000,
                "hemoglobin_g_dl": 11.5,
                "fib4_index": 2.8,
                "egfr_ml_min": 75.0,
                "hepatitis_c_coinfection": "no"
            }
        }


class Vacs10IndexResponse(BaseModel):
    """
    Response model for Veterans Aging Cohort Study (VACS) 1.0 Index calculation
    
    Returns the VACS 1.0 Index score with clinical interpretation and risk stratification.
    
    Score interpretation ranges:
    - 0-20 points: Low 5-year mortality risk
      → Continue standard HIV care, focus on viral suppression and adherence
    - 21-40 points: Moderate 5-year mortality risk  
      → Enhanced monitoring, address modifiable risk factors
    - 41-60 points: High 5-year mortality risk
      → Intensive management, specialist referrals, aggressive intervention
    - >60 points: Very high 5-year mortality risk
      → Urgent comprehensive care, consider palliative care discussions
    
    Component breakdown shows individual point contributions:
    - Age, CD4, HIV RNA: HIV-specific risk factors
    - Hemoglobin, FIB-4, eGFR: Non-HIV comorbidity markers
    - HCV co-infection: Additional liver disease risk
    
    Clinical utility:
    - Better discrimination than HIV markers alone (C-statistic 0.77 vs 0.74)
    - Validated across diverse populations (veterans, non-veterans, men, women)
    - Applicable to patients with ≥1 year antiretroviral therapy exposure
    - Useful for treatment prioritization and resource allocation
    
    Reference: Tate JP, et al. AIDS. 2013;27(4):563-572.
    """
    
    result: int = Field(
        ...,
        ge=0,
        le=200,
        description="VACS 1.0 Index total score calculated from all components",
        example=38
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the VACS score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with specific recommendations based on score and risk category",
        example="VACS 1.0 Index score of 38 indicates moderate 5-year mortality risk. Enhanced monitoring recommended. Address modifiable risk factors including liver disease (FIB-4 optimization), kidney function preservation, and anemia management. Consider more frequent clinical evaluations and specialist consultations as needed."
    )
    
    stage: str = Field(
        ...,
        description="Risk category based on VACS score (Low Risk, Moderate Risk, High Risk, Very High Risk)",
        example="Moderate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Moderate 5-year mortality risk"
    )
    
    component_breakdown: Dict[str, int] = Field(
        ...,
        description="Individual point contributions from each VACS component for transparency and clinical insight",
        example={
            "age_points": 12,
            "cd4_points": 6,
            "hiv_rna_points": 7,
            "hemoglobin_points": 10,
            "fib4_points": 6,
            "egfr_points": 0,
            "hcv_points": 0
        }
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 41,
                "unit": "points",
                "interpretation": "VACS 1.0 Index score of 41 indicates high 5-year mortality risk. Intensive management recommended. Prioritize aggressive treatment of liver disease, kidney dysfunction, and severe anemia. Consider hepatology, nephrology, and hematology referrals. Implement comprehensive care coordination and frequent monitoring.",
                "stage": "High Risk",
                "stage_description": "High 5-year mortality risk",
                "component_breakdown": {
                    "age_points": 12,
                    "cd4_points": 6,
                    "hiv_rna_points": 7,
                    "hemoglobin_points": 10,
                    "fib4_points": 6,
                    "egfr_points": 0,
                    "hcv_points": 0
                }
            }
        }