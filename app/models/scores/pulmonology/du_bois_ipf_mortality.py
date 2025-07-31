"""
du Bois Score for Idiopathic Pulmonary Fibrosis (IPF) Mortality Models

Request and response models for du Bois IPF mortality prediction.

References (Vancouver style):
1. du Bois RM, Weycker D, Albera C, Bradford WZ, Costabel U, Kartashov A, et al. 
   Ascertainment of individual risk of mortality for patients with idiopathic pulmonary 
   fibrosis. Am J Respir Crit Care Med. 2011;184(4):459-66. doi: 10.1164/rccm.201011-1790OC.
2. Ley B, Ryerson CJ, Vittinghoff E, Ryu JH, Tomassetti S, Lee JS, et al. A multidimensional 
   index and staging system for idiopathic pulmonary fibrosis. Ann Intern Med. 
   2012;156(10):684-91. doi: 10.7326/0003-4819-156-10-201205150-00004.
3. Raghu G, Collard HR, Egan JJ, Martinez FJ, Behr J, Brown KK, et al. An official 
   ATS/ERS/JRS/ALAT statement: idiopathic pulmonary fibrosis: evidence-based guidelines 
   for diagnosis and management. Am J Respir Crit Care Med. 2011;183(6):788-824. 
   doi: 10.1164/rccm.2009-040GL.

The du Bois Score predicts 1-year mortality risk in patients with idiopathic pulmonary 
fibrosis using four readily ascertainable clinical predictors: age, recent respiratory 
hospitalization, FVC % predicted, and FVC decline over 24 weeks. The score was developed 
from data of 1,099 IPF patients from two clinical trials and provides a practical tool 
for determining prognosis and guiding clinical management.
"""

from pydantic import BaseModel, Field
from typing import Literal


class DuBoisIpfMortalityRequest(BaseModel):
    """
    Request model for du Bois Score for Idiopathic Pulmonary Fibrosis (IPF) Mortality
    
    The du Bois Score uses four clinical predictors to assess 1-year mortality risk in IPF:
    
    Age Scoring:
    - ≤50 years: 0 points
    - 51-60 years: 1 point
    - 61-70 years: 2 points
    - >70 years: 3 points
    
    Recent Respiratory Hospitalization (within 6 months):
    - Yes: 2 points
    - No: 0 points
    
    Forced Vital Capacity (FVC) % Predicted:
    - >65%: 0 points
    - 50-65%: 1 point
    - <50%: 2 points
    
    FVC Decline over 24 weeks:
    - Decline >10% (absolute % predicted): 3 points
    - Decline ≤10%: 0 points
    
    Total Score Interpretation:
    - 0-4 points: Low risk of 1-year mortality
    - 5-8 points: Intermediate risk of 1-year mortality
    - 9-10 points: High risk of 1-year mortality
    
    Clinical Applications:
    - Prognosis assessment and patient counseling
    - Treatment planning and monitoring frequency decisions
    - Lung transplantation evaluation timing
    - Advance care planning discussions
    - Clinical trial stratification

    References (Vancouver style):
    1. du Bois RM, Weycker D, Albera C, Bradford WZ, Costabel U, Kartashov A, et al. 
       Ascertainment of individual risk of mortality for patients with idiopathic pulmonary 
       fibrosis. Am J Respir Crit Care Med. 2011;184(4):459-66. doi: 10.1164/rccm.201011-1790OC.
    2. Ley B, Ryerson CJ, Vittinghoff E, Ryu JH, Tomassetti S, Lee JS, et al. A multidimensional 
       index and staging system for idiopathic pulmonary fibrosis. Ann Intern Med. 
       2012;156(10):684-91. doi: 10.7326/0003-4819-156-10-201205150-00004.
    3. Raghu G, Collard HR, Egan JJ, Martinez FJ, Behr J, Brown KK, et al. An official 
       ATS/ERS/JRS/ALAT statement: idiopathic pulmonary fibrosis: evidence-based guidelines 
       for diagnosis and management. Am J Respir Crit Care Med. 2011;183(6):788-824.
    """
    
    age: int = Field(
        ...,
        description="Patient age in years. Scoring: ≤50 years (0 pts), 51-60 years (1 pt), 61-70 years (2 pts), >70 years (3 pts)",
        ge=18,
        le=120,
        example=65
    )
    
    respiratory_hospitalization: Literal["yes", "no"] = Field(
        ...,
        description="History of respiratory hospitalization within the past 6 months. Scoring: Yes (2 pts), No (0 pts)",
        example="no"
    )
    
    fvc_percent_predicted: float = Field(
        ...,
        description="Forced vital capacity (FVC) as percentage of predicted value. Scoring: >65% (0 pts), 50-65% (1 pt), <50% (2 pts)",
        ge=10.0,
        le=150.0,
        example=55.5
    )
    
    change_fvc_24_weeks: float = Field(
        ...,
        description="Change in FVC over 24 weeks (absolute change in % predicted). Scoring: Decline >10% absolute (3 pts), Decline ≤10% (0 pts). Negative values indicate decline",
        ge=-50.0,
        le=50.0,
        example=-5.2
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "age": 65,
                "respiratory_hospitalization": "no",
                "fvc_percent_predicted": 55.5,
                "change_fvc_24_weeks": -5.2
            }
        }


class DuBoisIpfMortalityResponse(BaseModel):
    """
    Response model for du Bois Score for Idiopathic Pulmonary Fibrosis (IPF) Mortality
    
    The du Bois Score ranges from 0-10 points and stratifies IPF patients into risk categories:
    
    Risk Categories:
    - Low Risk (0-4 points): Low 1-year mortality risk
      * Continue standard monitoring and treatment
      * Regular follow-up with pulmonary function tests
      * Standard clinical assessment intervals
    
    - Intermediate Risk (5-8 points): Intermediate 1-year mortality risk
      * Consider more frequent monitoring
      * Optimization of antifibrotic therapy
      * Evaluation for lung transplantation if appropriate
      * Discuss prognosis and advance care planning
    
    - High Risk (9-10 points): High 1-year mortality risk
      * Urgent consideration for lung transplantation evaluation
      * Optimize supportive care measures
      * Consider palliative care consultation
      * Discuss advance directives and goals of care
      * Close monitoring required
    
    Clinical Implications:
    - Higher scores correlate with increased 1-year mortality risk
    - Should be used with clinical judgment and other prognostic factors
    - Useful for treatment planning and patient counseling
    - Aids in timing of lung transplantation evaluation
    - Supports advance care planning discussions
    
    Important Considerations:
    - Score developed from clinical trial data (n=1,099 IPF patients)
    - Validates the use of readily available clinical parameters
    - Should complement comprehensive clinical assessment
    - Regular monitoring of pulmonary function is essential
    - Consider individual patient factors beyond the score
    
    Reference: du Bois RM, et al. Am J Respir Crit Care Med. 2011;184(4):459-66.
    """
    
    result: int = Field(
        ...,
        description="du Bois mortality risk score for IPF patients (0-10 points)",
        example=3
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and management recommendations based on risk category",
        example="Low risk of 1-year mortality in IPF. Continue standard monitoring and treatment. Regular follow-up with pulmonary function tests and clinical assessment recommended."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, Intermediate Risk, High Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Low 1-year mortality risk"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 3,
                "unit": "points",
                "interpretation": "Low risk of 1-year mortality in IPF. Continue standard monitoring and treatment. Regular follow-up with pulmonary function tests and clinical assessment recommended.",
                "stage": "Low Risk",
                "stage_description": "Low 1-year mortality risk"
            }
        }