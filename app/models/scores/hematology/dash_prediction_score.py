"""
DASH Prediction Score for Recurrent VTE Models

Request and response models for DASH (D-dimer, Age, Sex, Hormonal therapy) 
prediction score calculation.

References (Vancouver style):
1. Tosetto A, Iorio A, Marcucci M, et al. Predicting disease recurrence in patients 
   with previous unprovoked venous thromboembolism: a proposed prediction score (DASH). 
   J Thromb Haemost. 2012;10(6):1019-1025. doi: 10.1111/j.1538-7836.2012.04735.x.
2. Kearon C, Akl EA, Ornelas J, et al. Antithrombotic Therapy for VTE Disease: 
   CHEST Guideline and Expert Panel Report. Chest. 2016;149(2):315-352. 
   doi: 10.1016/j.chest.2015.11.026.
3. Ortel TL, Neumann I, Ageno W, et al. American Society of Hematology 2020 
   guidelines for management of venous thromboembolism: treatment of deep vein 
   thrombosis and pulmonary embolism. Blood Adv. 2020;4(19):4693-4738. 
   doi: 10.1182/bloodadvances.2020001830.
4. Eichinger S, Heinze G, Jandeck LM, Kyrle PA. Risk assessment of recurrence 
   in patients with unprovoked deep vein thrombosis or pulmonary embolism: 
   the Vienna prediction model. Circulation. 2010;121(14):1630-1636. 
   doi: 10.1161/CIRCULATIONAHA.109.925214.

The DASH prediction score is a validated clinical decision tool that predicts 
the likelihood of recurrence of first unprovoked venous thromboembolism (VTE) 
to guide anticoagulation duration decisions. The score uses four clinical factors:
D-dimer result (measured ~1 month after stopping anticoagulation), Age, Sex, 
and Hormonal therapy use at time of initial VTE.

Scoring System:
- D-dimer positive: +2 points
- Age ≤50 years: +1 point  
- Male sex: +1 point
- Hormonal therapy in women: -2 points

Risk Categories:
- Low Risk (-2 to 1 points): 3.1% annual recurrence risk
- Intermediate Risk (2 points): 6.4% annual recurrence risk  
- High Risk (3-6 points): 12.3% annual recurrence risk

The tool applies only to patients with first unprovoked VTE who have completed 
at least 3 months of anticoagulation therapy. It excludes VTE associated with 
pregnancy, surgery, trauma, immobilization, or active cancer.
"""

from pydantic import BaseModel, Field
from typing import Literal, Optional, List, Dict, Any


class DashPredictionScoreRequest(BaseModel):
    """
    Request model for DASH Prediction Score for Recurrent VTE
    
    The DASH score uses four clinical variables to predict VTE recurrence risk:
    
    D-dimer Result:
    - positive: Elevated D-dimer ~1 month after stopping anticoagulation (+2 points)
    - negative: Normal D-dimer ~1 month after stopping anticoagulation (0 points)
    
    Age:
    - ≤50 years: +1 point
    - >50 years: 0 points
    
    Sex:
    - male: +1 point
    - female: 0 points
    
    Hormonal Therapy (women only):
    - yes: Hormonal therapy at time of initial VTE (-2 points)
    - no: No hormonal therapy (0 points)
    - not_applicable: For male patients (0 points)
    
    Optional Parameters:
    - vte_type: Type of initial VTE for clinical context
    - anticoagulation_duration: Duration of initial treatment in months
    
    Clinical Application:
    This score helps guide decisions about anticoagulation duration after first 
    unprovoked VTE. Lower scores suggest safe discontinuation, while higher scores 
    indicate need for prolonged therapy based on recurrence risk.
    
    Important Notes:
    - Score applies only to first unprovoked VTE patients
    - D-dimer should be measured ~1 month after stopping anticoagulation
    - Excludes pregnancy-associated, trauma-related, or cancer-associated VTE
    - Should be used with bleeding risk assessment for complete evaluation
    
    References (Vancouver style):
    1. Tosetto A, Iorio A, Marcucci M, et al. Predicting disease recurrence in patients 
    with previous unprovoked venous thromboembolism: a proposed prediction score (DASH). 
    J Thromb Haemost. 2012;10(6):1019-1025. doi: 10.1111/j.1538-7836.2012.04735.x.
    2. Kearon C, Akl EA, Ornelas J, et al. Antithrombotic Therapy for VTE Disease: 
    CHEST Guideline and Expert Panel Report. Chest. 2016;149(2):315-352. 
    doi: 10.1016/j.chest.2015.11.026.
    """
    
    d_dimer_positive: Literal["positive", "negative"] = Field(
        ...,
        description="Post-anticoagulation D-dimer result measured approximately 1 month after stopping anticoagulation. Positive result scores +2 points",
        example="negative"
    )
    
    age: int = Field(
        ...,
        ge=18,
        le=100,
        description="Patient age in years. Age ≤50 years scores +1 point, age >50 years scores 0 points",
        example=55
    )
    
    sex: Literal["male", "female"] = Field(
        ...,
        description="Patient biological sex. Male sex scores +1 point, female sex scores 0 points",
        example="female"
    )
    
    hormonal_therapy: Literal["yes", "no", "not_applicable"] = Field(
        ...,
        description="Hormonal therapy use at time of initial VTE (oral contraceptives, hormone replacement therapy). Applies to women only - select 'not_applicable' for men. Yes scores -2 points for women",
        example="no"
    )
    
    vte_type: Optional[Literal["dvt_only", "pe_only", "dvt_and_pe", "not_specified"]] = Field(
        None,
        description="Type of initial venous thromboembolism for clinical context and risk assessment",
        example="dvt_only"
    )
    
    anticoagulation_duration: Optional[int] = Field(
        None,
        ge=3,
        le=24,
        description="Duration of initial anticoagulation treatment in months (typically 3-24 months)",
        example=6
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "d_dimer_positive": "negative",
                "age": 55,
                "sex": "female", 
                "hormonal_therapy": "no",
                "vte_type": "dvt_only",
                "anticoagulation_duration": 6
            }
        }


class DashPredictionScoreResponse(BaseModel):
    """
    Response model for DASH Prediction Score for Recurrent VTE
    
    The DASH score provides comprehensive assessment of VTE recurrence risk with:
    - Quantitative risk assessment (score -2 to +6)
    - Risk category classification (Low/Intermediate/High)
    - Annual recurrence risk percentages with confidence intervals
    - Evidence-based anticoagulation recommendations
    - Clinical assessment and decision support
    - Safety planning and monitoring guidance
    
    Risk Categories and Annual Recurrence Rates:
    - Low Risk (-2 to 1 points): 3.1% (95% CI 2.3-3.9%)
    - Intermediate Risk (2 points): 6.4% (95% CI 4.8-7.9%)
    - High Risk (3-6 points): 12.3% (95% CI 9.9-14.7%)
    
    Clinical Decision Support:
    Low risk patients may safely discontinue anticoagulation, intermediate risk 
    patients require individualized decision-making, and high risk patients warrant 
    consideration for prolonged anticoagulation therapy.
    
    Reference: Tosetto A, et al. J Thromb Haemost. 2012;10(6):1019-1025.
    """
    
    result: int = Field(
        ...,
        description="DASH prediction score calculated from clinical variables (range: -2 to +6 points)",
        example=1
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the DASH score",
        example="DASH score"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation with annual recurrence risk and anticoagulation recommendation",
        example="DASH score of 1 indicates Low Risk with 3.1% annual VTE recurrence risk (95% CI 2.3-3.9%). The low recurrence risk justifies discontinuing anticoagulation after 3-6 months of treatment, assuming bleeding risk is not elevated."
    )
    
    stage: str = Field(
        ...,
        description="Risk category classification based on DASH score",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Low annual recurrence risk"
    )
    
    dash_score: int = Field(
        ...,
        description="The calculated DASH prediction score",
        example=1
    )
    
    risk_category: str = Field(
        ...,
        description="Risk category classification (low, intermediate, high)",
        example="low"
    )
    
    annual_risk: str = Field(
        ...,
        description="Annual VTE recurrence risk percentage with confidence interval",
        example="3.1%"
    )
    
    annual_risk_numeric: float = Field(
        ...,
        description="Numeric annual recurrence risk percentage for calculations",
        example=3.1
    )
    
    confidence_interval: str = Field(
        ...,
        description="95% confidence interval for annual recurrence risk",
        example="2.3-3.9%"
    )
    
    recommendation: str = Field(
        ...,
        description="Primary anticoagulation recommendation based on risk category",
        example="Consider discontinuing anticoagulation"
    )
    
    clinical_assessment: Dict[str, Any] = Field(
        ...,
        description="Detailed clinical assessment including score components and risk factors"
    )
    
    anticoagulation_recommendations: Dict[str, Any] = Field(
        ...,
        description="Comprehensive anticoagulation recommendations including bleeding assessment guidance"
    )
    
    decision_support: Dict[str, Any] = Field(
        ...,
        description="Clinical decision support information for shared decision-making"
    )
    
    score_components: List[Dict[str, Any]] = Field(
        ...,
        description="Detailed breakdown of individual score components and their point contributions"
    )
    
    counseling_points: List[str] = Field(
        ...,
        description="Key counseling points for patient discussion about VTE recurrence risk"
    )
    
    follow_up_recommendations: Dict[str, Any] = Field(
        ...,
        description="Follow-up monitoring recommendations based on risk category"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 1,
                "unit": "DASH score",
                "interpretation": "DASH score of 1 indicates Low Risk with 3.1% annual VTE recurrence risk (95% CI 2.3-3.9%). The low recurrence risk justifies discontinuing anticoagulation after 3-6 months of treatment, assuming bleeding risk is not elevated.",
                "stage": "Low Risk",
                "stage_description": "Low annual recurrence risk",
                "dash_score": 1,
                "risk_category": "low",
                "annual_risk": "3.1%",
                "annual_risk_numeric": 3.1,
                "confidence_interval": "2.3-3.9%",
                "recommendation": "Consider discontinuing anticoagulation",
                "clinical_assessment": {
                    "dash_score": 1,
                    "risk_category": "low",
                    "score_components": [
                        "D-dimer negative (0 points)",
                        "Age >50 years (age 55, 0 points)",
                        "Female sex (0 points)",
                        "No hormonal therapy (0 points)"
                    ],
                    "clinical_factors": [
                        "First unprovoked VTE requiring anticoagulation duration decision",
                        "DASH score of 1 indicates low risk for recurrence",
                        "Post-anticoagulation D-dimer: negative"
                    ]
                },
                "anticoagulation_recommendations": {
                    "primary_recommendations": [
                        "Consider discontinuing anticoagulation after 3-6 months",
                        "Monitor for signs and symptoms of VTE recurrence"
                    ],
                    "bleeding_assessment": {
                        "assessment_tools": [
                            "HAS-BLED score for bleeding risk assessment",
                            "HEMORR2HAGES score for major bleeding risk"
                        ]
                    }
                },
                "decision_support": {
                    "primary_decision": "Anticoagulation discontinuation is reasonable",
                    "key_considerations": [
                        "Low 3.1% annual recurrence risk",
                        "Risk of continued anticoagulation may outweigh benefits"
                    ]
                },
                "score_components": [
                    {
                        "component": "D-dimer",
                        "value": "negative",
                        "points": 0,
                        "description": "D-dimer negative"
                    },
                    {
                        "component": "Age",
                        "value": 55,
                        "points": 0,
                        "description": "Age 55 years (>50)"
                    }
                ],
                "counseling_points": [
                    "Your low DASH score indicates relatively low recurrence risk",
                    "Stopping anticoagulation after 3-6 months is reasonable"
                ],
                "follow_up_recommendations": {
                    "frequency": "3 and 6 months after discontinuation, then as needed",
                    "components": [
                        "Clinical assessment for VTE symptoms",
                        "Review of new risk factors"
                    ]
                }
            }
        }