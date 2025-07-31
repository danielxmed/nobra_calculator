"""
National Early Warning Score (NEWS) 2 Models

Request and response models for NEWS 2 calculation.

References (Vancouver style):
1. Royal College of Physicians. National Early Warning Score (NEWS) 2: Standardising 
   the assessment of acute-illness severity in the NHS. Updated report of a working 
   party. London: RCP, 2017.
2. Pimentel MAF, Redfern OC, Gerry S, Collins GS, Malycha J, Prytherch D, et al. 
   A comparison of the ability of the National Early Warning Score and the National 
   Early Warning Score 2 to identify patients at risk of in-hospital mortality: 
   A multi-centre database study. Resuscitation. 2019 Jan;134:147-156. 
   doi: 10.1016/j.resuscitation.2018.09.026.
3. Smith GB, Redfern OC, Pimentel MA, Gerry S, Collins GS, Malycha J, et al. 
   The National Early Warning Score 2 (NEWS2). Clin Med (Lond). 2019 May;19(3):260. 
   doi: 10.7861/clinmedicine.19-3-260.

NEWS 2 is an updated version of the original NEWS that provides improved oxygen 
saturation scoring for patients with hypercapnic respiratory failure (Type 2 
respiratory failure), allowing for lower target oxygen saturations (88-92%) in 
these patients. It also explicitly includes new-onset confusion in the consciousness 
assessment.
"""

from pydantic import BaseModel, Field
from typing import Literal


class News2Request(BaseModel):
    """
    Request model for National Early Warning Score (NEWS) 2
    
    NEWS 2 uses 7 physiological parameters plus hypercapnic respiratory failure status:
    
    Respiratory Rate (breaths per minute):
    - ≤8: +3 points (dangerously low)
    - 9-11: +1 point (low)
    - 12-20: 0 points (normal)
    - 21-24: +2 points (elevated)
    - ≥25: +3 points (dangerously high)
    
    Hypercapnic Respiratory Failure:
    - Affects oxygen saturation scoring targets
    - Type 2 respiratory failure with CO2 retention
    - Common in COPD, obesity hypoventilation syndrome
    
    Oxygen Saturation - Standard (non-hypercapnic):
    - ≤91%: +3 points (severe hypoxemia)
    - 92-93%: +2 points (moderate hypoxemia)
    - 94-95%: +1 point (mild hypoxemia)
    - ≥96%: 0 points (normal)
    
    Oxygen Saturation - Hypercapnic respiratory failure:
    - ≤83%: +3 points
    - 84-85%: +2 points
    - 86-87%: +1 point
    - 88-92%: 0 points (target range)
    - ≥93% on room air: 0 points
    - 93-94% on supplemental O2: +1 point
    - 95-96% on supplemental O2: +2 points
    - ≥97% on supplemental O2: +3 points
    
    Supplemental Oxygen:
    - No: 0 points
    - Yes: +2 points (indicates respiratory compromise)
    
    Temperature (°C):
    - ≤35.0: +3 points (severe hypothermia)
    - 35.1-36.0: +1 point (mild hypothermia)
    - 36.1-38.0: 0 points (normal)
    - 38.1-39.0: +1 point (mild fever)
    - ≥39.1: +2 points (high fever)
    
    Systolic Blood Pressure (mmHg):
    - ≤90: +3 points (severe hypotension)
    - 91-100: +2 points (moderate hypotension)
    - 101-110: +1 point (mild hypotension)
    - 111-219: 0 points (normal)
    - ≥220: +3 points (severe hypertension)
    
    Heart Rate (beats per minute):
    - ≤40: +3 points (severe bradycardia)
    - 41-50: +1 point (bradycardia)
    - 51-90: 0 points (normal)
    - 91-110: +1 point (mild tachycardia)
    - 111-130: +2 points (moderate tachycardia)
    - ≥131: +3 points (severe tachycardia)
    
    Consciousness:
    - Alert: 0 points (normal consciousness)
    - Altered: +3 points (includes new-onset confusion, disorientation, 
      agitation, responds to voice/pain, or unresponsive)

    References (Vancouver style):
    1. Royal College of Physicians. National Early Warning Score (NEWS) 2: Standardising 
    the assessment of acute-illness severity in the NHS. Updated report of a working 
    party. London: RCP, 2017.
    """
    
    respiratory_rate: Literal["8_or_less", "9_to_11", "12_to_20", "21_to_24", "25_or_more"] = Field(
        ...,
        description="Respiratory rate in breaths per minute. ≤8 scores +3, 9-11 scores +1, 12-20 scores 0, 21-24 scores +2, ≥25 scores +3",
        example="12_to_20"
    )
    
    hypercapnic_respiratory_failure: Literal["yes", "no"] = Field(
        ...,
        description="Whether patient has hypercapnic respiratory failure (Type 2 respiratory failure with CO2 retention, e.g., COPD exacerbation). Affects oxygen saturation scoring",
        example="no"
    )
    
    oxygen_saturation: Literal[
        "83_or_less", "84_to_85", "86_to_87", "88_to_92", 
        "91_or_less", "92_to_93", "93_to_94", "94_to_95", 
        "95_to_96", "96_or_more", "97_or_more"
    ] = Field(
        ...,
        description="Oxygen saturation percentage (SpO2). Scoring differs based on hypercapnic respiratory failure status",
        example="96_or_more"
    )
    
    supplemental_oxygen: Literal["yes", "no"] = Field(
        ...,
        description="Whether patient is receiving any supplemental oxygen. Yes scores +2, No scores 0",
        example="no"
    )
    
    temperature: Literal["35_or_less", "35_1_to_36", "36_1_to_38", "38_1_to_39", "39_1_or_more"] = Field(
        ...,
        description="Body temperature in °C. ≤35.0 scores +3, 35.1-36.0 scores +1, 36.1-38.0 scores 0, 38.1-39.0 scores +1, ≥39.1 scores +2",
        example="36_1_to_38"
    )
    
    systolic_bp: Literal["90_or_less", "91_to_100", "101_to_110", "111_to_219", "220_or_more"] = Field(
        ...,
        description="Systolic blood pressure in mmHg. ≤90 scores +3, 91-100 scores +2, 101-110 scores +1, 111-219 scores 0, ≥220 scores +3",
        example="111_to_219"
    )
    
    heart_rate: Literal["40_or_less", "41_to_50", "51_to_90", "91_to_110", "111_to_130", "131_or_more"] = Field(
        ...,
        description="Heart rate in beats per minute. ≤40 scores +3, 41-50 scores +1, 51-90 scores 0, 91-110 scores +1, 111-130 scores +2, ≥131 scores +3",
        example="51_to_90"
    )
    
    consciousness: Literal["alert", "altered"] = Field(
        ...,
        description="Level of consciousness. Alert scores 0, Altered (new-onset confusion, disorientation, agitation, responds to voice/pain, unresponsive) scores +3",
        example="alert"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "respiratory_rate": "12_to_20",
                "hypercapnic_respiratory_failure": "no",
                "oxygen_saturation": "96_or_more",
                "supplemental_oxygen": "no",
                "temperature": "36_1_to_38",
                "systolic_bp": "111_to_219",
                "heart_rate": "51_to_90",
                "consciousness": "alert"
            }
        }


class News2Response(BaseModel):
    """
    Response model for National Early Warning Score (NEWS) 2
    
    The NEWS 2 score ranges from 0 to 20 points and classifies patients into risk categories:
    - 0: Very low risk - Continue routine monitoring
    - 1-4: Low risk - Nurse assessment for monitoring frequency changes
    - Score of 3 in any parameter: Low-Medium risk - Urgent doctor review required
    - 5-6: Medium risk - Urgent clinical review required
    - ≥7: High risk - Emergency assessment and critical care involvement
    
    Key improvements in NEWS 2:
    - Adjusted oxygen saturation targets for hypercapnic respiratory failure
    - Explicit inclusion of new-onset confusion in consciousness assessment
    - Maintained RED score concept for any parameter scoring 3 points
    
    Reference: Royal College of Physicians. National Early Warning Score (NEWS) 2. 2017.
    """
    
    result: int = Field(
        ...,
        description="NEWS 2 score calculated from physiological parameters (range: 0-20 points)",
        example=0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended response based on the score",
        example="Continue routine monitoring. Minimum monitoring frequency every 12 hours."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, Low-Medium Risk, Medium Risk, High Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Description of the early warning score level",
        example="Very low early warning score"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 0,
                "unit": "points",
                "interpretation": "Continue routine monitoring. Minimum monitoring frequency every 12 hours.",
                "stage": "Low Risk",
                "stage_description": "Very low early warning score"
            }
        }