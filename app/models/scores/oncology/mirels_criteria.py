"""
Mirels' Criteria for Prophylactic Fixation Models

Request and response models for Mirels' Criteria assessment.

References (Vancouver style):
1. Mirels H. Metastatic disease in long bones. A proposed scoring system for 
   diagnosing impending pathologic fractures. Clin Orthop Relat Res. 1989 Dec;
   (249):256-64.
2. Van der Linden YM, Dijkstra PD, Kroon HM, Lok JJ, Noordijk EM, Leer JW, et al. 
   Comparative analysis of risk factors for pathological fracture with femoral 
   metastases. J Bone Joint Surg Br. 2004 May;86(4):566-73.
3. Nazarian A, Entezari V, Villa-Camacho JC, Zurakowski D, Snyder BD. Treatment 
   planning and fracture prediction in patients with skeletal metastasis with 
   CT-based rigidity analysis. Clin Cancer Res. 2014 May 1;20(9):2465-73. 
   doi: 10.1158/1078-0432.CCR-13-2966.
4. Evans AR, Bottros J, Grant W, Chen BY, Damron TA. Mirels' rating for humerus 
   lesions is both reproducible and valid. Clin Orthop Relat Res. 2008 Jun;
   466(6):1279-84. doi: 10.1007/s11999-008-0200-0.

Mirels' Criteria for Prophylactic Fixation is a validated scoring system that 
predicts the risk of pathologic fracture in patients with long bone metastases. 
The score ranges from 4-12 points and helps clinicians decide whether prophylactic 
fixation should be performed prior to radiation therapy. Scores ≥9 indicate high 
fracture risk (>33%) and warrant prophylactic fixation, while scores ≤7 indicate 
low risk (0-4%) and can be safely managed with radiation alone.
"""

from pydantic import BaseModel, Field
from typing import Literal


class MirelsCriteriaRequest(BaseModel):
    """
    Request model for Mirels' Criteria for Prophylactic Fixation
    
    The Mirels' Criteria evaluates four parameters to predict pathologic fracture 
    risk in patients with long bone metastases:
    
    Site of Lesion (1-3 points):
    - upper_limb: Upper extremity (humerus, radius, ulna) - 1 point
    - lower_limb: Lower extremity (femur shaft, tibia, fibula) - 2 points  
    - trochanteric_region: Subtrochanteric/intertrochanteric femur - 3 points
    
    Size of Lesion (1-3 points) - measured on plain radiographs:
    - less_than_one_third: <1/3 of bone diameter - 1 point
    - one_third_to_two_thirds: 1/3 to 2/3 of bone diameter - 2 points
    - more_than_two_thirds: >2/3 of bone diameter - 3 points
    
    Nature of Lesion (1-3 points) - radiographic appearance:
    - blastic: Sclerotic/blastic appearance - 1 point
    - mixed: Mixed lytic and blastic components - 2 points
    - lytic: Purely lytic/destructive appearance - 3 points
    
    Pain Level (1-3 points):
    - mild: Mild pain not affecting function - 1 point
    - moderate: Moderate pain with some functional limitation - 2 points
    - functional: Functional pain preventing weight-bearing/use - 3 points

    References (Vancouver style):
    1. Mirels H. Metastatic disease in long bones. A proposed scoring system for 
       diagnosing impending pathologic fractures. Clin Orthop Relat Res. 1989 Dec;
       (249):256-64.
    2. Van der Linden YM, Dijkstra PD, Kroon HM, Lok JJ, Noordijk EM, Leer JW, et al. 
       Comparative analysis of risk factors for pathological fracture with femoral 
       metastases. J Bone Joint Surg Br. 2004 May;86(4):566-73.
    3. Nazarian A, Entezari V, Villa-Camacho JC, Zurakowski D, Snyder BD. Treatment 
       planning and fracture prediction in patients with skeletal metastasis with 
       CT-based rigidity analysis. Clin Cancer Res. 2014 May 1;20(9):2465-73. 
       doi: 10.1158/1078-0432.CCR-13-2966.
    4. Evans AR, Bottros J, Grant W, Chen BY, Damron TA. Mirels' rating for humerus 
       lesions is both reproducible and valid. Clin Orthop Relat Res. 2008 Jun;
       466(6):1279-84. doi: 10.1007/s11999-008-0200-0.
    """
    
    site_of_lesion: Literal["upper_limb", "lower_limb", "trochanteric_region"] = Field(
        ...,
        description="Location of the metastatic lesion. Upper limb (1 pt), lower limb (2 pts), trochanteric region (3 pts)",
        example="lower_limb"
    )
    
    size_of_lesion: Literal["less_than_one_third", "one_third_to_two_thirds", "more_than_two_thirds"] = Field(
        ...,
        description="Size of lesion relative to bone diameter on radiographs. <1/3 (1 pt), 1/3-2/3 (2 pts), >2/3 (3 pts)",
        example="one_third_to_two_thirds"
    )
    
    nature_of_lesion: Literal["blastic", "mixed", "lytic"] = Field(
        ...,
        description="Radiographic appearance of the metastatic lesion. Blastic (1 pt), mixed (2 pts), lytic (3 pts)",
        example="lytic"
    )
    
    pain: Literal["mild", "moderate", "functional"] = Field(
        ...,
        description="Level of pain related to the lesion. Mild (1 pt), moderate (2 pts), functional pain preventing weight-bearing (3 pts)",
        example="moderate"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "site_of_lesion": "lower_limb",
                "size_of_lesion": "one_third_to_two_thirds",
                "nature_of_lesion": "lytic",
                "pain": "moderate"
            }
        }


class MirelsCriteriaResponse(BaseModel):
    """
    Response model for Mirels' Criteria for Prophylactic Fixation
    
    The Mirels score ranges from 4-12 points and stratifies fracture risk:
    
    Low Risk (≤7 points):
    - 0-4% fracture risk at 6 months
    - Safe for radiation therapy alone
    - Prophylactic fixation not indicated
    
    Intermediate Risk (8 points):
    - 15% fracture risk at 6 months
    - Consider prophylactic fixation based on clinical judgment
    - Evaluate patient-specific factors
    
    High Risk (≥9 points):
    - >33% fracture risk at 6 months
    - Prophylactic fixation indicated prior to radiation
    - High risk warrants surgical intervention
    
    Special considerations:
    - Upper limb lesions may benefit from lower threshold (≥7 points)
    - Consider patient life expectancy, functional status, and surgical risk
    - Serial assessment may be needed for non-surgical management
    
    Reference: Mirels H. Clin Orthop Relat Res. 1989;(249):256-64.
    """
    
    result: int = Field(
        ...,
        ge=4,
        le=12,
        description="Total Mirels score predicting pathologic fracture risk (4-12 points)",
        example=9
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with fracture risk and management recommendations",
        example="Prophylactic fixation indicated prior to irradiation. High risk of pathologic fracture warrants surgical intervention to prevent fracture and maintain function."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, Intermediate Risk, High Risk)",
        example="High Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of fracture risk percentage at 6 months",
        example=">33% fracture risk at 6 months"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 9,
                "unit": "points",
                "interpretation": "Prophylactic fixation indicated prior to irradiation. High risk of pathologic fracture warrants surgical intervention to prevent fracture and maintain function.",
                "stage": "High Risk",
                "stage_description": ">33% fracture risk at 6 months"
            }
        }