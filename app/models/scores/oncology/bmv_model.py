"""
Brain Metastasis Velocity (BMV) Model Models

Request and response models for BMV Model calculation.

References (Vancouver style):
1. Farris M, McTyre ER, Cramer CK, Hughes R, Randolph DM 2nd, Ayala-Peacock DN, et al. 
   Brain Metastasis Velocity: A Novel Prognostic Metric Predictive of Overall Survival 
   and Freedom From Whole-Brain Radiation Therapy After Distant Brain Failure Following 
   Upfront Radiosurgery Alone. Int J Radiat Oncol Biol Phys. 2017 May 1;98(1):131-141. 
   doi: 10.1016/j.ijrobp.2017.01.201.
2. Yamamoto M, Aiyama H, Koiso T, Watanabe S, Kawabe T, Sato Y, et al. Validity of a 
   Recently Proposed Prognostic Grading Index, Brain Metastasis Velocity, for Patients 
   With Brain Metastasis Undergoing Multiple Radiosurgical Procedures. Int J Radiat 
   Oncol Biol Phys. 2019 Mar 15;103(3):631-637. doi: 10.1016/j.ijrobp.2018.10.036.

The Brain Metastasis Velocity (BMV) is a prognostic metric that calculates the rate 
of new brain metastases development after initial stereotactic radiosurgery (SRS). 
It is defined as the number of new brain metastases divided by the time interval 
(in years) since initial SRS. BMV correlates with overall survival and helps guide 
treatment decisions between localized therapy (SRS) and whole brain radiation therapy.
"""

from pydantic import BaseModel, Field, validator
from typing import Union


class BmvModelRequest(BaseModel):
    """
    Request model for Brain Metastasis Velocity (BMV) Model
    
    The BMV Model calculates the rate of distant brain failure after stereotactic 
    radiosurgery (SRS) to predict overall survival. It requires two parameters:
    
    1. Number of new brain metastases: Count of new lesions since initial SRS
       - Must be at least 1 (as BMV is calculated when new metastases appear)
       - Maximum reasonable value set at 100 for practical purposes
    
    2. Time interval: Years between initial SRS and new metastases appearance
       - Minimum 0.01 years (~3.6 days) to avoid division issues
       - Maximum 10 years for clinical relevance
    
    BMV = Number of new metastases / Time interval (years)
    
    Risk Stratification:
    - Low BMV (<4): Median OS 12.4 months, consider localized therapy
    - Intermediate BMV (4-13): Median OS 8.2 months, individualized approach
    - High BMV (>13): Median OS 4.3 months, consider whole brain RT
    
    References:
    1. Farris M, et al. Int J Radiat Oncol Biol Phys. 2017;98(1):131-141.
    2. Yamamoto M, et al. Int J Radiat Oncol Biol Phys. 2019;103(3):631-637.
    """
    
    new_metastases: int = Field(
        ...,
        ge=1,
        le=100,
        description="Number of new brain metastases since initial stereotactic radiosurgery (SRS). Must be at least 1, as BMV is calculated when distant brain failure occurs",
        example=6
    )
    
    time_interval: float = Field(
        ...,
        gt=0,
        le=10,
        description="Time interval between initial SRS and appearance of new brain metastases, in years. Minimum 0.01 years (~3.6 days), maximum 10 years",
        example=0.5
    )
    
    @validator('time_interval')
    def validate_time_interval(cls, v):
        """Ensures time interval is reasonable"""
        if v < 0.01:
            raise ValueError("Time interval must be at least 0.01 years (~3.6 days)")
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "new_metastases": 6,
                "time_interval": 0.5
            }
        }


class BmvModelResponse(BaseModel):
    """
    Response model for Brain Metastasis Velocity (BMV) Model
    
    The BMV stratifies patients into three risk categories based on the rate of 
    new brain metastases development:
    
    - Low BMV (<4 metastases/year): Better prognosis, median OS 12.4 months
    - Intermediate BMV (4-13 metastases/year): Moderate prognosis, median OS 8.2 months
    - High BMV (>13 metastases/year): Poor prognosis, median OS 4.3 months
    
    The BMV helps guide treatment decisions between repeat SRS for low BMV patients 
    versus whole brain radiation therapy for high BMV patients. Treatment decisions 
    should also consider tumor histology and extracranial disease control.
    
    Reference: Farris M, et al. Int J Radiat Oncol Biol Phys. 2017;98(1):131-141.
    """
    
    result: float = Field(
        ...,
        ge=0,
        description="Brain metastasis velocity in metastases per year (calculated as new metastases / time interval)",
        example=12.0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for BMV",
        example="metastases/year"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with median survival and treatment recommendations based on BMV category",
        example="Intermediate BMV (4-13 metastases/year). Median overall survival: 8.2 months. Consider patient factors including performance status, systemic disease control, and tumor histology when deciding between localized vs. whole brain radiation therapy."
    )
    
    stage: str = Field(
        ...,
        description="BMV risk category (Low BMV, Intermediate BMV, or High BMV)",
        example="Intermediate BMV"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the BMV category",
        example="Intermediate brain metastasis velocity"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 12.0,
                "unit": "metastases/year",
                "interpretation": "Intermediate BMV (4-13 metastases/year). Median overall survival: 8.2 months. Consider patient factors including performance status, systemic disease control, and tumor histology when deciding between localized vs. whole brain radiation therapy.",
                "stage": "Intermediate BMV",
                "stage_description": "Intermediate brain metastasis velocity"
            }
        }