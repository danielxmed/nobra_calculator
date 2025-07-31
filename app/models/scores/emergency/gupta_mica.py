"""
Gupta Perioperative Risk for Myocardial Infarction or Cardiac Arrest (MICA) Models

Request and response models for Gupta MICA risk calculation.

References (Vancouver style):
1. Gupta PK, Gupta H, Sundaram A, et al. Development and validation of a risk calculator 
   for prediction of cardiac risk after surgery. Circulation. 2011;124(4):381-387. 
   doi: 10.1161/CIRCULATIONAHA.110.015701
2. Bilimoria KY, Liu Y, Paruch JL, et al. Development and evaluation of the universal 
   ACS NSQIP surgical risk calculator: a decision aid and informed consent tool for 
   patients and surgeons. J Am Coll Surg. 2013;217(5):833-842. 
   doi: 10.1016/j.jamcollsurg.2013.07.385
3. Ford MK, Beattie WS, Wijeysundera DN. Systematic review: prediction of perioperative 
   cardiac complications and mortality by the revised cardiac risk index. Ann Intern Med. 
   2010;152(1):26-35. doi: 10.7326/0003-4819-152-1-201001050-00007

The Gupta Perioperative Risk for Myocardial Infarction or Cardiac Arrest (MICA) is a 
validated risk calculator that predicts the probability of cardiac events within 30 days 
after surgery. This tool represents a significant advancement in perioperative cardiac 
risk assessment, offering superior predictive ability compared to previous tools.

**Clinical Background**:
Perioperative cardiac events, including myocardial infarction and cardiac arrest, are 
major causes of morbidity and mortality in surgical patients. Accurate risk prediction 
is essential for optimal perioperative management, patient counseling, and resource 
allocation. The Gupta MICA calculator was developed to address limitations of existing 
risk assessment tools and provide more accurate predictions across diverse surgical populations.

**Development and Validation**:
The calculator was developed using data from more than 400,000 patients in the American 
College of Surgeons National Surgical Quality Improvement Program (ACS-NSQIP) database. 
The model demonstrated superior discriminative ability with a C-statistic of 0.88, 
significantly outperforming the Revised Cardiac Risk Index (C-statistic 0.75) and other 
existing tools.

**Five Key Risk Factors**:

**1. Age**:
- **Continuous Variable**: Each year of age increases risk
- **Points**: 0.02 points per year of age
- **Rationale**: Advanced age is associated with increased cardiovascular comorbidities, 
  reduced physiologic reserve, and higher perioperative cardiac event rates
- **Clinical Consideration**: Age-related risk increases gradually and continuously

**2. Functional Status** (Activities of Daily Living):
- **Independent**: 0.0 points - Can perform activities of daily living independently
- **Partially Dependent**: 0.65 points - Requires assistance with some activities
- **Totally Dependent**: 1.03 points - Requires assistance with all activities
- **Assessment**: Based on ability to perform bathing, dressing, feeding, toileting, 
  and mobility without assistance
- **Clinical Significance**: Functional status reflects overall health, cardiovascular 
  fitness, and ability to tolerate physiologic stress

**3. ASA Physical Status Classification**:
- **ASA I** (-5.17 points): Normal healthy patient without systemic disease
- **ASA II** (-3.29 points): Patient with mild systemic disease (controlled hypertension, 
  diabetes without complications, mild obesity)
- **ASA III** (-1.92 points): Patient with severe systemic disease that limits activity 
  but is not incapacitating (uncontrolled diabetes, moderate heart disease)
- **ASA IV** (-0.95 points): Patient with severe systemic disease that is a constant 
  threat to life (severe heart disease, renal failure)
- **ASA V** (0.0 points): Moribund patient not expected to survive without operation
- **Clinical Application**: Higher ASA classes indicate greater systemic illness and 
  reduced physiologic reserve

**4. Creatinine Status** (Kidney Function):
- **Normal** (0.0 points): Serum creatinine ≤1.5 mg/dL
- **Elevated** (0.61 points): Serum creatinine >1.5 mg/dL
- **Unknown** (-0.10 points): Creatinine level not available
- **Clinical Significance**: Elevated creatinine indicates reduced kidney function, 
  often associated with cardiovascular disease and increased perioperative risk
- **Considerations**: May reflect chronic kidney disease, acute kidney injury, or 
  cardiovascular-renal syndrome

**5. Surgery Type** (Procedure-Specific Risk):
Surgical procedures are categorized by inherent cardiac risk based on physiologic stress, 
duration, blood loss potential, and hemodynamic changes:

**Highest Risk Procedures**:
- **Aortic Surgery** (1.60 points): Major vascular surgery with significant hemodynamic stress
- **Brain Surgery** (1.40 points): Intracranial procedures with potential for hemodynamic instability
- **Cardiac Surgery** (1.01 points): Direct cardiac intervention with cardiopulmonary bypass

**High Risk Procedures**:
- **Foregut/Hepatobiliary** (0.82 points): Major abdominal surgery with significant fluid shifts
- **Gallbladder/Appendix/Adrenals/Spleen** (0.67 points): Intra-abdominal procedures
- **Intestinal Surgery** (0.58 points): Bowel surgery with potential complications

**Moderate Risk Procedures**:
- **Neck Surgery** (0.40 points): Head and neck procedures
- **Obstetric/Gynecologic** (0.28 points): Reproductive system surgery
- **Orthopedic Non-Spine** (0.20 points): Joint and bone surgery
- **Peripheral Vascular** (0.16 points): Non-aortic vascular procedures

**Low Risk Procedures**:
- **Skin Surgery** (0.12 points): Superficial procedures
- **Spine Surgery** (0.10 points): Spinal procedures
- **Thoracic Non-Cardiac** (0.06 points): Lung and chest wall surgery
- **Urology Non-Renal** (0.04 points): Urologic procedures excluding kidney
- **Renal Surgery** (0.02 points): Kidney procedures
- **Hernia Repair** (0.0 points): Hernia surgery (reference category)

**Lowest Risk Procedures**:
- **Thyroid/Parathyroid** (-0.32 points): Endocrine surgery
- **Eye Surgery** (-1.05 points): Ophthalmic procedures
- **Vein Surgery** (-1.09 points): Superficial vein procedures
- **Breast Surgery** (-1.61 points): Breast procedures

**Risk Calculation Formula**:
The calculator uses logistic regression: **Risk (%) = e^x / (1 + e^x) × 100**
Where: **x = -5.25 + (age × 0.02) + functional_status_points + asa_class_points + creatinine_points + surgery_type_points**

**Clinical Risk Categories**:

**Very Low Risk** (0.0-0.5%): Minimal cardiac risk, standard monitoring appropriate
**Low Risk** (0.5-1.0%): Low cardiac risk, standard monitoring with cardiac awareness
**Moderate Risk** (1.0-2.0%): Enhanced monitoring, consider telemetry and cardiology consultation
**High Risk** (2.0-5.0%): Intensive monitoring, preoperative optimization, cardiology evaluation
**Very High Risk** (>5.0%): Comprehensive evaluation, consider surgery delay for optimization

**Clinical Applications**:

**Preoperative Assessment**:
- Risk stratification for surgical planning and resource allocation
- Patient and family counseling with specific risk percentages
- Decision-making for preoperative cardiac testing and optimization
- Determination of appropriate level of perioperative monitoring

**Perioperative Management**:
- Selection of monitoring intensity (telemetry, ICU admission)
- Postoperative surveillance strategies and biomarker monitoring
- Cardiology consultation decisions and timing
- Discharge planning and follow-up care coordination

**Quality Improvement**:
- Benchmarking institutional cardiac complication rates
- Identification of high-risk patient populations for targeted interventions
- Resource planning and cost-effectiveness analysis
- Clinical pathway development and standardization

**Limitations and Considerations**:
- Does not include stress test results, echocardiography findings, or coronary anatomy
- May not capture all aspects of coronary artery disease not reflected in included variables
- Beta-blocker therapy status and other cardiac medications not incorporated
- Should complement, not replace, comprehensive clinical assessment and judgment
- Developed primarily in non-cardiac surgery populations

**Research and Validation**:
The Gupta MICA calculator has been externally validated in multiple populations and 
clinical settings, consistently demonstrating superior performance compared to existing 
risk assessment tools. It has become widely adopted for perioperative cardiac risk 
assessment and is incorporated into major clinical guidelines and quality improvement initiatives.

This calculator represents a significant advance in evidence-based perioperative medicine, 
providing clinicians with an accurate, practical tool for cardiac risk assessment that 
enhances patient care and clinical decision-making.
"""

from pydantic import BaseModel, Field, validator
from typing import Literal


class GuptaMicaRequest(BaseModel):
    """
    Request model for Gupta Perioperative Risk for Myocardial Infarction or Cardiac Arrest (MICA)
    
    The Gupta MICA calculator uses five validated risk factors to predict 30-day perioperative 
    cardiac events. All parameters should be assessed preoperatively for accurate risk stratification.
    
    **Age**: Continuous risk factor with 0.02 points per year of age. Advanced age reflects 
    reduced physiologic reserve and increased cardiovascular comorbidities.
    
    **Functional Status** (Activities of Daily Living Assessment):
    - **Independent**: Can perform all activities of daily living (bathing, dressing, feeding, 
      toileting, mobility) without assistance. Indicates good overall health and fitness.
    - **Partially Dependent**: Requires assistance with some but not all activities of daily 
      living. Suggests intermediate functional capacity and health status.
    - **Totally Dependent**: Requires assistance with all activities of daily living. 
      Indicates poor functional status and high vulnerability to stress.
    
    **ASA Physical Status Classification** (American Society of Anesthesiologists):
    - **Class I**: Normal healthy patient without systemic disease
    - **Class II**: Patient with mild systemic disease (e.g., controlled hypertension, 
      diabetes without complications, mild obesity)
    - **Class III**: Patient with severe systemic disease that limits activity but is not 
      incapacitating (e.g., uncontrolled diabetes, moderate heart disease)
    - **Class IV**: Patient with severe systemic disease that is a constant threat to life 
      (e.g., severe heart disease, advanced renal failure)
    - **Class V**: Moribund patient not expected to survive without operation
    
    **Creatinine Status** (Kidney Function Assessment):
    - **Normal**: Serum creatinine ≤1.5 mg/dL, indicating normal kidney function
    - **Elevated**: Serum creatinine >1.5 mg/dL, suggesting reduced kidney function and 
      associated cardiovascular risk
    - **Unknown**: Creatinine level not available or not measured preoperatively
    
    **Surgery Type** (Procedure-Specific Risk Classification):
    Surgical procedures are categorized by inherent cardiac risk based on physiologic 
    stress, duration, blood loss potential, and hemodynamic changes. Risk ranges from 
    highest (aortic surgery) to lowest (breast surgery).
    
    References (Vancouver style):
    1. Gupta PK, Gupta H, Sundaram A, et al. Development and validation of a risk calculator 
    for prediction of cardiac risk after surgery. Circulation. 2011;124(4):381-387. 
    doi: 10.1161/CIRCULATIONAHA.110.015701
    2. Bilimoria KY, Liu Y, Paruch JL, et al. Development and evaluation of the universal 
    ACS NSQIP surgical risk calculator: a decision aid and informed consent tool for 
    patients and surgeons. J Am Coll Surg. 2013;217(5):833-842. 
    doi: 10.1016/j.jamcollsurg.2013.07.385
    """
    
    age: int = Field(
        ...,
        description="Patient age in years. Each year adds 0.02 points to risk score. Advanced age increases cardiovascular risk due to reduced physiologic reserve",
        ge=18,
        le=120,
        example=65
    )
    
    functional_status: Literal["independent", "partially_dependent", "totally_dependent"] = Field(
        ...,
        description="Functional status based on activities of daily living. Independent: 0 pts, Partially dependent: 0.65 pts, Totally dependent: 1.03 pts",
        example="independent"
    )
    
    asa_class: Literal["1", "2", "3", "4", "5"] = Field(
        ...,
        description="ASA Physical Status Classification. Class 1: -5.17 pts (healthy), Class 2: -3.29 pts (mild disease), Class 3: -1.92 pts (severe disease), Class 4: -0.95 pts (life-threatening), Class 5: 0 pts (moribund)",
        example="2"
    )
    
    creatinine_status: Literal["normal", "elevated", "unknown"] = Field(
        ...,
        description="Serum creatinine status. Normal (≤1.5 mg/dL): 0 pts, Elevated (>1.5 mg/dL): 0.61 pts, Unknown: -0.10 pts",
        example="normal"
    )
    
    surgery_type: Literal[
        "aortic", "brain", "cardiac", "foregut_hepatobiliary", "gallbladder_appendix_adrenals_spleen",
        "intestinal", "neck", "obstetric_gynecologic", "orthopedic_non_spine", "peripheral_vascular",
        "skin", "spine", "thoracic_non_cardiac", "urology_non_renal", "renal", "hernia",
        "thyroid_parathyroid", "breast", "eye", "vein"
    ] = Field(
        ...,
        description="Type of surgical procedure. Risk ranges from aortic surgery (1.60 pts, highest risk) to breast surgery (-1.61 pts, lowest risk)",
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
                "age": 65,
                "functional_status": "independent",
                "asa_class": "2",
                "creatinine_status": "normal",
                "surgery_type": "hernia"
            }
        }


class GuptaMicaResponse(BaseModel):
    """
    Response model for Gupta Perioperative Risk for Myocardial Infarction or Cardiac Arrest (MICA)
    
    Provides the calculated cardiac risk percentage with comprehensive clinical interpretation 
    and management recommendations based on validated perioperative outcomes data.
    
    **Risk Categories and Clinical Management**:
    
    **Very Low Risk (0.0-0.5%)**:
    - **Clinical Approach**: Standard perioperative monitoring and routine postoperative care
    - **Monitoring**: Standard vital signs, routine nursing assessments
    - **Interventions**: Continue home medications as appropriate, no additional cardiac testing
    - **Discharge**: Standard discharge criteria and follow-up
    
    **Low Risk (0.5-1.0%)**:
    - **Clinical Approach**: Standard monitoring with heightened cardiac awareness
    - **Monitoring**: Standard care with attention to cardiac symptoms and signs
    - **Interventions**: Continue cardiac medications, monitor for ischemic symptoms
    - **Considerations**: Basic cardiac precautions, patient education about symptoms
    
    **Moderate Risk (1.0-2.0%)**:
    - **Clinical Approach**: Enhanced monitoring and cardiac-focused care
    - **Monitoring**: Consider cardiac telemetry monitoring, serial vital signs
    - **Interventions**: Serial troponin measurements, optimize cardiac medications
    - **Consultations**: Consider cardiology consultation for high-risk procedures
    - **Discharge**: Extended monitoring period, cardiac symptom education
    
    **High Risk (2.0-5.0%)**:
    - **Clinical Approach**: Intensive monitoring and proactive cardiac management
    - **Preoperative**: Strong consideration for cardiology evaluation and optimization
    - **Monitoring**: Continuous cardiac monitoring, frequent vital signs, ICU consideration
    - **Interventions**: Serial cardiac biomarkers, optimize beta-blockers and statins
    - **Postoperative**: Extended monitoring, prompt evaluation of symptoms
    - **Discharge**: Cardiology follow-up, comprehensive medication review
    
    **Very High Risk (>5.0%)**:
    - **Clinical Approach**: Comprehensive cardiac evaluation and multidisciplinary management
    - **Preoperative**: Mandatory cardiology consultation, consider surgery delay for optimization
    - **Testing**: Consider stress testing, echocardiography, coronary evaluation
    - **Monitoring**: ICU-level monitoring, invasive monitoring if indicated
    - **Interventions**: Aggressive medical optimization, consider prophylactic interventions
    - **Team Approach**: Multidisciplinary team including cardiology, anesthesia, surgery
    - **Discharge**: Intensive cardiology follow-up, medication optimization
    
    **Preoperative Optimization Strategies**:
    - **Beta-Blockers**: Continue existing therapy, consider initiation in high-risk patients
    - **Statins**: Continue or initiate high-intensity statin therapy when appropriate
    - **ACE Inhibitors/ARBs**: Optimize heart failure and hypertension management
    - **Antiplatelet Therapy**: Balance bleeding risk with thrombotic risk
    - **Smoking Cessation**: Encourage cessation with support resources
    - **Diabetic Control**: Optimize glycemic control while avoiding hypoglycemia
    
    **Postoperative Surveillance**:
    - **Cardiac Biomarkers**: Serial troponin measurements in higher-risk patients
    - **Electrocardiograms**: Baseline and follow-up ECGs to detect ischemic changes
    - **Symptom Monitoring**: Education about cardiac symptoms requiring immediate evaluation
    - **Hemodynamic Monitoring**: Blood pressure, heart rate, and rhythm monitoring
    - **Fluid Management**: Careful attention to volume status and cardiac loading conditions
    
    **Quality Improvement Applications**:
    - **Risk Stratification**: Systematic approach to identifying high-risk patients
    - **Resource Allocation**: Appropriate allocation of monitoring and consultation resources
    - **Patient Safety**: Proactive identification and management of cardiac risk factors
    - **Clinical Pathways**: Development of risk-stratified care protocols
    - **Outcome Tracking**: Benchmarking and quality improvement initiatives
    
    **Important Clinical Considerations**:
    - Calculator provides probability estimates, not absolute predictions
    - Should complement comprehensive clinical assessment and judgment
    - Individual patient factors may modify risk beyond model predictions
    - Urgent/emergent surgery may require risk acceptance despite high scores
    - Patient preferences and values should be incorporated into decision-making
    - Regular reassessment may be needed for changing clinical conditions
    
    **Limitations to Consider**:
    - Does not include coronary anatomy, stress test results, or echocardiographic findings
    - Beta-blocker therapy status and other cardiac medications not incorporated
    - May not fully capture complexity of certain patient populations or procedures
    - Developed primarily in non-cardiac surgery populations
    - Should be used as part of comprehensive perioperative assessment
    
    Reference: Gupta PK, et al. Circulation. 2011;124(4):381-387.
    """
    
    result: float = Field(
        ...,
        description="Predicted risk percentage of myocardial infarction or cardiac arrest within 30 days of surgery",
        ge=0.0,
        le=100.0,
        example=1.25
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the risk calculation",
        example="percentage"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including patient characteristics, risk percentage, risk category, and specific clinical recommendations for perioperative management",
        example="Patient characteristics: 65 years old, functionally independent, ASA Class II (mild systemic disease), normal creatinine (≤1.5 mg/dL), undergoing hernia repair. Gupta MICA Risk: 1.25% risk of perioperative cardiac events within 30 days. Risk Category: Moderate Risk (Moderate perioperative cardiac risk). Clinical recommendations: Moderate perioperative cardiac risk requiring enhanced monitoring. Consider cardiac telemetry monitoring, serial troponin measurements, and cardiology consultation for high-risk procedures. Optimize medical management of cardiovascular risk factors preoperatively. Important considerations: This calculator predicts 30-day perioperative myocardial infarction or cardiac arrest risk based on validated risk factors. Should be used in conjunction with clinical judgment and comprehensive patient assessment. Consider individual patient factors not captured in the model, such as coronary artery disease, medication compliance, and surgical urgency when making final management decisions."
    )
    
    stage: str = Field(
        ...,
        description="Risk category classification (Very Low Risk, Low Risk, Moderate Risk, High Risk, Very High Risk)",
        example="Moderate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Moderate perioperative cardiac risk"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 1.25,
                "unit": "percentage",
                "interpretation": "Patient characteristics: 65 years old, functionally independent, ASA Class II (mild systemic disease), normal creatinine (≤1.5 mg/dL), undergoing hernia repair. Gupta MICA Risk: 1.25% risk of perioperative cardiac events within 30 days. Risk Category: Moderate Risk (Moderate perioperative cardiac risk). Clinical recommendations: Moderate perioperative cardiac risk requiring enhanced monitoring. Consider cardiac telemetry monitoring, serial troponin measurements, and cardiology consultation for high-risk procedures. Optimize medical management of cardiovascular risk factors preoperatively. Important considerations: This calculator predicts 30-day perioperative myocardial infarction or cardiac arrest risk based on validated risk factors. Should be used in conjunction with clinical judgment and comprehensive patient assessment. Consider individual patient factors not captured in the model, such as coronary artery disease, medication compliance, and surgical urgency when making final management decisions.",
                "stage": "Moderate Risk",
                "stage_description": "Moderate perioperative cardiac risk"
            }
        }