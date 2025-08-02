"""
Mumtaz Score for Readmission in Cirrhosis Models

Request and response models for Mumtaz Score calculation.

References (Vancouver style):
1. Mumtaz K, Issak A, Porter K, Kelly S, Hanje J, Michaels AJ, et al. Validation of 
   Risk Score in Predicting Early Readmissions in Decompensated Cirrhotic Patients: 
   A Model Based on the Administrative Database. Hepatology. 2019;70(2):630-639. 
   doi: 10.1002/hep.30274.
2. Berman K, Tandra S, Forssell K, Vuppalanchi R, Burton JR Jr, Nguyen JH, et al. 
   Incidence and predictors of 30-day readmission among patients hospitalized for 
   advanced liver disease. Clin Gastroenterol Hepatol. 2011;9(3):254-9. 
   doi: 10.1016/j.cgh.2010.10.035.
3. Volk ML, Tocco RS, Bazick J, Rakoski MO, Lok AS. Hospital readmissions among 
   patients with decompensated cirrhosis. Am J Gastroenterol. 2012;107(2):247-52. 
   doi: 10.1038/ajg.2011.314.

The Mumtaz Score is a validated prognostic tool that predicts 30-day readmission risk 
in patients with decompensated cirrhosis. It incorporates clinical and laboratory 
parameters available at hospital discharge to identify high-risk patients who may 
benefit from enhanced transitional care interventions and close outpatient follow-up.
"""

from pydantic import BaseModel, Field
from typing import Literal


class MumtazScoreRequest(BaseModel):
    """
    Request model for Mumtaz Score for Readmission in Cirrhosis
    
    The Mumtaz Score predicts 30-day readmission risk in patients with decompensated 
    cirrhosis using eight clinical and laboratory parameters available at discharge:
    
    Clinical Parameters:
    - Age: Older patients have higher readmission risk due to increased comorbidities
    - Length of stay: Longer stays may indicate more severe illness or complications
    - Previous admissions: Strong predictor of future healthcare utilization
    - Hepatic encephalopathy: Indicates advanced liver disease and poor prognosis
    - Ascites: Associated with portal hypertension and increased complications
    
    Laboratory Parameters:
    - Serum sodium: Hyponatremia is common in advanced cirrhosis and indicates poor prognosis
    - Albumin: Reflects synthetic liver function; lower levels indicate worse liver function
    - MELD score: Validated marker of liver disease severity and mortality risk
    
    Clinical Applications:
    - Risk stratification for discharge planning and resource allocation
    - Identification of patients requiring enhanced transitional care interventions
    - Quality improvement initiatives to reduce preventable readmissions
    - Care coordination between inpatient and outpatient providers
    - Patient and family counseling about post-discharge risks and expectations
    
    Risk Categories:
    
    Low Risk (<15%):
    - Standard discharge planning and routine follow-up sufficient
    - Regular primary care and hepatology follow-up as clinically indicated
    - Standard patient education and medication reconciliation
    
    Moderate Risk (15-30%):
    - Enhanced discharge planning with structured follow-up protocols
    - Early outpatient follow-up within 7-14 days recommended
    - Comprehensive medication reconciliation and patient education
    - Assessment of social support systems and access to care
    
    High Risk (30-50%):
    - Intensive discharge planning and close post-discharge monitoring
    - Early contact within 48-72 hours and follow-up within 1 week
    - Consider transitional care programs and care coordination services
    - Subspecialty referrals and enhanced monitoring protocols
    
    Very High Risk (≥50%):
    - Comprehensive transitional care interventions required
    - Consider prolonged hospitalization for optimization if appropriate
    - Intensive case management and immediate subspecialty follow-up
    - Frequent monitoring and consideration of alternative care settings
    
    Validation and Implementation:
    - Developed and validated in large administrative database cohorts
    - Demonstrated good discrimination (C-statistic 0.68-0.72) in validation studies
    - Applicable to adult patients with decompensated cirrhosis being discharged
    - Should be used in conjunction with clinical judgment and comprehensive assessment
    
    Limitations and Considerations:
    - Does not replace clinical assessment or comprehensive discharge planning
    - May not capture all relevant clinical factors affecting readmission risk
    - Requires accurate documentation of clinical parameters and laboratory values
    - Should be interpreted in context of local healthcare systems and resources
    - May need recalibration for different populations or healthcare settings
    
    References (Vancouver style):
    1. Mumtaz K, Issak A, Porter K, Kelly S, Hanje J, Michaels AJ, et al. Validation of 
    Risk Score in Predicting Early Readmissions in Decompensated Cirrhotic Patients: 
    A Model Based on the Administrative Database. Hepatology. 2019;70(2):630-639. 
    doi: 10.1002/hep.30274.
    2. Berman K, Tandra S, Forssell K, Vuppalanchi R, Burton JR Jr, Nguyen JH, et al. 
    Incidence and predictors of 30-day readmission among patients hospitalized for 
    advanced liver disease. Clin Gastroenterol Hepatol. 2011;9(3):254-9. 
    doi: 10.1016/j.cgh.2010.10.035.
    3. Volk ML, Tocco RS, Bazick J, Rakoski MO, Lok AS. Hospital readmissions among 
    patients with decompensated cirrhosis. Am J Gastroenterol. 2012;107(2):247-52. 
    doi: 10.1038/ajg.2011.314.
    """
    
    age: int = Field(
        ...,
        ge=18,
        le=120,
        description="Patient age in years. Older age is associated with increased readmission risk due to higher comorbidity burden and functional decline",
        example=65
    )
    
    serum_sodium: float = Field(
        ...,
        ge=100,
        le=160,
        description="Serum sodium level in mEq/L. Hyponatremia is common in advanced cirrhosis and indicates poor prognosis, increased complications, and higher readmission risk",
        example=132.0
    )
    
    albumin: float = Field(
        ...,
        ge=1.0,
        le=6.0,
        description="Serum albumin level in g/dL. Lower albumin reflects poor synthetic liver function and is associated with increased mortality and readmission risk",
        example=2.8
    )
    
    length_of_stay: int = Field(
        ...,
        ge=1,
        le=365,
        description="Length of current hospital stay in days. Longer stays may indicate more severe illness, complications, or social factors affecting discharge readiness",
        example=7
    )
    
    previous_admissions_6_months: int = Field(
        ...,
        ge=0,
        le=20,
        description="Number of hospital admissions in the previous 6 months. Prior healthcare utilization is one of the strongest predictors of future readmissions",
        example=2
    )
    
    meld_score: int = Field(
        ...,
        ge=6,
        le=40,
        description="Model for End-Stage Liver Disease (MELD) score at discharge. Higher MELD scores indicate more severe liver disease and increased mortality risk",
        example=18
    )
    
    hepatic_encephalopathy: Literal["yes", "no"] = Field(
        ...,
        description="Presence of hepatic encephalopathy during current admission. HE indicates advanced liver disease and is associated with increased readmission risk and mortality",
        example="yes"
    )
    
    ascites: Literal["yes", "no"] = Field(
        ...,
        description="Presence of ascites during current admission. Ascites indicates portal hypertension and is associated with increased complications and readmission risk",
        example="yes"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": 65,
                "serum_sodium": 132.0,
                "albumin": 2.8,
                "length_of_stay": 7,
                "previous_admissions_6_months": 2,
                "meld_score": 18,
                "hepatic_encephalopathy": "yes",
                "ascites": "yes"
            }
        }


class MumtazScoreResponse(BaseModel):
    """
    Response model for Mumtaz Score for Readmission in Cirrhosis
    
    The Mumtaz Score provides a quantitative assessment of 30-day readmission risk 
    in patients with decompensated cirrhosis, enabling targeted interventions and 
    resource allocation to improve outcomes and reduce preventable readmissions.
    
    Risk Stratification and Clinical Management:
    
    Low Risk (<15% readmission probability):
    - Standard discharge planning protocols are typically sufficient
    - Routine outpatient follow-up with primary care and hepatology as indicated
    - Standard patient education, medication reconciliation, and discharge instructions
    - Monitor for routine signs of decompensation and provide emergency contact information
    - Consider standard post-discharge care coordination with outpatient providers
    
    Moderate Risk (15-30% readmission probability):
    - Enhanced discharge planning with structured follow-up protocols recommended
    - Early outpatient follow-up within 7-14 days with hepatology or primary care
    - Comprehensive medication reconciliation with emphasis on adherence strategies
    - Detailed patient and family education about warning signs and when to seek care
    - Assessment of social support systems, transportation, and access to care barriers
    - Consider care coordination services and communication with outpatient providers
    
    High Risk (30-50% readmission probability):
    - Intensive discharge planning and close post-discharge monitoring required
    - Early post-discharge contact within 48-72 hours via phone or home visit
    - Expedited outpatient follow-up within 1 week with hepatology subspecialist
    - Consider transitional care programs, case management, and care coordination
    - Enhanced monitoring for medication adherence, dietary compliance, and symptoms
    - Assess need for home health services, nutrition counseling, and social services
    - Ensure immediate access to healthcare providers and clear emergency protocols
    
    Very High Risk (≥50% readmission probability):
    - Comprehensive transitional care interventions strongly recommended
    - Consider prolonged hospitalization for clinical optimization if appropriate
    - Intensive case management with frequent outpatient monitoring and support
    - Immediate subspecialty follow-up within 48-72 hours of discharge
    - Daily to every-other-day monitoring initially with gradual transition to routine care
    - Consider alternative care settings such as skilled nursing or transitional care units
    - Implement comprehensive care plans addressing medical, social, and functional needs
    
    Quality Improvement and Care Coordination:
    - Use risk scores to allocate transitional care resources effectively
    - Implement targeted interventions based on risk stratification levels
    - Monitor readmission rates by risk category to assess intervention effectiveness
    - Coordinate care between inpatient teams, outpatient providers, and community resources
    - Engage patients and families in shared decision-making about post-discharge care plans
    
    Limitations and Clinical Context:
    - Readmission risk is influenced by multiple factors beyond those captured in the score
    - Should be used to supplement, not replace, comprehensive clinical assessment
    - Local healthcare system factors may influence actual readmission rates and outcomes
    - Consider patient preferences, goals of care, and quality of life in care planning
    - Regular reassessment may be needed as clinical status and social circumstances change
    
    Reference: Mumtaz K, et al. Hepatology. 2019;70(2):630-639.
    """
    
    result: float = Field(
        ...,
        description="Predicted 30-day readmission probability as a percentage",
        example=28.5
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the readmission risk",
        example="%"
    )
    
    interpretation: str = Field(
        ...,
        description="Detailed clinical interpretation with risk stratification and management recommendations",
        example="MODERATE READMISSION RISK: The patient has an intermediate probability of 30-day readmission. MANAGEMENT: Enhanced discharge planning recommended with structured follow-up. Consider early outpatient follow-up within 7-14 days, comprehensive medication reconciliation, and patient education about warning signs. INTERVENTIONS: Assess social support systems, medication adherence, and access to care. Consider care coordination with hepatology if available. MONITORING: Close monitoring for signs of hepatic decompensation, fluid overload, and medication compliance."
    )
    
    stage: str = Field(
        ...,
        description="Risk category classification",
        example="Moderate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk level",
        example="Moderate 30-day readmission risk"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 28.5,
                "unit": "%",
                "interpretation": "MODERATE READMISSION RISK: The patient has an intermediate probability of 30-day readmission. MANAGEMENT: Enhanced discharge planning recommended with structured follow-up. Consider early outpatient follow-up within 7-14 days, comprehensive medication reconciliation, and patient education about warning signs. INTERVENTIONS: Assess social support systems, medication adherence, and access to care. Consider care coordination with hepatology if available. MONITORING: Close monitoring for signs of hepatic decompensation, fluid overload, and medication compliance.",
                "stage": "Moderate Risk",
                "stage_description": "Moderate 30-day readmission risk"
            }
        }