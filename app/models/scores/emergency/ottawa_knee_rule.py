"""
Ottawa Knee Rule Models

Request and response models for Ottawa Knee Rule calculation.

References (Vancouver style):
1. Stiell IG, Greenberg GH, Wells GA, McDowell I, Cwinn AA, Smith NA, et al. 
   Prospective validation of a decision rule for the use of radiography in 
   acute knee injuries. JAMA. 1996 Feb 28;275(8):611-5. PMID: 8594242.
2. Stiell IG, Wells GA, Hoag RH, Sivilotti ML, Cacciotti TF, Verbeek PR, et al. 
   Implementation of the Ottawa Knee Rule for the use of radiography in 
   acute knee injuries. JAMA. 1997 Dec 17;278(23):2075-9. doi: 10.1001/jama.278.23.2075.
3. Bachmann LM, Haberzeth S, Steurer J, ter Riet G. The accuracy of the Ottawa 
   knee rule to rule out knee fractures: a systematic review. Ann Intern Med. 
   2004 Jan 6;140(1):121-4. doi: 10.7326/0003-4819-140-1-200401060-00013.
4. Seaberg DC, Yealy DM, Lukens T, Auble T, Mathias S. Multicenter comparison of 
   two clinical decision rules for the use of radiography in acute, high-risk 
   knee injuries. Ann Emerg Med. 1998 Jan;31(1):22-8. doi: 10.1016/s0196-0644(98)70277-9.

The Ottawa Knee Rule is a clinical decision tool used to determine when knee 
radiography is required in patients with acute knee trauma. It has high sensitivity 
(98-100%) for clinically significant fractures and can reduce unnecessary x-rays 
by 20-30%. The rule applies to patients aged 2 and older with acute knee trauma 
less than 7 days old.
"""

from pydantic import BaseModel, Field
from typing import Literal


class OttawaKneeRuleRequest(BaseModel):
    """
    Request model for Ottawa Knee Rule
    
    The Ottawa Knee Rule uses 5 clinical criteria to determine need for knee x-ray:
    
    1. Age ≥55 years: Increased fracture risk with age
    2. Isolated patellar tenderness: Tenderness only at patella (no other bone tenderness)
    3. Fibular head tenderness: Tenderness at the head of the fibula
    4. Unable to flex to 90°: Inability to flex knee to 90 degrees
    5. Unable to bear weight: Unable to take 4 steps both immediately after injury 
       and in the emergency department (limping is acceptable)
    
    X-ray is indicated if ANY criterion is positive. If all criteria are negative,
    x-ray is not needed (98-100% sensitivity for clinically significant fractures).
    
    Exclusions: The rule should not be applied if examination is unreliable due to:
    - Intoxication or uncooperative patient
    - Distracting injuries  
    - Diminished leg sensation
    - Age <2 years
    - Injuries >7 days old
    
    References (Vancouver style):
    1. Stiell IG, Greenberg GH, Wells GA, McDowell I, Cwinn AA, Smith NA, et al. 
       Prospective validation of a decision rule for the use of radiography in 
       acute knee injuries. JAMA. 1996 Feb 28;275(8):611-5. PMID: 8594242.
    2. Stiell IG, Wells GA, Hoag RH, Sivilotti ML, Cacciotti TF, Verbeek PR, et al. 
       Implementation of the Ottawa Knee Rule for the use of radiography in 
       acute knee injuries. JAMA. 1997 Dec 17;278(23):2075-9. doi: 10.1001/jama.278.23.2075.
    """
    
    age_55_or_older: Literal["yes", "no"] = Field(
        ...,
        description="Is the patient age 55 years or older? Older age increases fracture risk",
        example="no"
    )
    
    isolated_patellar_tenderness: Literal["yes", "no"] = Field(
        ...,
        description="Is there isolated tenderness of the patella (kneecap) with no other bone tenderness? This means tenderness only at the patella, not at other knee structures",
        example="no"
    )
    
    fibular_head_tenderness: Literal["yes", "no"] = Field(
        ...,
        description="Is there tenderness at the fibular head? The fibular head is the bony prominence on the outer side of the knee just below the knee joint",
        example="no"
    )
    
    unable_to_flex_90_degrees: Literal["yes", "no"] = Field(
        ...,
        description="Is the patient unable to flex the knee to 90 degrees? This assesses range of motion limitation due to pain or mechanical obstruction",
        example="no"
    )
    
    unable_to_bear_weight: Literal["yes", "no"] = Field(
        ...,
        description="Is the patient unable to bear weight both immediately after injury and in the emergency department? Unable to bear weight means unable to take 4 steps (limping is acceptable)",
        example="yes"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "age_55_or_older": "no",
                "isolated_patellar_tenderness": "no", 
                "fibular_head_tenderness": "no",
                "unable_to_flex_90_degrees": "no",
                "unable_to_bear_weight": "yes"
            }
        }


class OttawaKneeRuleResponse(BaseModel):
    """
    Response model for Ottawa Knee Rule
    
    The Ottawa Knee Rule determines need for knee x-ray based on 5 clinical criteria.
    If ANY criterion is positive, x-ray is indicated. If all criteria are negative,
    x-ray is not needed with 98-100% sensitivity for clinically significant fractures.
    
    Results:
    - no_xray_needed: All criteria negative, x-ray not required
    - xray_indicated: One or more criteria positive, knee x-ray series required
    
    The rule can safely reduce unnecessary x-rays by 20-30% while maintaining
    high sensitivity for detecting fractures requiring treatment.
    
    Reference: Stiell IG, et al. JAMA. 1996;275(8):611-5.
    """
    
    result: str = Field(
        ...,
        description="Ottawa Knee Rule result determining need for x-ray (no_xray_needed or xray_indicated)",
        example="xray_indicated"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the result",
        example="recommendation"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended next steps based on the rule",
        example="Based on the Ottawa Knee Rule, a knee x-ray series is indicated. The presence of one or more clinical criteria suggests possible knee fracture requiring radiographic evaluation. The rule has high sensitivity for detecting clinically significant fractures."
    )
    
    stage: str = Field(
        ...,
        description="Clinical recommendation category (No imaging required, X-ray indicated)",
        example="X-ray indicated"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the recommendation",
        example="Knee x-ray series required"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": "xray_indicated",
                "unit": "recommendation",
                "interpretation": "Based on the Ottawa Knee Rule, a knee x-ray series is indicated. The presence of one or more clinical criteria suggests possible knee fracture requiring radiographic evaluation. The rule has high sensitivity for detecting clinically significant fractures.",
                "stage": "X-ray indicated",
                "stage_description": "Knee x-ray series required"
            }
        }