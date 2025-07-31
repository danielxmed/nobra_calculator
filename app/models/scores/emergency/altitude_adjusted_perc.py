"""
Altitude-Adjusted PERC Rule Models

Request and response models for Altitude-Adjusted PERC Rule calculation.

References (Vancouver style):
1. Wolf SJ, McCubbin TR, Nordenholz KE, Naviaux NW, Haukoos JS, Kline JA. Assessment 
   of the pulmonary embolism rule-out criteria rule for evaluation of suspected pulmonary 
   embolism in the emergency department. Am J Emerg Med. 2008 Feb;26(2):181-5. 
   doi: 10.1016/j.ajem.2007.04.026.
2. Kline JA, Mitchell AM, Kabrhel C, Richman PB, Courtney DM. Clinical criteria to 
   prevent unnecessary diagnostic testing in emergency department patients with suspected 
   pulmonary embolism. J Thromb Haemost. 2004 Aug;2(8):1247-55. 
   doi: 10.1111/j.1538-7836.2004.00790.x.
3. Kline JA, Courtney DM, Kabrhel C, Moore CL, Smithline HA, Plewa MC, et al. Prospective 
   multicenter evaluation of the pulmonary embolism rule-out criteria. J Thromb Haemost. 
   2008 May;6(5):772-80. doi: 10.1111/j.1538-7836.2008.02944.x.

The Altitude-Adjusted PERC Rule is a modification of the original PERC (Pulmonary 
Embolism Rule-out Criteria) designed for use in high-altitude settings (>4000 ft). 
The key difference is the removal of the oxygen saturation criterion (<95% on room air) 
because normal SaO₂ is naturally lower at high altitude, making this criterion unreliable 
for ruling out PE in these environments.
"""

from pydantic import BaseModel, Field
from typing import Literal


class AltitudeAdjustedPercRequest(BaseModel):
    """
    Request model for Altitude-Adjusted PERC Rule
    
    The Altitude-Adjusted PERC Rule uses 7 clinical criteria to rule out pulmonary 
    embolism in patients with low pretest probability (<15%) who live at high altitude 
    (>4000 ft):
    
    Clinical Criteria:
    1. Age ≥50 years
    2. Heart rate ≥100 beats per minute
    3. Unilateral leg swelling
    4. Hemoptysis (coughing up blood)
    5. Recent surgery or trauma (≤4 weeks requiring general anesthesia)
    6. Prior history of PE or DVT
    7. Hormone use (oral contraceptives, HRT, estrogenic hormones)
    
    Key Features:
    - Intended ONLY for patients living at high altitude (>4000 ft)
    - Removes oxygen saturation criterion from standard PERC rule
    - Should only be used when clinician's pretest probability is <15%
    - If ALL criteria are negative, PE is ruled out (<2% chance)
    - If ANY criterion is positive, further workup is needed
    
    Exclusions:
    - Not validated for patients at sea level or low altitude
    - Should not be used in patients with moderate/high pretest probability
    - Not applicable if clinician gestalt suggests PE is likely

    References (Vancouver style):
    1. Wolf SJ, McCubbin TR, Nordenholz KE, Naviaux NW, Haukoos JS, Kline JA. Assessment 
    of the pulmonary embolism rule-out criteria rule for evaluation of suspected pulmonary 
    embolism in the emergency department. Am J Emerg Med. 2008 Feb;26(2):181-5. 
    doi: 10.1016/j.ajem.2007.04.026.
    2. Kline JA, Mitchell AM, Kabrhel C, Richman PB, Courtney DM. Clinical criteria to 
    prevent unnecessary diagnostic testing in emergency department patients with suspected 
    pulmonary embolism. J Thromb Haemost. 2004 Aug;2(8):1247-55. 
    doi: 10.1111/j.1538-7836.2004.00790.x.
    """
    
    high_altitude: Literal["yes", "no"] = Field(
        ...,
        description="Patient lives at high altitude (>4000 ft). This rule is ONLY applicable for high-altitude residents",
        example="yes"
    )
    
    age_50_or_older: Literal["yes", "no"] = Field(
        ...,
        description="Patient age ≥50 years. Older age increases PE risk",
        example="no"
    )
    
    hr_100_or_greater: Literal["yes", "no"] = Field(
        ...,
        description="Heart rate ≥100 beats per minute. Tachycardia may indicate physiologic stress from PE",
        example="no"
    )
    
    unilateral_leg_swelling: Literal["yes", "no"] = Field(
        ...,
        description="Unilateral leg swelling suggesting deep vein thrombosis (DVT), which can be associated with PE",
        example="no"
    )
    
    hemoptysis: Literal["yes", "no"] = Field(
        ...,
        description="Hemoptysis (coughing up blood). May indicate pulmonary pathology including PE",
        example="no"
    )
    
    recent_surgery_trauma: Literal["yes", "no"] = Field(
        ...,
        description="Recent surgery or trauma within 4 weeks requiring general anesthesia. Increases thrombotic risk due to immobilization and hypercoagulable state",
        example="no"
    )
    
    prior_pe_dvt: Literal["yes", "no"] = Field(
        ...,
        description="Prior history of pulmonary embolism (PE) or deep vein thrombosis (DVT). Previous VTE increases risk of recurrence",
        example="no"
    )
    
    hormone_use: Literal["yes", "no"] = Field(
        ...,
        description="Current hormone use including oral contraceptives, hormone replacement therapy, or estrogenic hormones. Estrogen increases thrombotic risk",
        example="no"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "high_altitude": "yes",
                "age_50_or_older": "no",
                "hr_100_or_greater": "no",
                "unilateral_leg_swelling": "no",
                "hemoptysis": "no",
                "recent_surgery_trauma": "no",
                "prior_pe_dvt": "no",
                "hormone_use": "no"
            }
        }


class AltitudeAdjustedPercResponse(BaseModel):
    """
    Response model for Altitude-Adjusted PERC Rule
    
    Interpretation:
    
    PERC Negative (0 criteria present):
    - PE can be safely ruled out (<2% chance)
    - No further diagnostic testing needed
    - Patient can be discharged
    - Only valid if pretest probability <15%
    
    PERC Positive (1+ criteria present):
    - Cannot rule out PE
    - Further diagnostic workup indicated
    - Consider D-dimer, CT pulmonary angiogram, V/Q scan
    - Clinical judgment required for next steps
    
    The rule is designed to help clinicians avoid unnecessary testing in very 
    low-risk patients while ensuring that appropriate testing is performed 
    when clinically indicated.
    
    Reference: Wolf SJ, et al. Am J Emerg Med. 2008;26(2):181-5.
    """
    
    result: str = Field(
        ...,
        description="PERC rule result: 'PERC Negative' if no criteria present, 'PERC Positive' if any criteria present",
        example="PERC Negative"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the result",
        example="recommendation"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with specific recommendations based on the result",
        example="PERC rule criteria satisfied. No need for further workup, as <2% chance of PE. Patient can be safely discharged without additional testing for PE if clinician's pretest probability is <15%."
    )
    
    stage: str = Field(
        ...,
        description="Clinical stage classification (PERC Negative or PERC Positive)",
        example="PERC Negative"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the clinical stage",
        example="No criteria present - PE ruled out"
    )
    
    positive_criteria_count: int = Field(
        ...,
        ge=0,
        le=7,
        description="Number of positive PERC criteria present (0-7)",
        example=0
    )
    
    perc_satisfied: bool = Field(
        ...,
        description="Whether PERC rule criteria are satisfied (true if 0 positive criteria)",
        example=True
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": "PERC Negative",
                "unit": "recommendation",
                "interpretation": "PERC rule criteria satisfied. No need for further workup, as <2% chance of PE. Patient can be safely discharged without additional testing for PE if clinician's pretest probability is <15%.",
                "stage": "PERC Negative",
                "stage_description": "No criteria present - PE ruled out",
                "positive_criteria_count": 0,
                "perc_satisfied": True
            }
        }