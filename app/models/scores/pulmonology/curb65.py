"""
CURB-65 Score calculation models
"""

from pydantic import BaseModel, Field, field_validator
from typing import Dict


class Curb65Request(BaseModel):
    """
    Request model for CURB-65 Score calculation
    
    The CURB-65 score is a clinical prediction rule for assessing pneumonia severity and 
    guiding treatment decisions regarding hospitalization and antibiotic therapy.
    
    **Clinical Use**:
    - Pneumonia severity assessment
    - Hospitalization decision-making
    - ICU admission criteria
    - Antibiotic therapy guidance
    - Mortality risk prediction
    
    **Score Components**:
    - C: Confusion (new onset mental confusion)
    - U: Urea >19 mg/dL (>7 mmol/L)
    - R: Respiratory rate ≥30/min
    - B: Blood pressure (systolic <90 or diastolic ≤60 mmHg)
    - 65: Age ≥65 years
    
    **Reference**: Lim WS, et al. Defining community acquired pneumonia severity on presentation to hospital: an international derivation and validation study. Thorax. 2003;58(5):377-82.
    """
    confusion: bool = Field(
        ..., 
        description="Recent onset mental confusion defined as disorientation in time, place, or person. New confusion not attributable to other causes.",
        example=False
    )
    urea: float = Field(
        ..., 
        ge=0, 
        le=200, 
        description="Serum urea (BUN) concentration in mg/dL. Values ≥19 mg/dL (≥7 mmol/L) indicate renal impairment and add 1 point.",
        example=25.0
    )
    respiratory_rate: int = Field(
        ..., 
        ge=0, 
        le=60, 
        description="Respiratory rate in breaths per minute. Values ≥30/min indicate respiratory compromise and add 1 point.",
        example=32
    )
    systolic_bp: int = Field(
        ..., 
        ge=0, 
        le=300, 
        description="Systolic blood pressure in mmHg. Values <90 mmHg indicate hemodynamic instability.",
        example=85
    )
    diastolic_bp: int = Field(
        ..., 
        ge=0, 
        le=200, 
        description="Diastolic blood pressure in mmHg. Values ≤60 mmHg indicate hemodynamic instability.",
        example=55
    )
    age: int = Field(
        ..., 
        ge=0, 
        le=120, 
        description="Patient's age in years. Age ≥65 years adds 1 point, reflecting increased mortality risk in elderly patients.",
        example=78
    )
    
    @field_validator('diastolic_bp')
    def validate_blood_pressure(cls, v, info):
        if 'systolic_bp' in info.data and v > info.data['systolic_bp']:
            raise ValueError('Diastolic pressure cannot be greater than systolic pressure')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "confusion": False,
                "urea": 25.0,
                "respiratory_rate": 32,
                "systolic_bp": 85,
                "diastolic_bp": 55,
                "age": 78
            }
        }


class Curb65Response(BaseModel):
    """
    Response model for CURB-65 Score calculation
    
    Provides pneumonia severity assessment with evidence-based treatment recommendations
    and mortality risk stratification.
    
    **Management Guidelines**:
    - Score 0-1: Low risk (1.5% mortality) - outpatient treatment usually appropriate
    - Score 2: Moderate risk (9.2% mortality) - consider hospitalization
    - Score 3-5: High risk (22% mortality) - hospitalization recommended, consider ICU if ≥4
    
    **Antibiotic Recommendations**:
    - Outpatient: Oral antibiotics (amoxicillin, macrolides, fluoroquinolones)
    - Inpatient: IV antibiotics (beta-lactam + macrolide, fluoroquinolone)
    - ICU: Broad-spectrum IV antibiotics with anti-pseudomonal coverage if indicated
    """
    result: int = Field(
        ..., 
        description="Total CURB-65 score ranging from 0-5 points. Higher scores indicate increased severity and mortality risk.",
        example=3
    )
    unit: str = Field(
        ..., 
        description="Unit of the score result",
        example="points"
    )
    interpretation: str = Field(
        ..., 
        description="Evidence-based clinical interpretation with specific treatment recommendations including hospitalization and antibiotic therapy guidance.",
        example="Mandatory hospital admission. Consider ICU admission, especially if CURB-65 ≥ 4. Start intravenous antibiotic therapy immediately."
    )
    stage: str = Field(
        ..., 
        description="Risk classification (Low Risk, Moderate Risk, High Risk) based on mortality prediction",
        example="High Risk"
    )
    stage_description: str = Field(
        ..., 
        description="Description of the risk level with associated mortality percentage",
        example="Mortality: 22%"
    )
    mortality_risk: str = Field(
        ..., 
        description="Estimated mortality risk percentage based on validation studies",
        example="22%"
    )
    components: Dict[str, int] = Field(
        ..., 
        description="Breakdown of points contributed by each CURB-65 component for clinical transparency",
        example={
            "confusion": 0,
            "urea": 1,
            "respiratory_rate": 1,
            "blood_pressure": 1,
            "age": 1
        }
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 3,
                "unit": "points",
                "interpretation": "Mandatory hospital admission. Consider ICU admission, especially if CURB-65 ≥ 4. Start intravenous antibiotic therapy immediately.",
                "stage": "High Risk",
                "stage_description": "Mortality: 22%",
                "mortality_risk": "22%",
                "components": {
                    "confusion": 0,
                    "urea": 1,
                    "respiratory_rate": 1,
                    "blood_pressure": 1,
                    "age": 1
                }
            }
        }