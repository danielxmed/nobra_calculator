"""
LRINEC Score for Necrotizing Soft Tissue Infection Models

Request and response models for LRINEC score calculation.

References (Vancouver style):
1. Wong CH, Khin LW, Heng KS, Tan KC, Low CO. The LRINEC (Laboratory Risk Indicator 
   for Necrotizing Fasciitis) score: a tool for distinguishing necrotizing fasciitis 
   from other soft tissue infections. Crit Care Med. 2004 Jul;32(7):1535-41. 
   doi: 10.1097/01.ccm.0000129486.35458.7d.
2. Bechar J, Sepehripour S, Hardwicke J, Filobbos G. Laboratory risk indicator for 
   necrotising fasciitis (LRINEC) score for the assessment of early necrotising fasciitis: 
   a systematic review of the literature. Ann R Coll Surg Engl. 2017 Jun;99(5):341-346. 
   doi: 10.1308/rcsann.2017.0053.
3. Fernando SM, Tran A, Cheng W, Rochwerg B, Kyeremanteng K, Seely AJE, et al. 
   Necrotizing soft tissue infection: diagnostic accuracy of physical examination, 
   imaging, and LRINEC score: a systematic review and meta-analysis. Ann Surg. 
   2019 Jan;269(1):58-65. doi: 10.1097/SLA.0000000000002774.

The LRINEC (Laboratory Risk Indicator for Necrotizing Fasciitis) score is a diagnostic 
tool using six routine laboratory parameters to distinguish necrotizing fasciitis from 
other soft tissue infections. It provides risk stratification to guide urgent surgical 
consultation and management decisions. While useful as an adjunct, clinical judgment 
remains paramount as 10% of patients with necrotizing fasciitis had scores <6 in the 
original study, and subsequent validation studies show variable performance.
"""

from pydantic import BaseModel, Field
from typing import Union


class LrinecScoreRequest(BaseModel):
    """
    Request model for LRINEC Score for Necrotizing Soft Tissue Infection
    
    The LRINEC score uses six laboratory parameters routinely obtained in emergency 
    departments to assess the probability of necrotizing fasciitis:
    
    Laboratory Parameters and Scoring:
    
    C-Reactive Protein (CRP):
    - <150 mg/L: 0 points
    - ≥150 mg/L: 4 points
    
    White Blood Cell Count (WBC):
    - <15,000 cells/µL: 0 points
    - 15,000-25,000 cells/µL: 1 point
    - >25,000 cells/µL: 2 points
    
    Hemoglobin:
    - >13.5 g/dL: 0 points
    - 11-13.5 g/dL: 1 point
    - <11 g/dL: 2 points
    
    Sodium:
    - ≥135 mEq/L: 0 points
    - <135 mEq/L: 2 points
    
    Creatinine:
    - ≤1.6 mg/dL: 0 points
    - >1.6 mg/dL: 2 points
    
    Glucose:
    - ≤180 mg/dL: 0 points
    - >180 mg/dL: 1 point
    
    Risk Stratification:
    - ≤5 points: Low risk (<50% probability of necrotizing fasciitis)
    - 6-7 points: Moderate risk (50-75% probability)
    - ≥8 points: High risk (>75% probability)
    
    Clinical Application:
    - Developed to assist early identification of necrotizing fasciitis
    - Should supplement, not replace, clinical assessment
    - High clinical suspicion warrants surgical consultation regardless of score
    - 10% of patients with necrotizing fasciitis had scores <6 in original study
    
    References (Vancouver style):
    1. Wong CH, Khin LW, Heng KS, Tan KC, Low CO. The LRINEC (Laboratory Risk Indicator 
    for Necrotizing Fasciitis) score: a tool for distinguishing necrotizing fasciitis 
    from other soft tissue infections. Crit Care Med. 2004 Jul;32(7):1535-41. 
    doi: 10.1097/01.ccm.0000129486.35458.7d.
    2. Bechar J, Sepehripour S, Hardwicke J, Filobbos G. Laboratory risk indicator for 
    necrotising fasciitis (LRINEC) score for the assessment of early necrotising fasciitis: 
    a systematic review of the literature. Ann R Coll Surg Engl. 2017 Jun;99(5):341-346. 
    doi: 10.1308/rcsann.2017.0053.
    3. Fernando SM, Tran A, Cheng W, Rochwerg B, Kyeremanteng K, Seely AJE, et al. 
    Necrotizing soft tissue infection: diagnostic accuracy of physical examination, 
    imaging, and LRINEC score: a systematic review and meta-analysis. Ann Surg. 
    2019 Jan;269(1):58-65. doi: 10.1097/SLA.0000000000002774.
    """
    
    crp: float = Field(
        ...,
        description="C-Reactive Protein level in mg/L. Scores 4 points if ≥150 mg/L, 0 points if <150 mg/L",
        ge=0,
        le=1000,
        example=85.5
    )
    
    wbc: float = Field(
        ...,
        description="White Blood Cell count in cells/µL. Scores 2 points if >25,000, 1 point if 15,000-25,000, 0 points if <15,000",
        ge=0,
        le=100000,
        example=18500
    )
    
    hemoglobin: float = Field(
        ...,
        description="Hemoglobin level in g/dL. Scores 2 points if <11, 1 point if 11-13.5, 0 points if >13.5",
        ge=0,
        le=25,
        example=10.2
    )
    
    sodium: float = Field(
        ...,
        description="Serum sodium level in mEq/L. Scores 2 points if <135, 0 points if ≥135",
        ge=100,
        le=180,
        example=132
    )
    
    creatinine: float = Field(
        ...,
        description="Serum creatinine level in mg/dL. Scores 2 points if >1.6, 0 points if ≤1.6",
        ge=0,
        le=20,
        example=1.8
    )
    
    glucose: float = Field(
        ...,
        description="Serum glucose level in mg/dL. Scores 1 point if >180, 0 points if ≤180",
        ge=0,
        le=1000,
        example=195
    )
    
    class Config:
        schema_extra = {
            "example": {
                "crp": 85.5,
                "wbc": 18500,
                "hemoglobin": 10.2,
                "sodium": 132,
                "creatinine": 1.8,
                "glucose": 195
            }
        }


class LrinecScoreResponse(BaseModel):
    """
    Response model for LRINEC Score for Necrotizing Soft Tissue Infection
    
    The LRINEC score provides risk stratification for necrotizing fasciitis diagnosis:
    
    Score Interpretation:
    - 0-5 points: Low risk (<50% probability of necrotizing fasciitis)
      Continue standard management with close monitoring
    
    - 6-7 points: Moderate risk (50-75% probability)
      Consider urgent surgical consultation and close monitoring
    
    - 8-13 points: High risk (>75% probability)
      Urgent surgical consultation and immediate operative intervention recommended
    
    Clinical Significance:
    - Original study: PPV 92%, NPV 96% for scores >6
    - Important limitation: 10% of patients with necrotizing fasciitis had scores <6
    - Should be used as adjunct to clinical assessment, not replacement
    - High clinical suspicion warrants surgical consultation regardless of score
    
    Reference: Wong CH, et al. Crit Care Med. 2004;32(7):1535-41.
    """
    
    result: int = Field(
        ...,
        description="LRINEC score calculated from laboratory parameters (range 0-13 points)",
        ge=0,
        le=13,
        example=8
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the LRINEC score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation with risk assessment and management recommendations",
        example="LRINEC Score Assessment for Necrotizing Soft Tissue Infection:\n\nComponent Scores:\n• C-Reactive Protein: 0 points\n• White Blood Cell count: 1 point\n• Hemoglobin: 2 points\n• Sodium: 2 points\n• Creatinine: 2 points\n• Glucose: 1 point\n• Total LRINEC score: 8/13 points"
    )
    
    stage: str = Field(
        ...,
        description="Risk category based on LRINEC score",
        example="High Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of necrotizing fasciitis probability",
        example="Necrotizing fasciitis likely"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 8,
                "unit": "points",
                "interpretation": "LRINEC Score Assessment for Necrotizing Soft Tissue Infection:\n\nComponent Scores:\n• C-Reactive Protein: 0 points\n• White Blood Cell count: 1 point\n• Hemoglobin: 2 points\n• Sodium: 2 points\n• Creatinine: 2 points\n• Glucose: 1 point\n• Total LRINEC score: 8/13 points\n\nRisk Assessment:\n• Risk category: High Risk\n• Probability of necrotizing fasciitis: >75%\n\nClinical Management:\n• Recommended management: Immediate operative intervention strongly recommended\n• Surgical consultation: Urgent surgical consultation required\n• Monitoring: Continuous monitoring in appropriate care setting",
                "stage": "High Risk",
                "stage_description": "Necrotizing fasciitis likely"
            }
        }