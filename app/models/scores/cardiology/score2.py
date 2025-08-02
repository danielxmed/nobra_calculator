"""
Systematic Coronary Risk Evaluation 2 (SCORE2) Models

Request and response models for SCORE2 calculation.

References (Vancouver style):
1. Visseren FLJ, Mach F, Smulders YM, Carballo D, Koskinas KC, Bäck M, et al. 2021 ESC 
   Guidelines on cardiovascular disease prevention in clinical practice. Eur Heart J. 
   2021 Sep 7;42(34):3227-3337. doi: 10.1093/eurheartj/ehab484.
2. SCORE2 working group and ESC Cardiovascular risk collaboration. SCORE2 risk prediction 
   algorithms: new models to estimate 10-year risk of cardiovascular disease in Europe. 
   Eur Heart J. 2021 Jul 1;42(25):2439-2454. doi: 10.1093/eurheartj/ehab309.
3. Hageman S, Pennells L, Ojeda F, Kaptoge S, Kuulasmaa K, de Vries T, et al. SCORE2 
   risk prediction algorithms: new models to estimate 10-year risk of cardiovascular 
   disease in Europe. Eur Heart J. 2021 Jul 1;42(25):2439-2454.

The Systematic Coronary Risk Evaluation 2 (SCORE2) is a sex-specific risk prediction 
algorithm that estimates 10-year risk of fatal and non-fatal cardiovascular disease 
(myocardial infarction and stroke) in apparently healthy individuals aged 40-69 years 
without previous cardiovascular disease or diabetes.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal


class Score2Request(BaseModel):
    """
    Request model for Systematic Coronary Risk Evaluation 2 (SCORE2)
    
    SCORE2 uses 7 parameters to estimate 10-year CVD risk:
    
    Demographics:
    - Sex: Risk algorithms are sex-specific
    - Age: 40-69 years (use SCORE2-OP for ≥70 years)
    
    Risk Factors:
    - Smoking: Current smoking significantly increases risk
    - Systolic BP: Higher blood pressure increases risk
    - Total Cholesterol: Higher levels increase risk
    - HDL Cholesterol: Higher levels are protective
    
    Geographic Calibration:
    - Risk Region: Based on country-specific CVD mortality rates
    
    References (Vancouver style):
    1. Visseren FLJ, Mach F, Smulders YM, Carballo D, Koskinas KC, Bäck M, et al. 2021 ESC 
       Guidelines on cardiovascular disease prevention in clinical practice. Eur Heart J. 
       2021 Sep 7;42(34):3227-3337. doi: 10.1093/eurheartj/ehab484.
    2. SCORE2 working group and ESC Cardiovascular risk collaboration. SCORE2 risk prediction 
       algorithms: new models to estimate 10-year risk of cardiovascular disease in Europe. 
       Eur Heart J. 2021 Jul 1;42(25):2439-2454. doi: 10.1093/eurheartj/ehab309.
    """
    
    sex: Literal["male", "female"] = Field(
        ...,
        description="Biological sex. SCORE2 algorithms are sex-specific",
        example="male"
    )
    
    age: int = Field(
        ...,
        ge=40,
        le=69,
        description="Age in years. SCORE2 is validated for ages 40-69. Use SCORE2-OP for patients ≥70 years",
        example=55
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
        example=130
    )
    
    total_cholesterol: float = Field(
        ...,
        ge=2.0,
        le=12.0,
        description="Total cholesterol in mmol/L. To convert from mg/dL: divide by 38.67",
        example=5.5
    )
    
    hdl_cholesterol: float = Field(
        ...,
        ge=0.5,
        le=3.5,
        description="HDL cholesterol in mmol/L. To convert from mg/dL: divide by 38.67",
        example=1.3
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
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "sex": "male",
                "age": 55,
                "smoking": "other",
                "systolic_bp": 130,
                "total_cholesterol": 5.5,
                "hdl_cholesterol": 1.3,
                "risk_region": "moderate"
            }
        }
    }


class Score2Response(BaseModel):
    """
    Response model for Systematic Coronary Risk Evaluation 2 (SCORE2)
    
    Risk categories are age-specific:
    - Age <50 years: Low-Moderate <2.5%, High 2.5-7.5%, Very High ≥7.5%
    - Age 50-69 years: Low-Moderate <5%, High 5-10%, Very High ≥10%
    
    Treatment recommendations:
    - Low-Moderate: Lifestyle interventions
    - High: Consider risk factor treatment
    - Very High: Recommend intensive risk factor treatment
    
    Reference: Visseren FLJ, et al. Eur Heart J. 2021;42(34):3227-3337.
    """
    
    result: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="10-year risk of fatal and non-fatal cardiovascular disease as percentage",
        example=6.5
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the risk",
        example="%"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with treatment recommendations based on risk level and age",
        example="High cardiovascular risk. Consider risk factor treatment including lipid-lowering therapy (statins) and blood pressure management. Lifestyle modification remains essential."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low to Moderate Risk, High Risk, or Very High Risk)",
        example="High Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Risk percentage with context",
        example="6.5% 10-year risk"
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "result": 6.5,
                "unit": "%",
                "interpretation": "High cardiovascular risk. Consider risk factor treatment including lipid-lowering therapy (statins) and blood pressure management. Lifestyle modification remains essential.",
                "stage": "High Risk",
                "stage_description": "6.5% 10-year risk"
            }
        }
    }