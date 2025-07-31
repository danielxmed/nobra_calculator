"""
Glasgow-Blatchford Bleeding Score (GBS) Models

Request and response models for Glasgow-Blatchford Bleeding Score calculation.

References (Vancouver style):
1. Blatchford O, Murray WR, Blatchford M. A risk score to predict need for treatment 
   for upper-gastrointestinal haemorrhage. Lancet. 2000;356(9238):1318-1321. 
   doi: 10.1016/S0140-6736(00)02816-6.
2. Stanley AJ, Ashley D, Dalton HR, et al. Outpatient management of patients with 
   low-risk upper-gastrointestinal haemorrhage: multicentre validation and prospective 
   evaluation. Lancet. 2009;373(9657):42-47. doi: 10.1016/S0140-6736(08)61769-9.
3. Saltzman JR, Tabak YP, Hyett BH, Sun X, Travis AC, Johannes RS. A simple risk 
   score accurately predicts in-hospital mortality, length of stay, and cost in 
   acute upper GI bleeding. Gastrointest Endosc. 2011;74(6):1215-1224. 
   doi: 10.1016/j.gie.2011.06.024.

The Glasgow-Blatchford Bleeding Score (GBS) is a clinical scoring system designed 
to assess the risk of upper gastrointestinal bleeding and identify patients who 
may require medical intervention such as blood transfusion or endoscopic intervention. 
Originally developed in Glasgow, Scotland, this score has become a widely adopted 
tool for risk stratification in upper GI bleeding, helping clinicians make informed 
decisions about patient disposition and management.

Key Clinical Applications:
- Risk stratification for upper gastrointestinal bleeding patients
- Identification of low-risk patients suitable for outpatient management
- Prediction of need for blood transfusion or endoscopic intervention
- Resource allocation and healthcare cost optimization
- Clinical decision support for hospital admission versus discharge

Clinical Significance and Validation:
The GBS has been extensively validated and is recommended by UK and European 
guidelines for upper GI bleeding management. A score of 0 indicates very low risk 
and suitability for outpatient management, while higher scores indicate increasing 
risk and need for hospital-based intervention. The score has superior predictive 
accuracy compared to other scoring systems like the Rockall score for predicting 
need for intervention, and it can be calculated without requiring endoscopy.

Advantages over other scoring systems include the absence of subjective variables, 
no requirement for endoscopy to complete the calculation, and better prediction 
of need for clinical intervention rather than just mortality risk.
"""

from pydantic import BaseModel, Field
from typing import Literal


class GlasgowBlatchfordBleedingScoreRequest(BaseModel):
    """
    Request model for Glasgow-Blatchford Bleeding Score (GBS)
    
    The GBS provides systematic risk assessment for upper gastrointestinal bleeding 
    using readily available clinical and laboratory parameters. This evidence-based 
    approach enables consistent evaluation across healthcare settings and supports 
    clinical decision-making regarding patient disposition and intervention needs.
    
    **CLINICAL ASSESSMENT FRAMEWORK**:
    
    **Laboratory Parameters**:
    
    **Blood Urea Nitrogen (BUN) Assessment**:
    
    **Clinical Significance**: Marker of upper GI bleeding severity and renal function
    - **Pathophysiology**: Elevated due to blood digestion and absorption in GI tract
    - **Bleeding Context**: Higher levels indicate more significant bleeding volume
    - **Scoring Ranges**: Progressive point increases with higher BUN levels
    - **Clinical Correlation**: Strong predictor of intervention need
    
    **BUN Scoring Criteria**:
    - **<18.2 mg/dL**: 0 points (normal range)
    - **18.2-22.3 mg/dL**: +2 points (mild elevation)
    - **22.4-28.0 mg/dL**: +3 points (moderate elevation)  
    - **28.1-70.0 mg/dL**: +4 points (significant elevation)
    - **>70.0 mg/dL**: +6 points (severe elevation)
    
    **Hemoglobin Assessment (Gender-Specific)**:
    
    **Clinical Significance**: Direct measure of anemia severity due to blood loss
    - **Pathophysiology**: Reflects acute and chronic blood loss effects
    - **Gender Differences**: Different baseline levels and thresholds for men vs women
    - **Clinical Context**: Lower levels indicate need for transfusion consideration
    - **Prognostic Value**: Strong predictor of clinical intervention requirements
    
    **Hemoglobin Scoring Criteria - Males**:
    - **>13.0 g/dL**: 0 points (normal range for males)
    - **12.0-13.0 g/dL**: +1 point (mild anemia)
    - **10.0-12.0 g/dL**: +3 points (moderate anemia)
    - **<10.0 g/dL**: +6 points (severe anemia)
    
    **Hemoglobin Scoring Criteria - Females**:
    - **>12.0 g/dL**: 0 points (normal range for females)
    - **10.0-12.0 g/dL**: +1 point (mild anemia)
    - **<10.0 g/dL**: +6 points (severe anemia)
    
    **Vital Signs Assessment**:
    
    **Systolic Blood Pressure Assessment**:
    
    **Clinical Significance**: Indicator of hemodynamic stability and shock risk
    - **Pathophysiology**: Reflects intravascular volume status and cardiac output
    - **Bleeding Context**: Lower pressures indicate more severe volume loss
    - **Clinical Urgency**: Hypotension signals need for immediate intervention
    - **Monitoring Value**: Guide for resuscitation and intervention timing
    
    **Systolic BP Scoring Criteria**:
    - **≥110 mmHg**: 0 points (normal hemodynamic status)
    - **100-109 mmHg**: +1 point (mild hypotension)
    - **90-99 mmHg**: +2 points (moderate hypotension)
    - **<90 mmHg**: +3 points (severe hypotension/shock)
    
    **Heart Rate Assessment**:
    
    **Clinical Significance**: Compensatory response to blood loss and volume depletion
    - **Pathophysiology**: Tachycardia compensates for reduced stroke volume
    - **Clinical Context**: Elevated heart rate indicates hemodynamic stress
    - **Threshold**: ≥100 bpm considered clinically significant tachycardia
    - **Monitoring Value**: Early indicator of hemodynamic compromise
    
    **Heart Rate Scoring Criteria**:
    - **<100 bpm**: 0 points (normal heart rate)
    - **≥100 bpm**: +1 point (tachycardia present)
    
    **Clinical Presentation Factors**:
    
    **Melena Assessment**:
    
    **Clinical Significance**: Pathognomonic sign of upper gastrointestinal bleeding
    - **Definition**: Black, tarry, foul-smelling stools from digested blood
    - **Pathophysiology**: Results from bacterial action on hemoglobin in GI tract
    - **Clinical Context**: Indicates significant upper GI bleeding
    - **Diagnostic Value**: Helps localize bleeding source to upper GI tract
    
    **Melena Scoring Criteria**:
    - **Present**: +1 point (upper GI bleeding confirmed)
    - **Absent**: 0 points (no evidence of upper GI bleeding by stool)
    
    **Syncope Assessment**:
    
    **Clinical Significance**: Indicator of significant volume loss and hemodynamic compromise
    - **Definition**: Transient loss of consciousness due to cerebral hypoperfusion
    - **Pathophysiology**: Results from reduced cardiac output and blood pressure
    - **Clinical Context**: Suggests significant blood loss requiring urgent attention
    - **Prognostic Value**: Associated with higher intervention requirements
    
    **Syncope Scoring Criteria**:
    - **Present**: +2 points (significant hemodynamic compromise)
    - **Absent**: 0 points (no evidence of hemodynamic compromise)
    
    **Comorbidity Assessment**:
    
    **Liver Disease Assessment**:
    
    **Clinical Significance**: Increases bleeding risk and complicates management
    - **Pathophysiology**: Portal hypertension, coagulopathy, varices, thrombocytopenia
    - **Bleeding Risk**: Higher risk of variceal bleeding and coagulation disorders
    - **Clinical Context**: Requires specialized management and higher acuity care
    - **Prognostic Impact**: Associated with worse outcomes and higher intervention needs
    
    **Liver Disease Scoring Criteria**:
    - **Present**: +2 points (significant comorbidity affecting management)
    - **Absent**: 0 points (no hepatic complications)
    
    **Heart Failure Assessment**:
    
    **Clinical Significance**: Cardiovascular comorbidity affecting resuscitation capacity
    - **Pathophysiology**: Reduced cardiac reserve and tolerance to volume changes
    - **Clinical Context**: Limits aggressive fluid resuscitation options
    - **Management Impact**: May require invasive monitoring and careful volume management
    - **Prognostic Value**: Associated with higher mortality and complication rates
    
    **Heart Failure Scoring Criteria**:
    - **Present**: +2 points (significant cardiovascular comorbidity)
    - **Absent**: 0 points (no cardiac limitations)
    
    **CLINICAL DECISION SUPPORT**:
    
    **Risk Stratification Framework**:
    - **Score 0**: Very low risk, suitable for outpatient management
    - **Score 1-5**: Low-moderate risk, consider observation and assessment
    - **Score 6-11**: Moderate risk, hospital admission recommended
    - **Score ≥12**: High risk, urgent intervention likely needed
    
    **Clinical Implementation Guidelines**:
    - Calculate score at initial presentation before intervention
    - Recalculate if clinical status changes significantly
    - Use in conjunction with clinical judgment and local protocols
    - Consider patient factors not captured in the score
    
    References (Vancouver style):
    1. Blatchford O, Murray WR, Blatchford M. A risk score to predict need for treatment 
       for upper-gastrointestinal haemorrhage. Lancet. 2000;356(9238):1318-1321.
    2. Stanley AJ, Ashley D, Dalton HR, et al. Outpatient management of patients with 
       low-risk upper-gastrointestinal haemorrhage: multicentre validation and prospective 
       evaluation. Lancet. 2009;373(9657):42-47.
    3. Saltzman JR, Tabak YP, Hyett BH, Sun X, Travis AC, Johannes RS. A simple risk 
       score accurately predicts in-hospital mortality, length of stay, and cost in 
       acute upper GI bleeding. Gastrointest Endosc. 2011;74(6):1215-1224.
    """
    
    bun: float = Field(
        ...,
        description="Blood urea nitrogen level in mg/dL. Higher levels indicate more significant GI bleeding",
        ge=5,
        le=200,
        example=25.0
    )
    
    hemoglobin: float = Field(
        ...,
        description="Hemoglobin level in g/dL. Lower levels indicate anemia from blood loss",
        ge=3.0,
        le=20.0,
        example=11.5
    )
    
    gender: Literal["male", "female"] = Field(
        ...,
        description="Patient gender. Affects hemoglobin scoring thresholds (males have higher baseline hemoglobin)",
        example="male"
    )
    
    systolic_bp: int = Field(
        ...,
        description="Systolic blood pressure in mmHg. Lower pressures indicate hemodynamic compromise",
        ge=50,
        le=250,
        example=105
    )
    
    heart_rate: int = Field(
        ...,
        description="Heart rate in beats per minute. Tachycardia ≥100 bpm indicates hemodynamic stress",
        ge=30,
        le=200,
        example=95
    )
    
    melena: Literal["yes", "no"] = Field(
        ...,
        description="Presence of melena (black, tarry stools). Pathognomonic sign of upper GI bleeding",
        example="yes"
    )
    
    syncope: Literal["yes", "no"] = Field(
        ...,
        description="History of syncope (fainting). Indicates significant hemodynamic compromise from blood loss",
        example="no"
    )
    
    liver_disease: Literal["yes", "no"] = Field(
        ...,
        description="History of hepatic disease. Increases bleeding risk and complicates management",
        example="no"
    )
    
    heart_failure: Literal["yes", "no"] = Field(
        ...,
        description="History of cardiac failure. Affects resuscitation capacity and monitoring needs",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "bun": 25.0,
                "hemoglobin": 11.5,
                "gender": "male",
                "systolic_bp": 105,
                "heart_rate": 95,
                "melena": "yes",
                "syncope": "no",
                "liver_disease": "no",
                "heart_failure": "no"
            }
        }


class GlasgowBlatchfordBleedingScoreResponse(BaseModel):
    """
    Response model for Glasgow-Blatchford Bleeding Score (GBS)
    
    The response provides the calculated GBS score with comprehensive clinical 
    interpretation and evidence-based management recommendations based on extensive 
    validation studies and clinical guidelines for upper gastrointestinal bleeding.
    
    **CLINICAL INTERPRETATION FRAMEWORK**:
    
    **GBS Score Validation and Clinical Significance**:
    - **Scoring Range**: 0-23 points combining laboratory, vital signs, and clinical factors
    - **Clinical Validation**: Extensively validated across multiple healthcare systems
    - **Predictive Accuracy**: Superior to other scores for predicting intervention needs
    - **Guidelines Integration**: Recommended by UK and European clinical guidelines
    
    **Risk Categories and Management Protocols**:
    
    **Low Risk (Score 0) - Outpatient Management**:
    - **Clinical Significance**: Very low risk for requiring medical intervention
    - **Management Protocol**: Safe for outpatient management with appropriate follow-up
    - **Intervention Likelihood**: <5% chance of requiring transfusion or endoscopy
    - **Cost-Effectiveness**: Reduces unnecessary hospital admissions by 20-30%
    - **Follow-up Requirements**: Outpatient gastroenterology within 7-14 days
    
    **Low-Moderate Risk (Scores 1-5) - Clinical Assessment**:
    - **Clinical Significance**: Low to moderate risk requiring clinical evaluation
    - **Management Protocol**: Consider hospital observation and assessment
    - **Intervention Likelihood**: 15-25% chance of requiring intervention
    - **Monitoring Requirements**: Vital signs, CBC, clinical status assessment
    - **Decision Support**: May warrant short observation period or early discharge
    
    **Moderate Risk (Scores 6-11) - Hospital Admission**:
    - **Clinical Significance**: Moderate risk requiring hospital-based care
    - **Management Protocol**: Hospital admission with gastroenterology consultation
    - **Intervention Likelihood**: 40-60% chance of requiring transfusion or endoscopy
    - **Monitoring Requirements**: Close monitoring, serial hemoglobin, endoscopy planning
    - **Resource Allocation**: Appropriate ward-level care with specialist availability
    
    **High Risk (Scores ≥12) - Urgent Intervention**:
    - **Clinical Significance**: High risk requiring immediate medical intervention
    - **Management Protocol**: Urgent admission with intensive monitoring
    - **Intervention Likelihood**: >75% chance of requiring immediate intervention
    - **Monitoring Requirements**: ICU consideration, emergency endoscopy, blood products
    - **Resource Allocation**: High-acuity care with immediate specialist involvement
    
    **EVIDENCE-BASED MANAGEMENT PROTOCOLS**:
    
    **Risk-Stratified Treatment Approaches**:
    
    **Low Risk Management (Score 0)**:
    - **Disposition**: Outpatient management with structured follow-up
    - **Medications**: Proton pump inhibitor therapy, H. pylori testing if indicated
    - **Monitoring**: Return precautions for worsening symptoms
    - **Follow-up**: Gastroenterology consultation within 1-2 weeks
    - **Cost Impact**: Reduces healthcare costs by avoiding unnecessary admissions
    
    **Moderate Risk Management (Scores 1-11)**:
    - **Disposition**: Hospital admission for observation and treatment
    - **Resuscitation**: IV access, fluid resuscitation, blood type and screen
    - **Monitoring**: Vital signs, serial CBC, clinical assessment
    - **Specialist Care**: Gastroenterology consultation within 24 hours
    - **Endoscopy**: Consider elective endoscopy within 24-48 hours
    
    **High Risk Management (Scores ≥12)**:
    - **Disposition**: Urgent hospital admission with intensive monitoring
    - **Resuscitation**: Large-bore IV access, aggressive resuscitation, blood products
    - **Monitoring**: Consider ICU admission, continuous monitoring
    - **Specialist Care**: Immediate gastroenterology consultation
    - **Endoscopy**: Urgent endoscopy within 12-24 hours or emergently if unstable
    
    **Quality Improvement Applications**:
    
    **Clinical Protocol Integration**:
    - **Standardization**: Consistent risk assessment across providers
    - **Resource Optimization**: Appropriate allocation of hospital resources
    - **Quality Metrics**: Track outcomes and intervention rates by risk category
    - **Clinical Decision Support**: Integration into electronic health records
    
    **Performance Monitoring**:
    - **Outcome Tracking**: Monitor intervention rates, mortality, length of stay
    - **Cost Analysis**: Evaluate cost-effectiveness of risk-stratified care
    - **Provider Education**: Train staff on score interpretation and protocols
    - **Continuous Improvement**: Refine protocols based on outcome data
    
    **SPECIAL CLINICAL CONSIDERATIONS**:
    
    **Limitations and Considerations**:
    - **Variceal Bleeding**: Score may underestimate risk in known variceal bleeding
    - **Anticoagulation**: May not fully account for anticoagulation effects
    - **Elderly Patients**: Consider age-related factors not captured in score
    - **Comorbidities**: Assess additional comorbidities affecting bleeding risk
    
    **Clinical Integration Requirements**:
    - **Clinical Judgment**: Use score to supplement, not replace, clinical assessment
    - **Local Protocols**: Adapt score application to local resources and protocols
    - **Monitoring Changes**: Recalculate score if clinical status changes
    - **Documentation**: Record score and rationale for management decisions
    
    Reference: Blatchford O, et al. Lancet. 2000;356(9238):1318-1321.
    """
    
    result: int = Field(
        ...,
        description="Total Glasgow-Blatchford Bleeding Score calculated from clinical parameters (0-23 points)",
        ge=0,
        le=23,
        example=4
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for GBS score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation with risk assessment and evidence-based management recommendations",
        example="Glasgow-Blatchford Bleeding Score: 4/23. [BUN: 25.0 mg/dL (3 points); Hemoglobin: 11.5 g/dL (3 points); Systolic BP: 105 mmHg (1 point); Heart rate: 95 bpm (0 points); Melena present (1 point)]. Low to moderate risk for intervention in upper GI bleeding. Consider hospital admission for clinical observation and assessment. Risk for blood transfusion or endoscopic intervention is present but relatively low. Monitor vital signs, complete blood count, and clinical status closely. Consider early gastroenterology consultation if symptoms worsen. Initiate proton pump inhibitor therapy. Ensure adequate IV access and type and screen blood products."
    )
    
    stage: str = Field(
        ...,
        description="Risk category based on GBS score (Low Risk, Low-Moderate Risk, Moderate Risk, High Risk)",
        example="Low-Moderate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of risk level and clinical significance",
        example="Low to moderate risk requiring clinical assessment"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 4,
                "unit": "points",
                "interpretation": "Glasgow-Blatchford Bleeding Score: 4/23. [BUN: 25.0 mg/dL (3 points); Hemoglobin: 11.5 g/dL (3 points); Systolic BP: 105 mmHg (1 point); Heart rate: 95 bpm (0 points); Melena present (1 point)]. Low to moderate risk for intervention in upper GI bleeding. Consider hospital admission for clinical observation and assessment. Risk for blood transfusion or endoscopic intervention is present but relatively low. Monitor vital signs, complete blood count, and clinical status closely. Consider early gastroenterology consultation if symptoms worsen. Initiate proton pump inhibitor therapy. Ensure adequate IV access and type and screen blood products.",
                "stage": "Low-Moderate Risk",
                "stage_description": "Low to moderate risk requiring clinical assessment"
            }
        }