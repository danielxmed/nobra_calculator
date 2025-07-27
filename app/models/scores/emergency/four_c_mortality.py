"""
FourCMortality calculation models
"""

from pydantic import BaseModel, Field
from app.models.shared import SexType

class FourCMortalityRequest(BaseModel):
    """
    Request model for 4C Mortality Score calculation
    
    The 4C Mortality Score predicts in-hospital mortality in patients with COVID-19,
    helping clinicians with risk stratification and treatment intensity decisions.
    
    **Clinical Use**:
    - COVID-19 mortality risk prediction
    - Hospital admission decision-making
    - ICU triage and resource allocation
    - Treatment intensity guidance
    - Patient and family counseling
    - Clinical trial stratification
    
    **Score Components**:
    - Age, sex, comorbidities
    - Respiratory rate, oxygen saturation
    - Glasgow Coma Scale
    - Urea, C-reactive protein
    
    **Reference**: Knight SR, et al. Risk stratification of patients admitted to hospital with covid-19 using the ISARIC WHO Clinical Characterisation Protocol: development and validation of the 4C Mortality Score. BMJ. 2020;370:m3339.
    """
    age: int = Field(
        ..., 
        ge=0, 
        le=120, 
        description="Patient's age in years. Age is the strongest predictor in the 4C score, with points increasing progressively: <50 years (0 points), 50-59 (2 points), 60-69 (4 points), 70-79 (6 points), ≥80 (7 points).",
        example=70
    )
    sex: SexType = Field(
        ..., 
        description="Patient's biological sex. Male sex adds 1 point, reflecting the observed higher mortality risk in men with COVID-19.",
        example="male"
    )
    comorbidities: int = Field(
        ..., 
        ge=0, 
        le=20, 
        description="Number of comorbidities from predefined list (chronic cardiac disease, chronic pulmonary disease, asthma, chronic kidney disease, mild/moderate/severe liver disease, dementia, chronic neurological conditions, connective tissue disease, diabetes, HIV/AIDS, malignancy). Each comorbidity adds 1 point.",
        example=2
    )
    respiratory_rate: int = Field(
        ..., 
        ge=5, 
        le=60, 
        description="Respiratory rate in breaths per minute. Higher rates indicate respiratory compromise: <20 (0 points), 20-29 (1 point), ≥30 (2 points).",
        example=24
    )
    oxygen_saturation: float = Field(
        ..., 
        ge=50.0, 
        le=100.0, 
        description="Peripheral oxygen saturation on room air or current oxygen therapy (%). Lower saturations indicate worse prognosis: >95% (0 points), 92-95% (2 points), <92% (3 points).",
        example=92.0
    )
    glasgow_coma_scale: int = Field(
        ..., 
        ge=3, 
        le=15, 
        description="Glasgow Coma Scale score. Lower scores indicate altered consciousness and worse prognosis: 15 (0 points), 12-14 (1 point), <12 (2 points).",
        example=15
    )
    urea_unit: UreaUnitType = Field(
        ..., 
        description="Unit for urea measurement. Can be mmol/L (standard international unit) or mg/dL (US unit). Conversion: mg/dL = mmol/L × 2.8.",
        example="mg_dL"
    )
    urea_value: float = Field(
        ..., 
        ge=0.1, 
        le=300.0, 
        description="Serum urea value. Elevated urea indicates renal impairment and worse prognosis. Points based on units: mmol/L (<7=0, 7-14=1, >14=3) or mg/dL (<19.6=0, 19.6-39.2=1, >39.2=3).",
        example=45.0
    )
    crp: float = Field(
        ..., 
        ge=0.0, 
        le=1000.0, 
        description="C-reactive protein in mg/L. Elevated CRP indicates systemic inflammation: <50 mg/L (0 points), 50-99 (1 point), ≥100 (2 points).",
        example=80.0
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": 70,
                "sex": "male",
                "comorbidities": 2,
                "respiratory_rate": 24,
                "oxygen_saturation": 92.0,
                "glasgow_coma_scale": 15,
                "urea_unit": "mg_dL",
                "urea_value": 45.0,
                "crp": 80.0
            }
        }


class FourCMortalityResponse(BaseModel):
    """
    Response model for 4C Mortality Score calculation
    
    Provides comprehensive COVID-19 mortality risk assessment with evidence-based
    management recommendations and resource allocation guidance.
    
    **Risk Stratification & Management**:
    - Score 0-3: Low risk (1.2% mortality) - standard ward care, monitor for deterioration
    - Score 4-8: Intermediate risk (9.9% mortality) - enhanced monitoring, consider high-dependency unit
    - Score 9-14: High risk (31.4% mortality) - intensive monitoring, consider ICU evaluation
    - Score ≥15: Very high risk (61.5% mortality) - ICU-level care, advanced life support planning
    
    **Clinical Actions**:
    - Corticosteroids (dexamethasone) for patients requiring oxygen
    - Remdesivir consideration in appropriate patients
    - Thromboprophylaxis for all hospitalized patients
    - Early identification of complications (ARDS, secondary infections)
    """
    result: int = Field(
        ..., 
        description="Total 4C score ranging from 0-21 points. Higher scores indicate progressively increased in-hospital mortality risk from COVID-19.",
        example=10
    )
    unit: str = Field(
        ..., 
        description="Unit of the score result",
        example="points"
    )
    interpretation: str = Field(
        ..., 
        description="Evidence-based clinical interpretation with specific mortality risk and management recommendations based on current COVID-19 treatment guidelines.",
        example="In-hospital mortality of 31.4-34.9%. Patients require intensive care or high-dependency unit monitoring."
    )
    stage: str = Field(
        ..., 
        description="Mortality risk classification (Low Risk, Intermediate Risk, High Risk, Very High Risk)",
        example="High Risk"
    )
    stage_description: str = Field(
        ..., 
        description="Description of the mortality risk level",
        example="High mortality risk"
    )
    mortality_risk: str = Field(
        ..., 
        description="Estimated in-hospital mortality risk percentage based on large validation cohorts",
        example="31.4-34.9%"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 10,
                "unit": "points",
                "interpretation": "In-hospital mortality of 31.4-34.9%. Patients require intensive care or high-dependency unit monitoring.",
                "stage": "High Risk",
                "stage_description": "High mortality risk",
                "mortality_risk": "31.4-34.9%"
            }
        }