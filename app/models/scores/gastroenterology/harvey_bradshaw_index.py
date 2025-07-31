"""
Harvey-Bradshaw Index (HBI) for Crohn's Disease Models

Request and response models for HBI calculation.

References (Vancouver style):
1. Harvey RF, Bradshaw JM. A simple index of Crohn's-disease activity. Lancet. 
   1980 Mar 8;1(8167):514. doi: 10.1016/s0140-6736(80)92767-1.
2. Peyrin-Biroulet L, Panés J, Sandborn WJ, Vermeire S, Danese S, Feagan BG, et al. 
   Defining Disease Severity in Inflammatory Bowel Diseases: Current and Future 
   Directions. Clin Gastroenterol Hepatol. 2016 Mar;14(3):348-354.e17. 
   doi: 10.1016/j.cgh.2015.06.001.
3. Gomes P, du Boulay C, Smith CL, Holdstock G. Relationship between disease activity 
   indices and colonoscopic findings in patients with colonic inflammatory bowel disease. 
   Gut. 1986 Jan;27(1):92-5. doi: 10.1136/gut.27.1.92.
4. Vermeire S, Schreiber S, Sandborn WJ, Dubois C, Rutgeerts P. Correlation between 
   the Crohn's disease activity and Harvey-Bradshaw indices in assessing Crohn's disease 
   severity. Clin Gastroenterol Hepatol. 2010 Apr;8(4):357-63. doi: 10.1016/j.cgh.2010.01.001.

The Harvey-Bradshaw Index (HBI) is a simplified clinical scoring system for assessing 
Crohn's disease activity. Developed in 1980 as a simpler alternative to the Crohn's 
Disease Activity Index (CDAI), it correlates 93% with CDAI but uses only clinical 
parameters without requiring laboratory tests. The HBI consists of 5 domains: general 
well-being, abdominal pain, number of liquid stools, abdominal mass, and complications.
"""

from pydantic import BaseModel, Field, validator
from typing import List, Literal
from enum import IntEnum


class GeneralWellbeing(IntEnum):
    """General well-being scores"""
    VERY_WELL = 0
    SLIGHTLY_BELOW_PAR = 1
    POOR = 2
    VERY_POOR = 3
    TERRIBLE = 4


class AbdominalPain(IntEnum):
    """Abdominal pain severity scores"""
    NONE = 0
    MILD = 1
    MODERATE = 2
    SEVERE = 3


class AbdominalMass(IntEnum):
    """Abdominal mass examination scores"""
    NONE = 0
    DUBIOUS = 1
    DEFINITE = 2
    DEFINITE_AND_TENDER = 3


class HarveyBradshawIndexRequest(BaseModel):
    """
    Request model for Harvey-Bradshaw Index (HBI) for Crohn's Disease
    
    The HBI uses 5 clinical parameters to assess Crohn's disease activity:
    
    1. General well-being (0-4 points): Assessed for the previous day
       - 0: Very well
       - 1: Slightly below par
       - 2: Poor
       - 3: Very poor
       - 4: Terrible
    
    2. Abdominal pain (0-3 points): Assessed for the previous day
       - 0: None
       - 1: Mild
       - 2: Moderate
       - 3: Severe
    
    3. Number of liquid/soft stools: Count from the previous day (1 point per stool)
    
    4. Abdominal mass (0-3 points): Based on physical examination
       - 0: None
       - 1: Dubious
       - 2: Definite
       - 3: Definite and tender
    
    5. Complications (1 point each): Extra-intestinal manifestations
    
    Total score interpretation:
    - <5: Remission
    - 5-7: Mild disease
    - 8-16: Moderate disease
    - >16: Severe disease
    
    References (Vancouver style):
    1. Harvey RF, Bradshaw JM. A simple index of Crohn's-disease activity. Lancet. 
       1980 Mar 8;1(8167):514. doi: 10.1016/s0140-6736(80)92767-1.
    2. Vermeire S, Schreiber S, Sandborn WJ, Dubois C, Rutgeerts P. Correlation between 
       the Crohn's disease activity and Harvey-Bradshaw indices in assessing Crohn's disease 
       severity. Clin Gastroenterol Hepatol. 2010 Apr;8(4):357-63. doi: 10.1016/j.cgh.2010.01.001.
    """
    
    general_wellbeing: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="General well-being assessed for the previous day. "
                    "0=Very well (no symptoms), 1=Slightly below par (minimal symptoms), "
                    "2=Poor (mild symptoms affecting daily activities), "
                    "3=Very poor (moderate symptoms significantly affecting activities), "
                    "4=Terrible (severe symptoms preventing normal activities)",
        example=1
    )
    
    abdominal_pain: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Abdominal pain severity assessed for the previous day. "
                    "0=None (no pain), 1=Mild (occasional discomfort), "
                    "2=Moderate (frequent pain affecting activities), "
                    "3=Severe (constant pain requiring analgesics)",
        example=1
    )
    
    liquid_stools: int = Field(
        ...,
        description="Number of liquid or soft stools in the previous day. "
                    "Each liquid/soft stool counts as 1 point. Normal formed stools are not counted.",
        example=3,
        ge=0,
        le=50
    )
    
    abdominal_mass: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Presence of abdominal mass on physical examination. "
                    "0=None (no palpable mass), 1=Dubious (uncertain if mass present), "
                    "2=Definite (clear palpable mass), "
                    "3=Definite and tender (palpable mass with tenderness)",
        example=0
    )
    
    complications: List[Literal[
        "none",
        "arthralgia",
        "uveitis",
        "erythema_nodosum",
        "aphthous_ulcers",
        "pyoderma_gangrenosum",
        "anal_fissures",
        "new_fistula",
        "abscess"
    ]] = Field(
        ...,
        description="Extra-intestinal manifestations or complications (1 point each). "
                    "Select all that apply: arthralgia (joint pain), uveitis (eye inflammation), "
                    "erythema nodosum (tender red nodules), aphthous ulcers (mouth sores), "
                    "pyoderma gangrenosum (skin ulcers), anal fissures, new fistula, abscess. "
                    "Select 'none' if no complications present.",
        example=["none"]
    )
    
    @validator('complications')
    def validate_complications(cls, v):
        """Ensure 'none' is not selected with other complications"""
        if 'none' in v and len(v) > 1:
            raise ValueError("Cannot select 'none' with other complications")
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "general_wellbeing": 1,
                "abdominal_pain": 1,
                "liquid_stools": 3,
                "abdominal_mass": 0,
                "complications": ["none"]
            }
        }


class HarveyBradshawIndexResponse(BaseModel):
    """
    Response model for Harvey-Bradshaw Index (HBI) for Crohn's Disease
    
    The HBI score provides a simple clinical assessment of Crohn's disease activity:
    - <5 points: Remission - minimal or no disease activity
    - 5-7 points: Mild disease - symptoms present but manageable
    - 8-16 points: Moderate disease - significant symptoms requiring treatment escalation
    - >16 points: Severe disease - urgent intervention needed
    
    Clinical response is defined as a reduction of ≥3 points from baseline.
    The HBI correlates 93% with CDAI, with scores ≤3 very likely indicating CDAI remission.
    
    Reference: Harvey RF, Bradshaw JM. Lancet. 1980;1(8167):514.
    """
    
    result: int = Field(
        ...,
        description="HBI score calculated from clinical parameters (typical range: 0-30+ points)",
        example=5,
        ge=0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of the HBI score with treatment recommendations",
        example="Patient has mild Crohn's disease activity. Consider optimization of current "
                "therapy or initiation of treatment if not already on therapy. Close monitoring "
                "is recommended."
    )
    
    stage: str = Field(
        ...,
        description="Disease activity category (Remission, Mild Disease, Moderate Disease, Severe Disease)",
        example="Mild Disease"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the disease activity level",
        example="Mild disease activity"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 5,
                "unit": "points",
                "interpretation": "Patient has mild Crohn's disease activity. Consider optimization of current "
                                  "therapy or initiation of treatment if not already on therapy. Close monitoring "
                                  "is recommended.",
                "stage": "Mild Disease",
                "stage_description": "Mild disease activity"
            }
        }