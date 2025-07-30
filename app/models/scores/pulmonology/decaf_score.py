"""
DECAF Score for Acute Exacerbation of COPD Models

Request and response models for DECAF (Dyspnoea, Eosinopenia, Consolidation, 
Acidaemia, atrial Fibrillation) score calculation.

References (Vancouver style):
1. Steer J, Gibson J, Bourke SC. The DECAF Score: predicting hospital mortality 
   in exacerbations of chronic obstructive pulmonary disease. Thorax. 
   2012;67(11):970-976. doi: 10.1136/thoraxjnl-2012-202103.
2. Echevarria C, Steer J, Heslop-Marshall K, et al. Validation of the DECAF score 
   to predict hospital mortality in acute exacerbations of COPD. Thorax. 
   2016;71(2):133-140. doi: 10.1136/thoraxjnl-2015-207775.
3. Zhou M, Chen Y, Yang M, et al. DECAF score as a mortality predictor for acute 
   exacerbation of chronic obstructive pulmonary disease: a systematic review and 
   meta-analysis. BMJ Open. 2021;11(2):e044923. doi: 10.1136/bmjopen-2020-044923.
4. Nafae RM, Embarak S, Gad DM. Value of the DECAF score in predicting hospital 
   mortality in patients with acute exacerbation of chronic obstructive pulmonary 
   disease admitted to Zagazig University Hospitals, Egypt. Egypt J Chest Dis 
   Tuberc. 2015;64(1):35-40. doi: 10.1016/j.ejcdt.2014.07.006.

The DECAF score is a validated clinical decision tool that predicts in-hospital 
mortality in acute COPD exacerbation using five key clinical variables. The score 
combines the strongest predictors of mortality: extended MRC Dyspnoea Score, 
eosinopenia, consolidation, acidaemia, and atrial fibrillation.

Scoring System:
- Dyspnoea (Extended MRC): 0-2 points based on functional limitation
- Eosinopenia (<0.05×10⁹/L): 0-1 point
- Consolidation on chest X-ray: 0-1 point  
- Acidaemia (pH <7.30): 0-1 point
- Atrial fibrillation: 0-1 point

Risk Categories:
- Low Risk (0-1 points): 0-1.5% mortality - routine management
- Intermediate Risk (2 points): 5.4% mortality - clinical judgment needed
- High Risk (3-6 points): 15.3-50% mortality - escalation/palliative care

The tool applies only to hospitalized patients ≥35 years old with acute COPD 
exacerbation and ≥10 pack-year smoking history. It has superior prognostic accuracy 
compared to other COPD severity scores and supports clinical decision-making for 
disposition and level of care.
"""

from pydantic import BaseModel, Field
from typing import Literal, Optional, List, Dict, Any


class DecafScoreRequest(BaseModel):
    """
    Request model for DECAF Score for Acute Exacerbation of COPD
    
    The DECAF score uses five clinical variables to predict in-hospital mortality:
    
    D - Dyspnoea (Extended MRC Dyspnoea Scale):
    - not_too_dyspneic: Not too dyspneic to leave house (0 points)
    - too_dyspneic_independent: Too dyspneic to leave house but independent with 
      washing/dressing (1 point)
    - too_dyspneic_dependent: Too dyspneic to leave house and wash/dress (2 points)
    
    E - Eosinopenia:
    - yes: Eosinophils <0.05×10⁹/L or <50 cells/μL (1 point)
    - no: Eosinophils ≥0.05×10⁹/L or ≥50 cells/μL (0 points)
    
    C - Consolidation:
    - yes: Consolidation present on chest X-ray (1 point)
    - no: No consolidation on chest X-ray (0 points)
    
    A - Acidaemia:
    - yes: Arterial blood gas pH <7.30 (1 point)
    - no: Arterial blood gas pH ≥7.30 (0 points)
    
    F - atrial Fibrillation:
    - yes: Atrial fibrillation on ECG or documented history (1 point)
    - no: No atrial fibrillation (0 points)
    
    Validity Criteria:
    This score is validated for patients ≥35 years old with acute COPD exacerbation 
    requiring hospitalization and ≥10 pack-year smoking history. It should only be 
    used in the inpatient setting, not for outpatient or stable COPD patients.
    
    Clinical Application:
    The DECAF score helps clinicians stratify mortality risk and guide decisions 
    about level of care, monitoring intensity, and potential need for escalation 
    or palliative care discussions.
    
    References (Vancouver style):
    1. Steer J, Gibson J, Bourke SC. The DECAF Score: predicting hospital mortality 
    in exacerbations of chronic obstructive pulmonary disease. Thorax. 
    2012;67(11):970-976. doi: 10.1136/thoraxjnl-2012-202103.
    2. Echevarria C, Steer J, Heslop-Marshall K, et al. Validation of the DECAF score 
    to predict hospital mortality in acute exacerbations of COPD. Thorax. 
    2016;71(2):133-140. doi: 10.1136/thoraxjnl-2015-207775.
    """
    
    emrcd_dyspnea: Literal["not_too_dyspneic", "too_dyspneic_independent", "too_dyspneic_dependent"] = Field(
        ...,
        description="Extended MRC Dyspnea Scale assessing functional limitation due to breathlessness. Not too dyspneic to leave house (0 points), too dyspneic to leave house but independent with washing/dressing (1 point), or too dyspneic to leave house and wash/dress (2 points)",
        example="too_dyspneic_independent"
    )
    
    eosinopenia: Literal["yes", "no"] = Field(
        ...,
        description="Presence of eosinopenia defined as eosinophils <0.05×10⁹/L (equivalent to <50 cells/μL). Yes scores 1 point, no scores 0 points",
        example="no"
    )
    
    consolidation: Literal["yes", "no"] = Field(
        ...,
        description="Presence of consolidation on chest X-ray imaging. Yes scores 1 point, no scores 0 points",
        example="yes"
    )
    
    acidemia: Literal["yes", "no"] = Field(
        ...,
        description="Presence of acidemia defined as arterial blood gas pH <7.30. Yes scores 1 point, no scores 0 points",
        example="no"
    )
    
    atrial_fibrillation: Literal["yes", "no"] = Field(
        ...,
        description="Presence of atrial fibrillation on ECG or documented history. Yes scores 1 point, no scores 0 points",
        example="no"
    )
    
    patient_age: Optional[int] = Field(
        None,
        ge=35,
        le=120,
        description="Patient age in years (≥35 years required for score validity). Used for clinical context and validity assessment",
        example=72
    )
    
    smoking_history: Optional[Literal["yes", "no", "unknown"]] = Field(
        None,
        description="Significant smoking history (≥10 pack-years required for score validity). Used for clinical context and validity assessment",
        example="yes"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "emrcd_dyspnea": "too_dyspneic_independent",
                "eosinopenia": "no",
                "consolidation": "yes", 
                "acidemia": "no",
                "atrial_fibrillation": "no",
                "patient_age": 72,
                "smoking_history": "yes"
            }
        }


class DecafScoreResponse(BaseModel):
    """
    Response model for DECAF Score for Acute Exacerbation of COPD
    
    The DECAF score provides comprehensive assessment of in-hospital mortality risk with:
    - Quantitative risk assessment (score 0-6)
    - Risk category classification (Low/Intermediate/High)
    - Specific mortality risk percentages
    - Clinical management and disposition recommendations
    - Monitoring and escalation guidance
    - Validity assessment and clinical context
    
    Risk Categories and Mortality Rates:
    - Low Risk (0-1 points): 0-1.5% mortality
    - Intermediate Risk (2 points): 5.4% mortality
    - High Risk (3-6 points): 15.3-50% mortality
    
    Clinical Decision Support:
    Low risk patients can receive routine ward care, intermediate risk patients 
    require clinical judgment and closer monitoring, and high risk patients warrant 
    consideration for intensive care or palliative care depending on goals of care.
    
    Reference: Steer J, et al. Thorax. 2012;67(11):970-976.
    """
    
    result: int = Field(
        ...,
        description="DECAF score calculated from clinical variables (range: 0-6 points)",
        example=2
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the DECAF score",
        example="DECAF score"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation with mortality risk and management recommendation",
        example="DECAF score of 2 indicates Intermediate Risk with 5.4% in-hospital mortality risk. Use clinical judgment regarding disposition and consider closer monitoring with frequent reassessment."
    )
    
    stage: str = Field(
        ...,
        description="Risk category classification based on DECAF score",
        example="Intermediate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Intermediate mortality risk"
    )
    
    decaf_score: int = Field(
        ...,
        description="The calculated DECAF score",
        example=2
    )
    
    risk_category: str = Field(
        ...,
        description="Risk category classification (low, intermediate, high)",
        example="intermediate"
    )
    
    mortality_risk: str = Field(
        ...,
        description="Specific mortality risk percentage for the calculated score",
        example="5.4%"
    )
    
    mortality_range: str = Field(
        ...,
        description="Mortality risk range for the risk category",
        example="5.4%"
    )
    
    recommendation: str = Field(
        ...,
        description="Primary clinical recommendation based on risk category",
        example="Use clinician judgment re: disposition"
    )
    
    disposition: str = Field(
        ...,
        description="Recommended disposition and level of care",
        example="Consider higher level care"
    )
    
    monitoring_level: str = Field(
        ...,
        description="Recommended monitoring intensity",
        example="Close monitoring"
    )
    
    clinical_assessment: Dict[str, Any] = Field(
        ...,
        description="Detailed clinical assessment including score components, validity criteria, and additional considerations"
    )
    
    management_recommendations: Dict[str, Any] = Field(
        ...,
        description="Comprehensive management recommendations including monitoring requirements and escalation criteria"
    )
    
    mortality_details: Dict[str, Any] = Field(
        ...,
        description="Detailed mortality risk information with confidence and comparison data"
    )
    
    score_components: List[Dict[str, Any]] = Field(
        ...,
        description="Detailed breakdown of individual score components and their point contributions"
    )
    
    clinical_guidance: Dict[str, Any] = Field(
        ...,
        description="Clinical guidance for disposition, priority, and communication with patients and families"
    )
    
    follow_up_recommendations: Dict[str, Any] = Field(
        ...,
        description="Follow-up recommendations for inpatient, discharge, and outpatient care"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 2,
                "unit": "DECAF score",
                "interpretation": "DECAF score of 2 indicates Intermediate Risk with 5.4% in-hospital mortality risk. Use clinical judgment regarding disposition and consider closer monitoring with frequent reassessment.",
                "stage": "Intermediate Risk",
                "stage_description": "Intermediate mortality risk",
                "decaf_score": 2,
                "risk_category": "intermediate",
                "mortality_risk": "5.4%",
                "mortality_range": "5.4%",
                "recommendation": "Use clinician judgment re: disposition",
                "disposition": "Consider higher level care",
                "monitoring_level": "Close monitoring",
                "clinical_assessment": {
                    "decaf_score": 2,
                    "risk_category": "intermediate",
                    "score_components": [
                        "Too dyspneic to leave house but independent with washing/dressing (1 point)",
                        "Eosinopenia (<0.05×10⁹/L): no (0 point)",
                        "Consolidation on chest X-ray: yes (1 point)",
                        "Acidemia (pH <7.30): no (0 point)",
                        "Atrial fibrillation: no (0 point)"
                    ],
                    "validity_criteria": [
                        "Age ≥35 years (age 72) - score validity met",
                        "≥10 pack-year smoking history assumed - score validity supported"
                    ]
                },
                "management_recommendations": {
                    "primary_recommendations": [
                        "Close clinical monitoring and frequent reassessment",
                        "Consider higher level of nursing care or step-down unit",
                        "Aggressive bronchodilator and anti-inflammatory therapy"
                    ],
                    "monitoring_requirements": [
                        "Enhanced nursing observations every 2-4 hours",
                        "Frequent assessment of respiratory status",
                        "Consider arterial blood gas monitoring"
                    ]
                },
                "mortality_details": {
                    "risk": "5.4%",
                    "confidence": "Moderate",
                    "time_frame": "In-hospital mortality risk",
                    "comparison": "Moderate risk - 5-10 times higher than low-risk patients"
                },
                "score_components": [
                    {
                        "component": "Extended MRC Dyspnea",
                        "value": "too_dyspneic_independent",
                        "points": 1,
                        "description": "Functional limitation due to dyspnea"
                    },
                    {
                        "component": "Consolidation",
                        "value": "yes",
                        "points": 1,
                        "description": "Consolidation on chest X-ray"
                    }
                ],
                "clinical_guidance": {
                    "disposition": "Consider higher level care or close monitoring",
                    "priority": "Moderate priority requiring frequent assessment",
                    "family_communication": "Guarded prognosis requiring close monitoring",
                    "prognosis_discussion": "Moderate risk requiring individualized care planning"
                },
                "follow_up_recommendations": {
                    "inpatient": "Twice daily specialist review",
                    "discharge": "Enhanced discharge planning with home monitoring",
                    "outpatient": "Early pulmonology follow-up within 1-2 weeks"
                }
            }
        }