"""
COVID Home Safely Now (CHOSEN) Risk Score Models

Request and response models for CHOSEN Risk Score calculation for COVID-19 discharge suitability.

References (Vancouver style):
1. Levine DM, Ouchi K, Blanchfield B, Diamond A, Licurse A, Pu CT, et al. 
   Hospital-level care at home for acutely ill adults: a pilot randomized 
   controlled trial. J Gen Intern Med. 2018;33(5):729-736.
2. Levine DM, Ouchi K, Blanchfield B, Saenz A, Burke K, Paz M, et al. 
   Hospital-Level Care at Home for Acutely Ill Adults: A Randomized Controlled Trial. 
   Ann Intern Med. 2020;172(2):77-85.

The COVID Home Safely Now (CHOSEN) Risk Score predicts suitability for discharge 
in COVID-19 patients by assessing the 14-day risk of needing supplemental oxygen, 
requiring ICU-level care, or death. This evidence-based tool supports clinical 
decision-making during COVID-19 pandemic periods when hospital capacity management 
is critical while maintaining patient safety standards.

Clinical Background and Development:

The CHOSEN Risk Score was developed during the COVID-19 pandemic to address the 
critical need for objective criteria to guide safe discharge decisions for COVID-19 
patients. Traditional discharge planning often relied on subjective clinical 
assessment, which could lead to either premature discharge with increased readmission 
risk or unnecessary prolonged hospitalization during surge periods.

Hospital-Level Care at Home Program:
The CHOSEN score emerged from research on hospital-level care at home programs, 
which provide acute care services in patients' homes as an alternative to traditional 
inpatient hospitalization. These programs demonstrated that carefully selected 
patients could receive safe, effective care at home with appropriate monitoring 
and support systems.

Validation and Performance Characteristics:
The CHOSEN Risk Score demonstrated 83% sensitivity and 82% specificity in the 
original validation study for predicting patients suitable for home-based care. 
The tool was specifically validated during COVID-19 surge periods when traditional 
hospital capacity was strained and alternative care models were essential.

Risk Prediction Framework:
The score predicts three critical outcomes within 14 days of potential discharge:
1. Need for supplemental oxygen therapy
2. Requirement for intensive care unit-level interventions
3. Mortality risk

Two-Version Scoring System:

Full CHOSEN Score (with albumin):
Uses three clinical variables with weighted point allocation:
- Age (demographic risk factor): 0-5 points
- Oxygen saturation (respiratory status): 0-21 points  
- Albumin level (nutritional/inflammatory marker): 0-29 points
Total possible points: 0-55
Discharge threshold: ≥30 points suggests suitability for home care

Modified CHOSEN Score (without albumin):
Alternative version when laboratory values are unavailable:
- Age (demographic risk factor): 0-5 points
- Oxygen saturation (respiratory status): 0-21 points
- Respiratory rate (respiratory effort): 0-10 points
Total possible points: 0-36
Discharge threshold: ≥20 points suggests suitability for home care

Clinical Variable Rationale:

Age Stratification:
Younger patients (18-45 years) receive maximum points (5) reflecting lower 
risk of severe COVID-19 outcomes. Point allocation decreases with advancing 
age, reflecting epidemiological data showing increased mortality and morbidity 
with older age groups during the COVID-19 pandemic.

Oxygen Saturation Assessment:
SpO2 serves as the primary indicator of respiratory function and disease severity. 
Higher oxygen saturations (>98%) receive maximum points (21), while hypoxemia 
(<94%) receives zero points, reflecting the strong association between hypoxemia 
and poor COVID-19 outcomes.

Albumin Level (Full Score):
Albumin serves as both a nutritional marker and inflammatory indicator. Lower 
albumin levels often reflect severe illness, poor nutritional status, or 
systemic inflammation - all associated with worse COVID-19 outcomes. Normal 
albumin levels (>3.7 g/dL) receive maximum points (29), making this the most 
heavily weighted variable in the full score.

Respiratory Rate (Modified Score):
When albumin is unavailable, respiratory rate serves as an alternative indicator 
of respiratory distress and disease severity. Normal respiratory rates (≤20 
breaths/min) suggest stable respiratory function, while tachypnea indicates 
potential respiratory compromise.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List


class ChosenCovidDischargeRequest(BaseModel):
    """
    Request model for COVID Home Safely Now (CHOSEN) Risk Score Calculation
    
    The CHOSEN Risk Score provides objective criteria for assessing COVID-19 
    patient suitability for home discharge by predicting 14-day risk of clinical 
    deterioration requiring supplemental oxygen, ICU care, or resulting in mortality.
    
    Clinical Assessment Framework and Parameter Specifications:
    
    The CHOSEN calculation supports two scoring approaches based on laboratory 
    availability, allowing flexibility in clinical settings while maintaining 
    validated predictive accuracy for discharge decision-making.
    
    Age Assessment:
    Age serves as a fundamental demographic risk factor for COVID-19 severity 
    and outcomes, with point allocation reflecting epidemiological risk patterns 
    observed throughout the pandemic across diverse patient populations.
    
    Clinical Age Categories:
    - Ages 18-45 years: Maximum points (5) reflecting lowest risk demographic
    - Ages 46-59 years: Moderate points (2) for intermediate risk group  
    - Ages 60-73 years: Minimal points (1) acknowledging increased risk
    - Ages >73 years: Zero points reflecting highest risk demographic
    
    Age-Related Risk Considerations:
    - Older patients demonstrate higher rates of severe disease progression
    - Immune senescence affects disease response and recovery capacity
    - Comorbidity burden typically increases with advancing age
    - Social support systems may vary across age groups affecting home care feasibility
    
    Oxygen Saturation Assessment:
    Oxygen saturation represents the primary objective measure of respiratory 
    function and COVID-19 disease severity, serving as a critical indicator 
    for discharge safety and monitoring respiratory status progression.
    
    SpO2 Measurement Standards:
    - Room air measurement preferred for accurate assessment
    - Pulse oximetry measurement using calibrated equipment
    - Multiple measurements recommended for accuracy verification
    - Consider patient positioning and environmental factors
    
    SpO2 Clinical Categories:
    - >98%: Excellent oxygenation (21 points) - optimal for discharge consideration
    - 97-98%: Good oxygenation (14 points) - generally suitable for home care
    - 94-96%: Mild hypoxemia (9 points) - requires careful evaluation
    - <94%: Significant hypoxemia (0 points) - high risk, consider inpatient care
    
    Respiratory Status Implications:
    - Higher saturations correlate with stable respiratory function
    - Hypoxemia indicates potential for rapid deterioration
    - Consider altitude and baseline patient oxygen requirements
    - Monitor for exercise desaturation if ambulation planned
    
    Albumin Level Assessment (Full CHOSEN Score):
    Serum albumin serves as both a nutritional marker and inflammatory indicator, 
    providing insight into disease severity, systemic inflammation, and overall 
    physiologic reserve for recovery and home-based care management.
    
    Laboratory Measurement Considerations:
    - Standard serum albumin measurement using automated chemistry analyzer
    - Fasting not required for accurate measurement
    - Consider timing relative to fluid resuscitation or diuretic therapy
    - Interpret in context of overall clinical presentation
    
    Albumin Clinical Categories:
    - >3.7 g/dL: Normal albumin (29 points) - excellent nutritional/inflammatory status
    - 3.4-3.7 g/dL: Mild hypoalbuminemia (15 points) - moderate concern
    - 2.8-3.3 g/dL: Moderate hypoalbuminemia (5 points) - significant concern
    - <2.8 g/dL: Severe hypoalbuminemia (0 points) - high risk for complications
    
    Clinical Significance of Albumin:
    - Reflects hepatic synthetic function and nutritional status
    - Lower levels associated with increased mortality in COVID-19
    - Marker of systemic inflammation and capillary leak syndrome
    - Prognostic indicator for recovery capacity and wound healing
    
    Respiratory Rate Assessment (Modified CHOSEN Score):
    When albumin laboratory values are unavailable, respiratory rate serves as 
    an alternative clinical indicator of respiratory effort, disease severity, 
    and physiologic stress, maintaining predictive accuracy for discharge planning.
    
    Measurement Standards:
    - Count respiratory rate over full 60-second period for accuracy
    - Observe patient at rest without awareness of monitoring when possible
    - Consider respiratory pattern, effort, and accessory muscle use
    - Document any supplemental oxygen requirements
    
    Respiratory Rate Clinical Categories:
    - ≤20 breaths/min: Normal respiratory effort (10 points) - stable for discharge
    - 21-24 breaths/min: Mild tachypnea (5 points) - requires evaluation
    - ≥25 breaths/min: Significant tachypnea (0 points) - concerning for instability
    
    Respiratory Effort Considerations:
    - Tachypnea may indicate respiratory distress or systemic illness
    - Consider baseline respiratory rate and chronic conditions
    - Evaluate work of breathing and patient comfort level
    - Assess correlation with oxygen saturation and clinical presentation
    
    Clinical Implementation Guidelines:
    
    Score Selection Strategy:
    - Use Full CHOSEN Score (with albumin) when laboratory values available
    - Use Modified CHOSEN Score (with respiratory rate) when albumin unavailable
    - Both versions maintain validated predictive accuracy for clinical decision-making
    - Consider institutional protocols and resource availability
    
    Patient Assessment Requirements:
    - Comprehensive clinical evaluation beyond score calculation
    - Assessment of social support systems and home environment
    - Evaluation of patient and family understanding of monitoring requirements
    - Consideration of follow-up care accessibility and telemedicine capabilities
    
    Quality Assurance Considerations:
    - Ensure accurate vital sign measurement using calibrated equipment
    - Verify laboratory values are current and reflect patient status
    - Document clinical reasoning and additional factors influencing discharge decision
    - Maintain clear communication with patient and family regarding discharge plan
    
    This comprehensive CHOSEN assessment provides clinicians with evidence-based 
    criteria for safe COVID-19 discharge planning while supporting efficient 
    resource utilization during pandemic surge periods and maintaining optimal 
    patient safety standards.
    
    References (Vancouver style):
    1. Levine DM, Ouchi K, Blanchfield B, Diamond A, Licurse A, Pu CT, et al. 
       Hospital-level care at home for acutely ill adults: a pilot randomized 
       controlled trial. J Gen Intern Med. 2018;33(5):729-736.
    2. Levine DM, Ouchi K, Blanchfield B, Saenz A, Burke K, Paz M, et al. 
       Hospital-Level Care at Home for Acutely Ill Adults: A Randomized Controlled Trial. 
       Ann Intern Med. 2020;172(2):77-85.
    """
    
    age: int = Field(
        ...,
        ge=18,
        le=120,
        description="Patient age in years. Age stratification reflects COVID-19 epidemiological risk patterns with younger patients receiving higher points due to lower risk of severe outcomes",
        example=45
    )
    
    oxygen_saturation: int = Field(
        ...,
        ge=80,
        le=100,
        description="Oxygen saturation on room air measured by pulse oximetry. Primary indicator of respiratory function and COVID-19 disease severity. Higher values indicate better respiratory status",
        example=98
    )
    
    albumin_level: Optional[float] = Field(
        None,
        ge=1.0,
        le=6.0,
        description="Serum albumin level in g/dL for Full CHOSEN Score. Serves as nutritional marker and inflammatory indicator. Higher levels suggest better nutritional status and lower systemic inflammation",
        example=3.8
    )
    
    respiratory_rate: Optional[int] = Field(
        None,
        ge=8,
        le=50,
        description="Respiratory rate in breaths per minute for Modified CHOSEN Score when albumin unavailable. Indicator of respiratory effort and disease severity. Lower rates suggest stable respiratory function",
        example=18
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": 45,
                "oxygen_saturation": 98,
                "albumin_level": 3.8,
                "respiratory_rate": 18
            }
        }


class CalculationDetails(BaseModel):
    """Detailed calculation information for CHOSEN assessment"""
    
    score_type: str = Field(
        ...,
        description="Type of CHOSEN score calculated (Full CHOSEN Score or Modified CHOSEN Score)",
        example="Full CHOSEN Score"
    )
    
    age_points: int = Field(
        ...,
        description="Points allocated for age category",
        example=5
    )
    
    spo2_points: int = Field(
        ...,
        description="Points allocated for oxygen saturation level",
        example=21
    )
    
    third_component: str = Field(
        ...,
        description="Description of third component (albumin or respiratory rate) with points",
        example="Albumin: 3.8 g/dL (29 pts)"
    )
    
    total_score: int = Field(
        ...,
        description="Total CHOSEN score calculated",
        example=55
    )
    
    threshold_used: int = Field(
        ...,
        description="Threshold value used for discharge suitability determination",
        example=30
    )
    
    discharge_recommendation: str = Field(
        ...,
        description="Clinical recommendation based on score",
        example="Consider for home discharge"
    )
    
    clinical_considerations: List[str] = Field(
        ...,
        description="List of clinical considerations for discharge planning",
        example=[
            "Low risk for clinical deterioration within 14 days",
            "Ensure appropriate follow-up is arranged",
            "Provide clear instructions for symptom monitoring"
        ]
    )


class ChosenCovidDischargeResponse(BaseModel):
    """
    Response model for COVID Home Safely Now (CHOSEN) Risk Score Calculation
    
    Provides comprehensive assessment of COVID-19 patient discharge suitability 
    with evidence-based recommendations, risk stratification, and clinical 
    guidance for safe home-based care planning during pandemic conditions.
    
    CHOSEN Risk Score Assessment Framework and Clinical Interpretation:
    
    Score Overview and Discharge Decision Support:
    The CHOSEN Risk Score provides objective, validated criteria for assessing 
    COVID-19 patient suitability for home discharge by predicting 14-day risk 
    of clinical deterioration requiring re-hospitalization, supplemental oxygen, 
    ICU-level care, or mortality. This evidence-based tool supports clinical 
    decision-making while maintaining patient safety standards.
    
    Clinical Applications and Discharge Planning Framework:
    
    High Risk - Unlikely Suitable for Discharge:
    
    Clinical Significance:
    - Score below discharge threshold indicates elevated risk for deterioration
    - High probability of requiring re-hospitalization or intensive interventions
    - Significant risk factors present requiring continued inpatient monitoring
    - Poor physiologic reserve or multiple concerning clinical parameters
    
    Immediate Clinical Actions:
    - Continued inpatient monitoring and management recommended
    - Comprehensive assessment of modifiable risk factors
    - Optimization of medical therapy and supportive care measures
    - Daily reassessment of clinical status and score re-calculation as appropriate
    
    Management Considerations:
    - Address underlying factors contributing to high risk score
    - Consider intensive monitoring protocols if discharge unavoidable
    - Ensure robust social support systems and immediate access to care
    - Arrange frequent follow-up with telemedicine or home nursing services
    
    Prognosis and Monitoring Requirements:
    - Requires close observation for signs of clinical deterioration
    - Higher likelihood of needing supplemental oxygen or ICU care
    - Enhanced monitoring protocols essential if home-based care considered
    - Family education crucial for recognition of warning signs
    
    Borderline Risk - Clinical Judgment Required:
    
    Clinical Significance:
    - Intermediate risk requiring individualized assessment and clinical judgment
    - Score near threshold necessitating consideration of additional factors
    - Balance between patient safety and resource utilization considerations
    - Opportunity for shared decision-making with patient and family
    
    Assessment Strategy:
    - Comprehensive evaluation of patient-specific circumstances
    - Assessment of social support systems and home environment safety
    - Evaluation of comorbidities and functional status
    - Consider availability and accessibility of follow-up care resources
    
    Decision-Making Framework:
    - Weight additional clinical factors beyond score components
    - Assess patient preference and confidence in home management
    - Evaluate caregiver capacity and support system adequacy
    - Consider geographic proximity to emergency care if needed
    
    Enhanced Monitoring Requirements:
    - More frequent follow-up than typical discharge planning
    - Consider home nursing visits or remote monitoring technology
    - Clear escalation protocols for symptom progression
    - Telemedicine appointments within 24-48 hours of discharge
    
    Low Risk - Likely Suitable for Discharge:
    
    Clinical Significance:
    - Score above threshold indicates low risk for clinical deterioration
    - Excellent physiologic parameters suggesting stable disease course
    - Appropriate candidate for home-based care with standard monitoring
    - Good prognosis with proper discharge planning and follow-up
    
    Discharge Planning Requirements:
    - Standard discharge education and symptom monitoring instructions
    - Arrangement of appropriate outpatient follow-up care
    - Prescription management and medication reconciliation
    - Clear instructions for accessing urgent care if symptoms worsen
    
    Home Care Optimization:
    - Patient and family education on COVID-19 home management
    - Symptom monitoring guidelines and warning sign recognition
    - Isolation precautions and infection control measures
    - Activity guidelines and return-to-work considerations
    
    Follow-up Care Coordination:
    - Routine outpatient follow-up within appropriate timeframe
    - Primary care provider notification and care coordination
    - Consider telemedicine options for convenience and safety
    - Community resource connection for ongoing support needs
    
    Special Clinical Considerations and Quality Assurance:
    
    Score Limitations and Clinical Context:
    - CHOSEN score provides objective guidance but does not replace clinical judgment
    - Additional factors may influence discharge safety beyond score components
    - Consider patient preference, social circumstances, and resource availability
    - Validate score accuracy with comprehensive clinical assessment
    
    Pandemic-Specific Considerations:
    - Tool developed and validated during COVID-19 surge periods
    - Particularly valuable when hospital capacity is constrained
    - Supports efficient resource allocation while maintaining safety
    - Consider evolving treatment standards and variant-specific considerations
    
    Quality Improvement and Safety Monitoring:
    - Track discharge outcomes and readmission rates for quality improvement
    - Monitor patient satisfaction and safety events in discharged patients
    - Regular assessment of score performance in local patient population
    - Continuous education for clinical staff on appropriate tool utilization
    
    Implementation Best Practices:
    - Integrate CHOSEN scoring into standard discharge planning workflows
    - Ensure consistent measurement techniques for score components
    - Document rationale for discharge decisions including additional factors considered
    - Maintain clear communication between inpatient and outpatient care teams
    
    This comprehensive CHOSEN assessment provides clinicians with validated, 
    evidence-based criteria for safe COVID-19 discharge planning, supporting 
    optimal patient outcomes while enabling efficient healthcare resource 
    utilization during challenging pandemic conditions.
    
    Reference: Levine DM, et al. Ann Intern Med. 2020;172(2):77-85.
    """
    
    result: int = Field(
        ...,
        description="CHOSEN Risk Score points indicating discharge suitability",
        example=55
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the CHOSEN score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of the CHOSEN score with specific discharge recommendations and risk assessment",
        example="Full CHOSEN Score of 55 points is above the threshold of 30, indicating the patient is likely suitable for home discharge with appropriate follow-up and monitoring arrangements."
    )
    
    stage: str = Field(
        ...,
        description="Discharge suitability classification (Unlikely Suitable for Discharge, Borderline Risk, Likely Suitable for Discharge)",
        example="Likely Suitable for Discharge"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the discharge suitability category",
        example="Low risk - may be appropriate for home management"
    )
    
    calculation_details: CalculationDetails = Field(
        ...,
        description="Detailed calculation information including score components and clinical recommendations"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 55,
                "unit": "points",
                "interpretation": "Full CHOSEN Score of 55 points is above the threshold of 30, indicating the patient is likely suitable for home discharge with appropriate follow-up and monitoring arrangements.",
                "stage": "Likely Suitable for Discharge",
                "stage_description": "Low risk - may be appropriate for home management",
                "calculation_details": {
                    "score_type": "Full CHOSEN Score",
                    "age_points": 5,
                    "spo2_points": 21,
                    "third_component": "Albumin: 3.8 g/dL (29 pts)",
                    "total_score": 55,
                    "threshold_used": 30,
                    "discharge_recommendation": "Consider for home discharge",
                    "clinical_considerations": [
                        "Low risk for clinical deterioration within 14 days",
                        "Ensure appropriate follow-up is arranged",
                        "Provide clear instructions for symptom monitoring",
                        "Consider telemedicine or nursing follow-up",
                        "Ensure patient has adequate social support"
                    ]
                }
            }
        }