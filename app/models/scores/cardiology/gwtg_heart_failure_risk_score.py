"""
GWTG-Heart Failure Risk Score Models

Request and response models for GWTG-Heart Failure Risk Score calculation.

References (Vancouver style):
1. Peterson PN, Rumsfeld JS, Liang L, et al. A validated risk score for in-hospital 
   mortality in patients with heart failure from the American Heart Association get 
   with the guidelines program. Circ Cardiovasc Qual Outcomes. 2010;3(1):25-32. 
   doi: 10.1161/CIRCOUTCOMES.109.854877
2. Fonarow GC, Adams KF Jr, Abraham WT, Yancy CW, Boscardin WJ; ADHERE Scientific 
   Advisory Committee, Study Group, and Investigators. Risk stratification for 
   in-hospital mortality in acutely decompensated heart failure: classification 
   and regression tree analysis. JAMA. 2005;293(5):572-580.
3. American Heart Association Get With The Guidelines - Heart Failure Program. 
   https://www.heart.org/en/professional/quality-improvement/get-with-the-guidelines

The GWTG-Heart Failure Risk Score is a validated tool that predicts all-cause 
in-hospital mortality in admitted patients with heart failure. This calculator was 
developed using the American Heart Association Get With The Guidelines-Heart Failure 
(GWTG-HF) program data from 39,783 patients from 198 hospitals and demonstrates 
good discriminative ability with a C-index of 0.75.

**Clinical Background**:
Heart failure is a leading cause of hospitalization and mortality in adults, with 
in-hospital mortality rates averaging 2.86% across diverse patient populations. 
Accurate risk prediction enables clinicians to identify high-risk patients who may 
benefit from intensive monitoring, advanced therapies, and appropriate resource 
allocation while facilitating informed discussions with patients and families about 
prognosis and care goals.

**Development and Validation**:
The GWTG-HF risk score was derived and validated using data from patients admitted 
between January 1, 2005, and June 26, 2007, with the cohort divided into derivation 
(70%, n=27,850) and validation (30%, n=11,933) samples. The model demonstrated 
consistent performance across both datasets and showed good discrimination with 
predicted mortality varying more than 24-fold across score deciles (range, 0.4% to 9.7%).

**Seven Key Risk Factors**:

**1. Age** (Continuous Variable):
- **Clinical Significance**: Advanced age is associated with reduced physiologic reserve, 
  increased comorbidities, and higher mortality risk in heart failure patients
- **Scoring**: Each year above 65 contributes incrementally to the risk score
- **Considerations**: Age reflects accumulated cardiovascular damage and reduced 
  adaptive capacity to hemodynamic stress

**2. Systolic Blood Pressure**:
- **Clinical Significance**: Lower systolic blood pressure indicates reduced cardiac 
  output, hemodynamic compromise, and cardiogenic shock risk
- **Scoring**: Values below 140 mmHg contribute to higher risk scores, with lower 
  pressures indicating greater severity
- **Assessment**: Measured on admission, reflects acute hemodynamic status and 
  cardiac contractile function

**3. Blood Urea Nitrogen (BUN)**:
- **Clinical Significance**: Elevated BUN indicates renal dysfunction, often reflecting 
  cardiorenal syndrome, volume overload, or reduced renal perfusion
- **Scoring**: Values above 20 mg/dL increase risk score proportionally
- **Clinical Context**: BUN elevation in heart failure often indicates more severe 
  disease with worse prognosis and increased mortality risk

**4. Heart Rate**:
- **Clinical Significance**: Elevated heart rate may indicate compensatory tachycardia, 
  increased sympathetic activation, or hemodynamic instability
- **Scoring**: Values above 70 bpm contribute to higher risk scores
- **Assessment**: Reflects autonomic nervous system activation and cardiovascular 
  stress response to reduced cardiac output

**5. Serum Sodium**:
- **Clinical Significance**: Hyponatremia in heart failure indicates neurohormonal 
  activation, volume overload, and dilutional effects
- **Scoring**: Values below 140 mEq/L increase risk score, with lower levels indicating 
  greater severity
- **Prognostic Impact**: Hyponatremia is strongly associated with increased mortality 
  and longer hospital stays in heart failure patients

**6. Chronic Obstructive Pulmonary Disease (COPD)**:
- **Present** (+2 points): Documented history of COPD
- **Absent** (0 points): No history of COPD
- **Clinical Significance**: COPD complicates heart failure management, increases 
  respiratory complications, and is associated with worse outcomes
- **Assessment**: Based on documented diagnosis, spirometry results, or clinical 
  history of chronic bronchitis or emphysema

**7. Race** (Black vs. Non-Black):
- **Black Race** (+1 point): Protective factor in this scoring system
- **Non-Black Race** (+4 points): Higher risk category
- **Clinical Significance**: Reflects population-based differences in heart failure 
  outcomes, potentially related to genetic, social, and healthcare access factors
- **Considerations**: This factor was identified in the original validation study 
  and should be interpreted within the context of comprehensive patient assessment

**Risk Calculation**:
The score ranges from 0-100 points, calculated by summing contributions from all 
seven variables. The final score corresponds to specific mortality risk categories 
with associated clinical management recommendations.

**Clinical Risk Categories and Management**:

**Very Low Risk (Score 0-33, <1% Mortality)**:
- **Clinical Approach**: Standard heart failure care protocols and monitoring
- **Management**: Evidence-based heart failure medications, fluid management, patient education
- **Discharge Planning**: Standard follow-up within 7-14 days, routine cardiology referral
- **Monitoring**: Standard vital signs, daily weights, symptom assessment

**Low Risk (Score 34-50, 1-5% Mortality)**:
- **Clinical Approach**: Standard care with optimization of heart failure therapy
- **Management**: Maximize guideline-directed medical therapy, attention to volume status
- **Discharge Planning**: Enhanced patient education, follow-up within 1-2 weeks
- **Monitoring**: Standard monitoring with attention to medication adherence and symptoms

**Moderate Risk (Score 51-57, 5-15% Mortality)**:
- **Clinical Approach**: Enhanced monitoring and aggressive heart failure management
- **Management**: Optimize diuretics, vasodilators, and neurohormonal blockade
- **Consultations**: Consider cardiology consultation, advanced heart failure evaluation
- **Discharge Planning**: Close outpatient follow-up within 3-7 days, medication reconciliation

**High Risk (Score 58-70, 15-30% Mortality)**:
- **Clinical Approach**: Intensive monitoring and consideration of advanced therapies
- **Management**: Evaluate for advanced heart failure interventions, inotropic support
- **Consultations**: Cardiology consultation, consider advanced heart failure referral
- **Care Planning**: Initiate palliative care discussions, assess for mechanical support

**Very High Risk (Score >70, >30% Mortality)**:
- **Clinical Approach**: Intensive care management with advanced therapies
- **Management**: ICU-level monitoring, inotropic support, mechanical circulatory support evaluation
- **Consultations**: Advanced heart failure specialist, palliative care involvement
- **Care Planning**: Comprehensive end-of-life care planning, family discussions

**Clinical Applications**:

**Risk Stratification**:
- Systematic identification of high-risk patients requiring intensive management
- Resource allocation decisions for monitoring intensity and specialized care
- Prognostic information for clinical decision-making and care planning
- Quality improvement initiatives and outcome prediction

**Patient and Family Communication**:
- Evidence-based prognostic information for informed consent discussions
- Risk-benefit analysis for advanced therapies and interventions
- Care goal discussions and advance directive planning
- Realistic expectation setting for hospitalization outcomes

**Quality Improvement**:
- Benchmarking institutional heart failure mortality rates
- Identification of patient populations for targeted interventions
- Resource planning and cost-effectiveness analysis
- Clinical pathway development and standardization

**Important Clinical Considerations**:
- Calculator provides probability estimates based on validated population data
- Should complement comprehensive clinical assessment and professional judgment
- Individual patient factors may modify risk beyond model predictions
- Score is applicable to both preserved and reduced ejection fraction heart failure
- Regular reassessment may be needed for changing clinical conditions
- Consider social determinants of health and individual patient preferences

**Limitations**:
- Does not include echocardiographic parameters or detailed hemodynamic data
- May not fully capture complexity of certain patient populations or comorbidities
- Race-based adjustment requires careful interpretation in clinical context
- Should be used as part of comprehensive heart failure assessment
- Developed primarily in hospitalized patients, may have limitations in other settings

**Research and Validation**:
The GWTG-Heart Failure Risk Score has been extensively validated across diverse 
clinical settings including cardiac intensive care units, general cardiology populations, 
and various procedural contexts. It represents a significant advance in evidence-based 
heart failure risk assessment and has been incorporated into major clinical guidelines 
and quality improvement initiatives.

This calculator enables clinicians to provide evidence-based prognostic information, 
make informed decisions about care intensity, and facilitate appropriate discussions 
with patients and families about goals of care and treatment options.
"""

from pydantic import BaseModel, Field, validator
from typing import Literal


class GwtgHeartFailureRiskScoreRequest(BaseModel):
    """
    Request model for GWTG-Heart Failure Risk Score Calculator
    
    The GWTG-Heart Failure Risk Score uses seven validated clinical variables 
    to predict in-hospital mortality in heart failure patients. All parameters 
    should be assessed on admission for accurate risk stratification.
    
    **Age**: Continuous risk factor with incremental contribution above 65 years. 
    Advanced age reflects reduced physiologic reserve and increased comorbidities.
    
    **Systolic Blood Pressure**: Lower values indicate hemodynamic compromise and 
    increased mortality risk. Values below 140 mmHg contribute to higher risk scores.
    
    **Blood Urea Nitrogen (BUN)**: Elevated values indicate renal dysfunction and 
    cardiorenal syndrome. Values above 20 mg/dL increase risk proportionally.
    
    **Heart Rate**: Elevated rates may indicate compensatory tachycardia or 
    hemodynamic instability. Values above 70 bpm contribute to higher scores.
    
    **Serum Sodium**: Lower values indicate neurohormonal activation and volume 
    overload. Hyponatremia below 140 mEq/L increases mortality risk.
    
    **Chronic Obstructive Pulmonary Disease (COPD)**:
    - **No**: Absence of COPD (0 points)
    - **Yes**: Documented COPD history (+2 points)
    COPD complicates heart failure management and is associated with worse outcomes.
    
    **Race** (Black vs. Non-Black):
    - **No**: Non-Black race (+4 points)
    - **Yes**: Black race (+1 point, protective factor)
    Reflects population-based differences in heart failure outcomes identified 
    in the original validation study.
    
    References (Vancouver style):
    1. Peterson PN, Rumsfeld JS, Liang L, et al. A validated risk score for in-hospital 
    mortality in patients with heart failure from the American Heart Association get 
    with the guidelines program. Circ Cardiovasc Qual Outcomes. 2010;3(1):25-32. 
    doi: 10.1161/CIRCOUTCOMES.109.854877
    2. American Heart Association Get With The Guidelines - Heart Failure Program. 
    https://www.heart.org/en/professional/quality-improvement/get-with-the-guidelines
    """
    
    age: int = Field(
        ...,
        description="Patient age in years. Advanced age increases mortality risk due to reduced physiologic reserve and increased comorbidities",
        ge=18,
        le=120,
        example=72
    )
    
    systolic_bp: int = Field(
        ...,
        description="Systolic blood pressure in mmHg on admission. Lower values indicate hemodynamic compromise and increased risk",
        ge=50,
        le=300,
        example=110
    )
    
    bun: int = Field(
        ...,
        description="Blood urea nitrogen in mg/dL. Elevated values indicate renal dysfunction and cardiorenal syndrome, increasing mortality risk",
        ge=5,
        le=200,
        example=35
    )
    
    heart_rate: int = Field(
        ...,
        description="Heart rate in beats per minute. Elevated rates may indicate compensatory tachycardia or hemodynamic instability",
        ge=30,
        le=200,
        example=95
    )
    
    sodium: int = Field(
        ...,
        description="Serum sodium in mEq/L. Lower values indicate neurohormonal activation and volume overload, associated with worse outcomes",
        ge=110,
        le=160,
        example=138
    )
    
    copd: Literal["no", "yes"] = Field(
        ...,
        description="History of chronic obstructive pulmonary disease. COPD complicates heart failure management and increases mortality risk. No: 0 pts, Yes: +2 pts",
        example="no"
    )
    
    black_race: Literal["no", "yes"] = Field(
        ...,
        description="Patient race (Black vs. Non-Black). Non-Black: +4 pts, Black: +1 pt (protective factor identified in original validation)",
        example="no"
    )
    
    @validator('age')
    def validate_age(cls, v):
        if v < 18 or v > 120:
            raise ValueError('Age must be between 18 and 120 years')
        return v
    
    @validator('systolic_bp')
    def validate_systolic_bp(cls, v):
        if v < 50 or v > 300:
            raise ValueError('Systolic BP must be between 50 and 300 mmHg')
        return v
    
    @validator('bun')
    def validate_bun(cls, v):
        if v < 5 or v > 200:
            raise ValueError('BUN must be between 5 and 200 mg/dL')
        return v
    
    @validator('heart_rate')
    def validate_heart_rate(cls, v):
        if v < 30 or v > 200:
            raise ValueError('Heart rate must be between 30 and 200 bpm')
        return v
    
    @validator('sodium')
    def validate_sodium(cls, v):
        if v < 110 or v > 160:
            raise ValueError('Sodium must be between 110 and 160 mEq/L')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "age": 72,
                "systolic_bp": 110,
                "bun": 35,
                "heart_rate": 95,
                "sodium": 138,
                "copd": "no",
                "black_race": "no"
            }
        }


class GwtgHeartFailureRiskScoreResponse(BaseModel):
    """
    Response model for GWTG-Heart Failure Risk Score Calculator
    
    Provides the calculated in-hospital mortality risk percentage with comprehensive 
    clinical interpretation and management recommendations based on validated 
    outcomes data from the AHA Get With The Guidelines-Heart Failure program.
    
    **Risk Categories and Clinical Management**:
    
    **Very Low Risk (<1% Mortality)**:
    - **Clinical Approach**: Standard heart failure care protocols and monitoring
    - **Management**: Evidence-based heart failure medications, standard fluid management
    - **Discharge Planning**: Routine follow-up within 7-14 days, standard patient education
    - **Monitoring**: Standard vital signs, daily weights, symptom assessment
    
    **Low Risk (1-5% Mortality)**:
    - **Clinical Approach**: Standard care with optimization of heart failure therapy
    - **Management**: Maximize guideline-directed medical therapy, optimize volume status
    - **Discharge Planning**: Enhanced patient education, follow-up within 1-2 weeks
    - **Monitoring**: Standard monitoring with attention to medication adherence
    
    **Moderate Risk (5-15% Mortality)**:
    - **Clinical Approach**: Enhanced monitoring and aggressive heart failure management
    - **Management**: Optimize diuretics, vasodilators, and neurohormonal blockade
    - **Consultations**: Consider cardiology consultation, advanced heart failure evaluation
    - **Discharge Planning**: Close outpatient follow-up within 3-7 days
    
    **High Risk (15-30% Mortality)**:
    - **Clinical Approach**: Intensive monitoring and consideration of advanced therapies
    - **Management**: Evaluate for advanced heart failure interventions, inotropic support
    - **Consultations**: Cardiology consultation, consider advanced heart failure referral
    - **Care Planning**: Initiate palliative care discussions, assess for mechanical support
    
    **Very High Risk (>30% Mortality)**:
    - **Clinical Approach**: Intensive care management with advanced therapies
    - **Management**: ICU-level monitoring, inotropic support, mechanical support evaluation
    - **Consultations**: Advanced heart failure specialist, palliative care involvement
    - **Care Planning**: Comprehensive end-of-life planning, family discussions
    
    **Clinical Applications**:
    - **Risk Stratification**: Systematic identification of high-risk patients for intensive management
    - **Resource Allocation**: Appropriate allocation of monitoring and specialized care resources
    - **Patient Communication**: Evidence-based prognostic information for informed discussions
    - **Quality Improvement**: Benchmarking and targeted interventions for high-risk populations
    
    **Important Clinical Considerations**:
    - Calculator provides probability estimates based on validated population data from 39,783 patients
    - Should complement comprehensive clinical assessment and professional judgment
    - Score is applicable to both preserved and reduced ejection fraction heart failure
    - Individual patient factors may modify risk beyond model predictions
    - Consider social determinants of health and patient preferences in care planning
    - Regular reassessment may be needed for changing clinical conditions
    
    **Limitations to Consider**:
    - Does not include echocardiographic parameters or detailed hemodynamic data
    - May not fully capture complexity of certain patient populations or comorbidities
    - Race-based adjustment requires careful interpretation in clinical context
    - Should be used as part of comprehensive heart failure assessment
    - Developed primarily in hospitalized patients, may have limitations in other settings
    
    Reference: Peterson PN, et al. Circ Cardiovasc Qual Outcomes. 2010;3(1):25-32.
    """
    
    result: float = Field(
        ...,
        description="Predicted in-hospital mortality risk percentage for heart failure patients",
        ge=0.0,
        le=100.0,
        example=8.5
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the mortality risk calculation",
        example="percentage"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including patient characteristics, risk percentage, risk category, and specific clinical recommendations for heart failure management",
        example="Patient characteristics: 72 years old, systolic BP 110 mmHg, BUN 35 mg/dL, heart rate 95 bpm, sodium 138 mEq/L, no COPD, non-Black race. GWTG-HF Score: 58 points. Predicted in-hospital mortality risk: 8.5%. Risk Category: Moderate Risk (Moderate mortality risk). Clinical recommendations: Moderate risk of in-hospital mortality (5-15%). Consider enhanced monitoring and aggressive heart failure management. Optimize diuretics, vasodilators, and neurohormonal blockade. Consider cardiology consultation, advanced heart failure evaluation, and closer outpatient follow-up within 3-7 days. Important considerations: The GWTG-HF risk score provides validated in-hospital mortality prediction for heart failure patients. This score is applicable to patients with both preserved and reduced ejection fraction. Use in conjunction with clinical judgment for comprehensive heart failure management, advanced therapy consideration, and care planning discussions with patients and families."
    )
    
    stage: str = Field(
        ...,
        description="Risk category classification (Very Low Risk, Low Risk, Moderate Risk, High Risk, Very High Risk)",
        example="Moderate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the mortality risk category",
        example="Moderate mortality risk"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 8.5,
                "unit": "percentage",
                "interpretation": "Patient characteristics: 72 years old, systolic BP 110 mmHg, BUN 35 mg/dL, heart rate 95 bpm, sodium 138 mEq/L, no COPD, non-Black race. GWTG-HF Score: 58 points. Predicted in-hospital mortality risk: 8.5%. Risk Category: Moderate Risk (Moderate mortality risk). Clinical recommendations: Moderate risk of in-hospital mortality (5-15%). Consider enhanced monitoring and aggressive heart failure management. Optimize diuretics, vasodilators, and neurohormonal blockade. Consider cardiology consultation, advanced heart failure evaluation, and closer outpatient follow-up within 3-7 days. Important considerations: The GWTG-HF risk score provides validated in-hospital mortality prediction for heart failure patients. This score is applicable to patients with both preserved and reduced ejection fraction. Use in conjunction with clinical judgment for comprehensive heart failure management, advanced therapy consideration, and care planning discussions with patients and families.",
                "stage": "Moderate Risk",
                "stage_description": "Moderate mortality risk"
            }
        }