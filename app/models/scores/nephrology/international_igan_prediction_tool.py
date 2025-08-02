"""
International IgA Nephropathy Prediction Tool Models

Request and response models for International IgAN Prediction Tool calculation.

References (Vancouver style):
1. Barbour SJ, Coppo R, Zhang H, Liu ZH, Suzuki Y, Matsuzaki K, et al. Evaluating a New 
   International Risk-Prediction Tool in IgA Nephropathy. JAMA Intern Med. 2019 Jul 1;179(7):942-952. 
   doi: 10.1001/jamainternmed.2019.0600.
2. Kidney Disease: Improving Global Outcomes (KDIGO) Glomerular Diseases Work Group. KDIGO 2021 
   Clinical Practice Guideline for the Management of Glomerular Diseases. Kidney Int. 2021 Oct;100(4S):S1-S276. 
   doi: 10.1016/j.kint.2021.05.021.
3. Zhang J, Huang B, Liu Z, Wang X, Xie M, Guo R, et al. External validation of the International 
   IgA Nephropathy Prediction Tool. Clin J Am Soc Nephrol. 2020 Jul 7;15(7):1112-1120. 
   doi: 10.2215/CJN.16021219.

The International IgA Nephropathy Prediction Tool predicts the 5-year risk of a 50% decline 
in eGFR or end-stage kidney disease in patients with biopsy-proven IgA nephropathy. This 
validated tool was developed using an international multi-ethnic cohort of 2,781 patients 
and is endorsed by the 2021 KDIGO guidelines as the preferred method for risk prediction 
in IgA nephropathy. The tool uses clinical, laboratory, and Oxford MEST histological 
parameters available at the time of kidney biopsy to provide risk stratification for 
clinical decision-making, patient counseling, and treatment planning.
"""

from pydantic import BaseModel, Field
from typing import Literal, Optional


class InternationalIganPredictionToolRequest(BaseModel):
    """
    Request model for International IgA Nephropathy Prediction Tool
    
    The International IgAN Prediction Tool uses clinical, laboratory, and histological 
    parameters to predict 5-year risk of kidney function decline:
    
    Clinical Parameters:
    - Age: Patient age at time of kidney biopsy (18-65 years)
    - eGFR: Estimated glomerular filtration rate using CKD-EPI equation (5-150 mL/min/1.73m²)
    - MAP: Mean arterial pressure calculated as (2×diastolic + systolic)/3 (60-140 mmHg)
    - Urine protein: 24-hour urine protein excretion or spot urine PCR (0.001-15 g/day)
    
    Oxford MEST Histological Scores:
    - M (Mesangial hypercellularity): M0 (≤0.5 mesangial cells/area) or M1 (>0.5)
    - E (Endocapillary hypercellularity): E0 (absent) or E1 (present)
    - S (Segmental sclerosis): S0 (absent) or S1 (present in any glomerulus)
    - T (Interstitial fibrosis/tubular atrophy): T0 (0-25%), T1 (26-50%), T2 (>50%)
    
    Treatment Parameters:
    - RASB use: Renin-angiotensin system blocker (ACE inhibitor or ARB) use at biopsy
    - Immunosuppression: Any immunosuppressive therapy use at biopsy
    - Race: Optional parameter for race-inclusive model (white is reference category)
    
    References (Vancouver style):
    1. Barbour SJ, Coppo R, Zhang H, Liu ZH, Suzuki Y, Matsuzaki K, et al. Evaluating a New 
    International Risk-Prediction Tool in IgA Nephropathy. JAMA Intern Med. 2019 Jul 1;179(7):942-952. 
    doi: 10.1001/jamainternmed.2019.0600.
    2. Kidney Disease: Improving Global Outcomes (KDIGO) Glomerular Diseases Work Group. KDIGO 2021 
    Clinical Practice Guideline for the Management of Glomerular Diseases. Kidney Int. 2021 Oct;100(4S):S1-S276. 
    doi: 10.1016/j.kint.2021.05.021.
    3. Zhang J, Huang B, Liu Z, Wang X, Xie M, Guo R, et al. External validation of the International 
    IgA Nephropathy Prediction Tool. Clin J Am Soc Nephrol. 2020 Jul 7;15(7):1112-1120. 
    doi: 10.2215/CJN.16021219.
    """
    
    age: int = Field(
        ...,
        description="Patient age at time of kidney biopsy. Age range for adults is 18-65 years. Tool was developed and validated in adult population",
        ge=18,
        le=65,
        example=45
    )
    
    egfr: float = Field(
        ...,
        description="Estimated glomerular filtration rate at time of biopsy calculated using CKD-EPI equation when possible. Units: mL/min/1.73m². Range: 5-150 mL/min/1.73m²",
        ge=5.0,
        le=150.0,
        example=75.0
    )
    
    map: float = Field(
        ...,
        description="Mean arterial pressure calculated as (2 × diastolic blood pressure + systolic blood pressure) / 3. Units: mmHg. Range: 60-140 mmHg. Use blood pressure at time of biopsy",
        ge=60.0,
        le=140.0,
        example=95.0
    )
    
    urine_protein: float = Field(
        ...,
        description="24-hour urine protein excretion in grams per day. If unavailable, spot urine protein-to-creatinine ratio can be used as approximation. Units: g/day. Range: 0.001-15 g/day",
        ge=0.001,
        le=15.0,
        example=1.2
    )
    
    mest_m: Literal[0, 1] = Field(
        ...,
        description="Oxford MEST Score - Mesangial hypercellularity. M0 (score 0): ≤0.5 mesangial cells per mesangial area. M1 (score 1): >0.5 mesangial cells per mesangial area",
        example=0
    )
    
    mest_e: Literal[0, 1] = Field(
        ...,
        description="Oxford MEST Score - Endocapillary hypercellularity. E0 (score 0): absent endocapillary hypercellularity. E1 (score 1): endocapillary hypercellularity present",
        example=0
    )
    
    mest_s: Literal[0, 1] = Field(
        ...,
        description="Oxford MEST Score - Segmental sclerosis. S0 (score 0): no segmental sclerosis in any glomerulus. S1 (score 1): segmental sclerosis present in any glomerulus",
        example=1
    )
    
    mest_t: Literal[0, 1, 2] = Field(
        ...,
        description="Oxford MEST Score - Interstitial fibrosis/tubular atrophy. T0 (score 0): 0-25% of cortical area. T1 (score 1): 26-50% of cortical area. T2 (score 2): >50% of cortical area",
        example=1
    )
    
    rasb_use: Literal["yes", "no"] = Field(
        ...,
        description="Renin-angiotensin system blocker use at time of biopsy. Includes ACE inhibitors (enalapril, lisinopril, etc.) and angiotensin receptor blockers (losartan, valsartan, etc.)",
        example="yes"
    )
    
    immunosuppression_use: Literal["yes", "no"] = Field(
        ...,
        description="Immunosuppressive therapy use at time of biopsy. Includes corticosteroids, mycophenolate mofetil, cyclophosphamide, azathioprine, cyclosporine, tacrolimus, or other immunosuppressive agents",
        example="no"
    )
    
    race: Optional[Literal["white", "chinese", "japanese", "other"]] = Field(
        None,
        description="Patient race/ethnicity for race-inclusive model (optional). White is the reference category. If not provided, race-free model will be used which performs similarly",
        example="white"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": 45,
                "egfr": 75.0,
                "map": 95.0,
                "urine_protein": 1.2,
                "mest_m": 0,
                "mest_e": 0,
                "mest_s": 1,
                "mest_t": 1,
                "rasb_use": "yes",
                "immunosuppression_use": "no",
                "race": "white"
            }
        }


class InternationalIganPredictionToolResponse(BaseModel):
    """
    Response model for International IgA Nephropathy Prediction Tool
    
    The tool provides 5-year risk prediction for the composite outcome of 50% decline 
    in eGFR or end-stage kidney disease. Risk stratification:
    
    Risk Categories:
    - Very Low Risk: <10% 5-year risk - Conservative management, standard monitoring
    - Low Risk: 10-25% 5-year risk - Close monitoring, optimize conservative therapy
    - Moderate Risk: 25-50% 5-year risk - Consider immunosuppression, frequent follow-up
    - High Risk: 50-75% 5-year risk - Strong consideration for immunosuppression
    - Very High Risk: >75% 5-year risk - Urgent treatment consideration, RRT planning
    
    The tool has been externally validated in multiple cohorts with good discrimination 
    (C-statistic ~0.72) and is endorsed by 2021 KDIGO guidelines for risk prediction 
    in IgA nephropathy patients.
    
    Reference: Barbour SJ, et al. JAMA Intern Med. 2019;179(7):942-952.
    """
    
    result: float = Field(
        ...,
        description="5-year risk percentage of 50% eGFR decline or end stage kidney disease (range: 0-100%)",
        ge=0.0,
        le=100.0,
        example=22.5
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the risk prediction",
        example="%"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with risk stratification and management recommendations based on predicted 5-year risk",
        example="Low risk of kidney function decline. Conservative management with close monitoring. Optimize RASB therapy and blood pressure control (<130/80 mmHg). Regular nephrology follow-up every 3-6 months. Monitor proteinuria and eGFR trends. Consider immunosuppression if rapid progression or high-risk features develop."
    )
    
    stage: str = Field(
        ...,
        description="Risk category based on 5-year risk percentage (Very Low Risk, Low Risk, Moderate Risk, High Risk, Very High Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category with 5-year risk range",
        example="5-year risk 10-25%"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 22.5,
                "unit": "%",
                "interpretation": "Low risk of kidney function decline. Conservative management with close monitoring. Optimize RASB therapy and blood pressure control (<130/80 mmHg). Regular nephrology follow-up every 3-6 months. Monitor proteinuria and eGFR trends. Consider immunosuppression if rapid progression or high-risk features develop.",
                "stage": "Low Risk",
                "stage_description": "5-year risk 10-25%"
            }
        }