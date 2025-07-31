"""
Edmonton Obesity Staging System (EOSS) Models

Request and response models for EOSS obesity health impact assessment.

References (Vancouver style):
1. Sharma AM, Kushner RF. A proposed clinical staging system for obesity. Int J Obes (Lond). 
   2009;33(3):289-95. doi: 10.1038/ijo.2009.2.
2. Padwal RS, Pajewski NM, Allison DB, Sharma AM. Using the Edmonton obesity staging system to 
   predict mortality in a population-representative cohort of people with overweight and obesity. 
   CMAJ. 2011;183(14):E1059-66. doi: 10.1503/cmaj.110387.
3. Aasheim ET, Aylwin SJ, Radhakrishnan ST, Sood AS, Jovanovic Z, Olbers T, et al. Assessment 
   of Obesity Beyond Body Mass Index to Guide Treatment. Curr Cardiol Rep. 2017;19(5):33. 
   doi: 10.1007/s11886-017-0849-1.
4. Canning KL, Brown RE, Jamnik VK, Salmon A, Ardern CI, Kuk JL. Individuals with obesity 
   and type 2 diabetes have additional immune dysfunction compared with obese individuals who 
   are metabolically healthy. BMJ Open Diabetes Res Care. 2017;5(1):e000379. 
   doi: 10.1136/bmjdrc-2016-000379.

The Edmonton Obesity Staging System (EOSS) stratifies the presence and severity of 
obesity-related health impairments across medical, functional, and psychological domains 
to guide treatment decisions and predict outcomes beyond traditional BMI classification.
"""

from pydantic import BaseModel, Field
from typing import Literal


class EdmontonObesityStagingSystemRequest(BaseModel):
    """
    Request model for Edmonton Obesity Staging System (EOSS)
    
    The EOSS evaluates obesity-related health impacts across three key domains rather than 
    relying solely on BMI. Each domain is independently assessed and scored from 0-4, with 
    the highest score across any domain determining the overall EOSS stage. This approach 
    provides a more comprehensive assessment of obesity-related health risk and helps guide 
    appropriate treatment intensity.
    
    Clinical Context and Assessment:
    - Designed to complement, not replace, BMI classification
    - Focuses on functional impact of obesity rather than weight alone
    - Validated for predicting mortality risk independent of BMI
    - Useful for prioritizing treatment resources and intensity
    - Can guide decisions about bariatric surgery candidacy
    
    Three Assessment Domains:
    
    1. Obesity-Related Medical Risk Factors and Comorbidities:
    - Stage 0: No risk factors present
    - Stage 1: Subclinical risk factors (borderline hypertension, impaired fasting glucose, 
               elevated liver enzymes, arthralgia)
    - Stage 2: Established obesity-related chronic disease (hypertension, type 2 diabetes, 
               sleep apnea, osteoarthritis, reflux disease, gallbladder disease, gout)
    - Stage 3: End-organ damage (myocardial infarction, heart failure, diabetic complications, 
               osteoarthritis requiring joint replacement, non-alcoholic steatohepatitis)
    - Stage 4: Severe, potentially end-stage chronic disease (advanced heart failure, stroke, 
               severe diabetic complications, severe osteoarthritis, cirrhosis)
    
    2. Physical Symptoms and Functional Limitations:
    - Stage 0: No physical symptoms or functional limitations
    - Stage 1: Mild physical symptoms or limitations with activities of daily living
    - Stage 2: Moderate physical symptoms or limitations with activities of daily living
    - Stage 3: Significant physical symptoms or limitations with activities of daily living
    - Stage 4: Severe physical symptoms or limitations with activities of daily living
    
    3. Psychological Symptoms and Mental Health Impact:
    - Stage 0: No psychological symptoms or mental health impact
    - Stage 1: Mild psychological symptoms or mental health impact
    - Stage 2: Moderate psychological symptoms or mental health impact
    - Stage 3: Significant psychological symptoms or mental health impact
    - Stage 4: Severe psychological symptoms or mental health impact
    
    Staging Algorithm:
    The final EOSS stage is determined by the highest stage rating across all three domains 
    (not an average). For example, a patient with Stage 1 medical risk factors, Stage 2 
    physical symptoms, and Stage 0 psychological symptoms would be classified as EOSS Stage 2.
    
    Clinical Validation and Outcomes:
    - Higher EOSS stages correlate with increased mortality risk independent of BMI
    - EOSS staging has been validated for predicting surgical outcomes
    - Studies show clear survival curve divergence when stratified by EOSS stage
    - More predictive of health outcomes than obesity class alone
    - Useful for guiding treatment intensity and resource allocation
    
    Treatment Implications by Stage:
    - Stage 0-1: Lifestyle interventions, prevention focus
    - Stage 2: Comprehensive obesity treatment, pharmacotherapy consideration
    - Stage 3-4: Aggressive management, bariatric surgery evaluation, multidisciplinary care
    
    Implementation Considerations:
    - Requires comprehensive clinical assessment across multiple domains
    - Should be reassessed periodically as health status may change
    - Most effective when used as part of comprehensive obesity care
    - Particularly valuable for treatment planning and resource allocation
    
    References (Vancouver style):
    1. Sharma AM, Kushner RF. A proposed clinical staging system for obesity. Int J Obes (Lond). 
       2009;33(3):289-95. doi: 10.1038/ijo.2009.2.
    2. Padwal RS, Pajewski NM, Allison DB, Sharma AM. Using the Edmonton obesity staging system to 
       predict mortality in a population-representative cohort of people with overweight and obesity. 
       CMAJ. 2011;183(14):E1059-66. doi: 10.1503/cmaj.110387.
    3. Aasheim ET, Aylwin SJ, Radhakrishnan ST, Sood AS, Jovanovic Z, Olbers T, et al. Assessment 
       of Obesity Beyond Body Mass Index to Guide Treatment. Curr Cardiol Rep. 2017;19(5):33. 
       doi: 10.1007/s11886-017-0849-1.
    """
    
    obesity_risk_factors: int = Field(
        ...,
        ge=0, le=4,
        description="Obesity-related medical risk factors and comorbidities. Stage 0: No risk factors. Stage 1: Subclinical risks (borderline hypertension, impaired fasting glucose). Stage 2: Established chronic disease (hypertension, diabetes, sleep apnea). Stage 3: End-organ damage (MI, heart failure, diabetic complications). Stage 4: Severe end-stage disease (advanced heart failure, stroke, cirrhosis)",
        example=2
    )
    
    physical_symptoms: int = Field(
        ...,
        ge=0, le=4,
        description="Physical symptoms and functional limitations related to obesity. Stage 0: No symptoms or limitations. Stage 1: Mild limitations with activities of daily living. Stage 2: Moderate limitations. Stage 3: Significant limitations. Stage 4: Severe limitations with activities of daily living",
        example=1
    )
    
    psychological_symptoms: int = Field(
        ...,
        ge=0, le=4,
        description="Psychological symptoms and mental health impact related to obesity. Stage 0: No psychological impact. Stage 1: Mild psychological symptoms or mental health impact. Stage 2: Moderate impact. Stage 3: Significant impact. Stage 4: Severe psychological symptoms or mental health impact",
        example=1
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "obesity_risk_factors": 2,
                "physical_symptoms": 1,
                "psychological_symptoms": 1
            }
        }


class EdmontonObesityStagingSystemResponse(BaseModel):
    """
    Response model for Edmonton Obesity Staging System (EOSS)
    
    The EOSS stage provides critical information for treatment planning and prognosis in 
    obesity management. The system moves beyond BMI to provide a comprehensive assessment 
    of obesity-related health impacts across medical, functional, and psychological domains.
    
    EOSS Stage Interpretation and Clinical Management:
    
    Stage 0 - No Obesity-Related Health Impairments:
    - Clinical Significance: No current obesity-related health problems
    - Management Approach:
      * Focus on prevention and lifestyle counseling
      * Promote healthy eating and regular physical activity
      * Weight maintenance strategies
      * Education about obesity-related health risks
      * Regular monitoring to prevent progression
    - Prognosis: Excellent with appropriate lifestyle maintenance
    
    Stage 1 - Mild Obesity-Related Health Impairments:
    - Clinical Significance: Subclinical risk factors or mild symptoms present
    - Management Approach:
      * Intensive lifestyle interventions (structured dietary counseling, exercise programs)
      * Behavioral modification programs
      * Regular monitoring of subclinical risk factors
      * Investigation of metabolic parameters
      * Consider consultation with dietitian or exercise physiologist
    - Prognosis: Good with early intervention and lifestyle changes
    - Monitoring: Regular assessment for progression of risk factors
    
    Stage 2 - Moderate Obesity-Related Health Impairments:
    - Clinical Significance: Established chronic diseases or moderate functional limitations
    - Management Approach:
      * Comprehensive obesity treatment including pharmacotherapy consideration
      * Active management of obesity-related comorbidities
      * Consider referral to obesity specialist or endocrinologist
      * Structured weight management programs
      * Address functional limitations through physical therapy if appropriate
    - Prognosis: Moderate, requires active medical management
    - Treatment Intensity: Escalated interventions beyond lifestyle alone
    
    Stage 3 - Severe Obesity-Related Health Impairments:
    - Clinical Significance: End-organ damage or significant functional/psychological impairment
    - Management Approach:
      * Aggressive obesity management required
      * Consider bariatric surgery evaluation if appropriate
      * Intensive management of comorbidities
      * Multidisciplinary care team approach (endocrinology, cardiology, psychology)
      * Psychological support and counseling
      * Comprehensive assessment of surgical candidacy
    - Prognosis: Guarded, requires intensive intervention
    - Priority: High priority for specialized obesity treatment
    
    Stage 4 - End-Stage Obesity-Related Health Impairments:
    - Clinical Significance: Severe, potentially life-threatening obesity-related conditions
    - Management Approach:
      * Most aggressive management options available
      * Urgent bariatric surgery evaluation if appropriate
      * Palliative care considerations may be indicated
      * Comprehensive support services
      * End-of-life planning discussions if appropriate
      * Intensive medical management of comorbidities
    - Prognosis: Poor without aggressive intervention
    - Priority: Highest priority for immediate specialized care
    
    Mortality Risk Correlation:
    - EOSS stages correlate with mortality risk independent of BMI
    - Stage 2: Hazard ratio 1.57 for death (95% CI 1.16-2.13)
    - Stage 3: Hazard ratio 2.69 for death (95% CI 1.98-3.67)
    - Clear survival curve divergence when stratified by EOSS stage
    
    Clinical Implementation Guidelines:
    - Use in conjunction with BMI, not as replacement
    - Regular reassessment recommended as health status may change
    - Particularly valuable for treatment resource allocation
    - Helps guide decisions about bariatric surgery candidacy
    - Useful for communicating obesity-related health risks to patients
    
    Treatment Planning Considerations:
    - Stage determines treatment intensity and resource allocation
    - Higher stages require more aggressive, multidisciplinary approaches
    - Consider patient's overall functional status and quality of life
    - Address all three domains (medical, physical, psychological) in treatment planning
    - Monitor for progression or improvement across domains
    
    Quality of Life and Functional Assessment:
    - EOSS stages correlate with quality of life measures
    - Functional limitations are key component of staging
    - Psychological impact is explicitly considered in assessment
    - Helps identify patients who may benefit from comprehensive support services
    
    Research and Validation:
    - Validated in multiple population-based studies
    - Predictive of surgical outcomes and long-term mortality
    - More predictive than BMI alone for health outcomes
    - Useful for epidemiological research and healthcare planning
    
    Reference: Sharma AM, Kushner RF. Int J Obes (Lond). 2009;33(3):289-95.
    """
    
    result: int = Field(
        ...,
        description="EOSS stage determined by highest severity across medical, physical, and psychological domains (range: 0-4)",
        example=2
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the EOSS stage",
        example="stage"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended management approach based on EOSS stage and domain assessment",
        example="Moderate obesity-related health impairments with established chronic disease. Initiate comprehensive obesity treatment including pharmacotherapy consideration if appropriate. Actively manage comorbidities and functional limitations. Consider referral to obesity specialist."
    )
    
    stage: str = Field(
        ...,
        description="EOSS stage classification (Stage 0, Stage 1, Stage 2, Stage 3, Stage 4)",
        example="Stage 2"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the obesity-related health impairment level",
        example="Moderate obesity-related health impairments"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 2,
                "unit": "stage",
                "interpretation": "Moderate obesity-related health impairments with established chronic disease. Initiate comprehensive obesity treatment including pharmacotherapy consideration if appropriate. Actively manage comorbidities and functional limitations. Consider referral to obesity specialist.",
                "stage": "Stage 2",
                "stage_description": "Moderate obesity-related health impairments"
            }
        }