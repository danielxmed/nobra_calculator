"""
GAP Index for Idiopathic Pulmonary Fibrosis (IPF) Mortality Models

Request and response models for GAP Index IPF mortality prediction.

References (Vancouver style):
1. Ley B, Ryerson CJ, Vittinghoff E, et al. A multidimensional index and staging system 
   for idiopathic pulmonary fibrosis. Ann Intern Med. 2012;156(10):684-91. 
   doi: 10.7326/0003-4819-156-10-201205150-00004.
2. Ryerson CJ, Vittinghoff E, Ley B, et al. Predicting survival across chronic interstitial 
   lung disease: the ILD-GAP model. Chest. 2014;145(4):723-8. doi: 10.1378/chest.13-1474.
3. Paterniti MO, Bi Y, Rekić D, et al. Acute Exacerbation and Decline in Forced Vital 
   Capacity Are Associated with Increased Mortality in Idiopathic Pulmonary Fibrosis. 
   Ann Am Thorac Soc. 2017;14(9):1395-1402. doi: 10.1513/AnnalsATS.201606-458OC.

The GAP Index is a validated prognostic scoring system for idiopathic pulmonary fibrosis 
that uses Gender, Age, and Physiology (FVC and DLCO) to predict 1-, 2-, and 3-year 
mortality risk. This tool enables clinicians to stratify patients into three risk 
categories for optimal management planning.

Clinical Applications:
- IPF prognosis and mortality risk stratification
- Lung transplant evaluation timing and prioritization
- Clinical trial stratification and patient selection
- Treatment planning and monitoring frequency determination
- Patient counseling and advance care planning discussions

Scoring Components:
- Gender: Female (0 points), Male (1 point)
- Age: ≤60y (0), 61-65y (1), >65y (2 points)
- FVC % predicted: >75% (0), 50-75% (1), <50% (2 points)
- DLCO % predicted: >55% (0), 36-55% (1), ≤35% (2), Cannot perform (3 points)

Stage Classification:
- Stage I (0-3 points): Low mortality risk, monitor every 6 months
- Stage II (4-5 points): Intermediate risk, monitor every 3-6 months
- Stage III (6-8 points): High mortality risk, monitor every 3 months
"""

from pydantic import BaseModel, Field, validator
from typing import Literal, Optional


class GapIndexIpfMortalityRequest(BaseModel):
    """
    Request model for GAP Index IPF Mortality Assessment
    
    The GAP Index predicts mortality risk in patients with idiopathic pulmonary fibrosis 
    using four clinical variables. This validated tool helps guide management decisions, 
    transplant evaluation timing, and patient counseling.
    
    **CLINICAL INDICATIONS**:
    - Confirmed diagnosis of idiopathic pulmonary fibrosis (IPF)
    - Prognosis assessment and risk stratification
    - Lung transplant evaluation and timing decisions
    - Clinical trial enrollment and stratification
    - Treatment planning and monitoring frequency determination
    
    **PARAMETER INTERPRETATION GUIDE**:
    
    **1. Gender**:
    - **Male patients** have higher mortality risk in IPF (1 point)
    - **Female patients** have lower mortality risk (0 points)
    - **Clinical Context**: Male gender is an independent risk factor for poor prognosis in IPF
    
    **2. Age Categories**:
    - **≤60 years** (0 points): Younger patients with better prognosis
    - **61-65 years** (1 point): Intermediate age group
    - **>65 years** (2 points): Older patients with higher mortality risk
    - **Clinical Context**: Age is a strong predictor of survival in IPF
    
    **3. FVC (Forced Vital Capacity) % Predicted**:
    - **>75%** (0 points): Preserved lung volume, better prognosis
    - **50-75%** (1 point): Moderate impairment
    - **<50%** (2 points): Severe impairment, worse prognosis
    - **Measurement Requirements**: 
      - Recent spirometry (within 6 months preferred)
      - Post-bronchodilator values when available
      - Quality-assured testing per ATS/ERS standards
    
    **4. DLCO (Diffusing Capacity) % Predicted**:
    - **>55%** (0 points): Preserved gas exchange
    - **36-55%** (1 point): Moderate impairment
    - **≤35%** (2 points): Severe impairment
    - **Cannot perform test** (3 points): Most severe category
    - **Measurement Considerations**:
      - Corrected for hemoglobin when available
      - Single-breath technique preferred
      - Use null/empty if patient cannot perform test
    
    **GAP STAGING AND CLINICAL MANAGEMENT**:
    
    **Stage I (0-3 points) - Low Mortality Risk**:
    - **Monitoring**: Every 6 months
    - **Management Focus**: 
      - Aggressive symptom management
      - Treatment of comorbid conditions
      - Pulmonary rehabilitation
      - Antifibrotic therapy consideration
    - **Transplant**: May not require immediate listing
    - **Prognosis**: Better long-term survival expected
    
    **Stage II (4-5 points) - Intermediate Mortality Risk**:
    - **Monitoring**: Every 3-6 months
    - **Management Focus**:
      - Consider lung transplant evaluation
      - Optimize medical management
      - Antifibrotic therapy strongly recommended
      - Pulmonary rehabilitation and oxygen therapy
    - **Counseling**: Discussion of prognosis and advance care planning
    
    **Stage III (6-8 points) - High Mortality Risk**:
    - **Monitoring**: Every 3 months or more frequently
    - **Management Focus**:
      - Urgent lung transplant evaluation if appropriate
      - Palliative care consultation
      - Aggressive symptom management
      - Oxygen therapy optimization
    - **Advance Planning**: Essential discussions about end-of-life care
    
    **CLINICAL DECISION SUPPORT**:
    
    **Lung Transplant Evaluation Timing**:
    - **Stage I**: May defer evaluation, monitor closely
    - **Stage II**: Consider evaluation, especially if declining
    - **Stage III**: Urgent evaluation if transplant candidate
    
    **Antifibrotic Therapy Considerations**:
    - **All Stages**: Consider nintedanib or pirfenidone
    - **Stage II-III**: Strongly recommended unless contraindicated
    - **Monitor**: Disease progression, side effects, quality of life
    
    **Monitoring Frequency Rationale**:
    - **Higher GAP scores**: More frequent monitoring due to higher risk
    - **Assess**: FVC decline rate, symptoms, functional status
    - **Imaging**: High-resolution CT for progression assessment
    
    References (Vancouver style):
    1. Ley B, Ryerson CJ, Vittinghoff E, et al. A multidimensional index and staging system 
       for idiopathic pulmonary fibrosis. Ann Intern Med. 2012;156(10):684-91.
    2. Ryerson CJ, Vittinghoff E, Ley B, et al. Predicting survival across chronic interstitial 
       lung disease: the ILD-GAP model. Chest. 2014;145(4):723-8.
    3. Paterniti MO, Bi Y, Rekić D, et al. Acute Exacerbation and Decline in Forced Vital 
       Capacity Are Associated with Increased Mortality in Idiopathic Pulmonary Fibrosis. 
       Ann Am Thorac Soc. 2017;14(9):1395-1402.
    """
    
    gender: Literal["male", "female"] = Field(
        ...,
        description="Patient's gender. Male patients have higher mortality risk in IPF",
        example="male"
    )
    
    age: int = Field(
        ...,
        description="Patient's age in years. Older age associated with worse prognosis",
        ge=18,
        le=100,
        example=67
    )
    
    fvc_percent_predicted: float = Field(
        ...,
        description="Forced Vital Capacity as percentage of predicted normal value. Lower values indicate worse prognosis",
        ge=10,
        le=150,
        example=65.5
    )
    
    dlco_percent_predicted: Optional[float] = Field(
        None,
        description="Diffusing capacity for CO as percentage of predicted. Use null if patient cannot perform test (scores 3 points)",
        ge=5,
        le=150,
        example=42.3
    )
    
    class Config:
        schema_extra = {
            "example": {
                "gender": "male",
                "age": 67,
                "fvc_percent_predicted": 65.5,
                "dlco_percent_predicted": 42.3
            }
        }


class GapIndexIpfMortalityResponse(BaseModel):
    """
    Response model for GAP Index IPF Mortality Assessment
    
    The response provides the calculated GAP score (0-8 points) with stage classification 
    and comprehensive clinical management recommendations based on validated mortality 
    risk stratification.
    
    **CLINICAL INTERPRETATION FRAMEWORK**:
    
    **GAP Score Interpretation**:
    - **Total Score Range**: 0-8 points
    - **Risk Stratification**: Higher scores indicate higher mortality risk
    - **Validation**: Based on 558 IPF patients from three academic centers
    - **Applicability**: Can be used at presentation and during follow-up
    
    **Stage-Based Management Protocols**:
    
    **GAP Stage I (0-3 points) - Low Mortality Risk**:
    - **Estimated Survival**: Better long-term prognosis
    - **Clinical Management**:
      - **Monitoring Frequency**: Every 6 months
      - **Primary Focus**: Symptom management and quality of life
      - **Comorbidity Management**: Aggressive treatment of GERD, OSA, PH
      - **Pulmonary Rehabilitation**: Strongly recommended
      - **Antifibrotic Therapy**: Consider based on progression risk
      - **Transplant Evaluation**: May defer unless rapid progression
    
    **GAP Stage II (4-5 points) - Intermediate Mortality Risk**:
    - **Estimated Survival**: Intermediate prognosis with variable outcomes
    - **Clinical Management**:
      - **Monitoring Frequency**: Every 3-6 months
      - **Transplant Evaluation**: Consider evaluation process
      - **Antifibrotic Therapy**: Strongly recommended
      - **Advanced Planning**: Begin prognostic discussions
      - **Specialist Care**: Regular pulmonologist follow-up
      - **Functional Assessment**: 6-minute walk test, oxygen needs
    
    **GAP Stage III (6-8 points) - High Mortality Risk**:
    - **Estimated Survival**: Poor prognosis, higher short-term mortality
    - **Clinical Management**:
      - **Monitoring Frequency**: Every 3 months or more frequently
      - **Urgent Actions**: Immediate transplant evaluation if appropriate
      - **Palliative Care**: Early consultation recommended
      - **Symptom Management**: Aggressive approach to dyspnea, cough
      - **Family Support**: Involve family in care planning
      - **End-of-Life Planning**: Advance directive discussions
    
    **TREATMENT CONSIDERATIONS BY STAGE**:
    
    **Antifibrotic Therapy Guidelines**:
    - **Stage I**: Consider if evidence of progression
    - **Stage II**: Recommended unless contraindicated
    - **Stage III**: Strongly recommended, monitor closely for benefits/risks
    - **Options**: Nintedanib or pirfenidone per guidelines
    
    **Lung Transplant Evaluation Criteria**:
    - **Age**: Generally <70 years for single lung, <65 for bilateral
    - **Functional Status**: Adequate rehabilitation potential
    - **Comorbidities**: Absence of significant contraindications
    - **Stage II-III**: Consider evaluation, especially with decline
    
    **Monitoring Parameters by Stage**:
    
    **All Stages Monitor**:
    - **Pulmonary Function**: FVC, DLCO every 3-6 months
    - **Functional Status**: 6-minute walk test, oxygen requirements
    - **Symptoms**: Dyspnea scales, cough assessment, quality of life
    - **Imaging**: HRCT for progression assessment
    
    **Stage III Additional Monitoring**:
    - **More Frequent PFTs**: Consider monthly if declining
    - **Hospitalization Risk**: Monitor for acute exacerbations
    - **Functional Decline**: Weekly symptom assessment
    - **Family Preparation**: Regular caregiver support
    
    **QUALITY OF LIFE INTERVENTIONS**:
    
    **All Stages**:
    - **Pulmonary Rehabilitation**: Exercise training, education
    - **Oxygen Therapy**: As needed for hypoxemia or exercise
    - **Cough Management**: Antitussives, avoid ACE inhibitors
    - **GERD Treatment**: PPI therapy for most patients
    - **Sleep Disorders**: Screen and treat sleep apnea
    
    **Advanced Stages (II-III)**:
    - **Opioid Therapy**: For refractory dyspnea
    - **Anxiety Management**: Counseling, medications as appropriate
    - **Social Support**: Connect with IPF support groups
    - **Home Services**: Consider home health, hospice referral
    
    **PROGNOSIS COMMUNICATION**:
    - **Stage I**: Emphasize variable course, importance of monitoring
    - **Stage II**: Discuss progression risk, treatment options
    - **Stage III**: Honest discussion of prognosis, focus on comfort
    - **All Stages**: Hope for new treatments, clinical trials
    
    Reference: Ley B, et al. Ann Intern Med. 2012;156(10):684-91.
    """
    
    result: int = Field(
        ...,
        description="GAP score calculated from gender, age, and physiology parameters (0-8 points)",
        ge=0,
        le=8,
        example=5
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for GAP score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation with stage-specific management recommendations",
        example="GAP score of 5 indicates intermediate mortality risk. Close monitoring every 3-6 months for evidence of disease progression. Consider lung transplant evaluation if appropriate candidate. Optimize medical management including antifibrotic therapy. Pulmonary rehabilitation and oxygen therapy as needed. Discussion of prognosis and advance care planning recommended."
    )
    
    stage: str = Field(
        ...,
        description="GAP stage classification (GAP Stage I, GAP Stage II, GAP Stage III)",
        example="GAP Stage II"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the mortality risk level",
        example="Intermediate mortality risk"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 5,
                "unit": "points",
                "interpretation": "GAP score of 5 indicates intermediate mortality risk. Close monitoring every 3-6 months for evidence of disease progression. Consider lung transplant evaluation if appropriate candidate. Optimize medical management including antifibrotic therapy. Pulmonary rehabilitation and oxygen therapy as needed. Discussion of prognosis and advance care planning recommended.",
                "stage": "GAP Stage II",
                "stage_description": "Intermediate mortality risk"
            }
        }