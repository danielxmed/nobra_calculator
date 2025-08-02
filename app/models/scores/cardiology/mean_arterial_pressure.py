"""
Mean Arterial Pressure (MAP) Models

Request and response models for MAP calculation.

References (Vancouver style):
1. Magder SA. The highs and lows of blood pressure: toward meaningful clinical targets 
   in patients with shock. Crit Care Med. 2014 May;42(5):1241-51. 
   doi: 10.1097/CCM.0000000000000324.
2. Walsh M, Devereaux PJ, Garg AX, Kurz A, Turan A, Rodseth RN, et al. Relationship 
   between intraoperative mean arterial pressure and clinical outcomes after noncardiac 
   surgery: toward an empirical definition of hypotension. Anesthesiology. 2013 
   Sep;119(3):507-15. doi: 10.1097/ALN.0b013e3182a10e26.
3. Sesso HD, Stampfer MJ, Rosner B, Hennekens CH, Gaziano JM, Manson JE, et al. 
   Systolic and diastolic blood pressure, pulse pressure, and mean arterial pressure 
   as predictors of cardiovascular disease risk in Men. Hypertension. 2000 Nov;36(5):801-7. 
   doi: 10.1161/01.hyp.36.5.801.

Mean Arterial Pressure (MAP) is the average arterial pressure throughout one cardiac 
cycle. It's calculated as (2 × Diastolic BP + Systolic BP) / 3, accounting for the 
fact that approximately two-thirds of the cardiac cycle is spent in diastole. MAP is 
a critical parameter for assessing tissue perfusion, particularly in critical care 
settings where maintaining adequate organ perfusion is essential.
"""

from pydantic import BaseModel, Field


class MeanArterialPressureRequest(BaseModel):
    """
    Request model for Mean Arterial Pressure (MAP) calculation
    
    MAP is calculated using systolic and diastolic blood pressure measurements.
    It provides a single value that represents the average pressure in the arteries
    during one cardiac cycle, which is more representative of tissue perfusion than
    systolic blood pressure alone.
    
    Clinical significance:
    - MAP ≥60 mmHg: Generally needed to maintain adequate tissue perfusion
    - MAP ≥65 mmHg: Recommended target in sepsis and septic shock
    - MAP 70-110 mmHg: Normal range for most adults
    - Higher MAP may be needed in chronic hypertensive patients
    
    The formula accounts for the cardiac cycle phases:
    - Systole (contraction): ~1/3 of the cycle
    - Diastole (relaxation): ~2/3 of the cycle
    
    References (Vancouver style):
    1. Magder SA. The highs and lows of blood pressure: toward meaningful clinical targets 
       in patients with shock. Crit Care Med. 2014 May;42(5):1241-51. 
       doi: 10.1097/CCM.0000000000000324.
    2. Walsh M, Devereaux PJ, Garg AX, Kurz A, Turan A, Rodseth RN, et al. Relationship 
       between intraoperative mean arterial pressure and clinical outcomes after noncardiac 
       surgery: toward an empirical definition of hypotension. Anesthesiology. 2013 
       Sep;119(3):507-15. doi: 10.1097/ALN.0b013e3182a10e26.
    """
    
    systolic_bp: float = Field(
        ...,
        ge=40,
        le=300,
        description="Systolic blood pressure in mmHg (the higher value when blood pressure is "
                    "measured). This represents the pressure in arteries during heart contraction. "
                    "Normal range is typically 90-120 mmHg. Values below 90 indicate hypotension, "
                    "while values above 140 indicate hypertension.",
        example=120.0
    )
    
    diastolic_bp: float = Field(
        ...,
        ge=20,
        le=200,
        description="Diastolic blood pressure in mmHg (the lower value when blood pressure is "
                    "measured). This represents the pressure in arteries during heart relaxation. "
                    "Normal range is typically 60-80 mmHg. Values below 60 may indicate hypotension, "
                    "while values above 90 indicate hypertension.",
        example=80.0
    )
    
    class Config:
        schema_extra = {
            "example": {
                "systolic_bp": 120.0,
                "diastolic_bp": 80.0
            }
        }


class MeanArterialPressureResponse(BaseModel):
    """
    Response model for Mean Arterial Pressure (MAP) calculation
    
    MAP interpretation guidelines:
    - <60 mmHg: Critical - High risk of organ hypoperfusion
    - 60-65 mmHg: Low - Minimum for organ perfusion
    - 65-70 mmHg: Borderline low - Target for septic shock
    - 70-90 mmHg: Low normal - Monitor in at-risk patients
    - 90-110 mmHg: Normal - Optimal tissue perfusion
    - 110-130 mmHg: Elevated - May indicate hypertension
    - >130 mmHg: High - Risk of end-organ damage
    
    Clinical applications:
    - Critical care: Guide vasopressor therapy
    - Sepsis management: Target MAP ≥65 mmHg
    - Perioperative care: Prevent organ hypoperfusion
    - Hypertension management: Assess overall pressure burden
    
    Reference: Magder SA. Crit Care Med. 2014;42(5):1241-51.
    """
    
    result: float = Field(
        ...,
        description="Calculated Mean Arterial Pressure in mmHg. This represents the average "
                    "pressure in the arteries during one complete cardiac cycle.",
        example=93.3
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for MAP (always mmHg)",
        example="mmHg"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of the MAP value, including significance for "
                    "tissue perfusion and recommendations for clinical management",
        example="Normal mean arterial pressure indicating adequate tissue perfusion. "
                "This range provides optimal blood flow to vital organs."
    )
    
    stage: str = Field(
        ...,
        description="Clinical stage category based on MAP value (Critical, Low, Borderline Low, "
                    "Low Normal, Normal, Elevated, or High)",
        example="Normal"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the MAP stage",
        example="Normal MAP"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 93.3,
                "unit": "mmHg",
                "interpretation": "Normal mean arterial pressure indicating adequate tissue perfusion. "
                                "This range provides optimal blood flow to vital organs.",
                "stage": "Normal",
                "stage_description": "Normal MAP"
            }
        }