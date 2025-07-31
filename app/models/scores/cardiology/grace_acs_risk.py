"""
GRACE ACS Risk and Mortality Calculator Models

Request and response models for GRACE ACS Risk Score calculation.

References (Vancouver style):
1. Fox KA, Dabbous OH, Goldberg RJ, Pieper KS, Eagle KA, Van de Werf F, et al. 
   Prediction of risk of death and myocardial infarction in the six months after 
   presentation with acute coronary syndrome: prospective multinational observational 
   study (GRACE). BMJ. 2006;333(7578):1091. doi: 10.1136/bmj.38985.646481.55.
2. Granger CB, Goldberg RJ, Dabbous O, Pieper KS, Eagle KA, Cannon CP, et al. 
   Predictors of hospital mortality in the global registry of acute coronary events. 
   Arch Intern Med. 2003;163(19):2345-53. doi: 10.1001/archinte.163.19.2345.
3. Abu-Assi E, Gracía-Acuña JM, Peña-Gil C, González-Juanatey JR. Validation of 
   the GRACE risk score for predicting death within 6 months of follow-up in a 
   contemporary cohort of patients with acute coronary syndrome. Rev Esp Cardiol 
   (Engl Ed). 2010;63(6):640-8. doi: 10.1016/s1885-5857(10)70139-4.

The GRACE (Global Registry of Acute Coronary Events) ACS Risk Score is a validated 
tool for estimating admission to 6-month mortality risk in patients with acute coronary 
syndrome. It is one of the most widely used and well-validated risk stratification 
tools in cardiovascular medicine.

**Clinical Applications**:
1. **Risk Stratification**: Identifies high-risk patients requiring intensive monitoring
2. **Treatment Decisions**: Guides decisions about invasive vs. conservative strategies
3. **Resource Allocation**: Helps determine appropriate level of care and monitoring
4. **Prognostic Communication**: Provides evidence-based information for patients/families
5. **Quality Improvement**: Supports standardized ACS care protocols

**Scoring Components (8 Variables)**:
The GRACE score uses 8 clinical variables measured at hospital admission:

**Continuous Variables** (with specific point algorithms):
- **Age**: Higher age increases risk (approximately 2.5 points per year over 40)
- **Heart Rate**: Tachycardia increases risk (0-46 points based on ranges)
- **Systolic Blood Pressure**: Hypotension increases risk (0-58 points, inverse relationship)
- **Serum Creatinine**: Renal dysfunction increases risk (1-28 points based on ranges)

**Categorical Variables**:
- **Killip Class**: Heart failure signs (0-59 points)
  * Class I: No CHF (0 points)
  * Class II: Pulmonary rales or JVD (20 points)
  * Class III: Pulmonary edema (39 points)
  * Class IV: Cardiogenic shock (59 points)

**Binary Variables** (present/absent):
- **Cardiac Arrest at Admission**: 39 points if present
- **ST Segment Deviation**: 28 points if present  
- **Elevated Cardiac Biomarkers**: 14 points if present (troponin, CK-MB)

**Risk Categories and Mortality Estimates**:
- **Very Low Risk (0-87 points)**: 0-2% mortality
- **Low Risk (88-128 points)**: 3-10% mortality
- **Intermediate Risk (129-149 points)**: 10-20% mortality
- **High Risk (150-173 points)**: 20-30% mortality
- **Very High Risk (174-284 points)**: 40-90% mortality
- **Extremely High Risk (≥285 points)**: ≥99% mortality

**Clinical Decision-Making Framework**:
- **Low Risk**: Conservative management, early discharge consideration
- **Intermediate Risk**: Careful monitoring, selective invasive strategy
- **High/Very High Risk**: Intensive monitoring, aggressive interventions, early invasive strategy

**Important Clinical Considerations**:
- Validated in over 43,000 patients from 94 hospitals worldwide
- Applicable to both STEMI and NSTEMI patients
- Recommended by NICE guidelines for ACS risk stratification
- Should be used in conjunction with clinical judgment and patient preferences
- Higher scores indicate increased need for intensive care and invasive interventions
- Provides both in-hospital and 6-month mortality predictions

The GRACE score represents a cornerstone of evidence-based ACS management, helping 
clinicians make informed decisions about treatment intensity and resource allocation 
while providing prognostic information to patients and families.
"""

from pydantic import BaseModel, Field
from typing import Literal


class GraceAcsRiskRequest(BaseModel):
    """
    Request model for GRACE ACS Risk and Mortality Calculator
    
    The GRACE score uses 8 clinical variables to estimate admission to 6-month mortality 
    risk in patients with acute coronary syndrome. All parameters should be measured at 
    the time of hospital admission.
    
    **Clinical Variables**:
    
    **Age**: Patient age in years. Higher age is associated with increased mortality risk 
    in ACS patients. Age contributes significantly to the overall score with approximately 
    2.5 points per year above 40.
    
    **Heart Rate**: Heart rate in beats per minute at admission. Both very low and very 
    high heart rates are associated with increased mortality risk:
    - <50 bpm: 0 points
    - 50-69 bpm: 3 points
    - 70-89 bpm: 9 points
    - 90-109 bpm: 15 points
    - 110-149 bpm: 24 points
    - 150-199 bpm: 38 points
    - ≥200 bpm: 46 points
    
    **Systolic Blood Pressure**: Systolic BP in mmHg at admission. Lower BP is associated 
    with higher mortality risk (inverse relationship):
    - <80 mmHg: 58 points (highest risk)
    - 80-99 mmHg: 53 points
    - 100-119 mmHg: 43 points
    - 120-139 mmHg: 34 points
    - 140-159 mmHg: 24 points
    - 160-199 mmHg: 10 points
    - ≥200 mmHg: 0 points
    
    **Serum Creatinine**: Creatinine level in mg/dL. Renal dysfunction is associated 
    with increased mortality risk in ACS:
    - <0.40 mg/dL: 1 point
    - 0.40-0.79 mg/dL: 4 points
    - 0.80-1.19 mg/dL: 7 points
    - 1.20-1.59 mg/dL: 10 points
    - 1.60-1.99 mg/dL: 13 points
    - 2.00-3.99 mg/dL: 21 points
    - ≥4.00 mg/dL: 28 points
    
    **Killip Class**: Classification based on signs of congestive heart failure:
    - class_1: No CHF (0 points)
    - class_2: Pulmonary rales and/or jugular venous distention (20 points)
    - class_3: Acute pulmonary edema (39 points)
    - class_4: Cardiogenic shock (59 points)
    
    **Cardiac Arrest**: Cardiac arrest at admission (39 points if present). This includes 
    ventricular fibrillation, ventricular tachycardia, or asystole requiring resuscitation.
    
    **ST Segment Deviation**: ST segment elevation or depression on admission ECG 
    (28 points if present). Indicates significant coronary artery occlusion or severe ischemia.
    
    **Elevated Cardiac Biomarkers**: Elevated troponin, CK-MB, or other cardiac enzymes 
    (14 points if present). Indicates myocardial necrosis and confirmed myocardial infarction.

    References (Vancouver style):
    1. Fox KA, Dabbous OH, Goldberg RJ, Pieper KS, Eagle KA, Van de Werf F, et al. 
    Prediction of risk of death and myocardial infarction in the six months after 
    presentation with acute coronary syndrome: prospective multinational observational 
    study (GRACE). BMJ. 2006;333(7578):1091. doi: 10.1136/bmj.38985.646481.55.
    2. Granger CB, Goldberg RJ, Dabbous O, Pieper KS, Eagle KA, Cannon CP, et al. 
    Predictors of hospital mortality in the global registry of acute coronary events. 
    Arch Intern Med. 2003;163(19):2345-53. doi: 10.1001/archinte.163.19.2345.
    """
    
    age: int = Field(
        ...,
        description="Patient age in years. Higher age increases mortality risk in ACS patients",
        ge=20,
        le=100,
        example=65
    )
    
    heart_rate: int = Field(
        ...,
        description="Heart rate in beats per minute at admission. Both very low and very high heart rates increase mortality risk",
        ge=30,
        le=250,
        example=85
    )
    
    systolic_bp: int = Field(
        ...,
        description="Systolic blood pressure in mmHg at admission. Lower BP is associated with higher mortality risk",
        ge=50,
        le=300,
        example=130
    )
    
    creatinine: float = Field(
        ...,
        description="Serum creatinine level in mg/dL. Renal dysfunction increases mortality risk in ACS patients",
        ge=0.3,
        le=15.0,
        example=1.2
    )
    
    killip_class: Literal["class_1", "class_2", "class_3", "class_4"] = Field(
        ...,
        description="Killip classification based on signs of congestive heart failure. Class I (no CHF), Class II (rales/JVD), Class III (pulmonary edema), Class IV (cardiogenic shock)",
        example="class_1"
    )
    
    cardiac_arrest: Literal["yes", "no"] = Field(
        ...,
        description="Cardiac arrest at admission (VF, VT, or asystole requiring resuscitation). Scores 39 points if present",
        example="no"
    )
    
    st_deviation: Literal["yes", "no"] = Field(
        ...,
        description="ST segment elevation or depression on admission ECG indicating significant coronary occlusion or severe ischemia. Scores 28 points if present",
        example="yes"
    )
    
    elevated_biomarkers: Literal["yes", "no"] = Field(
        ...,
        description="Elevated cardiac enzymes/biomarkers (troponin, CK-MB) indicating myocardial necrosis. Scores 14 points if present",
        example="yes"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": 65,
                "heart_rate": 85,
                "systolic_bp": 130,
                "creatinine": 1.2,
                "killip_class": "class_1",
                "cardiac_arrest": "no",
                "st_deviation": "yes",
                "elevated_biomarkers": "yes"
            }
        }


class GraceAcsRiskResponse(BaseModel):
    """
    Response model for GRACE ACS Risk and Mortality Calculator
    
    Provides the calculated GRACE score with mortality risk category and clinical 
    management recommendations based on validated risk thresholds.
    
    **Risk Categories and Clinical Implications**:
    
    **Very Low Risk (0-87 points, 0-2% mortality)**:
    - Excellent prognosis with very low risk of adverse outcomes
    - Patients may be suitable for early discharge and conservative management
    - Consider outpatient follow-up with cardiology
    - Standard medical therapy is appropriate
    
    **Low Risk (88-128 points, 3-10% mortality)**:
    - Good prognosis with low risk of adverse outcomes  
    - Standard care with consideration for early invasive strategy based on other factors
    - Appropriate for step-down unit care
    - Continue evidence-based medical therapy and monitor response
    
    **Intermediate Risk (129-149 points, 10-20% mortality)**:
    - Moderate prognosis requiring careful monitoring
    - Consider invasive management strategies
    - Early cardiology consultation recommended
    - Intensive medical therapy and frequent reassessment
    
    **High Risk (150-173 points, 20-30% mortality)**:
    - Poor prognosis with significant mortality risk
    - Intensive monitoring and aggressive interventional therapy indicated
    - Immediate cardiology consultation and invasive strategy
    - ICU-level care may be appropriate
    
    **Very High Risk (174-284 points, 40-90% mortality)**:
    - Very poor prognosis with high mortality risk
    - Immediate intensive care and aggressive interventional strategies required
    - Emergency cardiology consultation and immediate invasive management
    - Consider transfer to tertiary center with interventional capabilities
    
    **Extremely High Risk (≥285 points, ≥99% mortality)**:
    - Critical prognosis with extremely high mortality risk
    - Maximum intensive care and immediate life-saving interventions required
    - Emergency interventional cardiology consultation
    - Consider all therapeutic options including mechanical circulatory support
    
    **Clinical Decision-Making Guidelines**:
    - Use in conjunction with clinical judgment and patient preferences
    - Consider patient comorbidities and overall clinical picture
    - Higher scores indicate increased need for intensive monitoring and invasive interventions
    - Provides evidence-based framework for treatment intensity decisions
    - Supports communication with patients and families about prognosis
    
    Reference: Fox KA, et al. BMJ. 2006;333(7578):1091.
    """
    
    result: int = Field(
        ...,
        description="GRACE ACS Risk Score calculated from weighted clinical variables (range: 0-400+ points)",
        ge=0,
        le=500,
        example=142
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the GRACE score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including parameter summary, GRACE score, risk category, mortality estimate, and specific clinical management recommendations",
        example="Clinical parameters: Age 65 years, HR 85 bpm, SBP 130 mmHg, Creatinine 1.2 mg/dL, Killip Class I (No CHF), Cardiac arrest: no, ST deviation: yes, Elevated biomarkers: yes. GRACE Score: 142 points. Risk category: Intermediate Risk (10-20% mortality). Clinical recommendations: Intermediate mortality risk (10-20%). Requires careful monitoring and consideration for invasive management strategies. Consider early cardiology consultation. Intensive medical therapy and frequent reassessment recommended. Important note: Use in conjunction with clinical judgment and consider patient comorbidities, preferences, and overall clinical picture when making treatment decisions."
    )
    
    stage: str = Field(
        ...,
        description="Mortality risk category (Very Low Risk, Low Risk, Intermediate Risk, High Risk, Very High Risk, Extremely High Risk)",
        example="Intermediate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the prognosis category",
        example="Moderate prognosis"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 142,
                "unit": "points",
                "interpretation": "Clinical parameters: Age 65 years, HR 85 bpm, SBP 130 mmHg, Creatinine 1.2 mg/dL, Killip Class I (No CHF), Cardiac arrest: no, ST deviation: yes, Elevated biomarkers: yes. GRACE Score: 142 points. Risk category: Intermediate Risk (10-20% mortality). Clinical recommendations: Intermediate mortality risk (10-20%). Requires careful monitoring and consideration for invasive management strategies. Consider early cardiology consultation. Intensive medical therapy and frequent reassessment recommended. Important note: Use in conjunction with clinical judgment and consider patient comorbidities, preferences, and overall clinical picture when making treatment decisions.",
                "stage": "Intermediate Risk",
                "stage_description": "Moderate prognosis"
            }
        }