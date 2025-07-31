"""
FRACTURE Index Models

Request and response models for FRACTURE Index calculation.

References (Vancouver style):
1. Black DM, Steinbuch M, Palermo L, et al. An assessment tool for predicting fracture 
   risk in postmenopausal women. Osteoporos Int. 2001;12(7):519-28. 
   doi: 10.1007/s001980170072.
2. Black DM, Palermo L, Nevitt MC, et al. Defining incident vertebral deformity: a 
   prospective comparison of several approaches. The Study of Osteoporotic Fractures 
   Research Group. J Bone Miner Res. 1999;14(1):90-101. doi: 10.1359/jbmr.1999.14.1.90.
3. Cummings SR, Nevitt MC, Browner WS, et al. Risk factors for hip fracture in white 
   women. Study of Osteoporotic Fractures Research Group. N Engl J Med. 1995;332(12):767-73. 
   doi: 10.1056/NEJM199503233321202.
4. Ensrud KE, Lipschutz RC, Cauley JA, et al. Body size and hip fracture risk in older 
   women: a prospective study. Study of Osteoporotic Fractures Research Group. Am J Med. 
   1997;103(4):274-80. doi: 10.1016/s0002-9343(97)00142-2.

The FRACTURE Index is a simple, practical assessment tool developed to predict 5-year 
hip fracture risk in postmenopausal women. It was derived from the Study of Osteoporotic 
Fractures, a large prospective cohort study of older women. The tool can be used with 
or without bone mineral density measurements, making it accessible in various clinical 
settings.

Key Features:
- Predicts 5-year hip fracture risk specifically
- Designed for postmenopausal women aged 65 and older
- Can function with or without BMD measurements
- Simple scoring system using readily available clinical information
- Validated in large prospective cohort studies

Clinical Applications:
- Outpatient fracture risk screening
- Identifying patients who may benefit from further evaluation
- Supporting clinical decision-making for osteoporosis prevention
- Triaging patients for bone density testing

Limitations:
- Developed primarily for White postmenopausal women
- Not validated for men or those with secondary osteoporosis causes
- Should be used as part of comprehensive clinical assessment
"""

from pydantic import BaseModel, Field
from typing import Literal, Optional


class FractureIndexRequest(BaseModel):
    """
    Request model for FRACTURE Index calculation
    
    The FRACTURE Index predicts 5-year hip fracture risk in postmenopausal women 
    using seven clinical risk factors. It provides a simple, practical assessment 
    tool that can be used with or without bone mineral density measurements.
    
    **Scoring Components**:
    
    **Age (0-5 points)**:
    - <65 years: 0 points
    - 65-69 years: 1 point
    - 70-74 years: 2 points  
    - 75-79 years: 3 points
    - 80-84 years: 4 points
    - ≥85 years: 5 points
    
    **Clinical Risk Factors (0-1 point each)**:
    - **Fracture after age 50**: Any fracture occurring after menopause (1 point if yes)
    - **Mother's hip fracture**: Maternal history of hip fracture (1 point if yes)
    - **Low body weight**: Weight <57.7 kg (127 lbs) (1 point if yes)
    - **Current smoking**: Active tobacco use (1 point if yes)
    
    **Functional Assessment (0-2 points)**:
    - **Arms to stand from chair**: Inability to rise from chair without using arms (2 points if yes)
    
    **Bone Density (Optional, 0-4 points)**:
    - **BMD T-score ≥-1.0**: 0 points (normal/osteopenia)
    - **BMD T-score -1.1 to -2.0**: 1 point (mild osteopenia)
    - **BMD T-score -2.1 to -2.5**: 2 points (severe osteopenia)
    - **BMD T-score -2.6 to -3.0**: 3 points (mild osteoporosis)
    - **BMD T-score <-3.0**: 4 points (severe osteoporosis)
    
    **Interpretation Thresholds**:
    - **Without BMD**: Score ≥4 suggests further evaluation needed
    - **With BMD**: Score ≥6 suggests further evaluation needed
    - **Risk Range**: 5-year hip fracture risk from <0.6% to 8.7%
    
    **Clinical Applications**:
    - Primary care fracture risk screening
    - Identifying candidates for osteoporosis evaluation
    - Supporting decisions about bone density testing
    - Guiding preventive interventions
    
    References (Vancouver style):
    1. Black DM, Steinbuch M, Palermo L, et al. An assessment tool for predicting fracture 
       risk in postmenopausal women. Osteoporos Int. 2001;12(7):519-28.
    2. Cummings SR, Nevitt MC, Browner WS, et al. Risk factors for hip fracture in white 
       women. Study of Osteoporotic Fractures Research Group. N Engl J Med. 1995;332(12):767-73.
    """
    
    age: int = Field(
        ...,
        description=(
            "Patient age in years. Scoring: <65 years (0 points), 65-69 years (1 point), "
            "70-74 years (2 points), 75-79 years (3 points), 80-84 years (4 points), "
            "≥85 years (5 points). Age is the strongest predictor in the model."
        ),
        ge=50,
        le=100,
        example=72
    )
    
    fracture_after_50: Literal["yes", "no"] = Field(
        ...,
        description=(
            "History of any fracture after age 50 years. This includes any low-trauma fracture "
            "occurring after menopause, excluding skull, facial, ankle, finger, and toe fractures. "
            "Previous fracture is a strong predictor of future fracture risk. Scores 1 point if yes."
        ),
        example="no"
    )
    
    mother_hip_fracture: Literal["yes", "no"] = Field(
        ...,
        description=(
            "Mother's history of hip fracture at any age. Family history, particularly maternal "
            "hip fracture, indicates genetic predisposition to osteoporosis and fracture risk. "
            "This reflects both genetic and environmental factors. Scores 1 point if yes."
        ),
        example="yes"
    )
    
    weight: float = Field(
        ...,
        description=(
            "Patient weight in kilograms. Low body weight (<57.7 kg or 127 lbs) is associated "
            "with increased fracture risk due to lower bone mass, reduced muscle mass, and "
            "increased fall risk. Scores 1 point if weight is below 57.7 kg."
        ),
        ge=30,
        le=200,
        example=55.0
    )
    
    current_smoker: Literal["yes", "no"] = Field(
        ...,
        description=(
            "Current smoking status (active tobacco use). Smoking increases fracture risk through "
            "multiple mechanisms including decreased bone density, impaired bone healing, increased "
            "fall risk, and earlier menopause. Scores 1 point if yes."
        ),
        example="no"
    )
    
    arms_to_stand: Literal["yes", "no"] = Field(
        ...,
        description=(
            "Inability to rise from a chair without using arms for support. This functional assessment "
            "reflects muscle weakness, balance problems, and overall frailty - all associated with "
            "increased fall and fracture risk. Scores 2 points if yes (highest single risk factor)."
        ),
        example="no"
    )
    
    bmd_t_score: Optional[float] = Field(
        None,
        description=(
            "Bone Mineral Density T-score (optional) from femoral neck or total hip DXA scan. "
            "T-score compares patient's BMD to healthy 30-year-old reference population. "
            "Scoring: ≥-1.0 (0 points), -1.1 to -2.0 (1 point), -2.1 to -2.5 (2 points), "
            "-2.6 to -3.0 (3 points), <-3.0 (4 points). If provided, changes interpretation threshold to ≥6."
        ),
        ge=-5.0,
        le=3.0,
        example=-2.3
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": 72,
                "fracture_after_50": "no",
                "mother_hip_fracture": "yes",
                "weight": 55.0,
                "current_smoker": "no",
                "arms_to_stand": "no",
                "bmd_t_score": -2.3
            }
        }


class FractureIndexResponse(BaseModel):
    """
    Response model for FRACTURE Index calculation
    
    The FRACTURE Index provides a practical assessment of 5-year hip fracture risk 
    in postmenopausal women, helping clinicians identify patients who may benefit 
    from further evaluation and preventive interventions.
    
    **Score Interpretation**:
    
    **Low Risk (Score <4 without BMD or <6 with BMD)**:
    - 5-year hip fracture risk: <0.6% to 2.9%
    - Management: Continue routine care with lifestyle interventions
    - Interventions: Adequate calcium and vitamin D, weight-bearing exercise, fall prevention
    - Follow-up: Routine osteoporosis screening per guidelines
    
    **Elevated Risk (Score ≥4 without BMD or ≥6 with BMD)**:
    - 5-year hip fracture risk: 3.0% to 8.7%
    - Management: Further evaluation warranted
    - Considerations: Bone density testing (if not done), FRAX assessment, treatment evaluation
    - Interventions: Comprehensive fall prevention, consider pharmacologic therapy per guidelines
    
    **Clinical Decision Making**:
    - Use in conjunction with clinical judgment and current osteoporosis guidelines
    - Consider FRAX calculator for more comprehensive 10-year fracture risk assessment
    - Evaluate for secondary causes of osteoporosis in high-risk patients
    - Assess for contraindications to osteoporosis medications
    
    **Limitations**:
    - Developed primarily for White postmenopausal women aged 65+
    - Not validated for men or secondary osteoporosis causes
    - Predicts hip fracture specifically, not other fracture types
    - Should be part of comprehensive osteoporosis risk assessment
    
    **Quality Measures**:
    - Sensitivity: 91% for identifying women with 5-year hip fracture risk ≥3%
    - Specificity: 35% for identifying women with low fracture risk
    - Simple, practical tool with good clinical utility
    - Can be calculated quickly in clinical settings
    
    Reference: Black DM, et al. Osteoporos Int. 2001;12(7):519-28.
    """
    
    result: int = Field(
        ...,
        description="Total FRACTURE Index score (range: 0-15 points)",
        ge=0,
        le=15,
        example=6
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description=(
            "Clinical interpretation including risk level, 5-year fracture risk range, "
            "and recommended management approach based on current guidelines"
        ),
        example=(
            "FRACTURE Index score: 6/15. Score ≥6 (with BMD) suggests further evaluation is warranted. "
            "5-year hip fracture risk ranges from 3.0% to 8.7%. Consider bone density testing, "
            "FRAX assessment, and evaluation for osteoporosis treatment based on clinical judgment "
            "and current guidelines. Implement comprehensive fall prevention and bone health strategies."
        )
    )
    
    stage: str = Field(
        ...,
        description="Risk category based on the total score (Low Risk, Elevated Risk)",
        example="Elevated Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Elevated 5-year hip fracture risk requiring evaluation"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 6,
                "unit": "points",
                "interpretation": (
                    "FRACTURE Index score: 6/15. Score ≥6 (with BMD) suggests further evaluation is warranted. "
                    "5-year hip fracture risk ranges from 3.0% to 8.7%. Consider bone density testing, "
                    "FRAX assessment, and evaluation for osteoporosis treatment based on clinical judgment "
                    "and current guidelines. Implement comprehensive fall prevention and bone health strategies."
                ),
                "stage": "Elevated Risk",
                "stage_description": "Elevated 5-year hip fracture risk requiring evaluation"
            }
        }