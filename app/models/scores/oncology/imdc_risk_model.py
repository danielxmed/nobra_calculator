"""
IMDC (International Metastatic RCC Database Consortium) Risk Model Models

Request and response models for IMDC Risk Model calculation.

References (Vancouver style):
1. Heng DY, Xie W, Regan MM, Warren MA, Golshayan AR, Sahi C, et al. Prognostic factors for 
   overall survival in patients with metastatic renal cell carcinoma treated with vascular 
   endothelial growth factor-targeted agents: results from a large, multicenter study. 
   J Clin Oncol. 2009 Dec 1;27(34):5794-9. doi: 10.1200/JCO.2008.21.4809

2. Heng DY, Xie W, Regan MM, Harshman LC, Bjarnason GA, Vaishampayan UN, et al. External 
   validation and comparison with other models of the International Metastatic Renal-Cell 
   Carcinoma Database Consortium prognostic model: a population-based study. Lancet Oncol. 
   2013 Feb;14(2):141-8. doi: 10.1016/S1470-2045(12)70559-4

3. Motzer RJ, Tannir NM, McDermott DF, Arén Frontera O, Melichar B, Choueiri TK, et al. 
   Nivolumab plus Ipilimumab versus Sunitinib in Advanced Renal-Cell Carcinoma. N Engl J Med. 
   2018 Apr 5;378(14):1277-1290. doi: 10.1056/NEJMoa1712126

The IMDC Risk Model (also known as Heng criteria or IMDC criteria) is the gold standard 
for risk stratification in patients with metastatic renal cell carcinoma (mRCC). It uses 
6 clinical and laboratory variables to predict overall survival and guide treatment selection. 
The model has been validated across multiple treatment settings including VEGF-targeted therapy 
and modern immunotherapy combinations. It stratifies patients into three risk categories: 
Favorable (0 factors), Intermediate (1-2 factors), and Poor (3-6 factors), with median 
overall survivals of 43.2, 22.5, and 7.8 months respectively.
"""

from pydantic import BaseModel, Field
from typing import Literal


class ImdcRiskModelRequest(BaseModel):
    """
    Request model for IMDC (International Metastatic RCC Database Consortium) Risk Model
    
    The IMDC Risk Model uses 6 prognostic factors to predict survival in patients with 
    metastatic renal cell carcinoma treated with systemic therapy:
    
    Risk Factors (1 point each if present):
    - Time from RCC diagnosis to systemic therapy <1 year
    - Karnofsky Performance Status <80%
    - Hemoglobin below lower limit of normal
    - Corrected calcium above upper limit of normal
    - Neutrophil count above upper limit of normal
    - Platelet count above upper limit of normal
    
    Risk Categories:
    - Favorable (0 factors): Median OS 43.2 months
    - Intermediate (1-2 factors): Median OS 22.5 months
    - Poor (3-6 factors): Median OS 7.8 months
    
    Clinical Applications:
    - Treatment selection for first-line therapy
    - Patient counseling and prognosis discussion
    - Clinical trial stratification
    - Treatment sequencing decisions
    
    Treatment Recommendations:
    - Favorable risk: Pazopanib or sunitinib monotherapy preferred
    - Intermediate/Poor risk: Combination immunotherapy (ipilimumab + nivolumab) 
      or cabozantinib preferred over sunitinib monotherapy
    
    References (Vancouver style):
    1. Heng DY, Xie W, Regan MM, Warren MA, Golshayan AR, Sahi C, et al. Prognostic factors for 
    overall survival in patients with metastatic renal cell carcinoma treated with vascular 
    endothelial growth factor-targeted agents: results from a large, multicenter study. 
    J Clin Oncol. 2009 Dec 1;27(34):5794-9. doi: 10.1200/JCO.2008.21.4809
    2. Heng DY, Xie W, Regan MM, Harshman LC, Bjarnason GA, Vaishampayan UN, et al. External 
    validation and comparison with other models of the International Metastatic Renal-Cell 
    Carcinoma Database Consortium prognostic model: a population-based study. Lancet Oncol. 
    2013 Feb;14(2):141-8. doi: 10.1016/S1470-2045(12)70559-4
    3. Motzer RJ, Tannir NM, McDermott DF, Arén Frontera O, Melichar B, Choueiri TK, et al. 
    Nivolumab plus Ipilimumab versus Sunitinib in Advanced Renal-Cell Carcinoma. N Engl J Med. 
    2018 Apr 5;378(14):1277-1290. doi: 10.1056/NEJMoa1712126
    """
    
    time_to_systemic_therapy: Literal["less_than_1_year", "1_year_or_more"] = Field(
        ...,
        description="Time from RCC diagnosis to first-line systemic therapy. Less than 1 year indicates more aggressive disease (1 point)",
        example="1_year_or_more"
    )
    
    karnofsky_performance_status: Literal["less_than_80", "80_or_more"] = Field(
        ...,
        description="Karnofsky Performance Status. <80% indicates poor functional status (1 point). KPS 80-100% = good, 60-70% = restricted, <60% = disabled",
        example="80_or_more"
    )
    
    hemoglobin: Literal["below_normal", "normal_or_above"] = Field(
        ...,
        description="Hemoglobin level relative to institutional lower limit of normal. Below normal indicates anemia (1 point). Normal ranges vary by sex and institution",
        example="normal_or_above"
    )
    
    corrected_calcium: Literal["above_normal", "normal_or_below"] = Field(
        ...,
        description="Corrected calcium level relative to institutional upper limit of normal. Above normal indicates hypercalcemia (1 point). Use serum calcium corrected for albumin",
        example="normal_or_below"
    )
    
    neutrophils: Literal["above_normal", "normal_or_below"] = Field(
        ...,
        description="Absolute neutrophil count relative to institutional upper limit of normal. Above normal indicates elevated neutrophils (1 point)",
        example="normal_or_below"
    )
    
    platelets: Literal["above_normal", "normal_or_below"] = Field(
        ...,
        description="Platelet count relative to institutional upper limit of normal. Above normal indicates thrombocytosis (1 point)",
        example="normal_or_below"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "time_to_systemic_therapy": "1_year_or_more",
                "karnofsky_performance_status": "80_or_more",
                "hemoglobin": "normal_or_above",
                "corrected_calcium": "normal_or_below",
                "neutrophils": "normal_or_below",
                "platelets": "normal_or_below"
            }
        }


class ImdcRiskModelResponse(BaseModel):
    """
    Response model for IMDC (International Metastatic RCC Database Consortium) Risk Model
    
    The IMDC Risk Model score ranges from 0-6 points and stratifies patients into:
    - Favorable Risk (0 points): Median OS 43.2 months, consider VEGF-targeted monotherapy
    - Intermediate Risk (1-2 points): Median OS 22.5 months, consider combination immunotherapy
    - Poor Risk (3-6 points): Median OS 7.8 months, consider combination immunotherapy
    
    Treatment implications:
    - Favorable risk patients may not benefit from combination immunotherapy over sunitinib
    - Intermediate and poor risk patients derive survival benefit from ipilimumab + nivolumab 
      over sunitinib (CheckMate 214 trial)
    - Alternative first-line options include cabozantinib, pazopanib, or axitinib + pembrolizumab
    
    Reference: Heng DY, et al. J Clin Oncol. 2009;27(34):5794-9. Lancet Oncol. 2013;14(2):141-8.
    """
    
    result: int = Field(
        ...,
        description="IMDC risk score calculated from clinical and laboratory variables (range: 0-6 points)",
        example=1
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with survival estimates and treatment recommendations based on the risk category",
        example="Intermediate prognosis with median overall survival of 22.5 months. Consider ipilimumab plus nivolumab or cabozantinib as first-line therapy. These patients derive significant survival benefit from combination immunotherapy compared to sunitinib monotherapy."
    )
    
    stage: str = Field(
        ...,
        description="Risk category classification (Favorable Risk, Intermediate Risk, Poor Risk)",
        example="Intermediate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category with number of risk factors",
        example="1-2 risk factors"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 1,
                "unit": "points",
                "interpretation": "Intermediate prognosis with median overall survival of 22.5 months. Consider ipilimumab plus nivolumab or cabozantinib as first-line therapy. These patients derive significant survival benefit from combination immunotherapy compared to sunitinib monotherapy.",
                "stage": "Intermediate Risk",
                "stage_description": "1-2 risk factors"
            }
        }