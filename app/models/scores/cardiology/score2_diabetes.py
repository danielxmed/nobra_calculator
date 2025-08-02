"""
Systematic Coronary Risk Evaluation 2-Diabetes (SCORE2-Diabetes) Models

Request and response models for SCORE2-Diabetes calculation.

References (Vancouver style):
1. SCORE2-Diabetes Working Group and the ESC Cardiovascular Risk Collaboration. 
   SCORE2-Diabetes: 10-year cardiovascular risk estimation in type 2 diabetes in 
   Europe. Eur Heart J. 2023 Jul 21;44(28):2544-2556. doi: 10.1093/eurheartj/ehad260.
2. Pennells L, Kaptoge S, Østergaard HB, Read SH, Carinci F, Franch-Nadal J, et al. 
   SCORE2-Diabetes: 10-year cardiovascular risk estimation in type 2 diabetes in 
   Europe. Eur Heart J. 2023 Jul 21;44(28):2544-2556.
3. Visseren FLJ, Mach F, Smulders YM, Carballo D, Koskinas KC, Bäck M, et al. 2021 
   ESC Guidelines on cardiovascular disease prevention in clinical practice. Eur Heart 
   J. 2021 Sep 7;42(34):3227-3337. doi: 10.1093/eurheartj/ehab484.

SCORE2-Diabetes extends the SCORE2 algorithms by incorporating diabetes-specific 
variables (HbA1c, age at diabetes diagnosis, and eGFR) to provide more accurate 
cardiovascular risk prediction in patients with type 2 diabetes. The model was 
developed using data from 229,460 participants with type 2 diabetes across Europe.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal


class Score2DiabetesRequest(BaseModel):
    """
    Request model for Systematic Coronary Risk Evaluation 2-Diabetes (SCORE2-Diabetes)
    
    SCORE2-Diabetes predicts 10-year CVD risk in type 2 diabetes patients aged 40-69:
    
    Demographics:
    - Sex: Risk algorithms are sex-specific
    - Age: 40-69 years (use SCORE2-OP for ≥70 years)
    
    Conventional Risk Factors:
    - Smoking: Current smoking significantly increases risk
    - Systolic BP: Higher blood pressure increases risk
    - Total Cholesterol: Higher levels increase risk
    - HDL Cholesterol: Higher levels are protective
    
    Diabetes-Specific Variables:
    - Age at Diabetes Diagnosis: Earlier onset indicates longer exposure
    - HbA1c: Glycemic control indicator
    - eGFR: Kidney function (non-linear association with CVD)
    
    Geographic Calibration:
    - Risk Region: Based on country-specific CVD mortality rates
    
    References (Vancouver style):
    1. SCORE2-Diabetes Working Group and the ESC Cardiovascular Risk Collaboration. 
       SCORE2-Diabetes: 10-year cardiovascular risk estimation in type 2 diabetes in 
       Europe. Eur Heart J. 2023 Jul 21;44(28):2544-2556. doi: 10.1093/eurheartj/ehad260.
    """
    
    sex: Literal["male", "female"] = Field(
        ...,
        description="Biological sex. SCORE2-Diabetes algorithms are sex-specific",
        example="male"
    )
    
    age: int = Field(
        ...,
        ge=40,
        le=69,
        description="Age in years. SCORE2-Diabetes is validated for ages 40-69. Use SCORE2-OP for patients ≥70 years",
        example=58
    )
    
    smoking: Literal["current", "other"] = Field(
        ...,
        description="Current smoking status. 'current' = currently smoking tobacco, 'other' = never smoked or former smoker",
        example="other"
    )
    
    systolic_bp: int = Field(
        ...,
        ge=80,
        le=250,
        description="Systolic blood pressure in mmHg. Should be average of multiple readings",
        example=135
    )
    
    total_cholesterol: float = Field(
        ...,
        ge=2.0,
        le=12.0,
        description="Total cholesterol in mmol/L. To convert from mg/dL: divide by 38.67",
        example=5.8
    )
    
    hdl_cholesterol: float = Field(
        ...,
        ge=0.5,
        le=3.5,
        description="HDL cholesterol in mmol/L. To convert from mg/dL: divide by 38.67",
        example=1.1
    )
    
    age_diabetes_diagnosis: int = Field(
        ...,
        ge=18,
        le=69,
        description="Age at type 2 diabetes diagnosis in years. Earlier diagnosis indicates longer disease exposure",
        example=50
    )
    
    hba1c: float = Field(
        ...,
        ge=20,
        le=130,
        description="Glycated hemoglobin (HbA1c) in mmol/mol. To convert from %: multiply by 10.93 and subtract 23.5",
        example=53
    )
    
    egfr: float = Field(
        ...,
        ge=15,
        le=150,
        description="Estimated glomerular filtration rate (eGFR) in mL/min/1.73m². Calculated using CKD-EPI or similar equation",
        example=75
    )
    
    risk_region: Literal["low", "moderate", "high", "very_high"] = Field(
        ...,
        description="Cardiovascular risk region based on country. Low: Belgium, Denmark, France, Israel, Luxembourg, Norway, Spain, Switzerland, Netherlands, UK. Moderate: Austria, Cyprus, Finland, Germany, Greece, Iceland, Ireland, Italy, Malta, Portugal, San Marino, Slovenia, Sweden. High: Albania, Armenia, Azerbaijan, Bosnia & Herzegovina, Croatia, Czech Republic, Estonia, Hungary, Kazakhstan, Poland, Slovakia, Turkey. Very High: Algeria, Belarus, Bulgaria, Egypt, Georgia, Kyrgyzstan, Latvia, Lebanon, Libya, Lithuania, Montenegro, Morocco, Moldova, Romania, Russia, Serbia, Syria, North Macedonia, Tunisia, Ukraine, Uzbekistan",
        example="moderate"
    )
    
    @field_validator('total_cholesterol', 'hdl_cholesterol')
    def validate_cholesterol_ratio(cls, v, info):
        """Ensure HDL is not greater than total cholesterol"""
        if info.field_name == 'hdl_cholesterol' and 'total_cholesterol' in info.data:
            if v >= info.data['total_cholesterol']:
                raise ValueError("HDL cholesterol cannot be greater than or equal to total cholesterol")
        return v
    
    @field_validator('age_diabetes_diagnosis')
    def validate_diabetes_age(cls, v, info):
        """Ensure diabetes diagnosis age is not greater than current age"""
        if 'age' in info.data and v > info.data['age']:
            raise ValueError("Age at diabetes diagnosis cannot be greater than current age")
        return v
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "sex": "male",
                "age": 58,
                "smoking": "other",
                "systolic_bp": 135,
                "total_cholesterol": 5.8,
                "hdl_cholesterol": 1.1,
                "age_diabetes_diagnosis": 50,
                "hba1c": 53,
                "egfr": 75,
                "risk_region": "moderate"
            }
        }
    }


class Score2DiabetesResponse(BaseModel):
    """
    Response model for Systematic Coronary Risk Evaluation 2-Diabetes (SCORE2-Diabetes)
    
    Risk categories are age-specific:
    - Age <50 years: Low-Moderate <2.5%, High 2.5-7.5%, Very High ≥7.5%
    - Age 50-69 years: Low-Moderate <5%, High 5-10%, Very High ≥10%
    
    Treatment recommendations:
    - Low-Moderate: Lifestyle interventions, consider treatment if other risks
    - High: Risk factor treatment recommended (statins, BP control)
    - Very High: Intensive treatment including SGLT2i/GLP-1 RA with CV benefit
    
    Reference: SCORE2-Diabetes Working Group. Eur Heart J. 2023;44(28):2544-2556.
    """
    
    result: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="10-year risk of fatal and non-fatal cardiovascular disease as percentage",
        example=8.5
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the risk",
        example="%"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with treatment recommendations based on risk level, age, and diabetes status",
        example="High risk. Recommend risk factor treatment including lipid-lowering therapy (statins) and blood pressure management. Intensive diabetes control and lifestyle modification."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low to Moderate Risk, High Risk, or Very High Risk)",
        example="High Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Risk percentage with context",
        example="8.5% 10-year CVD risk"
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "result": 8.5,
                "unit": "%",
                "interpretation": "High risk. Recommend risk factor treatment including lipid-lowering therapy (statins) and blood pressure management. Intensive diabetes control and lifestyle modification.",
                "stage": "High Risk",
                "stage_description": "8.5% 10-year CVD risk"
            }
        }
    }