"""
AUDIT-C for Alcohol Use Models

Request and response models for AUDIT-C alcohol screening calculation.

References (Vancouver style):
1. Bush K, Kivlahan DR, McDonell MB, Fihn SD, Bradley KA. The AUDIT alcohol consumption 
   questions (AUDIT-C): an effective brief screening test for problem drinking. 
   Ambulatory Care Quality Improvement Project (ACQUIP). Alcohol Use Disorders 
   Identification Test. Arch Intern Med. 1998 Sep 14;158(16):1789-95. 
   doi: 10.1001/archinte.158.16.1789.
2. Bradley KA, DeBenedetti AF, Volk RJ, Williams EC, Frank D, Kivlahan DR. AUDIT-C 
   as a brief screen for alcohol misuse in primary care. Alcohol Clin Exp Res. 
   2007 Jul;31(7):1208-17. doi: 10.1111/j.1530-0277.2007.00403.x.
3. Frank D, DeBenedetti AF, Volk RJ, Williams EC, Kivlahan DR, Bradley KA. 
   Effectiveness of the AUDIT-C as a screening test for alcohol misuse in three 
   race/ethnic groups. J Gen Intern Med. 2008 Jun;23(6):781-7. 
   doi: 10.1007/s11606-008-0594-0.

The AUDIT-C is a 3-item alcohol screen that can help identify persons who are hazardous 
drinkers or have active alcohol use disorders (including alcohol abuse or dependence). 
It is a modified version of the 10-question AUDIT instrument.
"""

from pydantic import BaseModel, Field
from typing import Literal


class AuditCRequest(BaseModel):
    """
    Request model for AUDIT-C Alcohol Use Screening
    
    The AUDIT-C consists of 3 questions about alcohol consumption patterns:
    
    Question 1 - Frequency: How often alcohol is consumed
    Question 2 - Quantity: Number of drinks on a typical drinking day  
    Question 3 - Heavy drinking: Frequency of having 6 or more drinks
    
    Scoring:
    - Each question is scored 0-4 points
    - Total score ranges from 0-12 points
    - Cutoffs: ≥4 for males, ≥3 for females suggest alcohol misuse
    
    Standard drink definitions:
    - 12 oz beer (5% alcohol)
    - 8 oz malt liquor (7% alcohol)
    - 5 oz wine (12% alcohol)
    - 1.5 oz spirits (40% alcohol)
    
    References (Vancouver style):
    1. Bush K, Kivlahan DR, McDonell MB, Fihn SD, Bradley KA. The AUDIT alcohol consumption 
       questions (AUDIT-C): an effective brief screening test for problem drinking. 
       Arch Intern Med. 1998 Sep 14;158(16):1789-95.
    2. Bradley KA, DeBenedetti AF, Volk RJ, Williams EC, Frank D, Kivlahan DR. AUDIT-C 
       as a brief screen for alcohol misuse in primary care. Alcohol Clin Exp Res. 
       2007 Jul;31(7):1208-17.
    """
    
    frequency: Literal[
        "never",
        "monthly_or_less",
        "2_to_4_times_month",
        "2_to_3_times_week",
        "4_or_more_times_week"
    ] = Field(
        ...,
        description="""How often did you have a drink containing alcohol in the past year?
        Scoring: never (0), monthly or less (1), 2-4 times/month (2), 2-3 times/week (3), 4+ times/week (4)""",
        example="2_to_3_times_week"
    )
    
    typical_drinks: Literal[
        "1_or_2",
        "3_or_4",
        "5_or_6",
        "7_to_9",
        "10_or_more"
    ] = Field(
        ...,
        description="""How many drinks containing alcohol did you have on a typical day when you were drinking in the past year?
        Scoring: 1-2 drinks (0), 3-4 drinks (1), 5-6 drinks (2), 7-9 drinks (3), 10+ drinks (4)""",
        example="3_or_4"
    )
    
    six_or_more: Literal[
        "never",
        "less_than_monthly",
        "monthly", 
        "weekly",
        "daily_or_almost_daily"
    ] = Field(
        ...,
        description="""How often did you have six or more drinks on one occasion in the past year?
        Scoring: never (0), less than monthly (1), monthly (2), weekly (3), daily or almost daily (4)""",
        example="less_than_monthly"
    )
    
    sex: Literal["male", "female"] = Field(
        ...,
        description="Patient's biological sex. Different cutoff values apply: ≥4 for males, ≥3 for females",
        example="male"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "frequency": "2_to_3_times_week",
                "typical_drinks": "3_or_4",
                "six_or_more": "less_than_monthly",
                "sex": "male"
            }
        }


class AuditCResponse(BaseModel):
    """
    Response model for AUDIT-C Alcohol Use Screening
    
    Provides the total AUDIT-C score and interpretation based on sex-specific cutoffs.
    Higher scores indicate greater severity of alcohol misuse.
    
    Reference: Bush K, et al. Arch Intern Med. 1998;158(16):1789-95.
    """
    
    result: int = Field(
        ...,
        description="AUDIT-C total score (sum of 3 questions, range 0-12 points)",
        example=4,
        ge=0,
        le=12
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation based on score and sex-specific cutoffs",
        example="AUDIT-C Score: 4 points\n\nThis score suggests alcohol misuse for male patients (cutoff ≥4)..."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low risk or At risk with sex specification)",
        example="At risk (Male)"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk level",
        example="Score suggests alcohol misuse (Mild severity)"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 4,
                "unit": "points",
                "interpretation": "AUDIT-C Score: 4 points\n\nThis score suggests alcohol misuse for male patients (cutoff ≥4).\n\nSeverity assessment:\n• Score 4: Mild severity of alcohol misuse\n• Higher scores correlate with greater severity\n\nRecommended actions:\n• Further assessment with full AUDIT questionnaire may be warranted\n• Consider brief intervention or referral to treatment\n• Assess for alcohol use disorder using DSM-5 criteria\n• Evaluate for medical complications of alcohol use\n\nNote: The AUDIT-C is a screening tool and should be followed by clinical assessment for diagnosis.",
                "stage": "At risk (Male)",
                "stage_description": "Score suggests alcohol misuse (Mild severity)"
            }
        }