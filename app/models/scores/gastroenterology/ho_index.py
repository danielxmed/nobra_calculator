"""
Ho Index for Ulcerative Colitis Models

Request and response models for Ho Index calculation.

References (Vancouver style):
1. Ho GT, Mowat C, Goddard CJ, Fennell JM, Shah NB, Prescott RJ, Satsangi J. 
   Predicting the outcome of severe ulcerative colitis: development of a novel 
   risk score to aid early selection of patients for second-line medical therapy 
   or surgery. Aliment Pharmacol Ther. 2004 May 15;19(10):1079-87. 
   doi: 10.1111/j.1365-2036.2004.01932.x.
2. Lynch RW, Churchhouse AM, Protheroe A, Arnott ID; UK IBD Audit Steering Group. 
   Predicting outcome in acute severe ulcerative colitis: comparison of the Travis 
   and Ho scores using UK IBD audit data. Aliment Pharmacol Ther. 2016 Jun;43(11):
   1132-41. doi: 10.1111/apt.13614.

The Ho Index uses three clinical parameters assessed on day 3 of admission to predict 
the failure of intravenous corticosteroid therapy in patients with acute severe 
ulcerative colitis. This tool helps identify patients who may need early escalation 
to second-line medical therapy or surgery.
"""

from pydantic import BaseModel, Field
from typing import Literal


class HoIndexRequest(BaseModel):
    """
    Request model for Ho Index for Ulcerative Colitis
    
    The Ho Index predicts medical therapy failure in acute severe ulcerative colitis 
    by assessing three key parameters on day 3 of admission:
    
    1. Mean stool frequency (over previous 24 hours):
    - 4_or_less: ≤4 stools/24h (0 points)
    - over_4_to_6: >4 to ≤6 stools/24h (1 point)  
    - over_6_to_9: >6 to ≤9 stools/24h (2 points)
    - over_9: >9 stools/24h (4 points)
    
    2. Colonic dilatation on abdominal X-ray:
    - absent: No colonic dilatation (0 points)
    - present: Transverse colon ≥5.5cm (4 points)
    
    3. Hypoalbuminemia:
    - no: Albumin >3 g/dL or >30 g/L (0 points)
    - yes: Albumin ≤3 g/dL or ≤30 g/L (1 point)

    References (Vancouver style):
    1. Ho GT, Mowat C, Goddard CJ, Fennell JM, Shah NB, Prescott RJ, Satsangi J. 
    Predicting the outcome of severe ulcerative colitis: development of a novel 
    risk score to aid early selection of patients for second-line medical therapy 
    or surgery. Aliment Pharmacol Ther. 2004 May 15;19(10):1079-87.
    """
    
    mean_stool_frequency: Literal["4_or_less", "over_4_to_6", "over_6_to_9", "over_9"] = Field(
        ...,
        description="Mean stool frequency in stools per 24 hours on day 3 of admission. "
                    "≤4 stools scores 0 points, >4-6 scores 1 point, >6-9 scores 2 points, "
                    ">9 scores 4 points",
        example="over_6_to_9"
    )
    
    colonic_dilatation: Literal["absent", "present"] = Field(
        ...,
        description="Presence of colonic dilatation (transverse colon ≥5.5cm) on abdominal "
                    "X-ray within first 3 days. Absent scores 0 points, present scores 4 points",
        example="absent"
    )
    
    hypoalbuminemia: Literal["no", "yes"] = Field(
        ...,
        description="Presence of hypoalbuminemia (albumin ≤3 g/dL or ≤30 g/L) on day 3. "
                    "No scores 0 points, yes scores 1 point",
        example="yes"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "mean_stool_frequency": "over_6_to_9",
                "colonic_dilatation": "absent",
                "hypoalbuminemia": "yes"
            }
        }


class HoIndexResponse(BaseModel):
    """
    Response model for Ho Index for Ulcerative Colitis
    
    The Ho Index score ranges from 0-9 points and predicts medical therapy failure:
    - Score 0-1: Low risk (11% failure rate)
    - Score 2-3: Intermediate risk (45% failure rate)  
    - Score ≥4: High risk (85% failure rate)
    
    The score has 85% sensitivity and 75% specificity at cutoff ≥4 for predicting 
    non-response to corticosteroid therapy.
    
    Reference: Ho GT, et al. Aliment Pharmacol Ther. 2004;19(10):1079-87.
    """
    
    result: int = Field(
        ...,
        description="Ho Index score calculated from the three clinical parameters (range: 0-9 points)",
        example=3
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended management based on the score",
        example="Intermediate risk of medical therapy failure (45%). Consider early assessment "
                "for second-line medical therapy (e.g., infliximab, cyclosporine). Close "
                "monitoring required with low threshold for escalation."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, Intermediate Risk, High Risk)",
        example="Intermediate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Score range description for the risk category",
        example="Score 2-3"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 3,
                "unit": "points",
                "interpretation": "Intermediate risk of medical therapy failure (45%). Consider "
                                "early assessment for second-line medical therapy (e.g., infliximab, "
                                "cyclosporine). Close monitoring required with low threshold for escalation.",
                "stage": "Intermediate Risk",
                "stage_description": "Score 2-3"
            }
        }