"""
Gupta Postoperative Pneumonia Risk Models

Request and response models for Gupta Postoperative Pneumonia Risk calculation.

References (Vancouver style):
1. Gupta H, Gupta PK, Fang X, et al. Development and validation of a risk calculator 
   for predicting postoperative pneumonia. Mayo Clin Proc. 2013;88(11):1241-1249. 
   doi: 10.1016/j.mayocp.2013.06.027
2. American College of Surgeons National Surgical Quality Improvement Program. 
   ACS NSQIP Risk Calculator. https://riskcalculator.facs.org/
3. Smetana GW, Lawrence VA, Cornell JE. American College of Physicians. 
   Preoperative pulmonary risk stratification for noncardiothoracic surgery: 
   systematic review for the American College of Physicians. Ann Intern Med. 
   2006;144(8):581-595. doi: 10.7326/0003-4819-144-8-200604180-00007

The Gupta Postoperative Pneumonia Risk calculator is a validated tool that predicts 
the probability of pneumonia within 30 days after surgery. This calculator was 
developed using the American College of Surgeons' National Surgical Quality 
Improvement Program (ACS NSQIP) multicenter, prospective data set and demonstrates 
excellent predictive performance with a C-statistic of 0.860.

**Clinical Background**:
Postoperative pneumonia is a serious complication that occurs in approximately 1.8% 
of surgical patients and is associated with significantly higher 30-day mortality 
(17.0% vs 1.5% in patients without pneumonia). Accurate risk prediction enables 
clinicians to implement targeted prevention strategies, optimize perioperative care, 
and improve patient outcomes through evidence-based interventions.

**Development and Validation**:
The calculator was developed using 211,410 patients from the 2007 ACS NSQIP database 
as the training set and validated on 257,385 patients from the 2008 database. Seven 
preoperative predictors were identified through multivariate logistic regression 
analysis, creating a highly accurate prediction model that outperforms clinical 
judgment alone for pneumonia risk assessment.

**Seven Key Risk Factors**:

**1. Age** (Continuous Variable):
- **Points**: 0.0144 points per year of age
- **Clinical Significance**: Advanced age is associated with decreased immune function, 
  reduced respiratory muscle strength, impaired cough reflex, and increased susceptibility 
  to respiratory infections
- **Considerations**: Each year of age incrementally increases pneumonia risk due to 
  age-related physiological changes and comorbidity accumulation

**2. Chronic Obstructive Pulmonary Disease (COPD)**:
- **No COPD**: -0.4553 points (protective factor)
- **COPD Present**: 0.0 points (reference category)
- **Clinical Significance**: COPD patients have compromised lung function, impaired 
  secretion clearance, increased bacterial colonization, and reduced respiratory reserve
- **Assessment**: Based on documented diagnosis, spirometry results, or clinical history 
  of chronic bronchitis, emphysema, or obstructive lung disease

**3. Functional Status** (Activities of Daily Living):
- **Independent**: 0.0 points - Can perform all ADLs without assistance
- **Partially Dependent**: 0.7653 points - Requires assistance with some ADLs
- **Totally Dependent**: 0.9400 points - Requires assistance with all ADLs
- **Clinical Significance**: Functional status reflects overall health, mobility, 
  and ability to perform pulmonary hygiene measures such as deep breathing and coughing

**4. ASA Physical Status Classification**:
- **ASA I** (-3.0225 points): Normal healthy patient without systemic disease
- **ASA II** (-1.6057 points): Patient with mild systemic disease (controlled hypertension, 
  diabetes without complications, mild obesity)
- **ASA III** (-0.4915 points): Patient with severe systemic disease that limits activity 
  but is not incapacitating (uncontrolled diabetes, moderate heart disease)
- **ASA IV** (0.0123 points): Patient with severe systemic disease that is a constant 
  threat to life (severe heart disease, advanced renal failure)
- **ASA V** (0.0 points): Moribund patient not expected to survive without operation
- **Clinical Significance**: Higher ASA classes indicate greater systemic illness, 
  reduced physiologic reserve, and increased susceptibility to complications

**5. Preoperative Sepsis Status**:
- **None** (-0.7641 points): No signs of systemic inflammatory response or infection
- **SIRS** (0.0 points): Systemic Inflammatory Response Syndrome (reference category)
- **Sepsis** (-0.0842 points): SIRS with documented or suspected infection
- **Septic Shock** (0.1048 points): Sepsis with hypotension despite adequate fluid resuscitation
- **Clinical Significance**: Preoperative infection and systemic inflammation increase 
  susceptibility to postoperative complications and compromise immune function

**6. Smoking Within Last Year**:
- **No Smoking** (-0.4306 points): No tobacco use within 12 months (protective factor)
- **Current Smoking** (0.0 points): Tobacco use within 12 months (reference category)
- **Clinical Significance**: Smoking impairs ciliary function, increases secretions, 
  compromises immune function, and delays wound healing. Even recent smoking cessation 
  provides some protective benefit

**7. Type of Surgical Procedure** (Procedure-Specific Risk):
Surgical procedures are categorized by inherent pneumonia risk based on anatomical 
location, duration, invasiveness, and impact on respiratory function:

**Highest Risk Procedures**:
- **Aortic Surgery** (0.7178 points): Major vascular surgery with significant physiologic stress
- **Brain Surgery** (0.6405 points): Intracranial procedures with potential neurological complications
- **Cardiac Surgery** (0.4492 points): Cardiothoracic procedures with cardiopulmonary bypass

**High Risk Procedures**:
- **Thoracic Non-Cardiac** (0.2806 points): Lung and chest wall surgery directly affecting respiration
- **Neck Surgery** (0.1633 points): Head and neck procedures potentially affecting airway
- **Peripheral Vascular** (0.1382 points): Non-aortic vascular procedures

**Moderate Risk Procedures**:
- **Foregut/Hepatobiliary** (0.1239 points): Upper abdominal surgery affecting diaphragmatic function
- **Gallbladder/Appendix/Adrenals/Spleen** (0.0823 points): Intra-abdominal procedures
- **Intestinal Surgery** (0.0645 points): Bowel surgery with potential complications
- **Orthopedic Non-Spine** (0.0189 points): Joint and bone surgery

**Low Risk Procedures**:
- **Renal Surgery** (-0.0234 points): Kidney procedures
- **Spine Surgery** (-0.0689 points): Spinal procedures
- **Urology Non-Renal** (-0.1347 points): Urologic procedures excluding kidney
- **Hernia Repair** (-0.1456 points): Hernia surgery
- **Obstetric/Gynecologic** (-0.1789 points): Reproductive system surgery

**Lowest Risk Procedures**:
- **Skin Surgery** (-0.3254 points): Superficial procedures
- **Thyroid/Parathyroid** (-0.5632 points): Endocrine surgery
- **Vein Surgery** (-0.8945 points): Superficial vein procedures
- **Breast Surgery** (-2.3318 points): Breast procedures (lowest risk)

**Risk Calculation Formula**:
The calculator uses logistic regression: **Risk (%) = e^x / (1 + e^x) × 100**
Where: **x = -2.8977 + (age × 0.0144) + COPD_points + functional_status_points + ASA_points + sepsis_points + smoking_points + procedure_points**

**Clinical Risk Categories and Management**:

**Very Low Risk (0.0-1.0%)**:
- **Clinical Approach**: Standard perioperative care and monitoring
- **Interventions**: Routine pulmonary hygiene, early mobilization, standard pain management
- **Monitoring**: Standard nursing assessments and vital signs
- **Discharge**: Standard discharge criteria and follow-up

**Low Risk (1.0-3.0%)**:
- **Clinical Approach**: Standard care with enhanced pulmonary awareness
- **Interventions**: Incentive spirometry, deep breathing exercises, early ambulation
- **Monitoring**: Attention to respiratory symptoms and adequate pain control
- **Education**: Patient education about importance of pulmonary hygiene

**Moderate Risk (3.0-6.0%)**:
- **Clinical Approach**: Enhanced pulmonary care and closer monitoring
- **Interventions**: Chest physiotherapy, aggressive incentive spirometry protocols
- **Monitoring**: More frequent respiratory assessments, oxygen saturation monitoring
- **Consultations**: Consider respiratory therapy consultation
- **Pain Management**: Optimize pain control to facilitate coughing and mobility

**High Risk (6.0-15.0%)**:
- **Clinical Approach**: Aggressive pneumonia prevention strategies
- **Preoperative**: Consider pulmonary rehabilitation, smoking cessation programs
- **Interventions**: Intensive chest physiotherapy, respiratory therapy protocols
- **Monitoring**: Enhanced respiratory monitoring, consider pulmonology consultation
- **Postoperative**: Extended monitoring period, prompt evaluation of respiratory symptoms

**Very High Risk (>15.0%)**:
- **Clinical Approach**: Comprehensive pulmonary optimization and intensive monitoring
- **Preoperative**: Consider postponing elective surgery for optimization
- **Optimization**: Pulmonary rehabilitation, treatment of respiratory infections
- **Monitoring**: ICU-level respiratory monitoring, intensive pulmonary care protocols
- **Team Approach**: Multidisciplinary team including pulmonology, respiratory therapy
- **Discharge**: Extended hospitalization, intensive outpatient follow-up

**Clinical Applications**:

**Preoperative Assessment**:
- Risk stratification for surgical planning and resource allocation
- Patient and family counseling with specific risk percentages
- Decision-making for preoperative pulmonary optimization
- Determination of appropriate level of postoperative monitoring

**Perioperative Management**:
- Selection of pneumonia prevention interventions and monitoring intensity
- Respiratory therapy consultation decisions and protocols
- Pulmonology consultation decisions for high-risk patients
- Postoperative care planning and surveillance strategies

**Quality Improvement**:
- Benchmarking institutional pneumonia rates and prevention programs
- Identification of high-risk populations for targeted interventions
- Resource planning and cost-effectiveness analysis of prevention strategies
- Clinical pathway development and standardization of care protocols

**Prevention Strategies by Risk Level**:
- **All Patients**: Early mobilization, adequate pain control, smoking cessation counseling
- **Moderate Risk**: Incentive spirometry, chest physiotherapy, respiratory therapy consultation
- **High Risk**: Preoperative pulmonary rehabilitation, intensive postoperative monitoring
- **Very High Risk**: Comprehensive optimization, consider surgery delay for elective procedures

**Important Clinical Considerations**:
- Calculator provides probability estimates based on population data
- Should complement comprehensive clinical assessment and judgment
- Individual patient factors may modify risk beyond model predictions
- Urgent/emergent surgery may require risk acceptance despite high scores
- Regular reassessment may be needed for changing clinical conditions

**Limitations**:
- Does not include all potential risk factors such as specific comorbidities
- May not fully capture complexity of certain patient populations or procedures
- Should be used as part of comprehensive perioperative assessment
- Developed primarily in general surgical populations

This calculator represents a significant advance in evidence-based perioperative medicine, 
providing clinicians with an accurate, practical tool for pneumonia risk assessment that 
enhances patient care and clinical decision-making.
"""

from pydantic import BaseModel, Field, validator
from typing import Literal


class GuptaPostoperativePneumoniaRiskRequest(BaseModel):
    """
    Request model for Gupta Postoperative Pneumonia Risk Calculator
    
    The Gupta Postoperative Pneumonia Risk calculator uses seven validated preoperative 
    risk factors to predict 30-day postoperative pneumonia risk. All parameters should 
    be assessed preoperatively for accurate risk stratification.
    
    **Age**: Continuous risk factor with 0.0144 points per year. Advanced age is associated 
    with decreased immune function, reduced respiratory muscle strength, and impaired cough reflex.
    
    **Chronic Obstructive Pulmonary Disease (COPD)**:
    - **No**: Absence of COPD (protective factor, -0.4553 points)
    - **Yes**: Documented COPD diagnosis (reference category, 0.0 points)
    COPD assessment based on documented diagnosis, spirometry, or clinical history of 
    chronic bronchitis, emphysema, or obstructive lung disease.
    
    **Functional Status** (Activities of Daily Living Assessment):
    - **Independent**: Can perform all activities of daily living without assistance (0.0 points)
    - **Partially Dependent**: Requires assistance with some but not all ADLs (0.7653 points)
    - **Totally Dependent**: Requires assistance with all activities of daily living (0.9400 points)
    Functional status reflects overall health, mobility, and ability to perform pulmonary 
    hygiene measures such as deep breathing and effective coughing.
    
    **ASA Physical Status Classification** (American Society of Anesthesiologists):
    - **Class I** (-3.0225 points): Normal healthy patient without systemic disease
    - **Class II** (-1.6057 points): Patient with mild systemic disease (controlled hypertension, 
      uncomplicated diabetes, mild obesity)
    - **Class III** (-0.4915 points): Patient with severe systemic disease that limits activity 
      but is not incapacitating (uncontrolled diabetes, moderate heart disease)
    - **Class IV** (0.0123 points): Patient with severe systemic disease that is a constant 
      threat to life (severe heart disease, advanced renal failure)
    - **Class V** (0.0 points): Moribund patient not expected to survive without operation
    
    **Preoperative Sepsis Status**:
    - **None** (-0.7641 points): No signs of systemic inflammatory response or infection
    - **SIRS** (0.0 points): Systemic Inflammatory Response Syndrome (reference category)
    - **Sepsis** (-0.0842 points): SIRS with documented or suspected infection
    - **Septic Shock** (0.1048 points): Sepsis with hypotension despite adequate fluid resuscitation
    
    **Smoking Within Last Year**:
    - **No** (-0.4306 points): No tobacco use within 12 months (protective factor)
    - **Yes** (0.0 points): Tobacco use within 12 months (reference category)
    Smoking impairs ciliary function, increases secretions, and compromises immune function.
    
    **Surgical Procedure Type** (Procedure-Specific Risk Classification):
    Surgical procedures are categorized by inherent pneumonia risk based on anatomical 
    location, duration, invasiveness, and impact on respiratory function. Risk ranges 
    from highest (aortic surgery) to lowest (breast surgery).
    
    References (Vancouver style):
    1. Gupta H, Gupta PK, Fang X, et al. Development and validation of a risk calculator 
    for predicting postoperative pneumonia. Mayo Clin Proc. 2013;88(11):1241-1249. 
    doi: 10.1016/j.mayocp.2013.06.027
    2. American College of Surgeons National Surgical Quality Improvement Program. 
    ACS NSQIP Risk Calculator. https://riskcalculator.facs.org/
    """
    
    age: int = Field(
        ...,
        description="Patient age in years. Each year adds 0.0144 points to pneumonia risk score. Advanced age increases risk due to decreased immune function and respiratory muscle strength",
        ge=18,
        le=120,
        example=68
    )
    
    copd: Literal["no", "yes"] = Field(
        ...,
        description="Presence of chronic obstructive pulmonary disease. No COPD: -0.4553 pts (protective), COPD present: 0 pts. Based on documented diagnosis, spirometry, or clinical history",
        example="no"
    )
    
    functional_status: Literal["independent", "partially_dependent", "totally_dependent"] = Field(
        ...,
        description="Functional status based on activities of daily living. Independent: 0 pts, Partially dependent: 0.7653 pts, Totally dependent: 0.9400 pts",
        example="independent"
    )
    
    asa_class: Literal["1", "2", "3", "4", "5"] = Field(
        ...,
        description="ASA Physical Status Classification. Class 1: -3.0225 pts (healthy), Class 2: -1.6057 pts (mild disease), Class 3: -0.4915 pts (severe disease), Class 4: 0.0123 pts (life-threatening), Class 5: 0 pts (moribund)",
        example="2"
    )
    
    sepsis_status: Literal["none", "sirs", "sepsis", "septic_shock"] = Field(
        ...,
        description="Preoperative sepsis status. None: -0.7641 pts, SIRS: 0 pts (reference), Sepsis: -0.0842 pts, Septic shock: 0.1048 pts",
        example="none"
    )
    
    smoking: Literal["no", "yes"] = Field(
        ...,
        description="Smoking within the last year before operation. No smoking: -0.4306 pts (protective), Current smoking: 0 pts (reference)",
        example="no"
    )
    
    procedure_type: Literal[
        "aortic", "brain", "breast", "cardiac", "foregut_hepatobiliary",
        "gallbladder_appendix_adrenals_spleen", "intestinal", "neck",
        "obstetric_gynecologic", "orthopedic_non_spine", "peripheral_vascular",
        "renal", "skin", "spine", "thoracic_non_cardiac", "thyroid_parathyroid",
        "urology_non_renal", "vein", "hernia"
    ] = Field(
        ...,
        description="Type of surgical procedure. Risk ranges from aortic surgery (0.7178 pts, highest risk) to breast surgery (-2.3318 pts, lowest risk)",
        example="hernia"
    )
    
    @validator('age')
    def validate_age(cls, v):
        if v < 18 or v > 120:
            raise ValueError('Age must be between 18 and 120 years')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "age": 68,
                "copd": "no",
                "functional_status": "independent",
                "asa_class": "2",
                "sepsis_status": "none",
                "smoking": "no",
                "procedure_type": "hernia"
            }
        }


class GuptaPostoperativePneumoniaRiskResponse(BaseModel):
    """
    Response model for Gupta Postoperative Pneumonia Risk Calculator
    
    Provides the calculated pneumonia risk percentage with comprehensive clinical 
    interpretation and management recommendations based on validated perioperative 
    outcomes data from ACS NSQIP.
    
    **Risk Categories and Clinical Management**:
    
    **Very Low Risk (0.0-1.0%)**:
    - **Clinical Approach**: Standard perioperative care and monitoring
    - **Interventions**: Routine pulmonary hygiene measures, early mobilization
    - **Monitoring**: Standard nursing assessments and vital signs monitoring
    - **Discharge**: Standard discharge criteria and routine follow-up
    
    **Low Risk (1.0-3.0%)**:
    - **Clinical Approach**: Standard care with enhanced pulmonary awareness
    - **Interventions**: Incentive spirometry, deep breathing exercises, early ambulation
    - **Monitoring**: Attention to respiratory symptoms and adequate pain control
    - **Education**: Patient education about importance of pulmonary hygiene measures
    
    **Moderate Risk (3.0-6.0%)**:
    - **Clinical Approach**: Enhanced pulmonary care and closer respiratory monitoring
    - **Interventions**: Chest physiotherapy, aggressive incentive spirometry protocols
    - **Monitoring**: More frequent respiratory assessments, oxygen saturation monitoring
    - **Consultations**: Consider respiratory therapy consultation for specialized care
    - **Pain Management**: Optimize pain control to facilitate effective coughing and mobility
    
    **High Risk (6.0-15.0%)**:
    - **Clinical Approach**: Aggressive pneumonia prevention strategies and intensive monitoring
    - **Preoperative**: Consider pulmonary rehabilitation programs, smoking cessation interventions
    - **Interventions**: Intensive chest physiotherapy, specialized respiratory therapy protocols
    - **Monitoring**: Enhanced respiratory monitoring, consider pulmonology consultation
    - **Postoperative**: Extended monitoring period, prompt evaluation of respiratory symptoms
    
    **Very High Risk (>15.0%)**:
    - **Clinical Approach**: Comprehensive pulmonary optimization and intensive monitoring
    - **Preoperative**: Consider postponing elective surgery for pulmonary optimization
    - **Optimization**: Pulmonary rehabilitation, treatment of active respiratory infections
    - **Monitoring**: ICU-level respiratory monitoring, intensive pulmonary care protocols
    - **Team Approach**: Multidisciplinary team including pulmonology and respiratory therapy
    - **Discharge**: Extended hospitalization with intensive outpatient follow-up
    
    **Pneumonia Prevention Strategies by Risk Level**:
    
    **All Patients**: 
    - Early mobilization and ambulation protocols
    - Adequate pain control to facilitate deep breathing and coughing
    - Smoking cessation counseling and support
    - Patient education about pulmonary hygiene importance
    
    **Moderate to High Risk Patients**:
    - Incentive spirometry with structured protocols
    - Chest physiotherapy and postural drainage techniques
    - Respiratory therapy consultation and specialized interventions
    - Enhanced monitoring for early detection of respiratory complications
    
    **Very High Risk Patients**:
    - Preoperative pulmonary rehabilitation when feasible
    - Intensive postoperative respiratory monitoring and support
    - Consider postponing elective procedures for optimization
    - Multidisciplinary team approach with pulmonology involvement
    
    **Quality Improvement Applications**:
    - **Risk Stratification**: Systematic identification of high-risk patients for targeted interventions
    - **Resource Allocation**: Appropriate allocation of respiratory therapy and monitoring resources  
    - **Patient Safety**: Proactive implementation of evidence-based pneumonia prevention strategies
    - **Clinical Pathways**: Development of risk-stratified care protocols and standardized interventions
    - **Outcome Tracking**: Benchmarking and continuous quality improvement initiatives
    
    **Important Clinical Considerations**:
    - Calculator provides probability estimates based on validated population data
    - Should complement comprehensive clinical assessment and professional judgment
    - Individual patient factors may modify risk beyond model predictions
    - Urgent/emergent surgery may require risk acceptance despite high predicted risk
    - Patient preferences and values should be incorporated into decision-making
    - Regular reassessment may be needed for changing clinical conditions
    
    **Limitations to Consider**:
    - Does not include all potential pneumonia risk factors or specific comorbidities
    - May not fully capture complexity of certain patient populations or specialized procedures
    - Developed primarily in general surgical populations, may have limitations in specialty surgery
    - Should be used as part of comprehensive perioperative assessment, not as sole decision-making tool
    
    **Clinical Impact**:
    Postoperative pneumonia occurs in approximately 1.8% of surgical patients and is 
    associated with significantly higher 30-day mortality (17.0% vs 1.5% in patients 
    without pneumonia). This calculator enables targeted prevention strategies that can 
    significantly improve patient outcomes and reduce healthcare costs.
    
    Reference: Gupta H, et al. Mayo Clin Proc. 2013;88(11):1241-1249.
    """
    
    result: float = Field(
        ...,
        description="Predicted risk percentage of postoperative pneumonia within 30 days of surgery",
        ge=0.0,
        le=100.0,
        example=2.45
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the pneumonia risk calculation",
        example="percentage"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including patient characteristics, risk percentage, risk category, and specific clinical recommendations for pneumonia prevention and perioperative management",
        example="Patient characteristics: 68 years old, no COPD, functionally independent, ASA Class II (mild systemic disease), no sepsis, non-smoker, undergoing hernia repair. Gupta Postoperative Pneumonia Risk: 2.45% risk of pneumonia within 30 days after surgery. Risk Category: Low Risk (Low pneumonia risk). Clinical recommendations: Low risk of postoperative pneumonia. Standard care with attention to pulmonary hygiene and early mobilization. Consider incentive spirometry, deep breathing exercises, and adequate pain control to facilitate coughing and ambulation. Important considerations: This calculator predicts postoperative pneumonia risk based on validated ACS NSQIP data. Pneumonia is associated with significantly increased 30-day mortality (17.0% vs 1.5%). Use in conjunction with clinical judgment for surgical decision-making and targeted prevention strategies. Consider individual patient factors such as recent respiratory infections, medication compliance, and surgical urgency when making final management decisions."
    )
    
    stage: str = Field(
        ...,
        description="Risk category classification (Very Low Risk, Low Risk, Moderate Risk, High Risk, Very High Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the pneumonia risk category",
        example="Low pneumonia risk"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 2.45,
                "unit": "percentage",
                "interpretation": "Patient characteristics: 68 years old, no COPD, functionally independent, ASA Class II (mild systemic disease), no sepsis, non-smoker, undergoing hernia repair. Gupta Postoperative Pneumonia Risk: 2.45% risk of pneumonia within 30 days after surgery. Risk Category: Low Risk (Low pneumonia risk). Clinical recommendations: Low risk of postoperative pneumonia. Standard care with attention to pulmonary hygiene and early mobilization. Consider incentive spirometry, deep breathing exercises, and adequate pain control to facilitate coughing and ambulation. Important considerations: This calculator predicts postoperative pneumonia risk based on validated ACS NSQIP data. Pneumonia is associated with significantly increased 30-day mortality (17.0% vs 1.5%). Use in conjunction with clinical judgment for surgical decision-making and targeted prevention strategies. Consider individual patient factors such as recent respiratory infections, medication compliance, and surgical urgency when making final management decisions.",
                "stage": "Low Risk",
                "stage_description": "Low pneumonia risk"
            }
        }