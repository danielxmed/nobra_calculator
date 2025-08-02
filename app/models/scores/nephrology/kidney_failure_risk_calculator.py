"""
Kidney Failure Risk Calculator (4-Variable) Models

Request and response models for Kidney Failure Risk Calculator.

References (Vancouver style):
1. Tangri N, Stevens LA, Griffith J, Tighiouart H, Djurdjev O, Naimark D, et al. 
   A predictive model for progression of chronic kidney disease to kidney failure. 
   JAMA. 2011;305(15):1553-9.
2. Tangri N, Grams ME, Levey AS, Coresh J, Appel LJ, Astor BC, et al. 
   Multinational Assessment of Accuracy of Equations for Predicting Risk of 
   Kidney Failure: A Meta-analysis. JAMA. 2016;315(2):164-74.
3. Ramspek CL, de Jong Y, Dekker FW, van Diepen M. Towards the best kidney 
   failure prediction tool: a systematic review and selection aid. 
   Nephrol Dial Transplant. 2020;35(9):1527-1538.
4. Major RW, Shepherd D, Medcalf JF, Xu G, Gray LJ, Brunskill NJ. The Kidney 
   Failure Risk Equation for prediction of end stage renal disease in UK 
   primary care: An external validation and clinical impact projection cohort 
   study. PLoS Med. 2019;16(11):e1002955.

The Kidney Failure Risk Equation (KFRE) is the most accurate and widely validated 
tool for predicting progression to kidney failure in patients with CKD. Developed 
by Tangri et al. in 2011, it has been validated in over 700,000 individuals 
across more than 30 countries worldwide.

The 4-variable equation uses:
- Age
- Sex 
- Estimated glomerular filtration rate (eGFR)
- Urine albumin-to-creatinine ratio (ACR)

This tool is specifically designed for patients with CKD stages 3-5 (eGFR <60 
mL/min/1.73 m²) and predicts the risk of kidney failure requiring dialysis or 
transplantation at 2 and 5 years.

Clinical applications include:
- Nephrology referral triage (often triggered by 2-year risk >5% or 5-year risk >15%)
- Timing of dialysis access creation
- Transplant evaluation and planning
- Patient counseling and shared decision-making
- Resource allocation and healthcare planning

The equation has different calibration factors for North American vs. non-North 
American populations to improve accuracy across different healthcare systems and 
patient populations.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict


class KidneyFailureRiskCalculatorRequest(BaseModel):
    """
    Request model for Kidney Failure Risk Calculator (4-Variable KFRE)
    
    The 4-variable KFRE uses basic demographic and laboratory data to predict 
    kidney failure risk in CKD patients:
    
    Input Parameters:
    - Age: Patient age in years (18-110)
    - Sex: Biological sex (male/female)
    - eGFR: Estimated glomerular filtration rate (1-60 mL/min/1.73 m²)
    - Urine ACR: Albumin-to-creatinine ratio (0.1-25,000 mg/g)
    - Region: Geographic region for calibration (North America vs. other)
    
    Eligibility Criteria:
    - CKD stages 3-5 (eGFR <60 mL/min/1.73 m²)
    - Age ≥18 years
    - Not on dialysis or with kidney transplant
    - Stable kidney function (not AKI or rapidly progressive GN)
    
    Risk Thresholds for Clinical Action:
    - 2-year risk >5%: Consider nephrology referral
    - 5-year risk >15%: Strongly consider nephrology referral
    - 5-year risk >30%: Urgent referral and RRT planning
    
    Important Notes:
    - ACR can be in mg/g or mg/mmol (multiply mg/mmol by 8.84 to get mg/g)
    - If ACR unavailable, protein-to-creatinine ratio (PCR) may be used as approximation
    - 8-variable equation available for more detailed assessment
    - Not validated for acute kidney injury or rapidly progressive disease
    
    References (Vancouver style):
    1. Tangri N, Stevens LA, Griffith J, Tighiouart H, Djurdjev O, Naimark D, et al. 
       A predictive model for progression of chronic kidney disease to kidney failure. 
       JAMA. 2011;305(15):1553-9.
    2. Tangri N, Grams ME, Levey AS, Coresh J, Appel LJ, Astor BC, et al. 
       Multinational Assessment of Accuracy of Equations for Predicting Risk of 
       Kidney Failure: A Meta-analysis. JAMA. 2016;315(2):164-74.
    3. Ramspek CL, de Jong Y, Dekker FW, van Diepen M. Towards the best kidney 
       failure prediction tool: a systematic review and selection aid. 
       Nephrol Dial Transplant. 2020;35(9):1527-1538.
    4. Major RW, Shepherd D, Medcalf JF, Xu G, Gray LJ, Brunskill NJ. The Kidney 
       Failure Risk Equation for prediction of end stage renal disease in UK 
       primary care: An external validation and clinical impact projection cohort 
       study. PLoS Med. 2019;16(11):e1002955.
    """
    
    age: int = Field(
        ...,
        description="Patient age in years. Younger age is protective against kidney failure progression.",
        ge=18,
        le=110,
        example=65
    )
    
    sex: Literal["male", "female"] = Field(
        ...,
        description="Biological sex of the patient. Males have slightly higher risk of kidney failure progression.",
        example="male"
    )
    
    egfr: float = Field(
        ...,
        description="Estimated glomerular filtration rate (eGFR) in mL/min/1.73 m². "
                   "Calculator is validated for CKD stages 3-5 (eGFR <60). Lower eGFR "
                   "indicates worse kidney function and higher risk of progression.",
        ge=1,
        le=60,
        example=35.5
    )
    
    urine_acr: float = Field(
        ...,
        description="Urine albumin-to-creatinine ratio (ACR) in mg/g. Higher albuminuria "
                   "indicates greater kidney damage and risk of progression. Can convert "
                   "from mg/mmol by multiplying by 8.84. Normal is <30 mg/g.",
        ge=0.1,
        le=25000,
        example=450.0
    )
    
    region: Literal["north_america", "non_north_america"] = Field(
        ...,
        description="Geographic region for calibration. Non-North American populations "
                   "have different baseline risks and require adjusted calibration factors.",
        example="north_america"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": 65,
                "sex": "male",
                "egfr": 35.5,
                "urine_acr": 450.0,
                "region": "north_america"
            }
        }


class KidneyFailureRiskCalculatorResponse(BaseModel):
    """
    Response model for Kidney Failure Risk Calculator (4-Variable KFRE)
    
    Provides 2-year and 5-year kidney failure risk predictions with clinical 
    interpretation and management recommendations. The KFRE is the most accurate 
    tool for predicting kidney failure, outperforming clinical judgment and other 
    risk equations.
    
    Risk Categories:
    - Low (<5% at 5 years): Primary care management often appropriate
    - Intermediate (5-15% at 5 years): Consider nephrology referral
    - High (15-30% at 5 years): Nephrology referral recommended
    - Very High (>30% at 5 years): Urgent referral and RRT planning
    
    Clinical Actions Based on Risk:
    - Risk assessment guides timing of:
      * Nephrology referral
      * Dialysis access creation (typically when 2-year risk >20%)
      * Transplant evaluation and listing
      * Patient education about renal replacement options
      * Frequency of monitoring
    
    Accuracy and Validation:
    - C-statistic typically 0.83-0.92 for 2-year prediction
    - Validated in >700,000 patients across 30+ countries
    - Superior to eGFR alone or clinical judgment
    - Performs well across different ethnicities and healthcare systems
    
    Reference: Tangri N, et al. JAMA. 2011;305(15):1553-9.
    """
    
    result: Dict[str, float] = Field(
        ...,
        description="Kidney failure risk at 2 and 5 years as percentages",
        example={"risk_2_year": 8.5, "risk_5_year": 22.3}
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the risk values",
        example="percentage"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation including risk assessment, management recommendations, "
                   "and suggested follow-up based on the calculated kidney failure risk",
        example="Based on the 4-variable Kidney Failure Risk Equation, this patient with CKD (eGFR 35.5 mL/min/1.73 m²) has a 8.5% risk of kidney failure at 2 years and 22.3% risk at 5 years. Nephrology referral is strongly recommended. Begin preparation for renal replacement therapy including patient education, vascular access planning, and transplant evaluation if appropriate. Aggressive management of CKD complications and cardiovascular risk factors is essential."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low, Intermediate, High, Very High)",
        example="High"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the kidney failure risk level",
        example="High risk of kidney failure"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": {
                    "risk_2_year": 8.5,
                    "risk_5_year": 22.3
                },
                "unit": "percentage",
                "interpretation": "Based on the 4-variable Kidney Failure Risk Equation, this patient with CKD (eGFR 35.5 mL/min/1.73 m²) has a 8.5% risk of kidney failure at 2 years and 22.3% risk at 5 years. Nephrology referral is strongly recommended. Begin preparation for renal replacement therapy including patient education, vascular access planning, and transplant evaluation if appropriate. Aggressive management of CKD complications and cardiovascular risk factors is essential.",
                "stage": "High",
                "stage_description": "High risk of kidney failure"
            }
        }