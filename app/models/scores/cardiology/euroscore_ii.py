"""
European System for Cardiac Operative Risk Evaluation (EuroSCORE) II Models

Request and response models for EuroSCORE II calculator for predicting in-hospital mortality 
after major cardiac surgery.

References (Vancouver style):
1. Nashef SA, Roques F, Sharples LD, Nilsson J, Smith C, Goldstone AR, Lockowandt U. EuroSCORE II. 
   Eur J Cardiothorac Surg. 2012 Apr;41(4):734-44; discussion 744-5. doi: 10.1093/ejcts/ezs043.
2. Roques F, Michel P, Goldstone AR, Nashef SA. The logistic EuroSCORE. Eur Heart J. 2003 May;24(9):881-2. 
   doi: 10.1016/s0195-668x(02)00799-6.
3. Nashef SA, Roques F, Michel P, Gauducheau E, Lemeshow S, Salamon R. European system for cardiac 
   operative risk evaluation (EuroSCORE). Eur J Cardiothorac Surg. 1999 Jul;16(1):9-13. 
   doi: 10.1016/s1010-7940(99)00134-7.
4. Grant SW, Hickey GL, Dimarakis I, Trivedi U, Bryan A, Treasure T, Cooper G, Pagano D, McCollum C, 
   Bridgewater B. How does EuroSCORE II perform in UK cardiac surgery; an analysis of 23 740 patients 
   from the Society for Cardiothoracic Surgery in Great Britain and Ireland National Database. Heart. 
   2012 Dec;98(21):1568-72. doi: 10.1136/heartjnl-2012-302483.

The EuroSCORE II is a logistic regression model that predicts in-hospital mortality after cardiac 
surgery using 18 variables across patient-related, cardiac-related, and operation-related factors. 
It was developed from 22,381 consecutive patients in 154 hospitals across 43 countries and represents 
a significant improvement over the original EuroSCORE in contemporary cardiac surgical practice.
"""

from pydantic import BaseModel, Field
from typing import Literal


class EuroScoreIIRequest(BaseModel):
    """
    Request model for European System for Cardiac Operative Risk Evaluation (EuroSCORE) II
    
    The EuroSCORE II uses a logistic regression model to predict in-hospital mortality after 
    cardiac surgery. It incorporates 18 variables grouped into three categories:
    
    Patient-Related Factors (7 variables):
    1. Age: Coefficient increases by 0.0285181 per year after age 60
    2. Sex: Female patients have coefficient 0.2196434
    3. Insulin-dependent diabetes: Coefficient 0.3542749
    4. Chronic pulmonary dysfunction: Coefficient 0.1886564
    5. Neurological/musculoskeletal mobility dysfunction: Coefficient 0.2407181
    6. Creatinine clearance categories with specific coefficients
    7. Critical preoperative state: Coefficient 1.086517
    
    Cardiac-Related Factors (8 variables):
    1. NYHA functional class (I-IV) with increasing coefficients
    2. CCS Class 4 angina: Coefficient 0.2226147
    3. Extracardiac arteriopathy: Coefficient 0.5360268
    4. Previous cardiac surgery: Coefficient 1.118599
    5. Active endocarditis: Coefficient 0.6194522
    6. Left ventricular function categories with increasing coefficients
    7. Recent MI ≤90 days: Coefficient 0.1528943
    8. Pulmonary hypertension: Coefficient 0.1788899
    
    Operation-Related Factors (3 variables):
    1. Surgery urgency with increasing coefficients (elective → salvage)
    2. Weight/complexity of intervention with increasing coefficients
    3. Surgery on thoracic aorta: Coefficient 0.6527205
    
    Mathematical Formula:
    Predicted mortality (%) = 100 × e^y / (1 + e^y)
    Where y = -5.324537 + Σ(coefficient × variable)
    
    Model Performance:
    - Area under ROC curve: 0.8095
    - Well calibrated (predicted 3.95% vs actual 4.18% mortality)
    - Significant improvement over original EuroSCORE
    - Based on contemporary surgical outcomes (2010 data)
    
    Clinical Applications:
    - Preoperative risk assessment and informed consent
    - Surgical planning and resource allocation
    - Quality improvement and outcome benchmarking
    - Patient and family counseling
    - Multidisciplinary team decision-making
    
    Risk Stratification:
    - Low Risk (<2%): Standard care
    - Medium Risk (2-5%): Enhanced monitoring
    - High Risk (5-10%): Intensive care planning
    - Very High Risk (>10%): Consider alternatives
    
    Important Limitations:
    - Designed for in-hospital mortality, not long-term outcomes
    - May require local calibration in specific populations
    - Not applicable to transcatheter or minimally invasive procedures
    - Should complement, not replace, clinical judgment
    
    References (Vancouver style):
    1. Nashef SA, et al. EuroSCORE II. Eur J Cardiothorac Surg. 2012;41(4):734-44.
    2. Grant SW, et al. How does EuroSCORE II perform in UK cardiac surgery. Heart. 2012;98(21):1568-72.
    """
    
    age_years: int = Field(
        ...,
        description="Patient age in years. Coefficient increases by 0.0285181 per year after age 60",
        ge=18,
        le=110,
        example=65
    )
    
    sex: Literal["male", "female"] = Field(
        ...,
        description="Patient biological sex. Female sex carries coefficient 0.2196434",
        example="male"
    )
    
    insulin_dependent_diabetes: Literal["yes", "no"] = Field(
        ...,
        description="Insulin-dependent diabetes mellitus requiring insulin therapy. Coefficient 0.3542749 if yes",
        example="no"
    )
    
    chronic_pulmonary_dysfunction: Literal["yes", "no"] = Field(
        ...,
        description="Chronic pulmonary dysfunction requiring long-term bronchodilators or steroids for lung disease. Coefficient 0.1886564 if yes",
        example="no"
    )
    
    mobility_dysfunction: Literal["yes", "no"] = Field(
        ...,
        description="Neurological or musculoskeletal dysfunction severely affecting mobility or day-to-day functioning. Coefficient 0.2407181 if yes",
        example="no"
    )
    
    creatinine_clearance: Literal["greater_than_85", "51_to_85", "50_or_less", "on_dialysis"] = Field(
        ...,
        description="Creatinine clearance category or dialysis status. Categories: >85 mL/min (0), 51-85 mL/min (0.303553), ≤50 mL/min (0.8592256), on dialysis (0.6421508)",
        example="greater_than_85"
    )
    
    critical_preoperative_state: Literal["yes", "no"] = Field(
        ...,
        description="Critical preoperative state: mechanical ventilation, inotropic support, IABP, or acute renal failure. Coefficient 1.086517 if yes",
        example="no"
    )
    
    nyha_class: Literal["class_1", "class_2", "class_3", "class_4"] = Field(
        ...,
        description="NYHA functional classification. Coefficients: Class I (0), Class II (0.1070545), Class III (0.2958358), Class IV (0.5597929)",
        example="class_2"
    )
    
    ccs_class_4: Literal["yes", "no"] = Field(
        ...,
        description="Canadian Cardiovascular Society Class 4 angina (inability to perform any physical activity without discomfort). Coefficient 0.2226147 if yes",
        example="no"
    )
    
    extracardiac_arteriopathy: Literal["yes", "no"] = Field(
        ...,
        description="Extracardiac arteriopathy: claudication, carotid stenosis >50%, or previous/planned intervention on abdominal aorta, limb, or carotid arteries. Coefficient 0.5360268 if yes",
        example="no"
    )
    
    previous_cardiac_surgery: Literal["yes", "no"] = Field(
        ...,
        description="Previous cardiac surgery requiring opening of the pericardium. Coefficient 1.118599 if yes",
        example="no"
    )
    
    active_endocarditis: Literal["yes", "no"] = Field(
        ...,
        description="Active endocarditis (patient still on antimicrobial treatment for endocarditis at time of surgery). Coefficient 0.6194522 if yes",
        example="no"
    )
    
    left_ventricular_function: Literal["good_51_or_more", "moderate_31_to_50", "poor_21_to_30", "very_poor_20_or_less"] = Field(
        ...,
        description="Left ventricular ejection fraction category. Coefficients: Good ≥51% (0), Moderate 31-50% (0.3150652), Poor 21-30% (0.8084096), Very poor ≤20% (0.9346919)",
        example="good_51_or_more"
    )
    
    recent_mi: Literal["yes", "no"] = Field(
        ...,
        description="Recent myocardial infarction within 90 days of surgery. Coefficient 0.1528943 if yes",
        example="no"
    )
    
    pulmonary_hypertension: Literal["yes", "no"] = Field(
        ...,
        description="Pulmonary hypertension (systolic pulmonary artery pressure >60 mmHg). Coefficient 0.1788899 if yes",
        example="no"
    )
    
    urgency: Literal["elective", "urgent", "emergency", "salvage"] = Field(
        ...,
        description="Surgery urgency level. Coefficients: Elective (0), Urgent (0.3174673), Emergency (0.7039121), Salvage (1.362947)",
        example="elective"
    )
    
    weight_of_intervention: Literal["single_non_cabg", "two_procedures", "three_or_more_procedures"] = Field(
        ...,
        description="Weight/complexity of cardiac surgical intervention. Coefficients: Single non-CABG (0), Two procedures (0.5521478), Three or more procedures (0.9724533)",
        example="single_non_cabg"
    )
    
    surgery_on_thoracic_aorta: Literal["yes", "no"] = Field(
        ...,
        description="Surgery on thoracic aorta (ascending, arch, or descending aorta). Coefficient 0.6527205 if yes",
        example="no"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "age_years": 65,
                "sex": "male",
                "insulin_dependent_diabetes": "no",
                "chronic_pulmonary_dysfunction": "no",
                "mobility_dysfunction": "no",
                "creatinine_clearance": "greater_than_85",
                "critical_preoperative_state": "no",
                "nyha_class": "class_2",
                "ccs_class_4": "no",
                "extracardiac_arteriopathy": "no",
                "previous_cardiac_surgery": "no",
                "active_endocarditis": "no",
                "left_ventricular_function": "good_51_or_more",
                "recent_mi": "no",
                "pulmonary_hypertension": "no",
                "urgency": "elective",
                "weight_of_intervention": "single_non_cabg",
                "surgery_on_thoracic_aorta": "no"
            }
        }


class EuroScoreIIResponse(BaseModel):
    """
    Response model for European System for Cardiac Operative Risk Evaluation (EuroSCORE) II
    
    Provides predicted in-hospital mortality risk and clinical risk stratification for cardiac surgery:
    
    Risk Categories and Management:
    
    Low Risk (<2% mortality):
    - Standard perioperative care protocols
    - Routine monitoring and management
    - Excellent expected outcomes
    - Short ICU stay anticipated
    - Low resource utilization
    
    Medium Risk (2-5% mortality):
    - Enhanced perioperative monitoring
    - Careful care planning and coordination
    - Consider optimization of modifiable risk factors
    - Extended monitoring may be beneficial
    - Moderate resource allocation
    
    High Risk (5-10% mortality):
    - Intensive perioperative care required
    - Multidisciplinary team approach essential
    - Careful risk-benefit assessment
    - Consider alternative treatments if appropriate
    - High resource allocation and extended ICU stay
    
    Very High Risk (>10% mortality):
    - Detailed patient and family counseling required
    - Consider alternative treatments (medical management, transcatheter procedures)
    - Intensive perioperative support if surgery proceeds
    - Specialized cardiac surgery centers preferred
    - Maximum resource allocation and prolonged care
    
    Clinical Decision Support:
    
    Preoperative Planning:
    - Risk stratification for informed consent
    - Resource allocation and ICU bed planning
    - Multidisciplinary team consultation
    - Optimization of modifiable risk factors
    - Alternative treatment consideration for high-risk patients
    
    Quality Improvement:
    - Outcome benchmarking and comparison
    - Risk-adjusted mortality tracking
    - Surgical performance assessment
    - Program evaluation and improvement
    
    Patient Communication:
    - Informed consent discussions
    - Family counseling and expectation setting
    - Risk communication in understandable terms
    - Shared decision-making facilitation
    
    Model Validation and Performance:
    - Originally developed from 22,381 patients in 154 hospitals
    - Area under ROC curve: 0.8095 (excellent discrimination)
    - Well calibrated: predicted 3.95% vs actual 4.18% mortality
    - Represents 50% reduction in overestimation compared to original EuroSCORE
    - Contemporary surgical outcomes reflected
    
    Important Clinical Considerations:
    - Designed for in-hospital mortality prediction only
    - Does not predict long-term outcomes or quality of life
    - May require local calibration in specific populations
    - Should complement clinical judgment, not replace it
    - Not validated for transcatheter or minimally invasive procedures
    - Regular updates recommended as surgical practices evolve
    
    Limitations and Cautions:
    - Population-based model may not reflect individual patient factors
    - Based on 2010 data; surgical outcomes continue to improve
    - May overestimate risk in centers with superior outcomes
    - External validation shows variable performance across populations
    - Should be used as part of comprehensive risk assessment
    
    Reference: Nashef SA, et al. EuroSCORE II. Eur J Cardiothorac Surg. 2012;41(4):734-44.
    """
    
    result: float = Field(
        ...,
        description="Predicted in-hospital mortality risk as percentage (0-100%)",
        example=2.45
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for mortality risk (percentage)",
        example="percentage"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation including risk level, management recommendations, and expected outcomes",
        example="EuroSCORE II predicted in-hospital mortality: 2.45%. MEDIUM RISK for cardiac surgery. Enhanced perioperative monitoring and care planning recommended. Consider optimization of modifiable risk factors."
    )
    
    stage: str = Field(
        ...,
        description="Risk stratification level (Low Risk, Medium Risk, High Risk, Very High Risk)",
        example="Medium Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk level",
        example="Medium operative risk"
    )
    
    risk_category: str = Field(
        ...,
        description="Risk category classification based on mortality percentage",
        example="Medium Risk"
    )
    
    logistic_score: float = Field(
        ...,
        description="Logistic regression score (y value) used in mortality calculation",
        example=-3.8756
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 2.45,
                "unit": "percentage",
                "interpretation": "EuroSCORE II predicted in-hospital mortality: 2.45%. MEDIUM RISK for cardiac surgery. Enhanced perioperative monitoring and care planning recommended. Consider optimization of modifiable risk factors.",
                "stage": "Medium Risk",
                "stage_description": "Medium operative risk",
                "risk_category": "Medium Risk",
                "logistic_score": -3.8756
            }
        }