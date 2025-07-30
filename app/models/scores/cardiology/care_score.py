"""
Cardiac Anesthesia Risk Evaluation Score (CARE) Models

Request and response models for CARE Score calculation.

References (Vancouver style):
1. Dupuis JY, Wang F, Nathan H, Lam M, Grimes S, Bourke M. The cardiac anesthesia 
   risk evaluation score: a clinically useful predictor of mortality and morbidity 
   after cardiac surgery. Anesthesiology. 2001 Feb;94(2):194-204. 
   doi: 10.1097/00000542-200102000-00006.
2. Zingone B, Pappalardo A, Dreas L. Logistic versus clinical prediction models: 
   prognostic accuracy of the EuroSCORE and the cardiac anesthesia risk evaluation score. 
   Eur J Cardiothorac Surg. 2004 Nov;26(5):883-7. doi: 10.1016/j.ejcts.2004.07.014.
3. Ranucci M, Castelvecchio S, Menicanti L, Frigiola A, Pelissero G. A comparison of 
   the EuroSCORE and the Cardiac Anesthesia Risk Evaluation (CARE) score for risk-adjusted 
   mortality analysis in cardiac surgery. Eur J Cardiothorac Surg. 2012 Feb;41(2):307-13. 
   doi: 10.1016/j.ejcts.2011.05.043.

The CARE Score predicts mortality and morbidity after cardiac surgery using a simple 
clinical assessment based on cardiac disease status, medical comorbidities, surgical 
complexity, and urgency. It demonstrates excellent predictive performance with an 
AUC of 0.801 for mortality prediction.
"""

from pydantic import BaseModel, Field
from typing import Literal


class CareScoreRequest(BaseModel):
    """
    Request model for Cardiac Anesthesia Risk Evaluation Score (CARE)
    
    The CARE Score is a simple yet highly effective risk classification system 
    for cardiac surgical patients, providing excellent prognostic accuracy with 
    an area under the ROC curve of 0.801 for mortality prediction.
    
    The score is based on clinical judgment and five key variables:
    
    1. Cardiac Disease Status:
       - Stable: Well-compensated cardiac disease
       - Chronic/Advanced: Decompensated or end-stage cardiac disease
    
    2. Other Medical Problems:
       - None: No significant comorbidities
       - Controlled: Stable diabetes, hypertension, etc.
       - Uncontrolled: Pulmonary edema, renal insufficiency, etc.
    
    3. Surgery Complexity:
       - Noncomplex: Standard CABG, single valve replacement
       - Complex: Reoperation, combined procedures, multiple valves, etc.
    
    4. Emergency Surgery:
       - Required as soon as diagnosis made and OR available
    
    5. Last Hope Surgery:
       - Surgery performed as final attempt to save/improve life
    
    CARE Categories:
    - CARE 1: Stable cardiac, no problems, noncomplex surgery
    - CARE 2: Stable cardiac, controlled problems, noncomplex surgery  
    - CARE 3: Uncontrolled problems OR complex surgery
    - CARE 4: Uncontrolled problems AND complex surgery
    - CARE 5: Last hope surgery
    - CARE 6: Emergency + any CARE 5 situation
    
    Complex Surgery Examples:
    - Reoperation through scar tissue
    - Combined valve and coronary artery surgery
    - Multiple valve surgery (>1 valve)
    - Left ventricular aneurysmectomy
    - Repair of ventricular septal defect after MI
    - CABG of diffusely diseased or heavily calcified vessels
    
    Performance Characteristics:
    - Mortality prediction AUC: 0.801
    - Morbidity prediction AUC: 0.721
    - Comparable performance to complex multifactorial scores
    - Simple clinical assessment suitable for routine use
    
    References (Vancouver style):
    1. Dupuis JY, Wang F, Nathan H, Lam M, Grimes S, Bourke M. The cardiac anesthesia 
    risk evaluation score: a clinically useful predictor of mortality and morbidity 
    after cardiac surgery. Anesthesiology. 2001 Feb;94(2):194-204.
    """
    
    cardiac_disease_status: Literal["stable", "chronic_advanced"] = Field(
        ...,
        description="Status of cardiac disease: stable (well-compensated) or chronic_advanced (decompensated/end-stage)",
        example="stable"
    )
    
    other_medical_problems: Literal["none", "controlled", "uncontrolled"] = Field(
        ...,
        description="Other medical problems: none, controlled (stable diabetes/hypertension), or uncontrolled (pulmonary edema/renal insufficiency)",
        example="controlled"
    )
    
    surgery_complexity: Literal["noncomplex", "complex"] = Field(
        ...,
        description="Surgery complexity: noncomplex (standard CABG/single valve) or complex (reoperation/combined procedures/multiple valves)",
        example="noncomplex"
    )
    
    emergency_surgery: Literal["yes", "no"] = Field(
        ...,
        description="Emergency surgery required as soon as diagnosis is made and operating room is available. Adds +1 to final score if yes",
        example="no"
    )
    
    last_hope_surgery: Literal["yes", "no"] = Field(
        ...,
        description="Surgery performed as last hope to save or improve life (defines CARE 5 if yes)",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "cardiac_disease_status": "stable",
                "other_medical_problems": "controlled",
                "surgery_complexity": "noncomplex",
                "emergency_surgery": "no",
                "last_hope_surgery": "no"
            }
        }


class CareScoreResponse(BaseModel):
    """
    Response model for Cardiac Anesthesia Risk Evaluation Score (CARE)
    
    The CARE Score provides risk stratification for cardiac surgery patients 
    with excellent predictive accuracy and clinical utility:
    
    Risk Categories and Clinical Management:
    - CARE 1 (Very Low Risk): Standard perioperative care
    - CARE 2 (Low Risk): Enhanced monitoring based on comorbidities
    - CARE 3 (Moderate Risk): ICU monitoring, specialized anesthesia
    - CARE 4 (High Risk): Intensive monitoring, multidisciplinary approach
    - CARE 5 (Very High Risk): Maximum support, family counseling
    - CARE 6 (Extreme Risk): Emergency intervention, maximum support
    
    Clinical Applications:
    - Preoperative risk assessment and patient counseling
    - Resource allocation and staffing decisions
    - Quality assurance and outcome benchmarking
    - Research stratification for cardiac surgery studies
    
    Advantages:
    - Simple clinical assessment without complex calculations
    - Excellent inter-rater reliability across specialists
    - Comparable accuracy to complex multifactorial scores
    - Based on easily available clinical information
    - Suitable for routine clinical practice
    
    Morbidity Includes:
    - Cardiovascular: Low cardiac output, malignant arrhythmias
    - Respiratory: Prolonged ventilation >48h, tracheostomy
    - Neurologic: Stroke, irreversible encephalopathy
    - Renal: Acute renal failure requiring dialysis
    - Infectious: Septic shock, wound infections
    
    Reference: Dupuis JY, et al. Anesthesiology. 2001;94(2):194-204.
    """
    
    result: int = Field(
        ...,
        description="CARE Score category calculated from clinical assessment (range: 1 to 6)",
        example=2
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="category"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and perioperative management recommendations",
        example="Stable cardiac disease, one or more controlled medical problems, undergoing noncomplex surgery. Low risk with good prognosis. Enhanced monitoring may be considered based on specific comorbidities."
    )
    
    stage: str = Field(
        ...,
        description="CARE risk category (CARE 1 through CARE 6)",
        example="CARE 2"
    )
    
    stage_description: str = Field(
        ...,
        description="Risk level description",
        example="Low Risk"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 2,
                "unit": "category",
                "interpretation": "Stable cardiac disease, one or more controlled medical problems, undergoing noncomplex surgery. Low risk with good prognosis. Enhanced monitoring may be considered based on specific comorbidities.",
                "stage": "CARE 2",
                "stage_description": "Low Risk"
            }
        }