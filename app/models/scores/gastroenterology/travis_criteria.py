"""
Travis Criteria Models

Request and response models for Travis Criteria calculation.

References (Vancouver style):
1. Travis SP, Farrant JM, Ricketts C, et al. Predicting outcome in severe ulcerative 
   colitis. Gut. 1996 Jun;38(6):905-10. doi: 10.1136/gut.38.6.905. PMID: 8984031; 
   PMCID: PMC1383201.
2. Lynch RW, Churchhouse AMD, Protheroe A, Arnott IDR; UK IBD Audit Steering Group. 
   Predicting outcome in acute severe ulcerative colitis: comparison of the Travis 
   and Ho scores using UK IBD audit data. Aliment Pharmacol Ther. 2016 Jun;43(11):1132-41. 
   doi: 10.1111/apt.13614. Epub 2016 Apr 8. PMID: 27060985.
3. Pabla BS, Schwartz DA. Assessing severity of disease in patients with ulcerative 
   colitis. Gastroenterol Clin North Am. 2020 Dec;49(4):671-688. doi: 10.1016/j.gtc.2020.08.003. 
   Epub 2020 Sep 29. PMID: 33121688.

The Travis Criteria is a clinical prediction tool used on day 3 of treatment for 
acute severe ulcerative colitis to predict failure of medical therapy and need for 
colectomy. It uses stool frequency and C-reactive protein (CRP) levels to stratify 
patients into low or high risk categories.
"""

from pydantic import BaseModel, Field
from typing import Literal


class TravisCriteriaRequest(BaseModel):
    """
    Request model for Travis Criteria
    
    The Travis Criteria evaluates patients with acute severe ulcerative colitis on 
    day 3 of treatment. It combines clinical (stool frequency) and laboratory (CRP) 
    parameters to predict the likelihood of medical therapy failure and need for 
    colectomy.
    
    Risk stratification:
    - High risk: >8 stools/day OR 3-8 stools/day with CRP >45 mg/L
    - Low risk: All other combinations
    
    The original study showed 85% specificity for predicting need for colectomy in 
    patients meeting high-risk criteria.
    
    References (Vancouver style):
    1. Travis SP, Farrant JM, Ricketts C, et al. Predicting outcome in severe ulcerative 
       colitis. Gut. 1996 Jun;38(6):905-10. doi: 10.1136/gut.38.6.905.
    2. Lynch RW, Churchhouse AMD, Protheroe A, Arnott IDR; UK IBD Audit Steering Group. 
       Predicting outcome in acute severe ulcerative colitis: comparison of the Travis 
       and Ho scores using UK IBD audit data. Aliment Pharmacol Ther. 2016 Jun;43(11):1132-41.
    """
    
    stool_frequency: Literal["less_than_3", "3_to_8", "more_than_8"] = Field(
        ...,
        description="Number of stools on day 3 of treatment. Count total number of bowel movements "
                    "in the 24-hour period of day 3 of inpatient treatment for acute severe "
                    "ulcerative colitis. Include all bowel movements regardless of consistency.",
        example="3_to_8"
    )
    
    crp_elevated: Literal["yes", "no"] = Field(
        ...,
        description="Whether C-reactive protein (CRP) is >45 mg/L (>428 nmol/L) on day 3 of treatment. "
                    "CRP should be measured on the morning of day 3. The threshold of 45 mg/L was "
                    "determined from the original derivation cohort as the optimal cutoff for "
                    "predicting colectomy.",
        example="yes"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "stool_frequency": "3_to_8",
                "crp_elevated": "yes"
            }
        }


class TravisCriteriaResponse(BaseModel):
    """
    Response model for Travis Criteria
    
    Returns the risk category (low or high) for needing colectomy with appropriate 
    clinical interpretation and management recommendations. High-risk patients should 
    be considered for early surgical consultation and intensification of medical therapy 
    or second-line treatments.
    
    Management recommendations:
    - Low risk: Continue current medical therapy with close monitoring
    - High risk: Consider surgical consultation, intensify therapy, or initiate rescue therapy
    
    Reference: Travis SP, et al. Gut. 1996;38(6):905-10.
    """
    
    result: str = Field(
        ...,
        description="Risk category for needing colectomy (low or high)",
        example="high"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement (empty for categorical result)",
        example=""
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and management recommendations based on risk category",
        example="Patient has high risk of needing colectomy. Consider early surgical consultation and other therapies including surgery. Intensify medical therapy or consider second-line treatments (cyclosporine, infliximab) if not already initiated."
    )
    
    stage: str = Field(
        ...,
        description="Risk classification (Low Risk or High Risk)",
        example="High Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="High risk of needing colectomy"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "high",
                "unit": "",
                "interpretation": "Patient has high risk of needing colectomy. Consider early surgical consultation and other therapies including surgery. Intensify medical therapy or consider second-line treatments (cyclosporine, infliximab) if not already initiated.",
                "stage": "High Risk",
                "stage_description": "High risk of needing colectomy"
            }
        }