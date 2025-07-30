"""
CSHA Clinical Frailty Scale (CFS) Models

Request and response models for Clinical Frailty Scale assessment.

References (Vancouver style):
1. Rockwood K, Song X, MacKnight C, et al. A global clinical measure of fitness and frailty 
   in elderly people. CMAJ. 2005;173(5):489-495. doi: 10.1503/cmaj.050051.
2. Church S, Rogers E, Rockwood K, Theou O. A scoping review of the Clinical Frailty Scale. 
   BMC Geriatr. 2020;20(1):393. doi: 10.1186/s12877-020-01801-7.
3. Clegg A, Young J, Iliffe S, Rikkert MO, Rockwood K. Frailty in elderly people. 
   Lancet. 2013;381(9868):752-762. doi: 10.1016/S0140-6736(12)62167-9.
4. Dalhousie University. Clinical Frailty Scale. Available at: 
   https://www.dal.ca/sites/gmr/our-tools/clinical-frailty-scale.html
5. Canadian Study of Health and Aging Working Group. Canadian study of health and aging: 
   study methods and prevalence of dementia. CMAJ. 1994;150(6):899-913.

The Clinical Frailty Scale (CFS) is a 9-point judgement-based frailty assessment tool that 
evaluates fitness, comorbidity, function, and cognition to predict survival, mortality, 
need for institutional care, and other adverse outcomes in older adults aged 65 and over. 
It has been validated across multiple clinical settings and is predictive of mortality 
in 87% of studies, making it one of the most widely used frailty assessment tools globally.
"""

from pydantic import BaseModel, Field
from typing import Literal, Optional, Dict, Any, List


class ClinicalFrailtyScaleRequest(BaseModel):
    """
    Request model for CSHA Clinical Frailty Scale (CFS) assessment
    
    The CFS uses a 9-point scale to assess frailty based on clinical judgement considering:
    
    **Frailty Level Scale:**
    
    1. **Very Fit**: Robust, active, energetic, motivated. Exercise regularly. Fittest for age.
    2. **Fit**: No severe disease symptoms but less fit than category 1. Exercise occasionally.
    3. **Managing Well**: Medical problems well-controlled but not regularly active beyond walking.
    4. **Living with Very Mild Frailty**: Not dependent on daily help, but symptoms limit activities.
    5. **Living with Mild Frailty**: Need help with complex activities (finances, transportation, housework).
    6. **Living with Moderate Frailty**: Need help with all outside activities and keeping house.
    7. **Living with Severe Frailty**: Completely dependent for personal care but stable.
    8. **Living with Very Severe Frailty**: Completely dependent, approaching end of life.
    9. **Terminally Ill**: Life expectancy under 6 months, not otherwise evidently frail.
    
    **Age Requirements:**
    - Only validated for patients aged 65 years and older
    - Should be assessed by trained healthcare professionals
    
    **Clinical Applications:**
    - Predicting mortality in hospitalized older adults
    - Assessing suitability for intensive interventions  
    - Guiding care planning and resource allocation
    - Emergency department risk stratification
    - Surgical risk assessment and ICU admission decisions
    - Discharge planning and long-term care placement
    
    **Predictive Validity:**
    - Mortality prediction validated in 87% of studies
    - Associated with length of stay, complications, falls
    - Predicts functional decline and need for institutional care
    - Useful across emergency, surgical, ICU, and ward settings
    
    References (Vancouver style):
    1. Rockwood K, Song X, MacKnight C, et al. A global clinical measure of fitness and frailty 
       in elderly people. CMAJ. 2005;173(5):489-495. doi: 10.1503/cmaj.050051.
    2. Church S, Rogers E, Rockwood K, Theou O. A scoping review of the Clinical Frailty Scale. 
       BMC Geriatr. 2020;20(1):393. doi: 10.1186/s12877-020-01801-7.
    3. Clegg A, Young J, Iliffe S, Rikkert MO, Rockwood K. Frailty in elderly people. 
       Lancet. 2013;381(9868):752-762. doi: 10.1016/S0140-6736(12)62167-9.
    """
    
    frailty_level: Literal[1, 2, 3, 4, 5, 6, 7, 8, 9] = Field(
        ...,
        description=(
            "Clinical Frailty Scale level based on overall assessment of fitness, activity, "
            "comorbidity, function, and cognition. Scale: 1=Very Fit, 2=Fit, 3=Managing Well, "
            "4=Living with Very Mild Frailty, 5=Living with Mild Frailty, "
            "6=Living with Moderate Frailty, 7=Living with Severe Frailty, "
            "8=Living with Very Severe Frailty, 9=Terminally Ill"
        ),
        example=4
    )
    
    age: int = Field(
        ...,
        ge=65,
        le=120,
        description="Patient age in years (CFS is only validated for patients aged 65 and over)",
        example=78
    )
    
    dementia_present: Optional[Literal["yes", "no", "unknown"]] = Field(
        None,
        description=(
            "Presence of dementia or significant cognitive impairment. This affects frailty "
            "assessment as cognitive impairment can influence functional capacity and "
            "independence even in physically robust individuals"
        ),
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "frailty_level": 4,
                "age": 78,
                "dementia_present": "no"
            }
        }


class ClinicalFrailtyScaleResponse(BaseModel):
    """
    Response model for CSHA Clinical Frailty Scale (CFS) assessment
    
    Provides comprehensive frailty assessment with risk stratification, clinical 
    recommendations, predictive outcomes, and care planning guidance based on the 
    validated CFS scoring system.
    
    **Risk Categories:**
    - Very Low Risk (CFS 1-3): Suitable for intensive interventions, excellent prognosis
    - Mild Risk (CFS 4): Vulnerable but independent, monitor for decline
    - Moderate Risk (CFS 5-6): Limited independence, comprehensive assessment needed
    - High Risk (CFS 7-8): High dependency, focus on comfort and appropriate care setting
    - Very High Risk (CFS 9): Terminal illness, palliative care indicated
    
    **Predictive Outcomes:**
    - 6-month mortality risk ranges from <5% (CFS 1-3) to >40% (CFS 8-9)
    - Hospital readmission rates from <15% (low frailty) to >60% (severe frailty)
    - Functional decline probability increases significantly with higher CFS scores
    
    Reference: Rockwood K, et al. CMAJ. 2005;173(5):489-495.
    """
    
    result: int = Field(
        ...,
        description="Clinical Frailty Scale level (1-9) based on assessment",
        example=4
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the frailty scale",
        example="CFS level"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation of frailty assessment with prognosis and recommendations",
        example="CFS level 4 (Living with Very Mild Frailty) indicates vulnerability to stressors with need for close monitoring. Patient may benefit from preventive interventions and comprehensive assessment while maintaining relative independence."
    )
    
    stage: str = Field(
        ...,
        description="Frailty stage label (e.g., 'Very Fit', 'Living with Mild Frailty', 'Terminally Ill')",
        example="Living with Very Mild Frailty"
    )
    
    stage_description: str = Field(
        ...,
        description="Detailed description of the frailty stage characteristics",
        example="Previously named 'Vulnerable'. While not dependent on others for daily help, symptoms often limit activities."
    )
    
    risk_assessment: Dict[str, Any] = Field(
        ...,
        description="Comprehensive risk assessment including mortality, readmission, and functional decline risks",
        example={
            "overall_risk": "Mild Risk",
            "risk_color": "yellow",
            "mortality_6_month": "10-15%",
            "hospital_readmission": "25-35%", 
            "functional_decline": "20-30%",
            "institutionalization_risk": "Low risk of requiring institutional care"
        }
    )
    
    clinical_recommendations: Dict[str, Any] = Field(
        ...,
        description="Clinical recommendations including monitoring schedule and suggested interventions",
        example={
            "primary_recommendations": [
                "Close monitoring for early signs of decline",
                "Consider preventive interventions",
                "Optimize management of chronic conditions"
            ],
            "monitoring_schedule": ["6-monthly frailty reassessment"],
            "suggested_interventions": ["Comprehensive geriatric assessment", "Physical therapy"],
            "care_setting": "Community-based care with outpatient follow-up"
        }
    )
    
    predictive_outcomes: Dict[str, str] = Field(
        ...,
        description="Predicted outcomes for hospital stay, ICU mortality, surgical risk, and recovery potential",
        example={
            "hospital_length_of_stay": "Average",
            "icu_mortality": "Low to moderate risk",
            "surgical_outcomes": "Generally good candidate",
            "recovery_potential": "Good with support",
            "emergency_outcomes": "Moderate risk of adverse events"
        }
    )
    
    frailty_category: str = Field(
        ...,
        description="General frailty category grouping",
        example="Very Mild Frailty"
    )
    
    mortality_risk: str = Field(
        ...,
        description="Overall mortality risk level",
        example="low"
    )
    
    intervention_suitability: Dict[str, str] = Field(
        ...,
        description="Suitability assessment for different types of interventions",
        example={
            "intensive_interventions": "Generally suitable with monitoring",
            "surgical_procedures": "Good candidate with precautions",
            "rehabilitation": "Good potential",
            "clinical_trials": "Consider on case-by-case basis"
        }
    )
    
    care_planning: Dict[str, Any] = Field(
        ...,
        description="Care planning guidance including goals, advance directives, and resource needs",
        example={
            "goals_of_care": "Prevent progression, optimize function",
            "advance_directives": "Important to complete",
            "family_involvement": "Involve in care planning",
            "resource_needs": "Preventive services, monitoring"
        }
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 4,
                "unit": "CFS level",
                "interpretation": "CFS level 4 (Living with Very Mild Frailty) indicates vulnerability to stressors with need for close monitoring. Patient may benefit from preventive interventions and comprehensive assessment while maintaining relative independence.",
                "stage": "Living with Very Mild Frailty",
                "stage_description": "Previously named 'Vulnerable'. While not dependent on others for daily help, symptoms often limit activities.",
                "risk_assessment": {
                    "overall_risk": "Mild Risk",
                    "risk_color": "yellow",
                    "mortality_6_month": "10-15%",
                    "hospital_readmission": "25-35%",
                    "functional_decline": "20-30%",
                    "institutionalization_risk": "Low risk of requiring institutional care"
                },
                "clinical_recommendations": {
                    "primary_recommendations": [
                        "Close monitoring for early signs of decline",
                        "Consider preventive interventions",
                        "Optimize management of chronic conditions",
                        "Fall prevention strategies"
                    ],
                    "monitoring_schedule": ["6-monthly frailty reassessment"],
                    "suggested_interventions": ["Comprehensive geriatric assessment", "Physical therapy", "Medication review"],
                    "care_setting": "Community-based care with outpatient follow-up"
                },
                "predictive_outcomes": {
                    "hospital_length_of_stay": "Average",
                    "icu_mortality": "Low to moderate risk",
                    "surgical_outcomes": "Generally good candidate",
                    "recovery_potential": "Good with support",
                    "emergency_outcomes": "Moderate risk of adverse events"
                },
                "frailty_category": "Very Mild Frailty",
                "mortality_risk": "low",
                "intervention_suitability": {
                    "intensive_interventions": "Generally suitable with monitoring",
                    "surgical_procedures": "Good candidate with precautions",
                    "rehabilitation": "Good potential",
                    "clinical_trials": "Consider on case-by-case basis"
                },
                "care_planning": {
                    "goals_of_care": "Prevent progression, optimize function",
                    "advance_directives": "Important to complete",
                    "family_involvement": "Involve in care planning",
                    "resource_needs": "Preventive services, monitoring"
                }
            }
        }