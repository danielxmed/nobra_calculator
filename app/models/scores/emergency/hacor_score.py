"""
HACOR Score Models

Request and response models for HACOR Score calculation.

References (Vancouver style):
1. Duan J, Han X, Bai L, Zhou L, Huang S. Assessment of heart rate, acidosis, 
   consciousness, oxygenation, and respiratory rate to predict noninvasive ventilation 
   failure in hypoxemic patients. Intensive Care Med. 2017;43(2):192-199. 
   doi: 10.1007/s00134-016-4601-3
2. Liu J, Duan J, Bai L, Zhou L. Noninvasive Ventilation Intolerance: Characteristics, 
   Predictors, and Outcomes. Respir Care. 2016;61(3):277-284. doi: 10.4187/respcare.04220
3. Carrillo A, Gonzalez-Diaz G, Ferrer M, et al. Non-invasive ventilation in 
   community-acquired pneumonia and severe acute respiratory failure. Intensive Care Med. 
   2012;38(3):458-466. doi: 10.1007/s00134-012-2504-9

The HACOR Score predicts non-invasive ventilation (NIV) failure in hypoxemic patients 
and stands for Heart rate, Acidosis, Consciousness, Oxygenation, and Respiratory rate. 
This validated clinical tool helps clinicians make informed decisions about respiratory 
support management and the timing of potential intubation in critically ill patients.

**Clinical Background**:
Non-invasive ventilation has become a cornerstone of respiratory support for patients 
with acute hypoxemic respiratory failure. However, NIV failure occurs in approximately 
40-50% of patients and is associated with increased mortality, particularly when 
intubation is delayed. Early identification of patients at high risk for NIV failure 
is crucial for optimizing outcomes and resource allocation in intensive care settings.

**Development and Validation**:
The HACOR score was derived from a prospective cohort of 449 hypoxemic patients 
receiving NIV and validated in 358 additional patients. The score demonstrated 
excellent discriminative ability with an area under the receiver operating 
characteristic curve (AUC) of 0.88-0.90 across different validation cohorts. 
The score is most predictive when assessed 60 minutes after NIV initiation.

**Five Key Components**:

**1. Heart Rate (H)**:
- **Clinical Significance**: Tachycardia may indicate increased metabolic demands, 
  hemodynamic instability, or inadequate respiratory support
- **Scoring**: 
  - ≤120 beats/min: 0 points
  - ≥121 beats/min: 1 point
- **Assessment**: Measured at the time of evaluation, typically 60 minutes after NIV initiation

**2. Acidosis (A) - pH**:
- **Clinical Significance**: Acidosis reflects inadequate ventilation, metabolic 
  derangements, or both, and is a strong predictor of respiratory failure
- **Scoring**:
  - ≥7.35: 0 points (normal to mild alkalosis)
  - 7.30-7.34: 2 points (mild acidosis)
  - 7.25-7.29: 3 points (moderate acidosis)
  - <7.25: 4 points (severe acidosis)
- **Assessment**: Arterial blood gas pH measurement
- **Clinical Context**: Progressive acidosis indicates worsening respiratory or metabolic failure

**3. Consciousness (C) - Glasgow Coma Scale**:
- **Clinical Significance**: Altered consciousness may indicate hypercapnia, hypoxemia, 
  or underlying neurological compromise affecting respiratory drive
- **Scoring**:
  - 15: 0 points (normal consciousness)
  - 13-14: 2 points (mild alteration)
  - 11-12: 5 points (moderate alteration)
  - ≤10: 10 points (severe alteration)
- **Assessment**: Standard Glasgow Coma Scale evaluation
- **Clinical Context**: Decreased consciousness may compromise NIV tolerance and effectiveness

**4. Oxygenation (O) - PaO₂/FiO₂ Ratio**:
- **Clinical Significance**: The PaO₂/FiO₂ ratio reflects the severity of oxygenation 
  impairment and lung injury
- **Scoring**:
  - ≥201 mmHg: 0 points (mild impairment)
  - 176-200 mmHg: 2 points (moderate impairment)
  - 151-175 mmHg: 3 points (moderate-severe impairment)
  - 126-150 mmHg: 4 points (severe impairment)
  - 101-125 mmHg: 5 points (very severe impairment)
  - ≤100 mmHg: 6 points (critical impairment)
- **Assessment**: Arterial PaO₂ divided by fraction of inspired oxygen (FiO₂)
- **Clinical Context**: Lower ratios indicate more severe acute lung injury

**5. Respiratory Rate (R)**:
- **Clinical Significance**: Tachypnea may indicate increased work of breathing, 
  inadequate ventilatory support, or respiratory muscle fatigue
- **Scoring**:
  - ≤30 breaths/min: 0 points (normal to mild tachypnea)
  - 31-35 breaths/min: 1 point (moderate tachypnea)
  - 36-40 breaths/min: 2 points (severe tachypnea)
  - 41-45 breaths/min: 3 points (very severe tachypnea)
  - ≥46 breaths/min: 4 points (extreme tachypnea)
- **Assessment**: Respiratory rate measurement during NIV support
- **Clinical Context**: Progressive tachypnea may indicate impending respiratory failure

**Risk Categories and Clinical Management**:

**Low Risk (Score ≤5)**:
- **NIV Failure Risk**: <20% probability
- **Clinical Approach**: Continue NIV with standard monitoring
- **Management**: 
  - Maintain current NIV settings with routine optimization
  - Standard ICU monitoring protocols
  - Regular assessment of patient comfort and synchrony
  - Periodic reassessment of HACOR score (12, 24, 48 hours)
- **Follow-up**: Monitor for clinical deterioration, gas exchange worsening

**High Risk (Score >5)**:
- **NIV Failure Risk**: >50% probability  
- **Clinical Approach**: Consider early intubation within 12 hours
- **Management**:
  - Intensive monitoring with immediate intubation readiness
  - Ensure availability of experienced personnel and equipment
  - ICU or HDU-level care if not already provided
  - Optimize NIV settings while preparing for potential intubation
  - Close monitoring for respiratory fatigue, worsening hypoxemia
- **Outcome Impact**: Early intubation associated with reduced hospital mortality

**Clinical Applications**:

**Decision Support**:
- **Timing of Assessment**: Most predictive when evaluated 60 minutes after NIV initiation
- **Intubation Timing**: Helps identify patients who benefit from early intubation
- **Resource Allocation**: Guides intensity of monitoring and staffing requirements
- **Quality Improvement**: Standardizes NIV failure prediction across providers

**Patient Populations**:
- **Primary Indications**: Acute hypoxemic respiratory failure requiring NIV
- **Validated Conditions**: Pneumonia, ARDS, COPD exacerbations, cardiogenic pulmonary edema
- **Setting**: Intensive care units, emergency departments, respiratory care units
- **Exclusions**: Patients with contraindications to NIV or those requiring immediate intubation

**Advantages of HACOR Score**:
- **Objective**: Uses readily available physiological parameters
- **Validated**: Demonstrated accuracy across multiple patient populations
- **Practical**: Simple bedside calculation with immediate results
- **Predictive**: High discriminative ability (AUC 0.88-0.90)
- **Actionable**: Provides clear risk stratification for clinical decision-making

**Important Clinical Considerations**:
- **Timing**: Optimal assessment at 1 hour after NIV initiation
- **Dynamic Assessment**: Patient condition may change, requiring reassessment
- **Clinical Judgment**: Score should complement comprehensive patient evaluation
- **Institutional Factors**: Consider local expertise and resources in decision-making
- **Patient Preferences**: Incorporate goals of care discussions when appropriate

**Limitations**:
- **Single Time Point**: May not capture dynamic changes in patient condition
- **Population Specific**: Validated primarily in ICU populations with specific conditions
- **Operator Dependent**: Requires accurate assessment of clinical parameters
- **External Factors**: Does not account for NIV equipment quality or patient tolerance

**Research and Evidence**:
The HACOR score represents a significant advance in evidence-based respiratory care, 
providing objective criteria for NIV failure prediction. Multiple validation studies 
have confirmed its accuracy across diverse patient populations and clinical settings. 
The score has been incorporated into clinical protocols and guidelines for NIV management, 
supporting standardized approaches to respiratory failure care.

This calculator enables clinicians to make informed, evidence-based decisions about 
respiratory support strategies, optimize resource utilization, and improve patient 
outcomes through appropriate timing of respiratory interventions.
"""

from pydantic import BaseModel, Field, validator
from typing import Literal


class HacorScoreRequest(BaseModel):
    """
    Request model for HACOR Score Calculator
    
    The HACOR Score predicts non-invasive ventilation (NIV) failure in hypoxemic 
    patients using five readily available clinical parameters: Heart rate, Acidosis, 
    Consciousness, Oxygenation, and Respiratory rate. This tool should be used in 
    critically ill patients with acute hypoxic respiratory failure who require NIV.
    
    **Heart Rate**: Tachycardia (>120 bpm) may indicate increased metabolic demands, 
    hemodynamic instability, or inadequate respiratory support. Higher heart rates 
    contribute to increased risk of NIV failure.
    
    **Acidosis (pH)**: Arterial blood gas pH reflects ventilatory adequacy and 
    metabolic status. Progressive acidosis is a strong predictor of respiratory 
    failure and NIV ineffectiveness. More severe acidosis significantly increases 
    the risk of NIV failure.
    
    **Consciousness (Glasgow Coma Scale)**: Altered consciousness may indicate 
    hypercapnia, hypoxemia, or neurological compromise affecting respiratory drive. 
    Decreased GCS scores are associated with poor NIV tolerance and higher failure rates.
    
    **Oxygenation (PaO₂/FiO₂ Ratio)**: This ratio reflects the severity of oxygenation 
    impairment and acute lung injury. Lower ratios indicate more severe respiratory 
    failure and higher likelihood of NIV failure.
    
    **Respiratory Rate**: Tachypnea may indicate increased work of breathing, inadequate 
    ventilatory support, or impending respiratory muscle fatigue. Higher respiratory 
    rates are associated with increased NIV failure risk.
    
    **Clinical Application**:
    - Best used in critically ill patients with acute hypoxic respiratory failure requiring NIV
    - Should be assessed 60 minutes after initiating NIV for optimal predictive accuracy
    - Score >5 indicates high risk of NIV failure (>50% probability)
    - Score ≤5 indicates low risk of NIV failure (<20% probability)
    - Early intubation in high-risk patients may reduce hospital mortality
    
    References (Vancouver style):
    1. Duan J, Han X, Bai L, Zhou L, Huang S. Assessment of heart rate, acidosis, 
    consciousness, oxygenation, and respiratory rate to predict noninvasive ventilation 
    failure in hypoxemic patients. Intensive Care Med. 2017;43(2):192-199. 
    doi: 10.1007/s00134-016-4601-3
    2. Liu J, Duan J, Bai L, Zhou L. Noninvasive Ventilation Intolerance: Characteristics, 
    Predictors, and Outcomes. Respir Care. 2016;61(3):277-284. doi: 10.4187/respcare.04220
    """
    
    heart_rate: int = Field(
        ...,
        description="Heart rate in beats per minute. Tachycardia >120 bpm indicates increased metabolic demands or hemodynamic instability",
        ge=30,
        le=250,
        example=135
    )
    
    ph: float = Field(
        ...,
        description="Arterial blood gas pH value. Lower pH values indicate acidosis and are associated with higher NIV failure risk",
        ge=6.8,
        le=7.8,
        example=7.28
    )
    
    gcs: int = Field(
        ...,
        description="Glasgow Coma Scale score (3-15). Lower GCS scores indicate altered consciousness and poor NIV tolerance",
        ge=3,
        le=15,
        example=13
    )
    
    pao2_fio2_ratio: int = Field(
        ...,
        description="PaO₂/FiO₂ ratio in mmHg. Lower ratios indicate more severe oxygenation impairment and acute lung injury",
        ge=50,
        le=600,
        example=145
    )
    
    respiratory_rate: int = Field(
        ...,
        description="Respiratory rate in breaths per minute. Higher rates indicate increased work of breathing or respiratory muscle fatigue",
        ge=8,
        le=80,
        example=38
    )
    
    @validator('heart_rate')
    def validate_heart_rate(cls, v):
        if v < 30 or v > 250:
            raise ValueError('Heart rate must be between 30 and 250 bpm')
        return v
    
    @validator('ph')
    def validate_ph(cls, v):
        if v < 6.8 or v > 7.8:
            raise ValueError('pH must be between 6.8 and 7.8')
        return v
    
    @validator('gcs')
    def validate_gcs(cls, v):
        if v < 3 or v > 15:
            raise ValueError('Glasgow Coma Scale must be between 3 and 15')
        return v
    
    @validator('pao2_fio2_ratio')
    def validate_pao2_fio2_ratio(cls, v):
        if v < 50 or v > 600:
            raise ValueError('PaO₂/FiO₂ ratio must be between 50 and 600 mmHg')
        return v
    
    @validator('respiratory_rate')
    def validate_respiratory_rate(cls, v):
        if v < 8 or v > 80:
            raise ValueError('Respiratory rate must be between 8 and 80 breaths/min')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "heart_rate": 135,
                "ph": 7.28,
                "gcs": 13,
                "pao2_fio2_ratio": 145,
                "respiratory_rate": 38
            }
        }


class HacorScoreResponse(BaseModel):
    """
    Response model for HACOR Score Calculator
    
    Provides the calculated HACOR score with comprehensive clinical interpretation 
    and management recommendations for predicting non-invasive ventilation (NIV) 
    failure in hypoxemic patients.
    
    **Score Interpretation and Clinical Management**:
    
    **Low Risk (Score ≤5)**:
    - **NIV Failure Risk**: Less than 20% probability
    - **Clinical Approach**: Continue NIV with standard monitoring protocols
    - **Management Recommendations**:
      - Maintain current NIV settings with routine optimization for patient comfort
      - Standard ICU monitoring with regular assessment of gas exchange
      - Periodic reassessment of HACOR score at 12, 24, and 48 hours
      - Monitor for clinical deterioration including worsening oxygenation or increased work of breathing
      - Patient education about NIV compliance and comfort measures
    - **Follow-up**: Standard respiratory care protocols with routine evaluation
    
    **High Risk (Score >5)**:
    - **NIV Failure Risk**: Greater than 50% probability
    - **Clinical Approach**: Consider early intubation within 12 hours to reduce mortality
    - **Management Recommendations**:
      - Intensive monitoring with immediate preparation for intubation
      - Ensure availability of experienced personnel and intubation equipment
      - ICU or high-dependency unit level care if not already provided
      - Optimize NIV settings (pressure support, PEEP, FiO₂) while preparing for potential intubation
      - Close monitoring for signs of respiratory fatigue, worsening hypoxemia, or hemodynamic compromise
      - Consider cardiothoracic or critical care consultation for complex cases
    - **Evidence**: Early intubation in high-risk patients associated with improved survival outcomes
    
    **Clinical Applications**:
    - **Decision Support**: Provides objective criteria for respiratory management decisions
    - **Resource Allocation**: Guides appropriate intensity of monitoring and staffing
    - **Quality Improvement**: Standardizes NIV failure prediction across healthcare providers
    - **Patient Safety**: Enables proactive identification of patients requiring escalation of care
    
    **Important Clinical Considerations**:
    - **Optimal Timing**: Score is most predictive when assessed 60 minutes after NIV initiation
    - **Dynamic Assessment**: Patient condition may change requiring periodic reassessment
    - **Validated Populations**: Demonstrated accuracy in pneumonia, ARDS, COPD, and cardiogenic pulmonary edema
    - **Clinical Context**: Should be used in conjunction with comprehensive patient evaluation
    - **Institutional Factors**: Consider local expertise, resources, and protocols
    - **Patient Preferences**: Incorporate goals of care discussions when making management decisions
    
    **Limitations to Consider**:
    - **Single Assessment**: May not capture dynamic changes in patient condition over time
    - **Population Specific**: Validated primarily in ICU populations with specific conditions
    - **Technical Factors**: Requires accurate measurement and assessment of clinical parameters
    - **External Variables**: Does not account for NIV equipment quality, patient tolerance, or comfort
    - **Clinical Judgment**: Should complement rather than replace comprehensive clinical evaluation
    
    **Research Foundation**:
    The HACOR score was derived from prospective cohorts totaling over 800 patients 
    and demonstrates excellent discriminative ability (AUC 0.88-0.90) for predicting 
    NIV failure. Multiple validation studies have confirmed its accuracy across diverse 
    patient populations and clinical settings, making it a valuable evidence-based 
    tool for respiratory care decision-making.
    
    Reference: Duan J, et al. Intensive Care Med. 2017;43(2):192-199.
    """
    
    result: int = Field(
        ...,
        description="HACOR score points (0-28 range) calculated from the five clinical parameters",
        ge=0,
        le=28,
        example=9
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the HACOR score calculation",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including patient characteristics, score value, risk assessment, and specific clinical recommendations for NIV management",
        example="Patient characteristics: Heart rate 135 bpm, pH 7.28, GCS 13, PaO₂/FiO₂ ratio 145 mmHg, respiratory rate 38 breaths/min. HACOR Score: 9 points. Risk Category: High Risk (High risk of NIV failure). Clinical recommendations: High risk of non-invasive ventilation failure (HACOR score: 9 points, >5 = high risk). Greater than 50% probability of NIV failure. Clinical recommendations: Consider early intubation within 12 hours to reduce hospital mortality risk. Intensive monitoring is essential with preparation for mechanical ventilation. Ensure immediate availability of intubation equipment and experienced personnel. Consider ICU or HDU-level care if not already provided. Optimize NIV settings (pressure support, PEEP, FiO₂) while preparing for potential intubation. Monitor closely for signs of respiratory fatigue, worsening hypoxemia, or hemodynamic compromise. Early intubation in high-risk patients has been associated with improved survival outcomes compared to delayed intubation. Important considerations: The HACOR score should be assessed 60 minutes after initiating NIV for optimal predictive accuracy. This score has been validated in patients with various causes of hypoxemic respiratory failure including pneumonia, ARDS, and COPD exacerbations. The score demonstrates good discriminative ability with AUC 0.88-0.90 in validation studies. Clinical judgment should always be used in conjunction with the HACOR score for respiratory management decisions. Reassessment at regular intervals is recommended as patient condition may change during the course of treatment."
    )
    
    stage: str = Field(
        ...,
        description="Risk category classification (Low Risk, High Risk)",
        example="High Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the NIV failure risk category",
        example="High risk of NIV failure"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 9,
                "unit": "points",
                "interpretation": "Patient characteristics: Heart rate 135 bpm, pH 7.28, GCS 13, PaO₂/FiO₂ ratio 145 mmHg, respiratory rate 38 breaths/min. HACOR Score: 9 points. Risk Category: High Risk (High risk of NIV failure). Clinical recommendations: High risk of non-invasive ventilation failure (HACOR score: 9 points, >5 = high risk). Greater than 50% probability of NIV failure. Clinical recommendations: Consider early intubation within 12 hours to reduce hospital mortality risk. Intensive monitoring is essential with preparation for mechanical ventilation. Ensure immediate availability of intubation equipment and experienced personnel. Consider ICU or HDU-level care if not already provided. Optimize NIV settings (pressure support, PEEP, FiO₂) while preparing for potential intubation. Monitor closely for signs of respiratory fatigue, worsening hypoxemia, or hemodynamic compromise. Early intubation in high-risk patients has been associated with improved survival outcomes compared to delayed intubation. Important considerations: The HACOR score should be assessed 60 minutes after initiating NIV for optimal predictive accuracy. This score has been validated in patients with various causes of hypoxemic respiratory failure including pneumonia, ARDS, and COPD exacerbations. The score demonstrates good discriminative ability with AUC 0.88-0.90 in validation studies. Clinical judgment should always be used in conjunction with the HACOR score for respiratory management decisions. Reassessment at regular intervals is recommended as patient condition may change during the course of treatment.",
                "stage": "High Risk",
                "stage_description": "High risk of NIV failure"
            }
        }