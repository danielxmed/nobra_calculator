"""
REMS Score (Rapid Emergency Medicine Score) Models

Request and response models for REMS Score calculation.

References (Vancouver style):
1. Olsson T, Terent A, Lind L. Rapid Emergency Medicine score: a new prognostic 
   tool for in-hospital mortality in nonsurgical emergency department patients. 
   J Intern Med. 2004;255(5):579-587. doi: 10.1111/j.1365-2796.2004.01321.x.
2. Goodacre S, Turner J, Nicholl J. Prediction of mortality among emergency medical 
   admissions. Emerg Med J. 2006;23(5):372-375. doi: 10.1136/emj.2005.028522.
3. Imhoff BF, Thompson NJ, Hastings MA, et al. Rapid Emergency Medicine Score (REMS) 
   in the trauma population: a retrospective study. BMJ Open. 2014;4(5):e004738. 
   doi: 10.1136/bmjopen-2013-004738.
4. Chuang CL, Tsai KC, Wu CL, et al. The utility of the rapid emergency medicine score 
   (REMS) compared with SIRS, qSOFA and NEWS for predicting in-hospital mortality among 
   patients with suspicion of sepsis in an emergency department. BMC Emerg Med. 
   2021;21(1):2. doi: 10.1186/s12873-020-00396-x.

The REMS (Rapid Emergency Medicine Score) is an emergency department mortality risk 
prediction tool designed as an attenuated version of APACHE II for rapid calculation. 
It uses six readily available clinical parameters to assess in-hospital mortality risk 
and has been extensively validated across multiple patient populations including sepsis, 
trauma, COVID-19, and general emergency department admissions.

The score ranges from 0-26 points and provides excellent discrimination for mortality 
prediction, with every point increase associated with a 40% increase in odds of 
in-hospital mortality. REMS has demonstrated superior or comparable performance to 
other emergency scoring systems like NEWS, qSOFA, and SIRS, making it particularly 
valuable for early risk stratification and triage decisions.
"""

from pydantic import BaseModel, Field
from typing import Dict, Any


class RemsScoreRequest(BaseModel):
    """
    Request model for REMS (Rapid Emergency Medicine Score)
    
    The REMS is a 6-parameter emergency department mortality risk prediction tool 
    that combines physiological variables with patient age to provide rapid assessment 
    of in-hospital mortality risk. Each parameter is scored on a scale with higher 
    values indicating greater abnormality and increased mortality risk.
    
    **CLINICAL PARAMETERS:**
    
    **1. Age (0-6 points):**
    - <45 years: 0 points (baseline)
    - 45-54 years: 2 points
    - 55-64 years: 3 points  
    - 65-74 years: 5 points
    - >74 years: 6 points
    
    **2. Body Temperature (0-4 points):**
    - 36-38.4°C: 0 points (normal range)
    - 38.5-38.9°C: 1 point (mild fever)
    - 34-35.9°C: 1 point (mild hypothermia)
    - 32-33.9°C: 2 points (moderate hypothermia)
    - 39-40.9°C: 3 points (high fever)
    - 30-31.9°C: 3 points (severe hypothermia)
    - <30°C or >40.9°C: 4 points (extreme temperatures)
    
    **3. Mean Arterial Pressure (0-4 points):**
    - 70-109 mmHg: 0 points (normal range)
    - 50-69 mmHg: 1 point (mild hypotension)
    - <50 mmHg: 2 points (severe hypotension)
    - 110-129 mmHg: 2 points (mild hypertension)
    - 130-159 mmHg: 3 points (moderate hypertension)
    - ≥160 mmHg: 4 points (severe hypertension)
    
    **4. Heart Rate (0-4 points):**
    - 70-109 bpm: 0 points (normal range)
    - 55-69 bpm: 1 point (mild bradycardia)
    - 40-54 bpm: 2 points (moderate bradycardia)
    - 110-139 bpm: 2 points (mild tachycardia)
    - <40 bpm: 3 points (severe bradycardia)
    - 140-179 bpm: 3 points (moderate tachycardia)
    - ≥180 bpm: 4 points (severe tachycardia)
    
    **5. Respiratory Rate (0-4 points):**
    - 12-24 breaths/min: 0 points (normal range)
    - 10-11 breaths/min: 1 point (mild hypoventilation)
    - 6-9 breaths/min: 2 points (moderate hypoventilation)
    - 25-34 breaths/min: 2 points (mild tachypnea)
    - <6 breaths/min: 3 points (severe hypoventilation)
    - 35-49 breaths/min: 3 points (moderate tachypnea)
    - >49 breaths/min: 4 points (severe tachypnea)
    
    **6. Oxygen Saturation (0-4 points):**
    - >89%: 0 points (normal oxygenation)
    - 86-89%: 2 points (mild hypoxemia)
    - 75-85%: 3 points (moderate hypoxemia)
    - <75%: 4 points (severe hypoxemia)
    
    **7. Glasgow Coma Scale (0-4 points):**
    - >13: 0 points (normal consciousness)
    - 11-13: 1 point (mild impairment)
    - 8-10: 2 points (moderate impairment)
    - 5-7: 3 points (severe impairment)
    - <5: 4 points (profound impairment)
    
    **MORTALITY RISK STRATIFICATION:**
    - 0-2 points: Very Low Risk (0.3% mortality)
    - 3-5 points: Low Risk (2% mortality)
    - 6-9 points: Moderate Risk (6.7% mortality)
    - 10-11 points: High Risk (20.3% mortality)
    - 12-21 points: Very High Risk (>20% mortality)
    - 22-26 points: Extremely High Risk (approaching 100% mortality)
    
    **CLINICAL APPLICATIONS:**
    - Emergency department triage and risk stratification
    - Early identification of high-risk patients requiring intensive monitoring
    - Resource allocation and care escalation decisions
    - Prognostic assessment for family discussions
    - Quality improvement and outcome benchmarking
    
    References (Vancouver style):
    1. Olsson T, Terent A, Lind L. J Intern Med. 2004;255(5):579-587.
    2. Goodacre S, Turner J, Nicholl J. Emerg Med J. 2006;23(5):372-375.
    3. Imhoff BF, Thompson NJ, Hastings MA, et al. BMJ Open. 2014;4(5):e004738.
    4. Chuang CL, Tsai KC, Wu CL, et al. BMC Emerg Med. 2021;21(1):2.
    """
    
    age: int = Field(
        ...,
        description="Patient age in years. Scoring: <45 years (0 pts), 45-54 years (2 pts), 55-64 years (3 pts), 65-74 years (5 pts), >74 years (6 pts)",
        ge=0,
        le=120,
        example=67
    )
    
    body_temperature: float = Field(
        ...,
        description="Body temperature in degrees Celsius. Scoring: 36-38.4°C (0 pts), 38.5-38.9°C (1 pt), 34-35.9°C (1 pt), 32-33.9°C (2 pts), 39-40.9°C (3 pts), 30-31.9°C (3 pts), <30°C or >40.9°C (4 pts)",
        ge=25.0,
        le=45.0,
        example=37.2
    )
    
    mean_arterial_pressure: int = Field(
        ...,
        description="Mean arterial pressure in mmHg. Scoring: 70-109 mmHg (0 pts), 50-69 mmHg (1 pt), <50 mmHg (2 pts), 110-129 mmHg (2 pts), 130-159 mmHg (3 pts), ≥160 mmHg (4 pts)",
        ge=20,
        le=250,
        example=85
    )
    
    heart_rate: int = Field(
        ...,
        description="Heart rate in beats per minute. Scoring: 70-109 bpm (0 pts), 55-69 bpm (1 pt), 40-54 bpm (2 pts), 110-139 bpm (2 pts), <40 bpm (3 pts), 140-179 bpm (3 pts), ≥180 bpm (4 pts)",
        ge=20,
        le=250,
        example=95
    )
    
    respiratory_rate: int = Field(
        ...,
        description="Respiratory rate in breaths per minute. Scoring: 12-24 breaths/min (0 pts), 10-11 breaths/min (1 pt), 6-9 breaths/min (2 pts), 25-34 breaths/min (2 pts), <6 breaths/min (3 pts), 35-49 breaths/min (3 pts), >49 breaths/min (4 pts)",
        ge=1,
        le=80,
        example=18
    )
    
    oxygen_saturation: int = Field(
        ...,
        description="Peripheral oxygen saturation (SpO2) percentage. Scoring: >89% (0 pts), 86-89% (2 pts), 75-85% (3 pts), <75% (4 pts)",
        ge=50,
        le=100,
        example=96
    )
    
    glasgow_coma_scale: int = Field(
        ...,
        description="Glasgow Coma Scale score (3-15). Scoring: >13 (0 pts), 11-13 (1 pt), 8-10 (2 pts), 5-7 (3 pts), <5 (4 pts)",
        ge=3,
        le=15,
        example=14
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": 67,
                "body_temperature": 37.2,
                "mean_arterial_pressure": 85,
                "heart_rate": 95,
                "respiratory_rate": 18,
                "oxygen_saturation": 96,
                "glasgow_coma_scale": 14
            }
        }


class RemsScoreResponse(BaseModel):
    """
    Response model for REMS (Rapid Emergency Medicine Score)
    
    The REMS response provides the total score (0-26 points), mortality risk 
    stratification, clinical interpretation, and component scores breakdown. 
    The score has been extensively validated for predicting in-hospital mortality 
    in emergency department patients.
    
    **SCORE INTERPRETATION:**
    
    **Total Score Range:** 0-26 points (sum of all component scores)
    
    **Risk Stratification:**
    - **Very Low Risk (0-2 points):** 0.3% in-hospital mortality
    - **Low Risk (3-5 points):** 2% in-hospital mortality  
    - **Moderate Risk (6-9 points):** 6.7% in-hospital mortality
    - **High Risk (10-11 points):** 20.3% in-hospital mortality
    - **Very High Risk (12-21 points):** >20% in-hospital mortality
    - **Extremely High Risk (22-26 points):** Approaching 100% mortality
    
    **CLINICAL PERFORMANCE:**
    
    **Discrimination Ability:**
    - Excellent discrimination with AUC values typically >0.80
    - Every point increase associated with 40% increase in mortality odds
    - Superior or comparable performance to NEWS, qSOFA, and SIRS
    
    **Validation Results:**
    - Original validation: 1,629 patients, mortality rates as described above
    - Multiple subsequent validations across diverse populations
    - Consistent performance in sepsis, trauma, COVID-19, and general ED patients
    
    **CLINICAL MANAGEMENT IMPLICATIONS:**
    
    **Low Risk (≤5 points):**
    - Standard emergency department care appropriate
    - Routine monitoring and disposition planning
    - Outpatient management may be considered for appropriate patients
    
    **Moderate Risk (6-9 points):**
    - Enhanced monitoring and closer observation
    - Consider inpatient admission for further evaluation
    - Prompt intervention for clinical deterioration
    
    **High Risk (≥10 points):**
    - Immediate intensive monitoring required
    - Strong consideration for intensive care unit evaluation
    - Aggressive intervention and frequent reassessment
    - Early involvement of critical care specialists
    
    **Very High Risk (≥12 points):**
    - Critical care management essential
    - Continuous monitoring and life support measures
    - Family discussions regarding prognosis and goals of care
    - Consideration of palliative care for extremely high scores (≥22 points)
    
    **ADVANTAGES OF REMS:**
    
    **Rapid Calculation:**
    - Uses readily available clinical parameters
    - No laboratory tests required for basic calculation
    - Can be computed quickly at bedside or triage
    
    **Broad Applicability:**
    - Validated across multiple patient populations
    - Applicable to both medical and trauma patients
    - Useful across different healthcare settings
    
    **Clinical Integration:**
    - Easily incorporated into electronic health records
    - Supports triage and resource allocation decisions
    - Facilitates communication among healthcare providers
    
    Reference: Olsson T, et al. J Intern Med. 2004;255(5):579-587.
    """
    
    result: int = Field(
        ...,
        description="Total REMS score in points (0-26). Higher scores indicate increased mortality risk",
        ge=0,
        le=26,
        example=8
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with mortality risk assessment and management recommendations based on the REMS score",
        example="REMS Score: 8 points. Moderate risk of in-hospital mortality (6.7%). Enhanced monitoring and prompt intervention indicated."
    )
    
    stage: str = Field(
        ...,
        description="Mortality risk stratification category (Very Low Risk, Low Risk, Moderate Risk, High Risk, Very High Risk, Extremely High Risk)",
        example="Moderate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Moderate mortality risk"
    )
    
    component_scores: Dict[str, int] = Field(
        ...,
        description="Breakdown of scores from each component parameter",
        example={
            "age_score": 5,
            "temperature_score": 0,
            "map_score": 0,
            "heart_rate_score": 0,
            "respiratory_rate_score": 0,
            "oxygen_saturation_score": 0,
            "glasgow_coma_scale_score": 0
        }
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 8,
                "unit": "points",
                "interpretation": "REMS Score: 8 points. Moderate risk of in-hospital mortality (6.7%). Enhanced monitoring and prompt intervention indicated.",
                "stage": "Moderate Risk",
                "stage_description": "Moderate mortality risk",
                "component_scores": {
                    "age_score": 5,
                    "temperature_score": 0,
                    "map_score": 0,
                    "heart_rate_score": 0,
                    "respiratory_rate_score": 0,
                    "oxygen_saturation_score": 0,
                    "glasgow_coma_scale_score": 0
                }
            }
        }