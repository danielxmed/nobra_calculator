"""
Cardiac Output (Fick's Formula) Models

Request and response models for cardiac output calculation using Fick's principle.

References (Vancouver style):
1. Ragosta M. Textbook of Clinical Hemodynamics. 1st ed. Philadelphia: Elsevier; 2017.
2. Swan HJ, Ganz W, Forrester J, Marcus H, Diamond G, Chonette D. Catheterization 
   of the heart in man with use of a flow-directed balloon-tipped catheter. 
   N Engl J Med. 1970 Aug 27;283(9):447-51. doi: 10.1056/NEJM197008272830902.
3. LaFarge CG, Miettinen OS. The estimation of oxygen consumption. Cardiovasc Res. 
   1970 Jan;4(1):23-30. doi: 10.1093/cvr/4.1.23.

Fick's principle calculates cardiac output based on oxygen consumption and 
arteriovenous oxygen difference. It remains the gold standard method for 
measuring cardiac output in clinical practice.
"""

from pydantic import BaseModel, Field
from typing import Dict, Any


class CardiacOutputFickRequest(BaseModel):
    """
    Request model for Cardiac Output calculation using Fick's Formula
    
    Fick's principle states that cardiac output equals oxygen consumption divided 
    by the arteriovenous oxygen difference. This method is considered the gold 
    standard for cardiac output measurement.
    
    Formula: CO = VO2 / [(SaO2 - SvO2) × Hb × 13.4]
    
    Where:
    - VO2 = Oxygen consumption (125 mL O2/min/m² if age <70, 110 mL O2/min/m² if age ≥70)
    - BSA = Body Surface Area = √[(Height × Weight) / 3600] (Mosteller formula)
    - SaO2 = Arterial oxygen saturation (%)
    - SvO2 = Mixed venous oxygen saturation (%)
    - Hb = Hemoglobin concentration (g/dL)
    - 13.4 = Oxygen-carrying capacity constant (mL O2/g Hb)
    
    Derived Calculations:
    - Cardiac Index (CI) = CO / BSA (L/min/m²)
    - Stroke Volume (SV) = CO / Heart Rate (mL/beat)
    - Stroke Volume Index (SVI) = SV / BSA (mL/beat/m²)
    
    Normal Values:
    - Cardiac Output: 4.0-8.0 L/min
    - Cardiac Index: 2.5-4.0 L/min/m²
    - Stroke Volume: 60-100 mL/beat
    
    Clinical Applications:
    - Assessment of cardiac function in critically ill patients
    - Evaluation of heart failure and cardiogenic shock
    - Monitoring response to inotropic therapy
    - Research studies requiring accurate cardiac output measurement
    
    Requirements:
    - Arterial blood gas analysis (for SaO2)
    - Mixed venous blood gas analysis (requires pulmonary artery catheter for SvO2)
    - Hemoglobin level
    - Accurate heart rate measurement
    
    Limitations:
    - Requires invasive monitoring (pulmonary artery catheter)
    - Assumes steady-state oxygen consumption
    - Less accurate in conditions with abnormal oxygen consumption
    - May be affected by tricuspid regurgitation or intracardiac shunts
    
    References (Vancouver style):
    1. Ragosta M. Textbook of Clinical Hemodynamics. 1st ed. Philadelphia: Elsevier; 2017.
    2. Swan HJ, Ganz W, Forrester J, Marcus H, Diamond G, Chonette D. Catheterization 
    of the heart in man with use of a flow-directed balloon-tipped catheter. 
    N Engl J Med. 1970 Aug 27;283(9):447-51.
    """
    
    height_cm: float = Field(
        ...,
        description="Patient height in centimeters (used for BSA calculation)",
        ge=50,
        le=250,
        example=175.0
    )
    
    weight_kg: float = Field(
        ...,
        description="Patient weight in kilograms (used for BSA calculation)",
        ge=10,
        le=300,
        example=70.0
    )
    
    age_years: int = Field(
        ...,
        description="Patient age in years (≥70 years uses lower VO2 estimate of 110 mL O2/min/m²)",
        ge=0,
        le=120,
        example=45
    )
    
    hemoglobin_g_dl: float = Field(
        ...,
        description="Hemoglobin concentration in g/dL (determines oxygen-carrying capacity)",
        ge=3.0,
        le=25.0,
        example=12.5
    )
    
    sao2_percent: float = Field(
        ...,
        description="Arterial oxygen saturation as percentage (from arterial blood gas)",
        ge=50.0,
        le=100.0,
        example=98.0
    )
    
    svo2_percent: float = Field(
        ...,
        description="Mixed venous oxygen saturation as percentage (requires pulmonary artery catheter)",
        ge=30.0,
        le=90.0,
        example=70.0
    )
    
    heart_rate_bpm: int = Field(
        ...,
        description="Heart rate in beats per minute (for stroke volume calculation)",
        ge=30,
        le=250,
        example=75
    )
    
    class Config:
        schema_extra = {
            "example": {
                "height_cm": 175.0,
                "weight_kg": 70.0,
                "age_years": 45,
                "hemoglobin_g_dl": 12.5,
                "sao2_percent": 98.0,
                "svo2_percent": 70.0,
                "heart_rate_bpm": 75
            }
        }


class CardiacOutputFickResponse(BaseModel):
    """
    Response model for Cardiac Output calculation using Fick's Formula
    
    Provides comprehensive cardiac hemodynamic assessment including cardiac output, 
    cardiac index, stroke volume, and clinical interpretations.
    
    Results Include:
    - Cardiac Output (CO): Total blood flow from the heart (L/min)
    - Cardiac Index (CI): CO normalized to body surface area (L/min/m²)
    - Stroke Volume (SV): Blood ejected per heartbeat (mL/beat)
    - Stroke Volume Index (SVI): SV normalized to BSA (mL/beat/m²)
    - Body Surface Area (BSA): Calculated using Mosteller formula (m²)
    - Oxygen Consumption (VO2): Estimated metabolic oxygen demand (mL/min)
    - AV Oxygen Difference: Arteriovenous oxygen content difference
    
    Clinical Interpretation:
    
    Low Cardiac Output/Index may indicate:
    - Hypovolemia (dehydration, blood loss)
    - Cardiogenic shock (heart failure, MI)
    - Severe metabolic acidosis
    - Arrhythmias
    - Increased afterload (severe hypertension)
    
    High Cardiac Output/Index may indicate:
    - Hypoxia or hypoxemia
    - Early septic shock (hyperdynamic phase)
    - Severe anemia
    - Hyperthyroidism
    - Positive inotropic medications
    - Arteriovenous malformations
    
    Low Stroke Volume may indicate:
    - Impaired left ventricular contractility
    - Increased afterload
    - Decreased preload (hypovolemia)
    - Tachycardia
    - Acidosis or hypoxemia
    
    High Stroke Volume may indicate:
    - Bradycardia
    - Positive inotropic effects
    - Decreased afterload
    - Athletic conditioning
    
    Clinical Applications:
    - Critical care monitoring
    - Heart failure management
    - Shock evaluation and treatment
    - Cardiac surgery perioperative care
    - Research studies
    
    Reference: Ragosta M. Textbook of Clinical Hemodynamics. Elsevier; 2017.
    """
    
    result: Dict[str, Any] = Field(
        ...,
        description="Comprehensive cardiac measurements including CO, CI, SV, SVI, BSA, VO2, and AV O2 difference",
        example={
            "cardiac_output": 5.25,
            "cardiac_index": 2.75,
            "stroke_volume": 70.0,
            "stroke_volume_index": 36.8,
            "body_surface_area": 1.91,
            "oxygen_consumption": 238.8,
            "av_oxygen_difference": 4.55
        }
    )
    
    unit: str = Field(
        ...,
        description="Units for the measurements",
        example="L/min, L/min/m², mL/beat"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of cardiac output, cardiac index, and stroke volume",
        example="Cardiac Output: Normal cardiac output (4.0-8.0 L/min). Cardiac Index: Normal cardiac index (2.5-4.0 L/min/m²). Stroke Volume: Normal stroke volume (60-100 mL/beat)"
    )
    
    stage: str = Field(
        ...,
        description="Overall cardiac function assessment",
        example="Normal Cardiac Function"
    )
    
    stage_description: str = Field(
        ...,
        description="Description of overall cardiac performance",
        example="Normal cardiac parameters"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": {
                    "cardiac_output": 5.25,
                    "cardiac_index": 2.75,
                    "stroke_volume": 70.0,
                    "stroke_volume_index": 36.8,
                    "body_surface_area": 1.91,
                    "oxygen_consumption": 238.8,
                    "av_oxygen_difference": 4.55
                },
                "unit": "L/min, L/min/m², mL/beat",
                "interpretation": "Cardiac Output: Normal cardiac output (4.0-8.0 L/min). Cardiac Index: Normal cardiac index (2.5-4.0 L/min/m²). Stroke Volume: Normal stroke volume (60-100 mL/beat)",
                "stage": "Normal Cardiac Function",
                "stage_description": "Normal cardiac parameters"
            }
        }