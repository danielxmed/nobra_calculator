"""
HScore for Reactive Hemophagocytic Syndrome Models

Request and response models for HScore calculation.

References (Vancouver style):
1. Fardet L, Galicier L, Lambotte O, Marzac C, Aumont C, Chahwan D, Coppo P, Hie M. 
   Development and validation of the HScore, a score for the diagnosis of reactive 
   hemophagocytic syndrome. Arthritis Rheumatol. 2014 Sep;66(9):2613-20. 
   doi: 10.1002/art.38690.
2. Debaugnies F, Mahadeb B, Ferster A, Meuleman N, Rozen L, Demulder A, Corazza F. 
   Performances of the HScore in the diagnosis of hemophagocytic lymphohistiocytosis: 
   a multicenter study. J Clin Med. 2021 May 17;10(10):2143. doi: 10.3390/jcm10102143.
3. Henter JI, Horne A, Aricó M, Egeler RM, Filipovich AH, Imashuku S, et al. HLH-2004: 
   Diagnostic and therapeutic guidelines for hemophagocytic lymphohistiocytosis. 
   Pediatr Blood Cancer. 2007 Feb;48(2):124-31. doi: 10.1002/pbc.21039.

The HScore estimates the risk of having reactive hemophagocytic syndrome using nine 
variables: known immunosuppression, temperature, organomegaly, cytopenias, triglycerides, 
fibrinogen, ferritin, AST, and bone marrow hemophagocytosis. Scores range from 0-337 
points, with probabilities from <1% (≤90 points) to >99% (>250 points).
"""

from pydantic import BaseModel, Field
from typing import Literal


class HScoreRequest(BaseModel):
    """
    Request model for HScore for Reactive Hemophagocytic Syndrome
    
    The HScore uses 9 variables to estimate the probability of reactive hemophagocytic syndrome:
    
    Clinical Variables (3):
    - Known underlying immunosuppression (0-18 points)
    - Temperature: <38.4°C (0), 38.4-39.4°C (33), >39.4°C (49 points)
    - Organomegaly: None (0), hepato- or splenomegaly (23), both (38 points)
    
    Laboratory Variables (5):
    - Cytopenias: 1 lineage (0), 2 lineages (24), 3 lineages (34 points)
    - Triglycerides: <132.7 (0), 132.7-354 (44), 354-442.8 (64), >442.8 mg/dL (64 points)
    - Fibrinogen: >250 (0), ≤250 mg/dL (30 points)
    - Ferritin: <2000 (0), 2000-6000 (35), >6000 ng/mL (50 points)
    - AST: <30 (0), ≥30 IU/L (19 points)
    
    Histologic Variable (1):
    - Hemophagocytosis on bone marrow aspirate: No (0), Yes (35 points)
    
    References (Vancouver style):
    1. Fardet L, Galicier L, Lambotte O, Marzac C, Aumont C, Chahwan D, Coppo P, Hie M. 
       Development and validation of the HScore, a score for the diagnosis of reactive 
       hemophagocytic syndrome. Arthritis Rheumatol. 2014 Sep;66(9):2613-20. 
       doi: 10.1002/art.38690.
    2. Debaugnies F, Mahadeb B, Ferster A, Meuleman N, Rozen L, Demulder A, Corazza F. 
       Performances of the HScore in the diagnosis of hemophagocytic lymphohistiocytosis: 
       a multicenter study. J Clin Med. 2021 May 17;10(10):2143. doi: 10.3390/jcm10102143.
    """
    
    known_immunosuppression: Literal["yes", "no"] = Field(
        ...,
        description="Patient with known underlying immunosuppression (malignancy, immunosuppressive therapy, HIV, primary immunodeficiency). Scores 18 points if yes, 0 if no",
        example="no"
    )
    
    temperature: Literal["less_than_38.4", "38.4_to_39.4", "greater_than_39.4"] = Field(
        ...,
        description="Maximum temperature. <38.4°C (101.1°F) scores 0 points, 38.4-39.4°C (101.1-102.9°F) scores 33 points, >39.4°C (102.9°F) scores 49 points",
        example="greater_than_39.4"
    )
    
    organomegaly: Literal["none", "hepatomegaly_or_splenomegaly", "hepatomegaly_and_splenomegaly"] = Field(
        ...,
        description="Organomegaly on physical examination or imaging. None scores 0 points, hepatomegaly OR splenomegaly scores 23 points, hepatomegaly AND splenomegaly scores 38 points",
        example="hepatomegaly_and_splenomegaly"
    )
    
    cytopenias: Literal["one_lineage", "two_lineages", "three_lineages"] = Field(
        ...,
        description="Number of cytopenias (Hgb <9 g/dL, PLT <100K/μL, ANC <1K/μL). One lineage scores 0 points, two lineages score 24 points, three lineages score 34 points",
        example="three_lineages"
    )
    
    triglycerides: Literal["less_than_132.7", "132.7_to_354", "354_to_442.8", "greater_than_442.8"] = Field(
        ...,
        description="Triglyceride level in mg/dL. <132.7 (0 points), 132.7-354 (44 points), 354-442.8 (64 points), >442.8 (64 points). Convert from mmol/L: multiply by 88.5",
        example="greater_than_442.8"
    )
    
    fibrinogen: Literal["greater_than_250", "less_than_or_equal_250"] = Field(
        ...,
        description="Fibrinogen level in mg/dL. >250 mg/dL scores 0 points, ≤250 mg/dL scores 30 points. Convert from g/L: multiply by 100",
        example="less_than_or_equal_250"
    )
    
    ferritin: Literal["less_than_2000", "2000_to_6000", "greater_than_6000"] = Field(
        ...,
        description="Ferritin level in ng/mL (or μg/L). <2000 (0 points), 2000-6000 (35 points), >6000 (50 points). Hyperferritinemia is characteristic of HLH",
        example="greater_than_6000"
    )
    
    ast_sgot: Literal["less_than_30", "greater_than_or_equal_30"] = Field(
        ...,
        description="AST (SGOT) level in IU/L. <30 IU/L scores 0 points, ≥30 IU/L scores 19 points. Elevated transaminases are common in HLH",
        example="greater_than_or_equal_30"
    )
    
    hemophagocytosis: Literal["yes", "no"] = Field(
        ...,
        description="Hemophagocytosis features on bone marrow aspirate (macrophages engulfing blood cells). No scores 0 points, Yes scores 35 points. Not required for diagnosis",
        example="yes"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "known_immunosuppression": "no",
                "temperature": "greater_than_39.4",
                "organomegaly": "hepatomegaly_and_splenomegaly",
                "cytopenias": "three_lineages",
                "triglycerides": "greater_than_442.8",
                "fibrinogen": "less_than_or_equal_250",
                "ferritin": "greater_than_6000",  
                "ast_sgot": "greater_than_or_equal_30",
                "hemophagocytosis": "yes"
            }
        }


class HScoreResponse(BaseModel):
    """
    Response model for HScore for Reactive Hemophagocytic Syndrome
    
    The HScore ranges from 0-337 points and estimates probability of reactive 
    hemophagocytic syndrome:
    
    - ≤90 points: <1% probability (Very Low Risk)
    - 91-168 points: 1-25% probability (Low Risk)
    - 169-250 points: 25-99% probability (Intermediate Risk)
    - >250 points: >99% probability (High Risk)
    
    Reactive hemophagocytic syndrome is a life-threatening condition characterized by 
    excessive immune activation, requiring urgent hematology consultation and potential 
    immunosuppressive therapy.
    
    Reference: Fardet L, et al. Arthritis Rheumatol. 2014;66(9):2613-20.
    """
    
    result: int = Field(
        ...,
        ge=0,
        le=337,
        description="HScore points calculated from 9 clinical, laboratory, and histologic variables (range: 0-337 points)",
        example=286
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with probability of reactive hemophagocytic syndrome and recommended actions based on risk level",
        example="High probability of reactive hemophagocytic syndrome >99%. Diagnosis highly likely. Immediate hematology consultation and treatment initiation recommended."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Very Low Risk, Low Risk, Intermediate Risk, or High Risk)",
        example="High Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="HScore range description for the risk category",
        example="HScore >250"
    )
    
    probability_percent: float = Field(
        ...,
        ge=0,
        le=100,
        description="Estimated probability percentage of having reactive hemophagocytic syndrome based on the HScore",
        example=99.5
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 286,
                "unit": "points",
                "interpretation": "High probability of reactive hemophagocytic syndrome >99%. Diagnosis highly likely. Immediate hematology consultation and treatment initiation recommended.",
                "stage": "High Risk",
                "stage_description": "HScore >250",
                "probability_percent": 99.5
            }
        }