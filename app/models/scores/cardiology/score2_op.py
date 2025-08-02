"""
Systematic Coronary Risk Evaluation 2-Older Persons (SCORE2-OP) Models

Request and response models for SCORE2-OP calculation.

References (Vancouver style):
1. SCORE2-OP working group and ESC Cardiovascular risk collaboration. SCORE2-OP risk 
   prediction algorithms: estimating incident cardiovascular event risk in older persons 
   in four geographical risk regions. Eur Heart J. 2021 Jul 1;42(25):2455-2467. 
   doi: 10.1093/eurheartj/ehab312.
2. de Vries TI, Cooney MT, Selmer RM, Hageman SHJ, Pennells L, Wood A, et al. SCORE2-OP 
   risk prediction algorithms: estimating incident cardiovascular event risk in older 
   persons in four geographical risk regions. Eur Heart J. 2021 Jul 1;42(25):2455-2467.
3. Visseren FLJ, Mach F, Smulders YM, Carballo D, Koskinas KC, Bäck M, et al. 2021 ESC 
   Guidelines on cardiovascular disease prevention in clinical practice. Eur Heart J. 
   2021 Sep 7;42(34):3227-3337. doi: 10.1093/eurheartj/ehab484.

SCORE2-OP provides competing risk-adjusted cardiovascular risk estimates for older 
persons (≥70 years), accounting for the increasing risk of non-cardiovascular mortality 
with age and the attenuation of risk factor gradients.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal


class Score2OpRequest(BaseModel):
    """
    Request model for Systematic Coronary Risk Evaluation 2-Older Persons (SCORE2-OP)
    
    SCORE2-OP predicts CVD risk in older individuals aged 70-89 years:
    
    Demographics:
    - Sex: Risk algorithms are sex-specific
    - Age: 70-89 years (validated range for older persons)
    
    Risk Factors:
    - Diabetes: Presence increases cardiovascular risk
    - Smoking: Current smoking status
    - Systolic BP: Higher blood pressure increases risk
    - Total Cholesterol: Used to calculate non-HDL cholesterol
    - HDL Cholesterol: Used to calculate non-HDL cholesterol
    
    Geographic Calibration:
    - Risk Region: Based on country-specific CVD mortality rates
    
    Time Horizon:
    - 5-year or 10-year risk prediction available
    
    Key Differences from SCORE2:
    - Accounts for competing risk of non-CVD mortality
    - Risk factor effects attenuate with age
    - Different risk thresholds (7.5% and 15%)
    
    References (Vancouver style):
    1. SCORE2-OP working group and ESC Cardiovascular risk collaboration. SCORE2-OP risk 
       prediction algorithms: estimating incident cardiovascular event risk in older persons 
       in four geographical risk regions. Eur Heart J. 2021 Jul 1;42(25):2455-2467. 
       doi: 10.1093/eurheartj/ehab312.
    """
    
    sex: Literal["male", "female"] = Field(
        ...,
        description="Biological sex. SCORE2-OP algorithms are sex-specific",
        example="female"
    )
    
    age: int = Field(
        ...,
        ge=70,
        le=89,
        description="Age in years. SCORE2-OP is validated for ages 70-89",
        example=75
    )
    
    diabetes: Literal["yes", "no"] = Field(
        ...,
        description="Diabetes status. 'yes' = diagnosed with diabetes (type 1 or 2), 'no' = no diabetes",
        example="no"
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
        example=140
    )
    
    total_cholesterol: float = Field(
        ...,
        ge=2.0,
        le=12.0,
        description="Total cholesterol in mmol/L. To convert from mg/dL: divide by 38.67",
        example=5.2
    )
    
    hdl_cholesterol: float = Field(
        ...,
        ge=0.5,
        le=3.5,
        description="HDL cholesterol in mmol/L. To convert from mg/dL: divide by 38.67",
        example=1.4
    )
    
    risk_region: Literal["low", "moderate", "high", "very_high"] = Field(
        ...,
        description="Cardiovascular risk region based on country. Low: Belgium, Denmark, France, Israel, Luxembourg, Norway, Spain, Switzerland, Netherlands, UK. Moderate: Austria, Cyprus, Finland, Germany, Greece, Iceland, Ireland, Italy, Malta, Portugal, San Marino, Slovenia, Sweden. High: Albania, Armenia, Azerbaijan, Bosnia & Herzegovina, Croatia, Czech Republic, Estonia, Hungary, Kazakhstan, Poland, Slovakia, Turkey. Very High: Algeria, Belarus, Bulgaria, Egypt, Georgia, Kyrgyzstan, Latvia, Lebanon, Libya, Lithuania, Montenegro, Morocco, Moldova, Romania, Russia, Serbia, Syria, North Macedonia, Tunisia, Ukraine, Uzbekistan",
        example="moderate"
    )
    
    time_horizon: Literal["5_year", "10_year"] = Field(
        ...,
        description="Risk prediction time horizon. Both 5-year and 10-year risks are available",
        example="10_year"
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
                "sex": "female",
                "age": 75,
                "diabetes": "no",
                "smoking": "other",
                "systolic_bp": 140,
                "total_cholesterol": 5.2,
                "hdl_cholesterol": 1.4,
                "risk_region": "moderate",
                "time_horizon": "10_year"
            }
        }
    }


class Score2OpResponse(BaseModel):
    """
    Response model for Systematic Coronary Risk Evaluation 2-Older Persons (SCORE2-OP)
    
    Risk categories for older persons:
    - Low to Moderate: <7.5% (generally no treatment benefit)
    - High: 7.5-15% (treatment may be considered)
    - Very High: ≥15% (treatment generally recommended)
    
    Important considerations:
    - Competing risk of non-CVD mortality is accounted for
    - Treatment decisions should consider frailty, life expectancy, and patient preferences
    - Risk factor gradients attenuate with age
    
    Reference: SCORE2-OP working group. Eur Heart J. 2021;42(25):2455-2467.
    """
    
    result: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Cardiovascular disease risk as percentage at specified time horizon",
        example=9.8
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the risk",
        example="%"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with treatment recommendations considering age, frailty, and patient preferences",
        example="Treatment may be considered. Discuss benefits and risks with patient. Consider statin therapy and blood pressure management based on individual assessment and patient preferences."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low to Moderate Risk, High Risk, or Very High Risk)",
        example="High Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Risk percentage with time horizon context",
        example="9.8% 10-year CVD risk"
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "result": 9.8,
                "unit": "%",
                "interpretation": "Treatment may be considered. Discuss benefits and risks with patient. Consider statin therapy and blood pressure management based on individual assessment and patient preferences.",
                "stage": "High Risk",
                "stage_description": "9.8% 10-year CVD risk"
            }
        }
    }