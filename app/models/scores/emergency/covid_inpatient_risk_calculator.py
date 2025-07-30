"""
COVID-19 Inpatient Risk Calculator (CIRC) Models

Request and response models for CIRC risk assessment for COVID-19 hospitalized patients.

References (Vancouver style):
1. Garibaldi BT, Fiksel J, Muschelli J, Robinson ML, Rouhizadeh M, Perin J, et al. 
   Patient Trajectories Among Persons Hospitalized for COVID-19: A Cohort Study. 
   Ann Intern Med. 2021;174(1):33-41. doi: 10.7326/M20-3905.

The COVID-19 Inpatient Risk Calculator (CIRC) predicts the likelihood of inpatient 
mortality or severe disease progression in COVID-19 patients within 7 days of hospital 
admission. This machine learning-based model incorporates 23 clinical variables 
available at hospital admission to provide objective risk stratification and support 
clinical decision-making for hospitalized COVID-19 patients.

Clinical Background and Development:

The CIRC was developed from a cohort of 832 patients hospitalized with COVID-19 
across 5 hospitals in the Johns Hopkins Health System between March 1, 2020 and 
April 24, 2020, with follow-up through June 24, 2020. This represents one of the 
first comprehensive predictive models developed during the early pandemic period 
when clinical understanding of COVID-19 progression patterns was still evolving.

Model Performance and Validation:
The CIRC demonstrated strong predictive performance with area under the curve (AUC) 
values of 0.85 at day 2, 0.79 at day 4, and 0.79 at day 7. The model performs 
optimally for predicting outcomes in the first 2 days of hospitalization, making 
it particularly valuable for early risk stratification and resource allocation 
decisions at the time of hospital admission.

Primary Outcome Definition:
The model predicts progression to severe disease or death, where severe disease 
is defined as requiring any of the following interventions:
- High-flow nasal cannula oxygen therapy
- Non-invasive positive pressure ventilation (NIPPV)
- Invasive mechanical ventilation
- Extracorporeal membrane oxygenation (ECMO)
- Vasopressor support for hemodynamic instability

Risk Stratification Framework:
The CIRC provides risk probabilities ranging from as low as 5% to over 90% based 
on different combinations of risk factors present at admission. This wide range 
of risk stratification enables clinicians to identify both very low-risk patients 
who may be candidates for early discharge and very high-risk patients requiring 
immediate intensive monitoring and intervention.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any, List


class CovidInpatientRiskCalculatorRequest(BaseModel):
    """
    Request model for COVID-19 Inpatient Risk Calculator (CIRC)
    
    Comprehensive risk assessment model incorporating 23 clinical variables available 
    at hospital admission to predict 7-day risk of severe disease progression or 
    mortality in COVID-19 patients. The model supports evidence-based clinical 
    decision-making and resource allocation in hospitalized COVID-19 patients.
    
    Parameter Categories and Clinical Significance:
    
    Demographic and Social Factors:
    Age, sex, race, and nursing home residence status provide foundational risk 
    stratification based on well-established epidemiological patterns observed 
    during the COVID-19 pandemic across diverse patient populations.
    
    Comorbidity Assessment:
    Body Mass Index (BMI) and Charlson Comorbidity Index capture pre-existing 
    health conditions that significantly influence COVID-19 disease severity 
    and progression risk, enabling personalized risk assessment.
    
    Clinical Presentation:
    Symptom profiles including respiratory, gastrointestinal, constitutional 
    symptoms, loss of taste/smell, and fever presence provide insights into 
    disease manifestation patterns and severity indicators at presentation.
    
    Vital Signs Assessment:
    Respiratory rate and pulse measurements represent immediate physiologic 
    indicators of disease severity and hemodynamic stability at admission, 
    serving as critical early warning markers for clinical deterioration.
    
    Laboratory Risk Markers:
    Comprehensive laboratory panel including hematologic parameters (hemoglobin, 
    white blood cell count, absolute lymphocyte count), metabolic markers 
    (albumin, creatinine), inflammatory indicators (C-reactive protein, ferritin), 
    coagulation markers (D-dimer), hepatic function (ALT), and cardiac markers 
    (troponin) provide objective measures of organ system involvement and 
    systemic inflammatory response.
    
    Clinical Implementation Considerations:
    
    Data Collection Requirements:
    All 23 variables should ideally be collected within the first 24 hours of 
    hospital admission to optimize model performance and clinical utility. 
    The model was specifically designed and validated using admission data.
    
    Risk Stratification Applications:
    - Early identification of high-risk patients requiring intensive monitoring
    - Resource allocation decisions during surge capacity periods
    - Clinical trial enrollment and treatment escalation decisions
    - Goals of care discussions with patients and families
    - Discharge planning and step-down care considerations
    
    Model Limitations and Considerations:
    - Developed during early pandemic period (March-April 2020)
    - Not externally validated across different healthcare systems
    - Developed before widespread vaccine availability
    - Excludes pediatric patients (age <18 years)
    - Performance may vary with different COVID-19 variants
    - Should complement, not replace, clinical judgment
    
    Quality Assurance Requirements:
    - Ensure accurate and timely laboratory result availability
    - Verify vital sign measurements using calibrated equipment
    - Document symptom assessment using standardized protocols
    - Consider timing of measurements relative to presentation
    - Integrate results with comprehensive clinical assessment
    
    References (Vancouver style):
    1. Garibaldi BT, Fiksel J, Muschelli J, Robinson ML, Rouhizadeh M, Perin J, et al. 
       Patient Trajectories Among Persons Hospitalized for COVID-19: A Cohort Study. 
       Ann Intern Med. 2021;174(1):33-41. doi: 10.7326/M20-3905.
    """
    
    age: int = Field(
        ...,
        ge=18,
        le=120,
        description="Patient age in years. Age represents the strongest demographic risk factor for COVID-19 severity with exponential risk increase in older adults",
        example=65
    )
    
    sex: Literal["male", "female"] = Field(
        ...,
        description="Biological sex. Male sex associated with increased risk of severe COVID-19 outcomes across multiple studies and populations",
        example="male"
    )
    
    race: Literal["white", "non_white"] = Field(
        ...,
        description="Patient race category. Non-white race associated with increased COVID-19 severity risk due to complex social determinants and biological factors",
        example="white"
    )
    
    nursing_home_admission: Literal["yes", "no"] = Field(
        ...,
        description="Admission from nursing home or long-term care facility. Strong predictor of poor outcomes due to frailty and comorbidity burden",
        example="no"
    )
    
    bmi: float = Field(
        ...,
        ge=15.0,
        le=60.0,
        description="Body Mass Index in kg/m². Obesity (BMI >30) significantly increases risk of severe COVID-19 complications and mechanical ventilation requirements",
        example=28.5
    )
    
    charlson_score: int = Field(
        ...,
        ge=0,
        le=20,
        description="Charlson Comorbidity Index score. Quantifies comorbidity burden with higher scores indicating increased mortality risk",
        example=3
    )
    
    respiratory_symptoms: Literal["yes", "no"] = Field(
        ...,
        description="Presence of respiratory symptoms (cough, shortness of breath, chest pain). Primary COVID-19 manifestation with prognostic significance",
        example="yes"
    )
    
    gastrointestinal_symptoms: Literal["yes", "no"] = Field(
        ...,
        description="Presence of gastrointestinal symptoms (nausea, vomiting, diarrhea, abdominal pain). Associated with increased disease severity",
        example="no"
    )
    
    constitutional_symptoms: Literal["yes", "no"] = Field(
        ...,
        description="Presence of constitutional symptoms (fatigue, malaise, body aches, headache). Indicates systemic inflammatory response",
        example="yes"
    )
    
    loss_taste_smell: Literal["yes", "no"] = Field(
        ...,
        description="Loss of taste (ageusia) or smell (anosmia). Paradoxically may indicate less severe disease course in some studies",
        example="no"
    )
    
    fever: Literal["yes", "no"] = Field(
        ...,
        description="Presence of fever (temperature ≥100.4°F or 38°C). Common presenting symptom with variable prognostic significance",
        example="yes"
    )
    
    respiratory_rate: int = Field(
        ...,
        ge=8,
        le=50,
        description="Respiratory rate in breaths per minute. Tachypnea (>24) indicates respiratory distress and increased severity risk",
        example=22
    )
    
    pulse: int = Field(
        ...,
        ge=40,
        le=200,
        description="Heart rate in beats per minute. Tachycardia may indicate hemodynamic stress, hypoxemia, or systemic inflammatory response",
        example=95
    )
    
    hemoglobin: float = Field(
        ...,
        ge=5.0,
        le=20.0,
        description="Hemoglobin level in g/dL. Anemia associated with increased mortality risk and may indicate chronic disease or bleeding",
        example=12.8
    )
    
    white_blood_cell_count: float = Field(
        ...,
        ge=1.0,
        le=50.0,
        description="White blood cell count in ×10³/μL. Leukocytosis may indicate bacterial superinfection or severe inflammatory response",
        example=8.5
    )
    
    absolute_lymphocyte_count: float = Field(
        ...,
        ge=0.1,
        le=10.0,
        description="Absolute lymphocyte count in ×10³/μL. Lymphopenia (<1.0) strongly associated with severe COVID-19 and poor outcomes",
        example=0.8
    )
    
    albumin: float = Field(
        ...,
        ge=1.0,
        le=6.0,
        description="Serum albumin level in g/dL. Hypoalbuminemia (<3.5) indicates poor nutritional status, chronic disease, or systemic inflammation",
        example=3.2
    )
    
    creatinine: float = Field(
        ...,
        ge=0.5,
        le=15.0,
        description="Serum creatinine level in mg/dL. Elevated levels indicate kidney dysfunction, associated with increased COVID-19 mortality",
        example=1.1
    )
    
    alt: float = Field(
        ...,
        ge=5.0,
        le=1000.0,
        description="Alanine aminotransferase (ALT) in U/L. Elevated levels may indicate hepatic involvement or drug-induced liver injury",
        example=45
    )
    
    d_dimer: float = Field(
        ...,
        ge=0.1,
        le=50.0,
        description="D-dimer level in mg/L. Elevated levels (>1.0) indicate coagulopathy and thrombotic risk, strongly associated with poor outcomes",
        example=2.5
    )
    
    c_reactive_protein: float = Field(
        ...,
        ge=0.1,
        le=500.0,
        description="C-reactive protein level in mg/L. Acute phase reactant indicating systemic inflammation, with higher levels predicting severity",
        example=125
    )
    
    ferritin: float = Field(
        ...,
        ge=10.0,
        le=5000.0,
        description="Ferritin level in ng/mL. Hyperferritinemia (>500) indicates severe inflammation and cytokine storm, associated with poor prognosis",
        example=850
    )
    
    troponin_elevated: Literal["yes", "no"] = Field(
        ...,
        description="Elevated troponin levels above normal laboratory reference range. Indicates cardiac injury and significantly increases mortality risk",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": 65,
                "sex": "male",
                "race": "white",
                "nursing_home_admission": "no",
                "bmi": 28.5,
                "charlson_score": 3,
                "respiratory_symptoms": "yes",
                "gastrointestinal_symptoms": "no",
                "constitutional_symptoms": "yes",
                "loss_taste_smell": "no",
                "fever": "yes",
                "respiratory_rate": 22,
                "pulse": 95,
                "hemoglobin": 12.8,
                "white_blood_cell_count": 8.5,
                "absolute_lymphocyte_count": 0.8,
                "albumin": 3.2,
                "creatinine": 1.1,
                "alt": 45,
                "d_dimer": 2.5,
                "c_reactive_protein": 125,
                "ferritin": 850,
                "troponin_elevated": "no"
            }
        }


class CalculationDetails(BaseModel):
    """Detailed calculation information for CIRC assessment"""
    
    total_risk_score: float = Field(
        ...,
        description="Total calculated risk score from all components",
        example=5.2
    )
    
    age_score: float = Field(
        ...,
        description="Risk score contribution from age",
        example=1.8
    )
    
    vital_score: float = Field(
        ...,
        description="Risk score contribution from vital signs",
        example=0.0
    )
    
    lab_score: float = Field(
        ...,
        description="Risk score contribution from laboratory values",
        example=2.7
    )
    
    clinical_score: float = Field(
        ...,
        description="Risk score contribution from clinical factors",
        example=0.4
    )
    
    symptom_score: float = Field(
        ...,
        description="Risk score contribution from symptom profile",
        example=0.3
    )
    
    risk_factors: str = Field(
        ...,
        description="Summary of risk factor burden",
        example="Moderate risk factor burden"
    )
    
    monitoring_recommendations: str = Field(
        ...,
        description="Recommended level of monitoring and care",
        example="Enhanced monitoring with frequent assessments"
    )
    
    clinical_considerations: List[str] = Field(
        ...,
        description="List of clinical considerations for patient management",
        example=[
            "Moderate probability of clinical deterioration",
            "Enhanced monitoring protocols recommended",
            "Consider telemetry or step-down unit care"
        ]
    )


class CovidInpatientRiskCalculatorResponse(BaseModel):
    """
    Response model for COVID-19 Inpatient Risk Calculator (CIRC)
    
    Provides comprehensive risk assessment for COVID-19 hospitalized patients with 
    evidence-based risk stratification, clinical recommendations, and monitoring 
    guidance to support optimal patient care and resource allocation decisions.
    
    CIRC Risk Assessment Framework and Clinical Interpretation:
    
    Risk Probability Scale and Clinical Decision Support:
    The CIRC provides risk probabilities from 5% to over 90% for severe disease 
    progression or death within 7 days of hospital admission, enabling precise 
    risk stratification and individualized care planning for COVID-19 patients.
    
    Clinical Applications and Risk Management Framework:
    
    Low Risk (0-10%):
    
    Clinical Significance:
    - Minimal risk of severe disease progression or mortality within 7 days
    - Low probability of requiring intensive interventions or ICU care
    - Standard COVID-19 monitoring protocols appropriate for clinical management
    - Potential candidate for early discharge planning if clinically stable
    
    Management Recommendations:
    - Standard ward-level monitoring and nursing care protocols
    - Routine vital signs assessment every 4-6 hours
    - Daily clinical evaluation and symptom assessment
    - Standard laboratory monitoring as clinically indicated
    - Consider early discharge planning with appropriate follow-up
    
    Monitoring Requirements:
    - Standard telemetry monitoring if indicated by other conditions
    - Regular oxygen saturation monitoring on room air
    - Daily assessment of respiratory status and symptom progression
    - Standard infection control precautions and isolation protocols
    
    Discharge Considerations:
    - Potential candidate for early discharge if hemodynamically stable
    - Ensure appropriate outpatient follow-up arrangements
    - Provide clear instructions for symptom monitoring at home
    - Consider home monitoring programs or telemedicine follow-up
    
    Intermediate Risk (10-30%):
    
    Clinical Significance:
    - Moderate probability of clinical deterioration requiring intervention
    - Increased risk of respiratory decompensation or hemodynamic instability
    - Enhanced monitoring protocols recommended for early detection
    - Higher likelihood of prolonged hospitalization or complications
    
    Management Recommendations:
    - Enhanced monitoring with more frequent vital sign assessment
    - Consider telemetry monitoring for cardiac rhythm surveillance
    - Frequent respiratory status evaluation and oxygen requirement assessment
    - Proactive laboratory monitoring including inflammatory markers
    - Consider step-down unit care if available and appropriate
    
    Early Warning Systems:
    - Implement early warning score protocols for clinical deterioration
    - Lower threshold for rapid response team activation
    - Enhanced nursing assessment and documentation protocols
    - Consider continuous pulse oximetry monitoring
    
    Treatment Considerations:
    - Aggressive management of comorbid conditions
    - Optimization of supportive care measures
    - Consider anti-inflammatory or antiviral therapies if appropriate
    - Prophylactic anticoagulation per institutional protocols
    
    High Risk (30-60%):
    
    Clinical Significance:
    - High probability of requiring intensive interventions within 7 days
    - Significant risk of respiratory failure, shock, or multiorgan dysfunction
    - Intensive monitoring and close observation required
    - Strong consideration for ICU consultation or transfer
    
    Management Recommendations:
    - Intensive monitoring protocols with hourly assessments
    - ICU consultation for admission consideration and care planning
    - Continuous cardiac and respiratory monitoring
    - Frequent laboratory assessments including arterial blood gases
    - Aggressive supportive care and treatment optimization
    
    ICU Preparation:
    - Early ICU consultation for bed availability and transfer planning
    - Preparation for potential mechanical ventilation requirements
    - Hemodynamic monitoring and vasopressor availability
    - Consider prone positioning protocols if respiratory failure develops
    - Advanced cardiac monitoring and arrhythmia management
    
    Family Communication:
    - Goals of care discussion with patient and family members
    - Clear communication regarding prognosis and treatment options
    - Social work and chaplain services for psychosocial support
    - Advanced directive review and documentation
    
    Very High Risk (60%+):
    
    Clinical Significance:
    - Very high probability of severe complications or death within 7 days
    - Imminent risk of respiratory failure, circulatory shock, or multiorgan failure
    - Urgent ICU consultation and likely transfer indicated
    - Maximal supportive care and monitoring required
    
    Immediate Actions:
    - Urgent ICU consultation for immediate evaluation and transfer
    - Maximal supportive care with all available resources
    - Continuous invasive monitoring preparation
    - Consider advanced therapies including ECMO consultation
    - Immediate goals of care discussion with family
    
    Advanced Care Planning:
    - Comprehensive goals of care discussion with ethics consultation if needed
    - Advanced directive clarification and documentation
    - Family notification and support services activation
    - Consider palliative care consultation for symptom management
    - Documentation of resuscitation preferences and treatment limitations
    
    Resource Allocation:
    - Priority allocation of ICU beds and critical care resources
    - Advanced monitoring equipment and respiratory support devices
    - Specialized nursing care with enhanced staffing ratios
    - Multidisciplinary team involvement including critical care specialists
    
    Model Limitations and Clinical Integration:
    
    Validation Considerations:
    - Model developed during early pandemic period with limited external validation
    - Performance may vary with different COVID-19 variants and treatment standards
    - Should be integrated with clinical judgment and institutional protocols
    - Consider local population characteristics and resource availability
    
    Clinical Decision Integration:
    - Use as adjunct to comprehensive clinical assessment, not replacement
    - Consider additional factors not included in model (frailty, functional status)
    - Integrate with institutional early warning systems and protocols
    - Regular reassessment as clinical condition evolves
    
    Quality Improvement Applications:
    - Track model performance and outcomes in local patient population
    - Use for quality improvement initiatives and resource planning
    - Support clinical trial enrollment and treatment protocol decisions
    - Enable risk-adjusted outcome comparisons and benchmarking
    
    This comprehensive CIRC assessment provides clinicians with evidence-based 
    risk stratification for COVID-19 hospitalized patients, supporting optimal 
    resource allocation and individualized care planning during pandemic conditions.
    
    Reference: Garibaldi BT, et al. Ann Intern Med. 2021;174(1):33-41.
    """
    
    result: float = Field(
        ...,
        description="Risk probability percentage for severe disease progression or death within 7 days",
        example=25.8
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the risk assessment",
        example="%"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of the CIRC risk probability with specific management recommendations",
        example="CIRC risk probability of 25.8% indicates intermediate risk for severe disease progression or death within 7 days. Enhanced monitoring and close observation are recommended."
    )
    
    stage: str = Field(
        ...,
        description="Risk stratification category (Low Risk, Intermediate Risk, High Risk, Very High Risk)",
        example="Intermediate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Intermediate risk - enhanced monitoring recommended"
    )
    
    calculation_details: CalculationDetails = Field(
        ...,
        description="Detailed calculation information including score components and clinical recommendations"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 25.8,
                "unit": "%",
                "interpretation": "CIRC risk probability of 25.8% indicates intermediate risk for severe disease progression or death within 7 days. Enhanced monitoring and close observation are recommended.",
                "stage": "Intermediate Risk",
                "stage_description": "Intermediate risk - enhanced monitoring recommended",
                "calculation_details": {
                    "total_risk_score": 5.2,
                    "age_score": 1.8,
                    "vital_score": 0.0,
                    "lab_score": 2.7,
                    "clinical_score": 0.4,
                    "symptom_score": 0.3,
                    "risk_factors": "Moderate risk factor burden",
                    "monitoring_recommendations": "Enhanced monitoring with frequent assessments",
                    "clinical_considerations": [
                        "Moderate probability of clinical deterioration",
                        "Enhanced monitoring protocols recommended",
                        "Consider telemetry or step-down unit care",
                        "Frequent vital signs and laboratory monitoring",
                        "Early warning system alerts for clinical changes"
                    ]
                }
            }
        }