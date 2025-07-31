"""
Ottawa Ankle Rule Models

Request and response models for Ottawa Ankle Rule calculation.

References (Vancouver style):
1. Stiell IG, Greenberg GH, McKnight RD, Nair RC, McDowell I, Worthington JR. A study to 
   develop clinical decision rules for the use of radiography in acute ankle injuries. 
   Ann Emerg Med. 1992 Apr;21(4):384-90. doi: 10.1016/s0196-0644(05)82656-3. 
   PMID: 1554175.
2. Stiell IG, McKnight RD, Greenberg GH, McDowell I, Nair RC, Wells GA, et al. 
   Implementation of the Ottawa ankle rules. JAMA. 1994 Mar 16;271(11):827-32. 
   PMID: 8114236.
3. Bachmann LM, Kolb E, Koller MT, Steurer J, ter Riet G. Accuracy of Ottawa ankle rules 
   to exclude fractures of the ankle and mid-foot: systematic review. BMJ. 2003 Feb 
   22;326(7386):417. doi: 10.1136/bmj.326.7386.417. PMID: 12595378; PMCID: PMC149439.
4. Dowling S, Spooner CH, Liang Y, Dryden DM, Friesen C, Klassen TP, et al. Accuracy of 
   Ottawa Ankle Rules to exclude fractures of the ankle and midfoot in children: a 
   meta-analysis. Acad Emerg Med. 2009 Apr;16(4):277-87. doi: 10.1111/j.1553-2712.2008.00333.x. 
   PMID: 19187397.

The Ottawa Ankle Rule is a validated clinical decision tool with 98-100% sensitivity for 
detecting clinically significant ankle and foot fractures. It can reduce unnecessary 
radiographs by 30-40% when properly applied.
"""

from pydantic import BaseModel, Field
from typing import Literal


class OttawaAnkleRuleRequest(BaseModel):
    """
    Request model for Ottawa Ankle Rule
    
    The Ottawa Ankle Rule consists of two separate decision tools:
    
    Ankle X-ray Rule:
    - Required if malleolar zone pain AND any of:
      * Bone tenderness at posterior edge/tip of lateral malleolus (distal 6 cm)
      * Bone tenderness at posterior edge/tip of medial malleolus (distal 6 cm)
      * Unable to bear weight immediately and in ED (4 steps)
    
    Foot X-ray Rule:
    - Required if midfoot zone pain AND any of:
      * Bone tenderness at base of 5th metatarsal
      * Bone tenderness at navicular bone
      * Unable to bear weight immediately and in ED (4 steps)

    References (Vancouver style):
    1. Stiell IG, Greenberg GH, McKnight RD, Nair RC, McDowell I, Worthington JR. A study to 
    develop clinical decision rules for the use of radiography in acute ankle injuries. 
    Ann Emerg Med. 1992 Apr;21(4):384-90.
    2. Stiell IG, McKnight RD, Greenberg GH, McDowell I, Nair RC, Wells GA, et al. 
    Implementation of the Ottawa ankle rules. JAMA. 1994 Mar 16;271(11):827-32.
    """
    
    malleolar_zone_pain: Literal["yes", "no"] = Field(
        ...,
        description="Is there pain in the malleolar zone (area around the ankle)? This is required for the ankle x-ray criteria",
        example="yes"
    )
    
    lateral_malleolus_tenderness: Literal["yes", "no"] = Field(
        ...,
        description="Is there bone tenderness at the posterior edge or tip of the lateral malleolus (distal 6 cm)? Palpate the entire distal 6 cm",
        example="no"
    )
    
    medial_malleolus_tenderness: Literal["yes", "no"] = Field(
        ...,
        description="Is there bone tenderness at the posterior edge or tip of the medial malleolus (distal 6 cm)? Palpate the entire distal 6 cm",
        example="yes"
    )
    
    midfoot_zone_pain: Literal["yes", "no"] = Field(
        ...,
        description="Is there pain in the midfoot zone? This is required for the foot x-ray criteria",
        example="no"
    )
    
    fifth_metatarsal_tenderness: Literal["yes", "no"] = Field(
        ...,
        description="Is there bone tenderness at the base of the 5th metatarsal? This is a specific point tenderness",
        example="no"
    )
    
    navicular_tenderness: Literal["yes", "no"] = Field(
        ...,
        description="Is there bone tenderness at the navicular bone? This is a specific point tenderness",
        example="no"
    )
    
    unable_to_bear_weight: Literal["yes", "no"] = Field(
        ...,
        description="Is the patient unable to bear weight both immediately after injury AND in the emergency department? Unable means cannot take 4 steps (limping is considered able to bear weight)",
        example="no"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "malleolar_zone_pain": "yes",
                "lateral_malleolus_tenderness": "no",
                "medial_malleolus_tenderness": "yes",
                "midfoot_zone_pain": "no",
                "fifth_metatarsal_tenderness": "no",
                "navicular_tenderness": "no",
                "unable_to_bear_weight": "no"
            }
        }


class OttawaAnkleRuleResponse(BaseModel):
    """
    Response model for Ottawa Ankle Rule
    
    The Ottawa Ankle Rule provides x-ray recommendations with:
    - 98-100% sensitivity for clinically significant fractures
    - Low specificity (41% ankle, 79% foot)
    - Can reduce unnecessary radiographs by 30-40%
    
    Reference: Stiell IG, et al. Ann Emerg Med. 1992;21(4):384-90.
    """
    
    result: str = Field(
        ...,
        description="X-ray recommendation: no_xray_needed, ankle_xray_only, foot_xray_only, or both_xrays",
        example="ankle_xray_only"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the result",
        example="recommendation"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and detailed recommendation based on the Ottawa Ankle Rule criteria",
        example="Based on the Ottawa Ankle Rule, an ankle x-ray series is indicated due to malleolar zone pain with either malleolar tenderness or inability to bear weight. This combination suggests possible ankle fracture requiring radiographic evaluation."
    )
    
    stage: str = Field(
        ...,
        description="Summary of imaging recommendation",
        example="Ankle x-ray indicated"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the required imaging",
        example="Ankle x-ray series required"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": "ankle_xray_only",
                "unit": "recommendation",
                "interpretation": "Based on the Ottawa Ankle Rule, an ankle x-ray series is indicated due to malleolar zone pain with either malleolar tenderness or inability to bear weight. This combination suggests possible ankle fracture requiring radiographic evaluation.",
                "stage": "Ankle x-ray indicated",
                "stage_description": "Ankle x-ray series required"
            }
        }