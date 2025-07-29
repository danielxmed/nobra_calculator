"""
APACHE II Score Models

Request and response models for APACHE II Score calculation.

References (Vancouver style):
1. Knaus WA, Draper EA, Wagner DP, Zimmerman JE. APACHE II: a severity of disease 
   classification system. Crit Care Med. 1985;13(10):818-29. doi: 10.1097/00003246-198510000-00009. 
   PMID: 3928249.
2. Vincent JL, Moreno R. Clinical review: scoring systems in the critically ill. 
   Crit Care. 2010;14(2):207. doi: 10.1186/cc8204. PMID: 20392287.
3. Zimmerman JE, Kramer AA, McNair DS, Malila FM. Acute Physiology and Chronic Health 
   Evaluation (APACHE) IV: hospital mortality assessment for today's critically ill patients. 
   Crit Care Med. 2006;34(5):1297-310. doi: 10.1097/01.CCM.0000215112.84523.F0. PMID: 16540951.

The APACHE II (Acute Physiology and Chronic Health Evaluation II) score is a severity-of-disease 
classification system used to estimate ICU mortality. It is calculated using the worst values 
from 12 physiological variables within the first 24 hours of ICU admission, plus age and 
chronic health status. The score ranges from 0-71 points, with higher scores indicating 
higher mortality risk. It is one of the most widely used ICU scoring systems globally.
"""

from pydantic import BaseModel, Field
from typing import Literal, Optional


class ApacheIiScoreRequest(BaseModel):
    """
    Request model for APACHE II Score calculation
    
    The APACHE II score uses the worst values from 12 physiological variables within 
    the first 24 hours of ICU admission, plus age and chronic health status:
    
    Physiological Variables (Acute Physiology Score):
    - Temperature: Worst body temperature (rectal) in °C
    - Mean Arterial Pressure: Worst MAP in mmHg
    - Heart Rate: Worst heart rate in bpm  
    - Respiratory Rate: Worst respiratory rate in breaths/min
    - pH: Worst arterial pH
    - Sodium: Worst serum sodium in mEq/L
    - Potassium: Worst serum potassium in mEq/L
    - Creatinine: Worst serum creatinine in mg/dL (doubled if acute renal failure)
    - Hematocrit: Worst hematocrit in %
    - White Blood Cell Count: Worst WBC in ×10³/mm³
    - Glasgow Coma Scale: GCS score (15 - actual GCS = points)
    - Oxygenation: PaO2 (if FiO2 <0.5) or A-aDO2 (if FiO2 ≥0.5)
    
    Age Points:
    - ≤44 years: 0 points
    - 45-54 years: 2 points
    - 55-64 years: 3 points
    - 65-74 years: 5 points
    - ≥75 years: 6 points
    
    Chronic Health Points:
    - None: 0 points
    - Present + elective postoperative: 2 points
    - Present + nonoperative/emergency postoperative: 5 points
    
    Chronic health criteria include: liver cirrhosis with portal hypertension, 
    NYHA Class IV heart failure, severe respiratory disease requiring chronic 
    restrictions, dialysis dependence, or immunocompromised state.

    References (Vancouver style):
    1. Knaus WA, Draper EA, Wagner DP, Zimmerman JE. APACHE II: a severity of disease 
    classification system. Crit Care Med. 1985;13(10):818-29. doi: 10.1097/00003246-198510000-00009. 
    PMID: 3928249.
    2. Vincent JL, Moreno R. Clinical review: scoring systems in the critically ill. 
    Crit Care. 2010;14(2):207. doi: 10.1186/cc8204. PMID: 20392287.
    3. Zimmerman JE, Kramer AA, McNair DS, Malila FM. Acute Physiology and Chronic Health 
    Evaluation (APACHE) IV: hospital mortality assessment for today's critically ill patients. 
    Crit Care Med. 2006;34(5):1297-310. doi: 10.1097/01.CCM.0000215112.84523.F0. PMID: 16540951.
    """
    
    age: int = Field(
        ...,
        description="Patient's age in years. Used for age points: ≤44y=0pts, 45-54y=2pts, 55-64y=3pts, 65-74y=5pts, ≥75y=6pts",
        ge=0,
        le=120,
        example=65
    )
    
    temperature: float = Field(
        ...,
        description="Worst body temperature (rectal) in first 24 hours of ICU admission, in degrees Celsius. Range: 25.0-46.0°C",
        ge=25.0,
        le=46.0,
        example=38.5
    )
    
    mean_arterial_pressure: int = Field(
        ...,
        description="Worst mean arterial pressure in first 24 hours of ICU admission, in mmHg. MAP = (2×diastolic + systolic)/3",
        ge=30,
        le=250,
        example=85
    )
    
    ph: float = Field(
        ...,
        description="Worst arterial blood pH in first 24 hours of ICU admission. Normal range: 7.35-7.45",
        ge=6.5,
        le=8.0,
        example=7.35
    )
    
    heart_rate: int = Field(
        ...,
        description="Worst heart rate in first 24 hours of ICU admission, in beats per minute",
        ge=20,
        le=250,
        example=110
    )
    
    respiratory_rate: int = Field(
        ...,
        description="Worst respiratory rate in first 24 hours of ICU admission, in breaths per minute",
        ge=5,
        le=80,
        example=24
    )
    
    sodium: int = Field(
        ...,
        description="Worst serum sodium in first 24 hours of ICU admission, in mEq/L. Normal range: 136-145 mEq/L",
        ge=100,
        le=200,
        example=140
    )
    
    potassium: float = Field(
        ...,
        description="Worst serum potassium in first 24 hours of ICU admission, in mEq/L. Normal range: 3.5-5.0 mEq/L",
        ge=1.0,
        le=10.0,
        example=4.2
    )
    
    creatinine: float = Field(
        ...,
        description="Worst serum creatinine in first 24 hours of ICU admission, in mg/dL. Normal range: 0.6-1.4 mg/dL. Points are doubled if acute renal failure is present",
        ge=0.1,
        le=20.0,
        example=1.2
    )
    
    acute_renal_failure: Literal["yes", "no"] = Field(
        ...,
        description="Presence of acute renal failure. If yes, creatinine points are doubled. Use clinical judgment to determine acute kidney injury",
        example="no"
    )
    
    hematocrit: float = Field(
        ...,
        description="Worst hematocrit in first 24 hours of ICU admission, as percentage. Normal range: 30-46%",
        ge=10.0,
        le=70.0,
        example=35.0
    )
    
    white_blood_cell_count: float = Field(
        ...,
        description="Worst white blood cell count in first 24 hours of ICU admission, in ×10³/mm³. Normal range: 3-15 ×10³/mm³",
        ge=0.1,
        le=100.0,
        example=12.0
    )
    
    glasgow_coma_scale: int = Field(
        ...,
        description="Glasgow Coma Scale score (3-15 points). If patient is sedated, record estimated GCS before sedation. Points = 15 - actual GCS",
        ge=3,
        le=15,
        example=13
    )
    
    fio2: float = Field(
        ...,
        description="Fraction of inspired oxygen as decimal (0.21-1.0). Room air = 0.21, 100% oxygen = 1.0. Determines whether to use PaO2 or A-aDO2",
        ge=0.21,
        le=1.0,
        example=0.40
    )
    
    pao2: Optional[float] = Field(
        None,
        description="Arterial oxygen pressure in mmHg. Required if FiO2 < 0.5. Normal range on room air: 80-100 mmHg",
        ge=30.0,
        le=700.0,
        example=85.0
    )
    
    aado2: Optional[float] = Field(
        None,
        description="Alveolar-arterial oxygen gradient in mmHg. Required if FiO2 ≥ 0.5. A-aDO2 = PAO2 - PaO2, where PAO2 = (FiO2 × 713) - (PaCO2/0.8)",
        ge=0.0,
        le=800.0,
        example=250.0
    )
    
    chronic_health_status: Literal["none", "present"] = Field(
        ...,
        description="History of severe organ system insufficiency or immunocompromised state. Severe insufficiency includes: liver cirrhosis with portal hypertension, NYHA Class IV heart failure, severe respiratory disease, dialysis dependence, or immunocompromised state",
        example="none"
    )
    
    admission_type: Literal["elective_postoperative", "nonoperative", "emergency_postoperative"] = Field(
        ...,
        description="Type of ICU admission. Elective postoperative = surgery scheduled ≥24h prior, nonoperative = no surgery within 1 week, emergency postoperative = surgery scheduled ≤24h prior",
        example="nonoperative"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": 65,
                "temperature": 38.5,
                "mean_arterial_pressure": 85,
                "ph": 7.35,
                "heart_rate": 110,
                "respiratory_rate": 24,
                "sodium": 140,
                "potassium": 4.2,
                "creatinine": 1.2,
                "acute_renal_failure": "no",
                "hematocrit": 35.0,
                "white_blood_cell_count": 12.0,
                "glasgow_coma_scale": 13,
                "fio2": 0.40,
                "pao2": 85.0,
                "aado2": None,
                "chronic_health_status": "none",
                "admission_type": "nonoperative"
            }
        }


class ApacheIiScoreResponse(BaseModel):
    """
    Response model for APACHE II Score calculation
    
    The APACHE II score ranges from 0-71 points and is associated with increasing 
    mortality risk. The score is composed of:
    - Acute Physiology Score (0-60 points): Based on worst values of 12 physiological variables
    - Age Points (0-6 points): Based on patient age
    - Chronic Health Points (0-5 points): Based on chronic health status and admission type
    
    General mortality risk by score range:
    - 0-9 points: <10% mortality (Low Risk)
    - 10-19 points: 10-25% mortality (Moderate Risk)  
    - 20-29 points: 25-50% mortality (High Risk)
    - 30-39 points: 50-75% mortality (Very High Risk)
    - ≥40 points: >75% mortality (Extremely High Risk)
    
    Note: Predicted mortality requires specific ICU admission diagnosis in addition 
    to APACHE II score for accurate calculation.
    
    Reference: Knaus WA, et al. Crit Care Med. 1985;13(10):818-29.
    """
    
    result: int = Field(
        ...,
        description="APACHE II score calculated from physiological variables, age, and chronic health status (range: 0-71 points)",
        ge=0,
        le=71,
        example=18
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and mortality risk assessment based on the score",
        example="APACHE II score 10-19 points indicates moderate severity of illness with predicted mortality typically 10-25%. Close monitoring and standard ICU care are appropriate."
    )
    
    stage: str = Field(
        ...,
        description="Risk category based on score (Low Risk, Moderate Risk, High Risk, Very High Risk, Extremely High Risk)",
        example="Moderate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Moderate mortality risk"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 18,
                "unit": "points",
                "interpretation": "APACHE II score 10-19 points indicates moderate severity of illness with predicted mortality typically 10-25%. Close monitoring and standard ICU care are appropriate.",
                "stage": "Moderate Risk",
                "stage_description": "Moderate mortality risk"
            }
        }