"""
MuLBSTA Score for Viral Pneumonia Mortality Models

Request and response models for MuLBSTA Score calculation.

References (Vancouver style):
1. Guo L, Wei D, Zhang X, Wu Y, Li Q, Zhou M, et al. Clinical Features Predicting 
   Mortality Risk in Patients With Viral Pneumonia: The MuLBSTA Score. Front Microbiol. 
   2019;10:2752. doi: 10.3389/fmicb.2019.02752.
2. Chen N, Zhou M, Dong X, Qu J, Gong F, Han Y, et al. Epidemiological and clinical 
   characteristics of 99 cases of 2019 novel coronavirus pneumonia in Wuhan, China: 
   a descriptive study. Lancet. 2020;395(10223):507-513. doi: 10.1016/S0140-6736(20)30211-7.
3. Fan G, Tu C, Zhou F, Liu Z, Wang Y, Song B, et al. Comparison of severity scores 
   for COVID-19 patients with pneumonia: a retrospective study. Eur Respir J. 
   2020;56(3):2002113. doi: 10.1183/13993003.02113-2020.

The MuLBSTA Score is a clinical prediction tool designed to predict 90-day mortality 
in patients with viral pneumonia. It incorporates six clinical and laboratory 
parameters and has been validated for various viral pneumonias including influenza 
and COVID-19.
"""

from pydantic import BaseModel, Field
from typing import Literal


class MulbstaScoreRequest(BaseModel):
    """
    Request model for MuLBSTA Score for Viral Pneumonia Mortality
    
    The MuLBSTA Score uses 6 clinical parameters to predict 90-day mortality risk:
    
    MuLBSTA Components and Scoring:
    - **Mu**ltilobar infiltrates (5 points): ≥2 lobes involved on chest imaging
    - **L**ymphopenia (4 points): Lymphocyte count ≤0.8 × 10⁹/L
    - **B**acterial coinfection (4 points): Clinical/laboratory/microbiologic evidence
    - **S**moking history (3 points): Current or former smoking
    - Hyper**T**ension (2 points): Medical history or current treatment
    - **A**ge ≥60 years (2 points): Elderly risk factor
    
    Score Interpretation:
    - 0-5 points: Low risk (0-1.7% 90-day mortality)
    - 6-11 points: Moderate risk (7.3-26.7% 90-day mortality)
    - 12+ points: High risk (42.9% 90-day mortality)
    
    Clinical Applications:
    - Risk stratification for viral pneumonia patients
    - Treatment intensity guidance
    - Resource allocation decisions
    - Early identification of high-risk patients
    - Prognostic counseling for patients and families
    
    Validation:
    - Originally developed for influenza and viral pneumonia
    - Successfully applied to COVID-19 patients
    - Good discriminative ability across different viral pathogens
    - Useful in resource-limited settings
    - Helps guide ICU admission decisions

    References (Vancouver style):
    1. Guo L, Wei D, Zhang X, Wu Y, Li Q, Zhou M, et al. Clinical Features Predicting 
    Mortality Risk in Patients With Viral Pneumonia: The MuLBSTA Score. Front Microbiol. 
    2019;10:2752. doi: 10.3389/fmicb.2019.02752.
    2. Chen N, Zhou M, Dong X, Qu J, Gong F, Han Y, et al. Epidemiological and clinical 
    characteristics of 99 cases of 2019 novel coronavirus pneumonia in Wuhan, China: 
    a descriptive study. Lancet. 2020;395(10223):507-513. doi: 10.1016/S0140-6736(20)30211-7.
    3. Fan G, Tu C, Zhou F, Liu Z, Wang Y, Song B, et al. Comparison of severity scores 
    for COVID-19 patients with pneumonia: a retrospective study. Eur Respir J. 
    2020;56(3):2002113. doi: 10.1183/13993003.02113-2020.
    """
    
    multilobar_infiltrates: Literal["yes", "no"] = Field(
        ...,
        description="Multilobar infiltrates on chest imaging (≥2 lobes involved). Worth 5 points if present. Assess via chest X-ray or CT scan",
        example="no"
    )
    
    lymphopenia: Literal["yes", "no"] = Field(
        ...,
        description="Lymphopenia defined as lymphocyte count ≤0.8 × 10⁹/L (800/μL). Worth 4 points if present. Check complete blood count",
        example="yes"
    )
    
    bacterial_coinfection: Literal["yes", "no"] = Field(
        ...,
        description="Bacterial coinfection based on clinical, laboratory, or microbiologic evidence. Worth 4 points if present. Consider sputum culture, blood culture, procalcitonin",
        example="no"
    )
    
    smoking_history: Literal["yes", "no"] = Field(
        ...,
        description="Current or former smoking history. Worth 3 points if present. Include any significant tobacco use history",
        example="yes"
    )
    
    hypertension: Literal["yes", "no"] = Field(
        ...,
        description="History of hypertension or current antihypertensive treatment. Worth 2 points if present. Based on medical history or current medications",
        example="yes"
    )
    
    age_60_or_older: Literal["yes", "no"] = Field(
        ...,
        description="Age 60 years or older. Worth 2 points if present. Elderly risk factor for poor outcomes in viral pneumonia",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "multilobar_infiltrates": "no",
                "lymphopenia": "yes",
                "bacterial_coinfection": "no",
                "smoking_history": "yes",
                "hypertension": "yes",
                "age_60_or_older": "no"
            }
        }


class MulbstaScoreResponse(BaseModel):
    """
    Response model for MuLBSTA Score for Viral Pneumonia Mortality
    
    The MuLBSTA Score ranges from 0-20 points theoretically, but practical maximum 
    observed is 12 points. It predicts 90-day mortality risk in viral pneumonia:
    
    Risk Categories:
    - Low Risk (0-5 points): 0-1.7% 90-day mortality
    - Moderate Risk (6-11 points): 7.3-26.7% 90-day mortality  
    - High Risk (12+ points): 42.9% 90-day mortality
    
    Clinical Management by Risk Level:
    
    Low Risk (0-5 points):
    - Standard supportive care and monitoring
    - Outpatient management may be appropriate for stable patients
    - Routine pneumonia care protocols
    - Regular monitoring for deterioration
    
    Moderate Risk (6-11 points):
    - Enhanced monitoring and potentially more aggressive care
    - Consider hospitalization for closer observation
    - Frequent vital signs and serial laboratory assessments
    - Monitor for respiratory failure and secondary infections
    - Consider ICU consultation if deterioration occurs
    
    High Risk (12+ points):
    - Intensive monitoring and aggressive treatment
    - ICU admission strongly recommended
    - Mechanical ventilation if indicated
    - Broad-spectrum antibiotics for bacterial coinfection
    - Continuous monitoring for multi-organ dysfunction
    - Early involvement of critical care specialists
    
    Prognostic Value:
    - Helps identify patients at highest risk for poor outcomes
    - Guides resource allocation and treatment intensity
    - Useful for family counseling and goals of care discussions
    - Validated across multiple viral pneumonia types including COVID-19
    - Particularly valuable in resource-constrained settings
    
    Reference: Guo L, et al. Front Microbiol. 2019;10:2752.
    """
    
    result: int = Field(
        ...,
        description="MuLBSTA score calculated from clinical parameters (range: 0-20 points, practical maximum 12)",
        example=9
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and mortality risk assessment with management recommendations",
        example="MuLBSTA Score 9: Moderate risk of 90-day mortality (approximately 7.3-26.7%). This score indicates intermediate risk requiring enhanced monitoring and potentially more aggressive supportive care. Consider hospitalization for closer observation, frequent vital sign monitoring, and serial laboratory assessments."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, Moderate Risk, High Risk)",
        example="Moderate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the mortality risk level",
        example="Moderate risk of 90-day mortality"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 9,
                "unit": "points",
                "interpretation": "MuLBSTA Score 9: Moderate risk of 90-day mortality (approximately 7.3-26.7%). This score indicates intermediate risk requiring enhanced monitoring and potentially more aggressive supportive care. Consider hospitalization for closer observation, frequent vital sign monitoring, and serial laboratory assessments.",
                "stage": "Moderate Risk",
                "stage_description": "Moderate risk of 90-day mortality"
            }
        }