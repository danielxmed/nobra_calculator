"""
Global Initiative for Obstructive Lung Disease (GOLD) Criteria for COPD Models

Request and response models for GOLD COPD Criteria calculation.

References (Vancouver style):
1. Global Initiative for Chronic Obstructive Lung Disease. Global Strategy for the 
   Diagnosis, Management, and Prevention of Chronic Obstructive Pulmonary Disease, 
   2025 Report. Available from: https://goldcopd.org/
2. Singh SJ, Augustin IML, Correia de Sousa R, et al. An official systematic review 
   of the European Respiratory Society/American Thoracic Society: measurement 
   properties of field walking tests in chronic respiratory disease. Eur Respir J. 
   2014;44(6):1447-1478. doi: 10.1183/09031936.00150414.
3. Jones PW, Harding G, Berry P, et al. Development and first validation of the 
   COPD Assessment Test. Eur Respir J. 2009;34(3):648-654. 
   doi: 10.1183/09031936.00102509.
4. Bestall JC, Paul EA, Garrod R, et al. Usefulness of the Medical Research Council 
   (MRC) dyspnoea scale as a measure of disability in patients with chronic obstructive 
   pulmonary disease. Thorax. 1999;54(7):581-586. doi: 10.1136/thx.54.7.581.

The GOLD criteria provide a standardized framework for the diagnosis, assessment, and 
management of chronic obstructive pulmonary disease (COPD). The GOLD 2025 guidelines 
use a comprehensive approach combining:

1. **Spirometric Assessment**: Post-bronchodilator FEV1/FVC ratio <0.70 confirms COPD diagnosis
2. **Severity Staging**: FEV1 percentage predicted determines GOLD stages 1-4
3. **Symptom Assessment**: Modified Medical Research Council (mMRC) dyspnea scale or COPD Assessment Test (CAT)
4. **Exacerbation Risk**: History of exacerbations and hospitalizations

GOLD Spirometric Stages:
- GOLD 1 (Mild): FEV1 ≥80% predicted
- GOLD 2 (Moderate): FEV1 50-79% predicted  
- GOLD 3 (Severe): FEV1 30-49% predicted
- GOLD 4 (Very Severe): FEV1 <30% predicted

COPD Groups (ABE Classification):
- Group A: Low symptoms (mMRC 0-1, CAT <10), low exacerbation risk
- Group B: High symptoms (mMRC ≥2, CAT ≥10), low exacerbation risk
- Group E: High exacerbation risk (≥2 exacerbations OR ≥1 hospitalization)

Treatment follows the ABE framework:
- **Assessment**: Comprehensive evaluation of symptoms, lung function, and exacerbation risk
- **Bronchodilator**: Long-acting bronchodilators (LABA/LAMA) as cornerstone therapy
- **Exacerbation**: Prevention strategies including ICS based on phenotype and eosinophil count

The system emphasizes individualized treatment, smoking cessation, vaccination, 
pulmonary rehabilitation, and management of comorbidities.
"""

from pydantic import BaseModel, Field
from typing import Optional, Literal


class GoldCopdCriteriaRequest(BaseModel):
    """
    Request model for Global Initiative for Obstructive Lung Disease (GOLD) Criteria for COPD
    
    The GOLD criteria provide comprehensive assessment of COPD using multiple parameters:
    
    Spirometric Parameters:
    - FEV1 % predicted: Measures airflow obstruction severity and determines GOLD stage
    - FEV1/FVC ratio: Must be <0.70 post-bronchodilator to confirm COPD diagnosis
    
    Symptom Assessment Tools:
    - mMRC Dyspnea Scale (0-4): Assesses functional impairment from breathlessness
      * 0: Breathless only with strenuous exercise
      * 1: Short of breath when hurrying on level ground or walking up slight hill
      * 2: Walks slower than people of same age due to breathlessness
      * 3: Stops for breath after walking ~100 meters on level ground
      * 4: Too breathless to leave house or breathless when dressing
    - CAT Score (0-40): Alternative comprehensive symptom assessment (optional)
      * Covers cough, phlegm, chest tightness, breathlessness, activities, confidence, 
        sleep, and energy levels
      * Score ≥10 indicates significant symptom burden
    
    Exacerbation Risk Assessment:
    - Exacerbations: Episodes requiring oral corticosteroids and/or antibiotics
    - Hospitalizations: COPD-related admissions due to exacerbations
    - High risk defined as: ≥2 exacerbations OR ≥1 hospitalization in past year
    
    Clinical Applications:
    - Diagnosis confirmation (FEV1/FVC <0.70)
    - Severity staging (GOLD 1-4 based on FEV1% predicted)
    - Group classification (A, B, E) for treatment selection
    - Treatment escalation and monitoring guidance
    - Prognosis and disease progression assessment

    References (Vancouver style):
    1. Global Initiative for Chronic Obstructive Lung Disease. Global Strategy for the 
    Diagnosis, Management, and Prevention of Chronic Obstructive Pulmonary Disease, 
    2025 Report. Available from: https://goldcopd.org/
    2. Jones PW, Harding G, Berry P, et al. Development and first validation of the 
    COPD Assessment Test. Eur Respir J. 2009;34(3):648-654. 
    doi: 10.1183/09031936.00102509.
    3. Bestall JC, Paul EA, Garrod R, et al. Usefulness of the Medical Research Council 
    (MRC) dyspnoea scale as a measure of disability in patients with chronic obstructive 
    pulmonary disease. Thorax. 1999;54(7):581-586. doi: 10.1136/thx.54.7.581.
    """
    
    fev1_percent_predicted: float = Field(
        ...,
        description="Forced expiratory volume in 1 second (FEV1) as percentage of predicted normal value from post-bronchodilator spirometry. Determines GOLD severity stage: ≥80% (Stage 1), 50-79% (Stage 2), 30-49% (Stage 3), <30% (Stage 4)",
        ge=10.0,
        le=120.0,
        example=65.0
    )
    
    fvc_fev1_ratio: float = Field(
        ...,
        description="Post-bronchodilator FEV1/FVC ratio. Values <0.70 confirm airflow obstruction and COPD diagnosis according to GOLD criteria. Should be measured 15-20 minutes after bronchodilator administration",
        ge=0.30,
        le=1.00,
        example=0.65
    )
    
    dyspnea_mmrc: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Modified Medical Research Council (mMRC) Dyspnea Scale grade. Assesses functional impact of breathlessness: 0=breathless only with strenuous exercise; 1=short of breath when hurrying; 2=walks slower than same-age peers; 3=stops for breath after ~100m; 4=too breathless to leave house",
        example=2
    )
    
    exacerbations_last_year: int = Field(
        ...,
        description="Number of COPD exacerbations in the last 12 months requiring treatment with oral corticosteroids and/or antibiotics. Exacerbations are acute worsening of respiratory symptoms beyond normal day-to-day variation",
        ge=0,
        le=20,
        example=1
    )
    
    hospitalizations_last_year: int = Field(
        ...,
        description="Number of COPD-related hospitalizations in the last 12 months due to exacerbations. Indicates severe exacerbations requiring inpatient management. ≥1 hospitalization places patient in high exacerbation risk category",
        ge=0,
        le=10,
        example=0
    )
    
    cat_score: Optional[int] = Field(
        None,
        description="COPD Assessment Test (CAT) score (0-40 points). Alternative or complementary to mMRC for comprehensive symptom assessment. Evaluates cough, phlegm, chest tightness, breathlessness, activity limitation, confidence, sleep, and energy. Score ≥10 indicates significant symptom burden",
        ge=0,
        le=40,
        example=15
    )
    
    class Config:
        schema_extra = {
            "example": {
                "fev1_percent_predicted": 65.0,
                "fvc_fev1_ratio": 0.65,
                "dyspnea_mmrc": 2,
                "exacerbations_last_year": 1,
                "hospitalizations_last_year": 0,
                "cat_score": 15
            }
        }


class GoldCopdCriteriaResponse(BaseModel):
    """
    Response model for Global Initiative for Obstructive Lung Disease (GOLD) Criteria for COPD
    
    Provides comprehensive COPD classification including:
    
    GOLD Spirometric Stages:
    - GOLD 1 (Mild): FEV1 ≥80% predicted - mild airflow limitation
    - GOLD 2 (Moderate): FEV1 50-79% predicted - worsening airflow limitation  
    - GOLD 3 (Severe): FEV1 30-49% predicted - severe airflow limitation
    - GOLD 4 (Very Severe): FEV1 <30% predicted - very severe airflow limitation
    
    COPD Groups (for treatment selection):
    - Group A: Low symptoms (mMRC 0-1, CAT <10) + low exacerbation risk
    - Group B: High symptoms (mMRC ≥2, CAT ≥10) + low exacerbation risk
    - Group E: High exacerbation risk (≥2 exacerbations OR ≥1 hospitalization)
    
    Treatment Implications:
    - Group A: Short-acting bronchodilators as needed, focus on smoking cessation
    - Group B: Long-acting bronchodilators (LABA or LAMA), pulmonary rehabilitation
    - Group E: Combination LABA+LAMA, consider ICS based on eosinophils and phenotype
    
    The classification guides evidence-based treatment decisions, monitoring frequency,
    and prognosis assessment according to GOLD 2025 guidelines.
    
    Reference: Global Initiative for Chronic Obstructive Lung Disease. GOLD 2025 Report.
    """
    
    result: str = Field(
        ...,
        description="Complete GOLD COPD classification including severity stage and group assignment for treatment guidance",
        example="GOLD 2 - Moderate COPD, Group B"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the classification",
        example="classification"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including spirometry results, symptom assessment, exacerbation risk, group classification rationale, and detailed treatment recommendations based on GOLD 2025 guidelines",
        example="GOLD 2 - Moderate COPD, Group B. Post-bronchodilator spirometry: FEV1/FVC 0.65 (<0.70 confirms COPD), FEV1 65.0% predicted. Symptoms: mMRC 2 (Walks slower than people of same age due to breathlessness), CAT 15/40. Exacerbation history: 1 exacerbations, 0 hospitalizations in last year. Classification: High symptom burden, low exacerbation risk. Treatment recommendations: Long-acting bronchodilator (LABA or LAMA). If still breathless: LABA + LAMA combination. Regular long-acting bronchodilator therapy with pulmonary rehabilitation."
    )
    
    stage: str = Field(
        ...,
        description="GOLD classification stage and group with severity description",
        example="GOLD 2 - Moderate COPD, Group B"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the airflow limitation severity and group characteristics",
        example="Moderate airflow limitation, Group B"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "GOLD 2 - Moderate COPD, Group B",
                "unit": "classification",
                "interpretation": "GOLD 2 - Moderate COPD, Group B. Post-bronchodilator spirometry: FEV1/FVC 0.65 (<0.70 confirms COPD), FEV1 65.0% predicted. Symptoms: mMRC 2 (Walks slower than people of same age due to breathlessness), CAT 15/40. Exacerbation history: 1 exacerbations, 0 hospitalizations in last year. Classification: High symptom burden, low exacerbation risk. Treatment recommendations: Long-acting bronchodilator (LABA or LAMA). If still breathless: LABA + LAMA combination. Regular long-acting bronchodilator therapy with pulmonary rehabilitation. Essential interventions: smoking cessation (most important), annual influenza vaccination, pneumococcal vaccination, COVID-19 vaccination. Pulmonary rehabilitation recommended for all symptomatic patients (Groups B and E). Monitor for comorbidities especially cardiovascular disease.",
                "stage": "GOLD 2 - Moderate COPD, Group B",
                "stage_description": "Moderate airflow limitation, Group B"
            }
        }