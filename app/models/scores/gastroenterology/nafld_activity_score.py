"""
NAFLD (Non-Alcoholic Fatty Liver Disease) Activity Score Models

Request and response models for NAFLD Activity Score calculation.

References (Vancouver style):
1. Kleiner DE, Brunt EM, Van Natta M, Behling C, Contos MJ, Cummings OW, et al. Design and 
   validation of a histological scoring system for nonalcoholic fatty liver disease. 
   Hepatology. 2005 Jun;41(6):1313-21. doi: 10.1002/hep.20701.
2. Brunt EM, Kleiner DE, Wilson LA, Belt P, Neuschwander-Tetri BA; NASH Clinical Research 
   Network (CRN). Nonalcoholic fatty liver disease (NAFLD) activity score and the 
   histopathologic diagnosis in NAFLD: distinct clinicopathologic meanings. Hepatology. 
   2011 Mar;53(3):810-20. doi: 10.1002/hep.24127.
3. Sanyal AJ, Brunt EM, Kleiner DE, Kowdley KV, Chalasani N, Lavine JE, et al. Endpoints 
   and clinical trial design for nonalcoholic steatohepatitis. Hepatology. 2011 
   Jul;54(1):344-53. doi: 10.1002/hep.24376.

The NAFLD Activity Score (NAS) is a semi-quantitative scoring system designed to evaluate 
the severity of disease activity in nonalcoholic fatty liver disease. It assesses three 
histological features: steatosis (0-3), lobular inflammation (0-3), and hepatocellular 
ballooning (0-2), yielding a total score of 0-8. While not intended as a diagnostic tool 
for NASH, the NAS provides a standardized method for assessing disease activity and is 
widely used in clinical trials to evaluate treatment response.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal, Dict, Any


class NafldActivityScoreRequest(BaseModel):
    """
    Request model for NAFLD (Non-Alcoholic Fatty Liver Disease) Activity Score
    
    The NAS evaluates three histological components on liver biopsy:
    
    1. Steatosis (0-3 points):
       - <5%: 0 points (minimal to no fat)
       - 5-33%: 1 point (mild steatosis)
       - 34-66%: 2 points (moderate steatosis)
       - >66%: 3 points (severe steatosis)
    
    2. Lobular Inflammation (0-3 points):
       - No foci: 0 points
       - 1 focus per 200× field: 1 point (mild)
       - 2-4 foci per 200× field: 2 points (moderate)
       - >4 foci per 200× field: 3 points (severe)
    
    3. Hepatocellular Ballooning (0-2 points):
       - None: 0 points
       - Few balloon cells: 1 point
       - Many cells/prominent ballooning: 2 points
    
    Important considerations:
    - Fibrosis is staged separately (0-4) and not included in NAS
    - NAS ≥5 correlates with "definite NASH" diagnosis
    - NAS ≤2 correlates with "not NASH"
    - NAS 3-4 is indeterminate and requires clinical correlation
    - A ≥2-point improvement in NAS is a common endpoint in clinical trials
    
    References (Vancouver style):
    1. Kleiner DE, Brunt EM, Van Natta M, Behling C, Contos MJ, Cummings OW, et al. Design and 
       validation of a histological scoring system for nonalcoholic fatty liver disease. 
       Hepatology. 2005 Jun;41(6):1313-21. doi: 10.1002/hep.20701.
    2. Brunt EM, Kleiner DE, Wilson LA, Belt P, Neuschwander-Tetri BA; NASH Clinical Research 
       Network (CRN). Nonalcoholic fatty liver disease (NAFLD) activity score and the 
       histopathologic diagnosis in NAFLD: distinct clinicopathologic meanings. Hepatology. 
       2011 Mar;53(3):810-20. doi: 10.1002/hep.24127.
    """
    
    steatosis: Literal["<5%", "5-33%", "34-66%", ">66%"] = Field(
        ...,
        description="Percentage of hepatocytes containing fat droplets on liver biopsy. <5% scores 0 points (minimal), 5-33% scores 1 point (mild), 34-66% scores 2 points (moderate), >66% scores 3 points (severe)",
        example="5-33%"
    )
    
    lobular_inflammation: Literal["No foci", "1 focus per 200× field", "2-4 foci per 200× field", ">4 foci per 200× field"] = Field(
        ...,
        description="Number of inflammatory foci per 200× microscopic field. No foci scores 0 points, 1 focus scores 1 point (mild), 2-4 foci score 2 points (moderate), >4 foci score 3 points (severe)",
        example="2-4 foci per 200× field"
    )
    
    ballooning: Literal["None", "Few balloon cells", "Many cells/prominent ballooning"] = Field(
        ...,
        description="Hepatocellular ballooning (enlarged hepatocytes with rarefied cytoplasm). None scores 0 points, few balloon cells score 1 point, many cells/prominent ballooning scores 2 points",
        example="Few balloon cells"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "steatosis": "5-33%",
                "lobular_inflammation": "2-4 foci per 200× field",
                "ballooning": "Few balloon cells"
            }
        }


class NafldActivityScoreResponse(BaseModel):
    """
    Response model for NAFLD (Non-Alcoholic Fatty Liver Disease) Activity Score
    
    The NAS ranges from 0-8 points and provides a semi-quantitative assessment of disease activity:
    - 0: No activity
    - 1-2: Mild activity (generally "not NASH")
    - 3-5: Moderate activity (NAS ≥4 optimal for clinical trials, NAS ≥5 correlates with "definite NASH")
    - 6-8: Marked activity (strongly correlates with definite NASH)
    
    Reference: Kleiner DE, et al. Hepatology. 2005;41(6):1313-21.
    """
    
    result: int = Field(
        ...,
        description="NAFLD Activity Score calculated from histological components (range: 0-8 points)",
        example=4
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of the NAS score and its correlation with NASH diagnosis",
        example="NAS of 3-5 indicates moderate NAFLD activity. Scores ≥4 have optimal sensitivity and specificity for predicting steatohepatitis. NAS ≥5 strongly correlates with 'definite NASH' diagnosis."
    )
    
    stage: str = Field(
        ...,
        description="Activity level category (No activity, Mild activity, Moderate activity, Marked activity)",
        example="Moderate activity"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the activity level",
        example="Moderate NAFLD activity"
    )
    
    component_scores: Dict[str, int] = Field(
        ...,
        description="Individual component scores for steatosis, lobular inflammation, and ballooning",
        example={"steatosis": 1, "lobular_inflammation": 2, "ballooning": 1}
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 4,
                "unit": "points",
                "interpretation": "NAS of 3-5 indicates moderate NAFLD activity. Scores ≥4 have optimal sensitivity and specificity for predicting steatohepatitis. NAS ≥5 strongly correlates with 'definite NASH' diagnosis.",
                "stage": "Moderate activity",
                "stage_description": "Moderate NAFLD activity",
                "component_scores": {
                    "steatosis": 1,
                    "lobular_inflammation": 2,
                    "ballooning": 1
                }
            }
        }