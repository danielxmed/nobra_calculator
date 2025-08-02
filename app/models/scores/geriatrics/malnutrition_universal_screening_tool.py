"""
Malnutrition Universal Screening Tool (MUST) Models

Request and response models for MUST malnutrition screening calculation.

References (Vancouver style):
1. Elia M. The 'MUST' report. Nutritional screening of adults: a multidisciplinary 
   responsibility. Redditch: BAPEN; 2003.
2. Kondrup J, Allison SP, Elia M, Vellas B, Plauth M. ESPEN guidelines for nutrition 
   screening 2002. Clin Nutr. 2003 Aug;22(4):415-21. doi: 10.1016/s0261-5614(02)00194-7.
3. Stratton RJ, Hackston A, Longmore D, Dixon R, Price S, Stroud M, et al. 
   Malnutrition in hospital outpatients and inpatients: prevalence, concurrent validity 
   and ease of use of the 'malnutrition universal screening tool' ('MUST') for adults. 
   Br J Nutr. 2004 Nov;92(5):799-808. doi: 10.1079/bjn20041258.

The Malnutrition Universal Screening Tool (MUST) is a validated screening tool 
developed by BAPEN in 2003 to identify adults who are malnourished or at risk 
of malnutrition. It uses three key indicators: BMI, recent weight loss, and 
acute disease effects. MUST is widely used across UK healthcare settings and 
is linked to evidence-based care pathways for nutritional intervention.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any


class MalnutritionUniversalScreeningToolRequest(BaseModel):
    """
    Request model for Malnutrition Universal Screening Tool (MUST)
    
    MUST assesses malnutrition risk using three key components:
    
    1. Body Mass Index (BMI):
       - ≥20 kg/m²: 0 points (normal/overweight)
       - 18.5-19.9 kg/m²: 1 point (mild underweight)
       - <18.5 kg/m²: 2 points (underweight)
    
    2. Unplanned Weight Loss (past 3-6 months):
       - <5% of body weight: 0 points
       - 5-10% of body weight: 1 point
       - >10% of body weight: 2 points
    
    3. Acute Disease Effect:
       - No acute illness or intake maintained: 0 points
       - Acutely ill with no intake for >5 days (or likely to): 2 points
    
    Total Score Interpretation:
    - 0 points: Low risk - routine care
    - 1 point: Medium risk - observe and document intake
    - ≥2 points: High risk - refer to dietitian/nutrition team
    
    Clinical Applications:
    - Hospital admission screening
    - Care home nutrition assessment
    - Community health monitoring
    - Outpatient clinic screening
    - Pre-operative assessment
    - Elderly care evaluation
    
    Screening Frequency:
    - Hospitals: Weekly
    - Care homes: Monthly  
    - Community: Monthly (high risk), annually (special groups)

    References (Vancouver style):
    1. Elia M. The 'MUST' report. Nutritional screening of adults: a multidisciplinary 
    responsibility. Redditch: BAPEN; 2003.
    2. Kondrup J, Allison SP, Elia M, Vellas B, Plauth M. ESPEN guidelines for nutrition 
    screening 2002. Clin Nutr. 2003 Aug;22(4):415-21. doi: 10.1016/s0261-5614(02)00194-7.
    3. Stratton RJ, Hackston A, Longmore D, Dixon R, Price S, Stroud M, et al. 
    Malnutrition in hospital outpatients and inpatients: prevalence, concurrent validity 
    and ease of use of the 'malnutrition universal screening tool' ('MUST') for adults. 
    Br J Nutr. 2004 Nov;92(5):799-808. doi: 10.1079/bjn20041258.
    """
    
    bmi: float = Field(
        ...,
        ge=10.0,
        le=60.0,
        description="Body Mass Index in kg/m². Use measured height and weight when possible. BMI ≥20 (0pts), 18.5-19.9 (1pt), <18.5 (2pts)",
        example=22.5
    )
    
    weight_loss_percentage: float = Field(
        ...,
        ge=0.0,
        le=50.0,
        description="Unplanned weight loss in the past 3-6 months as percentage of body weight. <5% (0pts), 5-10% (1pt), >10% (2pts)",
        example=3.0
    )
    
    acute_disease_effect: Literal["yes", "no"] = Field(
        ...,
        description="Patient acutely ill with no nutritional intake for >5 days or likely to have no intake for >5 days. This includes conditions causing poor appetite, nausea, vomiting, or inability to eat",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "bmi": 22.5,
                "weight_loss_percentage": 3.0,
                "acute_disease_effect": "no"
            }
        }


class MalnutritionUniversalScreeningToolResponse(BaseModel):
    """
    Response model for Malnutrition Universal Screening Tool (MUST)
    
    MUST provides systematic malnutrition risk assessment with three risk levels:
    
    Low Risk (0 points):
    - Normal BMI, minimal weight loss, no acute illness
    - Routine clinical care with regular screening
    - Weekly in hospitals, monthly in care homes, annually in community
    
    Medium Risk (1 point):
    - Mild nutritional concerns requiring monitoring
    - Document dietary intake for 3 days
    - Clinical intervention if no improvement
    
    High Risk (≥2 points):
    - Significant malnutrition risk requiring immediate action
    - Dietitian referral and nutrition support team involvement
    - Implement nutritional intervention strategies
    - Regular monitoring and care plan review
    
    The tool links to evidence-based care pathways and treatment protocols,
    making it practical for implementation across healthcare settings.
    
    Reference: Elia M. The 'MUST' report. BAPEN; 2003.
    """
    
    result: Dict[str, Any] = Field(
        ...,
        description="MUST assessment results including total score, component scores, and category classifications",
        example={
            "total_score": 0,
            "bmi_score": 0,
            "weight_loss_score": 0,
            "disease_score": 0,
            "bmi_category": "Normal/Overweight (≥20.0 kg/m²): 22.5",
            "weight_loss_category": "Minimal weight loss (<5%): 3.0%"
        }
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with specific care recommendations and screening frequency guidance",
        example="Low risk of malnutrition. Routine clinical care with repeat screening: in hospital weekly, in care homes monthly, and in community annually for special groups (>75 years, concern about underlying conditions). Continue normal diet and monitor as per routine clinical care."
    )
    
    stage: str = Field(
        ...,
        description="Malnutrition risk level (Low Risk, Medium Risk, High Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk level",
        example="Low risk of malnutrition"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": {
                    "total_score": 0,
                    "bmi_score": 0,
                    "weight_loss_score": 0,
                    "disease_score": 0,
                    "bmi_category": "Normal/Overweight (≥20.0 kg/m²): 22.5",
                    "weight_loss_category": "Minimal weight loss (<5%): 3.0%"
                },
                "unit": "points",
                "interpretation": "Low risk of malnutrition. Routine clinical care with repeat screening: in hospital weekly, in care homes monthly, and in community annually for special groups (>75 years, concern about underlying conditions). Continue normal diet and monitor as per routine clinical care.",
                "stage": "Low Risk",
                "stage_description": "Low risk of malnutrition"
            }
        }