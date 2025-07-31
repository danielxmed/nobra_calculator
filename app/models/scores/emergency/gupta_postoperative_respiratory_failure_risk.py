"""
Gupta Postoperative Respiratory Failure Risk Models

Request and response models for Gupta Postoperative Respiratory Failure Risk calculation.

References (Vancouver style):
1. Gupta H, Gupta PK, Fang X, et al. Development and validation of a risk calculator 
   predicting postoperative respiratory failure. Chest. 2011;140(5):1207-1215. 
   doi: 10.1378/chest.11-0466
2. American College of Surgeons National Surgical Quality Improvement Program. 
   ACS NSQIP Risk Calculator. https://riskcalculator.facs.org/
3. Canet J, Gallart L, Gomar C, et al. Prediction of postoperative pulmonary 
   complications in a population-based surgical cohort. Anesthesiology. 
   2010;113(6):1338-1350. doi: 10.1097/ALN.0b013e3181fc6e0a

The Gupta Postoperative Respiratory Failure Risk calculator is a validated tool that 
predicts the probability of respiratory failure requiring mechanical ventilation for 
>48 hours after surgery or unplanned intubation within 30 days of surgery. This 
calculator was developed using the American College of Surgeons' National Surgical 
Quality Improvement Program (ACS NSQIP) multicenter, prospective data set and 
demonstrates excellent predictive performance with a C-statistic of 0.894-0.897.

**Clinical Background**:
Postoperative respiratory failure is a serious complication that occurs in approximately 
3.1% of surgical patients and is associated with significantly higher 30-day mortality 
(25.62% vs 0.98% in patients without respiratory failure). This dramatic difference in 
mortality rates underscores the critical importance of accurate preoperative risk 
prediction to enable targeted prevention strategies and appropriate care planning.

**Development and Validation**:
The calculator was developed using 211,410 patients from the 2007 ACS NSQIP database 
as the training set and validated on 257,385 patients from the 2008 database. Five 
preoperative predictors were identified through multivariate logistic regression 
analysis, creating a highly accurate prediction model that significantly outperforms 
clinical judgment alone for respiratory failure risk assessment.

**Five Key Risk Factors**:

**1. Functional Status** (Activities of Daily Living):
- **Independent** (0.0 points): Can perform all activities of daily living without assistance
- **Partially Dependent** (0.7678 points): Requires assistance with some but not all ADLs
- **Totally Dependent** (1.4046 points): Requires assistance with all activities of daily living
- **Clinical Significance**: Functional status reflects overall health, respiratory muscle 
  strength, mobility, and ability to perform respiratory hygiene measures such as deep 
  breathing, coughing, and early mobilization

**2. ASA Physical Status Classification**:
- **ASA I** (-3.5265 points): Normal healthy patient without systemic disease
- **ASA II** (-2.0008 points): Patient with mild systemic disease (controlled hypertension, 
  uncomplicated diabetes, mild obesity)
- **ASA III** (-0.6201 points): Patient with severe systemic disease that limits activity 
  but is not incapacitating (uncontrolled diabetes, moderate heart disease)
- **ASA IV** (0.2441 points): Patient with severe systemic disease that is a constant 
  threat to life (severe heart disease, advanced renal failure)
- **ASA V** (0.0 points): Moribund patient not expected to survive without operation (reference)
- **Clinical Significance**: Higher ASA classes indicate greater systemic illness, 
  reduced physiologic reserve, and increased susceptibility to respiratory complications

**3. Preoperative Sepsis Status**:
- **None** (-0.7840 points): No signs of systemic inflammatory response or infection (protective)
- **SIRS** (0.0 points): Systemic Inflammatory Response Syndrome (reference category)
- **Sepsis** (0.2752 points): SIRS with documented or suspected infection
- **Septic Shock** (0.9035 points): Sepsis with hypotension despite adequate fluid resuscitation
- **Clinical Significance**: Preoperative infection and systemic inflammation significantly 
  increase susceptibility to postoperative respiratory complications, compromise immune 
  function, and impair wound healing and recovery

**4. Emergency Case Status**:
- **Elective Surgery** (-0.5739 points): Planned, scheduled surgical procedure (protective)
- **Emergency Surgery** (0.0 points): Urgent or emergent surgical procedure (reference)
- **Clinical Significance**: Emergency surgery is associated with higher complication rates 
  due to lack of preoperative optimization time, acute illness severity, hemodynamic 
  instability, and inability to implement standard preoperative preparation protocols

**5. Type of Surgical Procedure** (Procedure-Specific Risk):
Surgical procedures are categorized by inherent respiratory failure risk based on 
anatomical location, duration, invasiveness, impact on respiratory mechanics, and 
physiologic stress:

**Highest Risk Procedures**:
- **Aortic Surgery** (1.0781 points): Major vascular surgery with significant hemodynamic stress
- **Brain Surgery** (0.8086 points): Intracranial procedures with potential neurological complications
- **Thoracic Non-Cardiac** (0.7737 points): Lung and chest wall surgery directly affecting respiration
- **Cardiac Surgery** (0.6959 points): Cardiothoracic procedures with cardiopulmonary bypass

**High Risk Procedures**:
- **Foregut/Hepatobiliary** (0.4949 points): Upper abdominal surgery affecting diaphragmatic function
- **Peripheral Vascular** (0.3646 points): Non-aortic vascular procedures
- **Neck Surgery** (0.2701 points): Head and neck procedures potentially affecting airway
- **Gallbladder/Appendix/Adrenals/Spleen** (0.2135 points): Intra-abdominal procedures

**Moderate Risk Procedures**:
- **Intestinal Surgery** (0.1964 points): Bowel surgery with potential complications
- **Renal Surgery** (0.1460 points): Kidney procedures
- **Spine Surgery** (0.1139 points): Spinal procedures
- **Orthopedic Non-Spine** (0.0654 points): Joint and bone surgery

**Low Risk Procedures**:
- **Other Abdomen** (0.0481 points): General abdominal procedures
- **Urology Non-Renal** (0.0089 points): Urologic procedures excluding kidney
- **Hernia Repair** (0.0 points): Hernia surgery (reference category)
- **Gynecologic Oncology** (-0.0234 points): Specialized gynecologic cancer surgery

**Lowest Risk Procedures**:
- **Obstetric/Gynecologic** (-0.1456 points): Reproductive system surgery
- **Other Hematologic** (-0.2341 points): Hematologic procedures
- **Skin Surgery** (-0.3678 points): Superficial procedures
- **Thyroid/Parathyroid** (-0.4927 points): Endocrine surgery
- **Vein Surgery** (-0.8934 points): Superficial vein procedures
- **Breast Surgery** (-2.6462 points): Breast procedures (lowest risk)

**Risk Calculation Formula**:
The calculator uses logistic regression: **Risk (%) = e^x / (1 + e^x) × 100**
Where: **x = -1.7397 + functional_status_points + ASA_points + sepsis_points + emergency_points + procedure_points**

**Clinical Risk Categories and Management**:

**Very Low Risk (0.0-1.0%)**:
- **Clinical Approach**: Standard perioperative care and monitoring protocols
- **Interventions**: Routine respiratory care, early mobilization, standard pain management
- **Monitoring**: Standard nursing assessments and vital signs monitoring
- **Discharge**: Standard discharge criteria and routine follow-up

**Low Risk (1.0-3.0%)**:
- **Clinical Approach**: Standard care with enhanced respiratory awareness
- **Interventions**: Ensure adequate pain control to facilitate deep breathing and coughing
- **Monitoring**: Monitor for signs of respiratory complications and implement pulmonary hygiene
- **Education**: Patient education about importance of respiratory exercises and early mobilization

**Moderate Risk (3.0-8.0%)**:
- **Clinical Approach**: Enhanced respiratory monitoring and pulmonary care protocols
- **Interventions**: Aggressive pulmonary hygiene, incentive spirometry, respiratory therapy consultation
- **Monitoring**: Closer respiratory assessment, oxygen saturation monitoring, early detection protocols
- **Pain Management**: Optimize pain control to facilitate effective coughing and deep breathing

**High Risk (8.0-20.0%)**:
- **Clinical Approach**: Intensive respiratory monitoring and consider ICU-level care
- **Preoperative**: Strong consideration for pulmonology consultation and preoperative optimization
- **Interventions**: Intensive respiratory therapy, mechanical ventilation readiness protocols
- **Monitoring**: Enhanced postoperative surveillance, continuous respiratory monitoring
- **Team Approach**: Multidisciplinary involvement including pulmonology and critical care

**Very High Risk (>20.0%)**:
- **Clinical Approach**: Comprehensive respiratory optimization and intensive monitoring
- **Preoperative**: Consider postponing elective surgery for respiratory optimization and preparation
- **Care Level**: ICU-level monitoring and care with mechanical ventilation readily available
- **Team Approach**: Multidisciplinary team including pulmonology, anesthesia, and critical care
- **Discharge**: Extended hospitalization with intensive outpatient respiratory follow-up

**Clinical Applications**:

**Preoperative Assessment**:
- Risk stratification for surgical planning and resource allocation
- Patient and family counseling with specific respiratory failure risk percentages
- Decision-making for preoperative respiratory optimization strategies
- Determination of appropriate level of postoperative monitoring and care intensity

**Perioperative Management**:
- Selection of targeted respiratory failure prevention interventions based on risk level
- ICU admission decisions and mechanical ventilation readiness protocols
- Pulmonology consultation decisions for high-risk patients requiring specialized management
- Postoperative care planning and surveillance strategies for early complication detection

**Quality Improvement**:
- Benchmarking institutional respiratory failure rates and prevention program effectiveness
- Identification of high-risk patient populations for targeted interventions and protocols
- Resource planning and cost-effectiveness analysis of prevention strategies and ICU utilization
- Clinical pathway development and standardization of evidence-based respiratory care protocols

**Prevention Strategies by Risk Level**:
- **All Patients**: Early mobilization protocols, adequate pain control, standard respiratory care
- **Moderate Risk**: Intensive pulmonary hygiene, respiratory therapy consultation, enhanced monitoring
- **High Risk**: Preoperative optimization, ICU-level care consideration, pulmonology involvement
- **Very High Risk**: Comprehensive optimization, surgery delay consideration for elective procedures

**Important Clinical Considerations**:
- Calculator provides probability estimates based on validated population data from large cohorts
- Should complement comprehensive clinical assessment and professional judgment
- Individual patient factors may modify risk beyond model predictions (pulmonary function, recent infections)
- Urgent/emergent surgery may require risk acceptance despite high predicted risk scores
- Regular reassessment may be needed for changing clinical conditions during hospitalization

**Limitations**:
- Does not include specific pulmonary function test results or detailed respiratory history
- May not fully capture complexity of certain patient populations or highly specialized procedures
- Developed primarily in general surgical populations with potential limitations in specialty surgery
- Should be used as part of comprehensive perioperative assessment, not as sole decision-making tool

**Research and Validation**:
The Gupta Postoperative Respiratory Failure Risk calculator has been extensively validated 
and is widely adopted in clinical practice. It is incorporated into major clinical 
guidelines and quality improvement initiatives, representing a significant advance in 
evidence-based perioperative medicine that enhances patient care and clinical decision-making.

This calculator enables clinicians to identify patients at highest risk for respiratory 
failure, implement targeted prevention strategies, and allocate appropriate resources 
to improve patient outcomes and reduce the significant mortality associated with 
postoperative respiratory complications.
"""

from pydantic import BaseModel, Field
from typing import Literal


class GuptaPostoperativeRespiratoryFailureRiskRequest(BaseModel):
    """
    Request model for Gupta Postoperative Respiratory Failure Risk Calculator
    
    The Gupta Postoperative Respiratory Failure Risk calculator uses five validated 
    preoperative risk factors to predict 30-day postoperative respiratory failure risk. 
    All parameters should be assessed preoperatively for accurate risk stratification.
    
    **Functional Status** (Activities of Daily Living Assessment):
    - **Independent**: Can perform all activities of daily living without assistance (0.0 points)
    - **Partially Dependent**: Requires assistance with some but not all ADLs (0.7678 points)
    - **Totally Dependent**: Requires assistance with all activities of daily living (1.4046 points)
    Functional status reflects overall health, respiratory muscle strength, and ability to 
    perform respiratory hygiene measures such as deep breathing and effective coughing.
    
    **ASA Physical Status Classification** (American Society of Anesthesiologists):
    - **Class I** (-3.5265 points): Normal healthy patient without systemic disease
    - **Class II** (-2.0008 points): Patient with mild systemic disease (controlled hypertension, 
      uncomplicated diabetes, mild obesity)
    - **Class III** (-0.6201 points): Patient with severe systemic disease that limits activity 
      but is not incapacitating (uncontrolled diabetes, moderate heart disease)
    - **Class IV** (0.2441 points): Patient with severe systemic disease that is a constant 
      threat to life (severe heart disease, advanced renal failure)
    - **Class V** (0.0 points): Moribund patient not expected to survive without operation
    
    **Preoperative Sepsis Status**:
    - **None** (-0.7840 points): No signs of systemic inflammatory response or infection
    - **SIRS** (0.0 points): Systemic Inflammatory Response Syndrome (reference category)
    - **Sepsis** (0.2752 points): SIRS with documented or suspected infection
    - **Septic Shock** (0.9035 points): Sepsis with hypotension despite adequate fluid resuscitation
    
    **Emergency Case Status**:
    - **No** (-0.5739 points): Elective, scheduled surgical procedure (protective factor)
    - **Yes** (0.0 points): Emergency or urgent surgical procedure (reference category)
    Emergency surgery is associated with higher complication rates due to lack of 
    preoperative optimization time and acute illness severity.
    
    **Surgical Procedure Type** (Procedure-Specific Risk Classification):
    Surgical procedures are categorized by inherent respiratory failure risk based on 
    anatomical location, duration, invasiveness, and impact on respiratory mechanics. 
    Risk ranges from highest (aortic surgery) to lowest (breast surgery).
    
    References (Vancouver style):
    1. Gupta H, Gupta PK, Fang X, et al. Development and validation of a risk calculator 
    predicting postoperative respiratory failure. Chest. 2011;140(5):1207-1215. 
    doi: 10.1378/chest.11-0466
    2. American College of Surgeons National Surgical Quality Improvement Program. 
    ACS NSQIP Risk Calculator. https://riskcalculator.facs.org/
    """
    
    functional_status: Literal["independent", "partially_dependent", "totally_dependent"] = Field(
        ...,
        description="Functional status based on activities of daily living. Independent: 0 pts, Partially dependent: 0.7678 pts, Totally dependent: 1.4046 pts",
        example="independent"
    )
    
    asa_class: Literal["1", "2", "3", "4", "5"] = Field(
        ...,
        description="ASA Physical Status Classification. Class 1: -3.5265 pts (healthy), Class 2: -2.0008 pts (mild disease), Class 3: -0.6201 pts (severe disease), Class 4: 0.2441 pts (life-threatening), Class 5: 0 pts (moribund)",
        example="2"
    )
    
    sepsis_status: Literal["none", "sirs", "sepsis", "septic_shock"] = Field(
        ...,
        description="Preoperative sepsis status. None: -0.7840 pts, SIRS: 0 pts (reference), Sepsis: 0.2752 pts, Septic shock: 0.9035 pts",
        example="none"
    )
    
    emergency_case: Literal["no", "yes"] = Field(
        ...,
        description="Emergency surgical case status. Elective (no): -0.5739 pts (protective), Emergency (yes): 0 pts (reference)",
        example="no"
    )
    
    procedure_type: Literal[
        "aortic", "brain", "breast", "cardiac", "foregut_hepatobiliary",
        "gallbladder_appendix_adrenals_spleen", "intestinal", "neck",
        "obstetric_gynecologic", "orthopedic_non_spine", "peripheral_vascular",
        "renal", "skin", "spine", "thoracic_non_cardiac", "thyroid_parathyroid",
        "urology_non_renal", "vein", "hernia", "gynecologic_oncology", 
        "other_abdomen", "other_hematologic"
    ] = Field(
        ...,
        description="Type of surgical procedure. Risk ranges from aortic surgery (1.0781 pts, highest risk) to breast surgery (-2.6462 pts, lowest risk)",
        example="hernia"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "functional_status": "independent",
                "asa_class": "2",
                "sepsis_status": "none",
                "emergency_case": "no",
                "procedure_type": "hernia"
            }
        }


class GuptaPostoperativeRespiratoryFailureRiskResponse(BaseModel):
    """
    Response model for Gupta Postoperative Respiratory Failure Risk Calculator
    
    Provides the calculated respiratory failure risk percentage with comprehensive 
    clinical interpretation and management recommendations based on validated 
    perioperative outcomes data from ACS NSQIP.
    
    **Definition**: Respiratory failure is defined as requiring mechanical ventilation 
    for >48 hours after surgery or unplanned intubation within 30 days of surgery.
    
    **Risk Categories and Clinical Management**:
    
    **Very Low Risk (0.0-1.0%)**:
    - **Clinical Approach**: Standard perioperative care and monitoring protocols
    - **Interventions**: Routine respiratory care, early mobilization, standard pain management
    - **Monitoring**: Standard nursing assessments and vital signs monitoring
    - **Discharge**: Standard discharge criteria and routine follow-up
    
    **Low Risk (1.0-3.0%)**:
    - **Clinical Approach**: Standard care with enhanced respiratory awareness
    - **Interventions**: Ensure adequate pain control to facilitate deep breathing and coughing
    - **Monitoring**: Monitor for signs of respiratory complications, implement pulmonary hygiene
    - **Education**: Patient education about importance of respiratory exercises and early mobilization
    
    **Moderate Risk (3.0-8.0%)**:
    - **Clinical Approach**: Enhanced respiratory monitoring and pulmonary care protocols
    - **Interventions**: Aggressive pulmonary hygiene, incentive spirometry, respiratory therapy consultation
    - **Monitoring**: Closer respiratory assessment, oxygen saturation monitoring, early detection protocols
    - **Pain Management**: Optimize pain control to facilitate effective coughing and deep breathing
    
    **High Risk (8.0-20.0%)**:
    - **Clinical Approach**: Intensive respiratory monitoring and consider ICU-level care
    - **Preoperative**: Strong consideration for pulmonology consultation and preoperative optimization
    - **Interventions**: Intensive respiratory therapy, mechanical ventilation readiness protocols
    - **Monitoring**: Enhanced postoperative surveillance, continuous respiratory monitoring
    - **Team Approach**: Multidisciplinary involvement including pulmonology and critical care
    
    **Very High Risk (>20.0%)**:
    - **Clinical Approach**: Comprehensive respiratory optimization and intensive monitoring
    - **Preoperative**: Consider postponing elective surgery for respiratory optimization
    - **Care Level**: ICU-level monitoring with mechanical ventilation readily available
    - **Team Approach**: Multidisciplinary team including pulmonology, anesthesia, and critical care
    - **Discharge**: Extended hospitalization with intensive outpatient respiratory follow-up
    
    **Prevention Strategies by Risk Level**:
    
    **All Patients**: 
    - Early mobilization and ambulation protocols
    - Adequate pain control to facilitate deep breathing and coughing
    - Standard respiratory care and pulmonary hygiene measures
    - Patient education about respiratory exercises and importance of mobilization
    
    **Moderate to High Risk Patients**:
    - Intensive pulmonary hygiene and incentive spirometry protocols
    - Respiratory therapy consultation and specialized interventions
    - Enhanced respiratory monitoring for early detection of complications
    - Consider preoperative optimization and pulmonology consultation
    
    **Very High Risk Patients**:
    - Comprehensive preoperative respiratory optimization when feasible
    - ICU-level respiratory monitoring and mechanical ventilation readiness
    - Consider postponing elective procedures for respiratory preparation
    - Multidisciplinary team approach with specialized respiratory care expertise
    
    **Quality Improvement Applications**:
    - **Risk Stratification**: Systematic identification of high-risk patients for targeted interventions
    - **Resource Allocation**: Appropriate allocation of ICU beds and respiratory therapy resources  
    - **Patient Safety**: Proactive implementation of evidence-based respiratory failure prevention strategies
    - **Clinical Pathways**: Development of risk-stratified care protocols and standardized interventions
    - **Outcome Tracking**: Benchmarking and continuous quality improvement initiatives
    
    **Important Clinical Considerations**:
    - Calculator provides probability estimates based on validated population data from large cohorts
    - Should complement comprehensive clinical assessment and professional judgment
    - Individual patient factors may modify risk beyond model predictions (pulmonary function tests, recent infections)
    - Urgent/emergent surgery may require risk acceptance despite high predicted risk scores
    - Patient preferences and values should be incorporated into decision-making processes
    - Regular reassessment may be needed for changing clinical conditions during hospitalization
    
    **Limitations to Consider**:
    - Does not include specific pulmonary function test results or detailed respiratory history
    - May not fully capture complexity of certain patient populations or highly specialized procedures
    - Developed primarily in general surgical populations with potential limitations in specialty surgery
    - Should be used as part of comprehensive perioperative assessment, not as sole decision-making tool
    
    **Clinical Impact**:
    Postoperative respiratory failure occurs in approximately 3.1% of surgical patients 
    and is associated with dramatically higher 30-day mortality (25.62% vs 0.98% in 
    patients without respiratory failure). This calculator enables targeted prevention 
    strategies that can significantly improve patient outcomes and reduce healthcare costs.
    
    Reference: Gupta H, et al. Chest. 2011;140(5):1207-1215.
    """
    
    result: float = Field(
        ...,
        description="Predicted risk percentage of postoperative respiratory failure requiring mechanical ventilation >48 hours or unplanned intubation within 30 days",
        ge=0.0,
        le=100.0,
        example=1.85
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the respiratory failure risk calculation",
        example="percentage"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including patient characteristics, risk percentage, risk category, and specific clinical recommendations for respiratory failure prevention and perioperative management",
        example="Patient characteristics: functionally independent, ASA Class II (mild systemic disease), no sepsis, elective case, undergoing hernia repair. Gupta Postoperative Respiratory Failure Risk: 1.85% risk of respiratory failure requiring mechanical ventilation >48 hours or unplanned intubation within 30 days. Risk Category: Low Risk (Low respiratory failure risk). Clinical recommendations: Low risk of postoperative respiratory failure. Standard care with attention to respiratory status and pain management. Ensure adequate pain control to facilitate deep breathing and coughing. Monitor for signs of respiratory complications and implement standard pulmonary hygiene measures. Important considerations: This calculator predicts postoperative respiratory failure risk (mechanical ventilation >48 hours or unplanned intubation ≤30 days). Respiratory failure is associated with significantly increased 30-day mortality (25.62% vs 0.98%). Use in conjunction with clinical judgment for surgical decision-making and care planning. Consider individual patient factors such as pulmonary function tests, recent respiratory infections, and surgical urgency when making final management decisions."
    )
    
    stage: str = Field(
        ...,
        description="Risk category classification (Very Low Risk, Low Risk, Moderate Risk, High Risk, Very High Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the respiratory failure risk category",
        example="Low respiratory failure risk"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 1.85,
                "unit": "percentage",
                "interpretation": "Patient characteristics: functionally independent, ASA Class II (mild systemic disease), no sepsis, elective case, undergoing hernia repair. Gupta Postoperative Respiratory Failure Risk: 1.85% risk of respiratory failure requiring mechanical ventilation >48 hours or unplanned intubation within 30 days. Risk Category: Low Risk (Low respiratory failure risk). Clinical recommendations: Low risk of postoperative respiratory failure. Standard care with attention to respiratory status and pain management. Ensure adequate pain control to facilitate deep breathing and coughing. Monitor for signs of respiratory complications and implement standard pulmonary hygiene measures. Important considerations: This calculator predicts postoperative respiratory failure risk (mechanical ventilation >48 hours or unplanned intubation ≤30 days). Respiratory failure is associated with significantly increased 30-day mortality (25.62% vs 0.98%). Use in conjunction with clinical judgment for surgical decision-making and care planning. Consider individual patient factors such as pulmonary function tests, recent respiratory infections, and surgical urgency when making final management decisions.",
                "stage": "Low Risk",
                "stage_description": "Low respiratory failure risk"
            }
        }