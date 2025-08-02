"""
HERDOO2 Rule for Discontinuing Anticoagulation in Unprovoked VTE Models

Request and response models for HERDOO2 calculation.

References (Vancouver style):
1. Rodger MA, Kahn SR, Wells PS, Anderson DA, Chagnon I, Le Gal G, et al. Identifying 
   unprovoked thromboembolism patients at low risk for recurrence who can discontinue 
   anticoagulant therapy. CMAJ. 2008 Aug 26;179(5):417-26. doi: 10.1503/cmaj.080493.
2. Rodger MA, Le Gal G, Anderson DR, Schmidt J, Pernod G, Kahn SR, et al.; REVERSE II 
   Study Investigators. Validating the HERDOO2 rule to guide treatment duration for 
   women with unprovoked venous thrombosis: multinational prospective cohort management 
   study. BMJ. 2017 Mar 17;356:j1065. doi: 10.1136/bmj.j1065.
3. Kearon C, Ageno W, Cannegieter SC, Cosmi B, Geersing GJ, Kyrle PA; Subcommittees 
   on Control of Anticoagulation, and Predictive and Diagnostic Variables in Thrombotic 
   Disease. Categorization of patients as having provoked or unprovoked venous 
   thromboembolism: guidance from the SSC of ISTH. J Thromb Haemost. 2016 Jul;14(7):1480-3. 
   doi: 10.1111/jth.13336.

The HERDOO2 rule is a clinical decision tool specifically designed for women with 
first unprovoked VTE who have completed 5-12 months of anticoagulation. It identifies 
those at low risk of recurrence (≤1 point) who can safely discontinue anticoagulation 
with an annual recurrence risk of only 3.0%.
"""

from pydantic import BaseModel, Field
from typing import Literal


class Herdoo2Request(BaseModel):
    """
    Request model for HERDOO2 Rule for Discontinuing Anticoagulation in Unprovoked VTE
    
    The HERDOO2 rule uses 4 clinical variables to identify low-risk women who can 
    safely discontinue anticoagulation after treatment for unprovoked VTE:
    
    Clinical Variables (each worth 1 point if positive):
    - Post-thrombotic signs: Hyperpigmentation, edema, or redness in either leg
    - D-dimer level: ≥250 μg/L measured while on anticoagulation
    - BMI: ≥30 kg/m²
    - Age: ≥65 years
    
    Important Notes:
    - Only applicable to WOMEN with FIRST UNPROVOKED VTE
    - Patient must have completed 5-12 months of anticoagulation
    - D-dimer should be measured while patient is still on anticoagulation
    - Not validated for men or patients with provoked VTE
    - Not validated for patients with cancer-associated thrombosis
    
    References (Vancouver style):
    1. Rodger MA, Kahn SR, Wells PS, Anderson DA, Chagnon I, Le Gal G, et al. Identifying 
       unprovoked thromboembolism patients at low risk for recurrence who can discontinue 
       anticoagulant therapy. CMAJ. 2008 Aug 26;179(5):417-26. doi: 10.1503/cmaj.080493.
    2. Rodger MA, Le Gal G, Anderson DR, Schmidt J, Pernod G, Kahn SR, et al.; REVERSE II 
       Study Investigators. Validating the HERDOO2 rule to guide treatment duration for 
       women with unprovoked venous thrombosis: multinational prospective cohort management 
       study. BMJ. 2017 Mar 17;356:j1065. doi: 10.1136/bmj.j1065.
    """
    
    post_thrombotic_signs: Literal["yes", "no"] = Field(
        ...,
        description="Presence of post-thrombotic signs including hyperpigmentation, edema, or redness in either leg. "
                    "These signs indicate venous insufficiency and are associated with higher recurrence risk. "
                    "Scores 1 point if present.",
        example="no"
    )
    
    d_dimer_level: Literal["normal", "elevated"] = Field(
        ...,
        description="D-dimer level measured while patient is on anticoagulation. "
                    "'elevated' means ≥250 μg/L (or above the laboratory's normal range). "
                    "An elevated D-dimer while on anticoagulation suggests ongoing thrombotic activity. "
                    "Scores 1 point if elevated.",
        example="normal"
    )
    
    bmi: Literal["under_30", "30_or_over"] = Field(
        ...,
        description="Body Mass Index (BMI) category. Obesity (BMI ≥30 kg/m²) is an independent "
                    "risk factor for VTE recurrence. Scores 1 point if BMI is 30 or over.",
        example="under_30"
    )
    
    age: Literal["under_65", "65_or_over"] = Field(
        ...,
        description="Patient age category. Advanced age (≥65 years) is associated with "
                    "increased VTE recurrence risk. Scores 1 point if age is 65 or over.",
        example="under_65"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "post_thrombotic_signs": "no",
                "d_dimer_level": "normal",
                "bmi": "under_30",
                "age": "under_65"
            }
        }


class Herdoo2Response(BaseModel):
    """
    Response model for HERDOO2 Rule for Discontinuing Anticoagulation in Unprovoked VTE
    
    The HERDOO2 score ranges from 0-4 points and classifies women into:
    - Low Risk (0-1 points): 3.0% annual recurrence risk - can discontinue anticoagulation
    - Not Low Risk (2-4 points): 7.4% annual recurrence risk - continue anticoagulation
    
    Clinical Application:
    - Women scoring 0-1 points can safely discontinue anticoagulation
    - This decision should be made in consultation with the patient considering:
      - Individual bleeding risk
      - Patient preference
      - Access to medical care if recurrence occurs
    
    Reference: Rodger MA, et al. CMAJ. 2008;179(5):417-26.
    """
    
    result: int = Field(
        ...,
        description="HERDOO2 score calculated from clinical variables (range: 0-4 points)",
        example=1
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation including recurrence risk and anticoagulation recommendation",
        example="Low risk of VTE recurrence (3.0% annual risk). Anticoagulation can be safely discontinued after completing initial treatment period."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk or Not Low Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the recommended action",
        example="Can discontinue anticoagulation"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 1,
                "unit": "points",
                "interpretation": "Low risk of VTE recurrence (3.0% annual risk). Anticoagulation can be safely discontinued after completing initial treatment period.",
                "stage": "Low Risk",
                "stage_description": "Can discontinue anticoagulation"
            }
        }